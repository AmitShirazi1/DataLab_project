# Databricks notebook source
# MAGIC %pip install aiohttp asyncio

# COMMAND ----------

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
import aiohttp
from abc import ABC, abstractmethod

class JobBoardAPI(ABC):
    """Abstract base class for job board APIs"""
    
    @abstractmethod
    async def search_jobs(self, company_name: str, location: str = "") -> List[Dict]:
        pass
    
    @abstractmethod
    def process_jobs(self, raw_data: Dict) -> List[Dict]:
        pass

class IndeedAPI(JobBoardAPI):
    def __init__(self, publisher_id: str):
        self.base_url = "https://api.indeed.com/ads/apisearch"
        self.publisher_id = publisher_id
    
    async def search_jobs(self, company_name: str, location: str = "") -> List[Dict]:
        params = {
            "publisher": self.publisher_id,
            "format": "json",
            "v": "2",
            "company": company_name,
            "location": location,
            "limit": 25
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return None
    
    def process_jobs(self, raw_data: Dict) -> List[Dict]:
        if not raw_data or 'results' not in raw_data:
            return []
            
        return [{
            'source': 'Indeed',
            'title': job.get('jobtitle', ''),
            'company': job.get('company', ''),
            'location': job.get('formattedLocation', ''),
            'description': job.get('snippet', ''),
            'url': job.get('url', ''),
            'date_posted': job.get('date', ''),
            'job_type': job.get('jobtype', ''),
            'salary': job.get('formattedRelativeTime', '')
        } for job in raw_data['results']]

class GlassdoorAPI(JobBoardAPI):
    def __init__(self, partner_id: str, partner_key: str):
        self.base_url = "https://api.glassdoor.com/api/api.htm"
        self.partner_id = partner_id
        self.partner_key = partner_key
    
    async def search_jobs(self, company_name: str, location: str = "") -> List[Dict]:
        params = {
            "v": "1",
            "format": "json",
            "t.p": self.partner_id,
            "t.k": self.partner_key,
            "action": "jobs-prog",
            "q": company_name,
            "l": location,
            "userip": "0.0.0.0",
            "useragent": "Mozilla/5.0"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return None

    def process_jobs(self, raw_data: Dict) -> List[Dict]:
        if not raw_data or 'response' not in raw_data or 'jobs' not in raw_data['response']:
            return []
            
        return [{
            'source': 'Glassdoor',
            'title': job.get('jobTitle', ''),
            'company': job.get('employer', {}).get('name', ''),
            'location': job.get('location', ''),
            'description': job.get('description', ''),
            'url': job.get('jobLink', ''),
            'date_posted': job.get('postedDate', ''),
            'job_type': job.get('jobType', ''),
            'salary': job.get('salarySource', {}).get('payPeriod', {}).get('name', '')
        } for job in raw_data['response']['jobs']]

class ZipRecruiterAPI(JobBoardAPI):
    def __init__(self, api_key: str):
        self.base_url = "https://api.ziprecruiter.com/jobs/v1"
        self.api_key = api_key
    
    async def search_jobs(self, company_name: str, location: str = "") -> List[Dict]:
        params = {
            "api_key": self.api_key,
            "search": company_name,
            "location": location
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return None

    def process_jobs(self, raw_data: Dict) -> List[Dict]:
        if not raw_data or 'jobs' not in raw_data:
            return []
            
        return [{
            'source': 'ZipRecruiter',
            'title': job.get('name', ''),
            'company': job.get('hiring_company', {}).get('name', ''),
            'location': job.get('location', ''),
            'description': job.get('snippet', ''),
            'url': job.get('url', ''),
            'date_posted': job.get('posted_time', ''),
            'job_type': job.get('job_type', ''),
            'salary': job.get('salary_interval', '')
        } for job in raw_data['jobs']]

class JobAggregator:
    def __init__(self):
        self.apis: List[JobBoardAPI] = []
        
    def add_api(self, api: JobBoardAPI):
        self.apis.append(api)
    
    async def gather_all_jobs(self, company_name: str, location: str = "") -> List[Dict]:
        all_jobs = []
        
        # Gather jobs from all sources concurrently
        tasks = [api.search_jobs(company_name, location) for api in self.apis]
        raw_results = await asyncio.gather(*tasks)
        
        # Process results from each source
        for api, raw_data in zip(self.apis, raw_results):
            if raw_data:
                processed_jobs = api.process_jobs(raw_data)
                all_jobs.extend(processed_jobs)
        
        return self.deduplicate_jobs(all_jobs)
    
    def deduplicate_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate job listings based on title and company"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = (job['title'], job['company'])
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs

def save_jobs(jobs: List[Dict], company_name: str):
    """Save aggregated jobs to a JSON file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"aggregated_jobs_{company_name.lower().replace(' ', '_')}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(jobs, f, indent=2)
    
    return filename

async def main():
    # Initialize APIs with your credentials
    indeed_api = IndeedAPI("YOUR_INDEED_PUBLISHER_ID")
    glassdoor_api = GlassdoorAPI("YOUR_GLASSDOOR_PARTNER_ID", "YOUR_GLASSDOOR_PARTNER_KEY")
    ziprecruiter_api = ZipRecruiterAPI("YOUR_ZIPRECRUITER_API_KEY")
    
    # Create aggregator and add APIs
    aggregator = JobAggregator()
    aggregator.add_api(indeed_api)
    aggregator.add_api(glassdoor_api)
    aggregator.add_api(ziprecruiter_api)
    
    # Search parameters
    COMPANY_NAME = "Continental Resources"
    LOCATION = "United States"
    
    # Gather and process jobs
    jobs = await aggregator.gather_all_jobs(COMPANY_NAME, LOCATION)
    
    # Save results
    output_file = save_jobs(jobs, COMPANY_NAME)
    print(f"Successfully retrieved and saved {len(jobs)} unique jobs to {output_file}")
    
    # Print summary
    sources = {}
    for job in jobs:
        sources[job['source']] = sources.get(job['source'], 0) + 1
    
    print("\nJobs by source:")
    for source, count in sources.items():
        print(f"{source}: {count} jobs")

if __name__ == "__main__":
    asyncio.run(main())
