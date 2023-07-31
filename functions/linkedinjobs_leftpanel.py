import random
from selenium.webdriver.common.by import By
import datetime

def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest



def basic_info(rand_jobs,job_title_list = [],company_name_list = [],
               location_list = [],date_list = [],job_link_list = []):
    job_title_list = []
    company_name_list = []
    location_list = []
    date_list = []
    job_link_list = []
    #We loop over every job and obtain all the wanted info.
    for job in rand_jobs:
        #job_title
        job_title = job.find_element(By.CSS_SELECTOR,"h3").get_attribute("innerText")
        job_title_list.append(job_title)
        
        #company_name
        company_name = job.find_element(By.CSS_SELECTOR,"h4").get_attribute("innerText")
        company_name_list.append(company_name)
        print(company_name)
        
        #location
        location = job.find_element(By.CSS_SELECTOR,"div>div>span").get_attribute("innerText")
        location_list.append(location)
        
        #date
        date = job.find_element(By.CSS_SELECTOR,"div>div>time").get_attribute("datetime")
        date_list.append(date)
        
        #job_link
        job_link = job.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
        job_link_list.append(job_link)
    
    return company_name_list,job_link_list,date_list,location_list,job_title_list


#basicinfo_time_start=datetime.datetime.now()
#company_name_list,job_link_list,date_list,location_list,job_title_list= basic_info(rand_jobs=rand_jobs) #changed at 18.07.2023
# 3min 30
#basicinfo_time_end=datetime.datetime.now()
#basicinfo_time=basicinfo_time_end-basicinfo_time_start
#basicinfo_time