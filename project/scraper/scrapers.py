import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import re
from datetime import datetime, timedelta
from .models import JobListing

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def parse_relative_date(text):
    text = text.lower()
    if "day" in text:
        days = int(re.search(r'(\d+)', text).group(1))
        return (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    elif "just" in text or "today" in text:
        return datetime.today().strftime('%Y-%m-%d')
    return None

class IndiaJobScraper:
    def __init__(self):
        self.driver = None

    def scrape_naukri(self, search_term, location="India"):
        try:
            self.driver = setup_driver()
            url = f"https://www.naukri.com/{search_term.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            jobs = []

            for job in soup.find_all('div', class_='jobTuple'):
                try:
                    title = job.find('a', class_='title').text.strip()
                    company = job.find('a', class_='subTitle').text.strip()
                    location = job.find('li', class_='location').text.strip()
                    url = job.find('a', class_='title')['href']

                    desc_tag = job.find('div', class_='job-description')
                    description = desc_tag.text.strip() if desc_tag else "No description available"

                    posted_tag = job.find('span', class_='type')
                    posted_text = posted_tag.text.strip().replace("Posted", "").strip() if posted_tag else ""
                    posted_date = parse_relative_date(posted_text) or datetime.today().strftime('%Y-%m-%d')

                    skills_tag = job.find('ul', class_='tags')
                    skills = ", ".join([li.text.strip() for li in skills_tag.find_all('li')]) if skills_tag else "Not mentioned"

                    salary_tag = job.find('li', class_='salary')
                    salary = salary_tag.text.strip() if salary_tag else "Not mentioned"

                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'url': url,
                        'source': 'Naukri',
                        'description': description,
                        'posted_date': posted_date,
                        'skills': skills,
                        'salary': salary
                    })
                except:
                    continue
            return jobs
        except Exception as e:
            print(f"⚠️ Naukri Error: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()

    def scrape_indeed_india(self, search_term, location="India"):
        try:
            params = {'q': search_term, 'l': location, 'fromage': '3'}
            response = requests.get("https://www.indeed.co.in/jobs", params=params, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = []

            for job in soup.find_all('div', class_='job_seen_beacon'):
                try:
                    title = job.find('h2').text.strip()
                    company = job.find('span', class_='companyName').text.strip()
                    location = job.find('div', class_='companyLocation').text.strip()
                    url = "https://www.indeed.co.in" + job.find('a')['href']

                    desc_tag = job.find('div', class_='job-snippet')
                    description = desc_tag.text.strip().replace('\n', ' ') if desc_tag else "No description available"

                    posted_tag = job.find('span', class_='date')
                    posted_text = posted_tag.text.strip() if posted_tag else ""
                    posted_date = parse_relative_date(posted_text) or datetime.today().strftime('%Y-%m-%d')

                    salary_tag = job.find('div', class_='salary-snippet')
                    salary = salary_tag.text.strip() if salary_tag else "Not mentioned"

                    skills = "Not mentioned"

                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'url': url,
                        'source': 'Indeed India',
                        'description': description,
                        'posted_date': posted_date,
                        'skills': skills,
                        'salary': salary
                    })
                except:
                    continue
            return jobs
        except Exception as e:
            print(f"⚠️ Indeed Error: {str(e)}")
            return []

    def scrape_linkedin_india(self, search_term, location="India"):
        try:
            self.driver = setup_driver()
            url = f"https://www.linkedin.com/jobs/search/?keywords={search_term.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            jobs = []

            for job in soup.find_all('div', class_='base-card'):
                try:
                    title = job.find('h3').text.strip()
                    company = job.find('h4').text.strip()
                    location = job.find('span', class_='job-search-card__location').text.strip()
                    url = job.find('a')['href']

                    posted_tag = job.find('time')
                    posted_date = posted_tag['datetime'][:10] if posted_tag and posted_tag.has_attr('datetime') else datetime.today().strftime('%Y-%m-%d')

                    description = "No description available"
                    skills = "Not mentioned"
                    salary = "Not mentioned"

                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'url': url,
                        'source': 'LinkedIn India',
                        'description': description,
                        'posted_date': posted_date,
                        'skills': skills,
                        'salary': salary
                    })
                except:
                    continue
            return jobs
        except Exception as e:
            print(f"⚠️ LinkedIn Error: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()

    def scrape_internshala(self, search_term):
        try:
            self.driver = setup_driver()
            url = f"https://internshala.com/internships/{search_term.replace(' ', '%20')}-internship"
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            jobs = []

            for job in soup.find_all('div', class_='individual_internship'):
                try:
                    title = job.find('h3', class_='heading_4_5').text.strip()
                    company = job.find('h4', class_='heading_6').text.strip()
                    location = job.find('a', class_='location_link').text.strip()
                    url = "https://internshala.com" + job.find('a', class_='view_detail_button')['href']

                    desc_tag = job.find('div', class_='internship_other_details_container')
                    description = desc_tag.text.strip() if desc_tag else "No description available"

                    posted_tag = job.find('span', class_='status')
                    posted_date = posted_tag.text.replace("Posted on", "").strip() if posted_tag else datetime.today().strftime('%Y-%m-%d')

                    skills_tag = job.find('div', class_='individual_internship_skills')
                    skills = skills_tag.text.strip() if skills_tag else "Not mentioned"

                    salary_tag = job.find('span', class_='stipend')
                    salary = salary_tag.text.strip() if salary_tag else "Not mentioned"

                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'url': url,
                        'source': 'Internshala',
                        'description': description,
                        'posted_date': posted_date,
                        'skills': skills,
                        'salary': salary
                    })
                except:
                    continue
            return jobs
        except Exception as e:
            print(f"⚠️ Internshala Error: {str(e)}")
            return []
        finally:
            if self.driver:
                self.driver.quit()

def run_scrapers(search_term, location="India"):
    scraper = IndiaJobScraper()
    jobs = []
    jobs.extend(scraper.scrape_naukri(search_term, location))
    jobs.extend(scraper.scrape_indeed_india(search_term, location))
    jobs.extend(scraper.scrape_linkedin_india(search_term, location))
    jobs.extend(scraper.scrape_internshala(search_term))

    for job in jobs:
        JobListing.objects.update_or_create(
            title=job['title'],
            company=job['company'],
            url=job['url'],
            defaults={
                'location': job['location'],
                'source': job['source'],
                'is_active': True,
                'description': job.get('description', 'No description available'),
                'posted_date': job.get('posted_date', datetime.today().strftime('%Y-%m-%d')),
                'skills': job.get('skills', 'Not mentioned'),
                'salary': job.get('salary', 'Not mentioned'),
            }
        )
    return jobs
