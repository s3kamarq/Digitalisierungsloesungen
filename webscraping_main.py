###################################################################################
######## Main execution file for Webscraping LinkedIn Jobs ########################
###################################################################################

# import the required packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time #
import pandas as pd
import datetime #to check the performance of the code
import random # to randomize the webscraping procedure, in order to prevent being banned
from selenium.webdriver.support import expected_conditions as EC # want to continue execution of webscraping only after the detailed description has loaded
from selenium.webdriver.support.ui import WebDriverWait # wait for the data to load before continueing the loop
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import concurrent.futures # For Multithreading
import multiprocessing as mp

### import own functions
from functions.url import create_url
from functions.jobnumer import get_numberOfJobs
from functions.linkedinjobs_leftpanel import *
from functions.linkedinjobs_rightpanel import detail_info
from functions.company_profiles import scrape_profiles

# Define the static variables we want to inspect

techlist=['Cloud-Computing', 'Online-Marketing','E-Commerce','Künstliche Intelligenz','AI','Analytics', 'Big Data',
          'Internet of Things (IoT)', 'IoT','Deep Tech','Digitale Transformation', 'Industrie 4.0',
          'Robotik','Fintech', 'Blockchain','3D-Druck']
location= "Deutschland"
# Split up the search requests by using filter options. We do that to get more results, as one 
# search request always has an upper bound of 1000 job postings, even tough it might be more
# This restriction is given by LinkedI and cannot be changed.
berufserfahrunglist=[1,2,3,4,5]
ortlist= [1,2,3]


#combine techlist and berufserfahrunglist
list_of_tuples= [(x,y) for x in techlist for y in berufserfahrunglist]
#len(list_of_tuples) # This gives us 16*5=80 combination

#for testing the inner part of the loop
#job_name= techlist[1] 
ort=ortlist[0]
job_name, erfahrung = list_of_tuples[0]


def page_webscraping(tuple, ort):

    job_name, erfahrung = tuple

    # create the URL  
    url = create_url(job_name, location, ort, erfahrung)

    # set-up the browser
    s=Service(ChromeDriverManager().install())
    driver= webdriver.Chrome(service=s)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("--diable-notifications") #new 16.02 
    driver.get(url)

    # save the given number of jobs given by LinkedIn
    jobs_num = get_numberOfJobs(driver=driver)

    # Scroll to make all job postings visible
    i = 2
    while i <= 60: #1000jobs/25 jobs per load= 40 should be enough but we want to be sure, thus take 60..
        #We keep scrollind down to the end of the view.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i = i + 1
        print("Current at: ", i,end="\r")
        try:
            #We try to click on the load more results buttons in case it is already displayed.
            infinite_scroller_button = driver.find_element(By.XPATH, ".//button[@aria-label='Weitere Jobs anzeigen']") # hat sich geändert 13.02.23, vorher'Weitere Ergebnisse laden'
            infinite_scroller_button.click()
            #random_decimal= random.randint(1,9)/10 #new 10.03
            random_decimal= random.randint(1,4) #new 10.03

            time.sleep(random_decimal)
        except:
            #If there is no button, there will be an error, so we keep scrolling down.
            time.sleep(0.3)
            pass
    
    # save the Job Boxes as Webelements in a list
    job_lists = driver.find_element(By.CLASS_NAME,"jobs-search__results-list")
    jobs = job_lists.find_elements(By.TAG_NAME,"li") # return a list

    # webscrape the Job Boxes (left panel) and save them in lists
    rand_jobs= scrambled(jobs)
    company_name_list,job_link_list,date_list,location_list,job_title_list= basic_info()

    # webscrape the detailed information (right panel) and saves them in list
    id_num, jd,seniority,emp_type, job_func,job_ind ,prof =detail_info(start=0, end=len(rand_jobs),rand_jobs=rand_jobs,jobs=jobs, driver=driver)

    #intermediate save of data
    dataMerge= pd.DataFrame({
    'Date': date_list,
    'Company': company_name_list,
    'Title': job_title_list,
    'Location': location_list,
    'Link': job_link_list,
    'Description': jd,
    'Level': seniority,
    'Type': emp_type,
    'Function': job_func,
    'Industry': job_ind,
    'profile_Link': prof
    #'Profile': prof_text,
    #'Company_Size': comp_size
    })

    # webscrape company profiles (new URL pages)
    #initialize lists
    temp= pd.DataFrame([prof,rand_jobs]).transpose()
    unique=temp.drop_duplicates(subset=[0], keep='first') # Company link + corresponding WebElement 
    u_webelem= unique[1]
    df_companies= scrape_profiles(webelements= u_webelem,unique=unique, maxtab=10, jobs=jobs,driver=driver)

    # merge the dataframes using full outer join
    scraped_data= pd.merge(dataMerge,df_companies,how='outer', on=['prof'])

    return scraped_data
















# set up multithreading 
mp.cpu_count()# 8 Kerne
max_worker=3
with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
    executor.map(page_webscraping,list_of_tuples)