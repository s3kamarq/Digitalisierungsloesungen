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

### 
### import own functions
from functions.url import create_url
from functions.jobnumer import get_numberOfJobs
from functions.linkedinjobs_leftpanel import *
#from functions.linkedinjobs_rightpanel import detail_info
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
tuple_pair = list_of_tuples[1]

#start=0
#end=len(rand_jobs)
#rand_jobs=rand_jobs
#jobs=jobs
#driver=driver
#jd=[]
#seniority=[]#
#emp_type=[]
#job_func=[]
#job_ind=[]
#prof=[]
#id_num=[]
#x=0
from tkinter import filedialog
from tkinter import messagebox

def openpreviousdata():
    m= messagebox.askyesno(message=r'Möchten Sie das Zwischnergebnis einlesen?')
    if m==True:
        inputfile= filedialog.askopenfilename()
        eingelesenesDataframe= pd.read_pickle(inputfile)
    else:
        eingelesenesDataframe=pd.DataFrame()
    return eingelesenesDataframe


# error testing parameter
#start=0
#end=len(rand_jobs)
#rand_jobs=rand_jobs
#jobs=jobs
#driver=driver



def detail_info(start, end,rand_jobs, jobs, driver, x, jd, seniority, emp_type, job_func,job_ind, prof,id_num):

    #read in previous data if necessary

    print(x)
    detail_timestart=datetime.datetime.now()
    intermediate_result=openpreviousdata()
    # 
    for item in rand_jobs[start:end]: #range(len(jobs)):
        num= jobs.index(item) # not rand_jobs, because the order changed there!

        id_num.append(num)
        x+=1
        print(x)
        print("Scraping Status: {} %  _________________ Time elapsed: {} minutes ".format(x/len(rand_jobs), int((datetime.datetime.now()-detail_timestart).seconds/60)))
        #job_func0=[]
        #industries0=[]
        # clicking job to view job details
        
        #__________________________________________________________________________ JOB Link
        
        try: 
            job_click_path = f'/html/body/div[1]/div/main/section[2]/ul/li[{num+1}]'
            #Wait as long as required, or maximum 10 sec before for the page loading of the detailed job description on the right side of the page
            element= WebDriverWait(driver= driver, timeout=60).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
            time.sleep(random.randint(2,3)) # to ensure that the scrolling is not faster than my code on saving the data 
            element.click() 


            #job_click = item.find_element(By.XPATH,job_click_path).click() # The URL changes when clicking on a certain job offer
            # random waiting time to avoid a certain structure,so I do not get banned
            #job_click = item.find_element(By.XPATH,'.//a[@class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"]')
        except TimeoutException:
            print(r"Loading took too much time")
            driver.refresh()
            job_click_path = f'/html/body/div[1]/div/main/section[2]/ul/li[{num+1}]'
            element= WebDriverWait(driver= driver, timeout=60).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
            time.sleep(random.randint(2,3)) 
            element.click() 
            pass
        
        #__________________________________________________________________________ JOB Description
        jd_path = '/html/body/div/div/section/div/div/section/div/div/section/div'
        try:
            jd0 = item.find_element(By.XPATH,jd_path).get_attribute('innerText')
            jd.append(jd0)
        except:
            jd0=None # Not all job postings have all of these detailed information 
            jd.append(jd0)
            pass

        #__________________________________________________________________________ JOB Seniority
        seniority_path='/html/body/div/div/section/div/div/section/div/ul/li[1]/span'
        
        try:
            seniority0 = item.find_element(By.XPATH,seniority_path).get_attribute('innerText')
            seniority.append(seniority0)
        except:
            seniority0=None
            seniority.append(seniority0)
            pass

        #__________________________________________________________________________ JOB Time
        emp_type_path='/html/body/div/div/section/div/div/section/div/ul/li[2]/span'
        
        try:
            emp_type0 = item.find_element(By.XPATH,emp_type_path).get_attribute('innerText')
            emp_type.append(emp_type0)
        except:
            emp_type0=None
            emp_type.append(emp_type0)
            pass

        #__________________________________________________________________________ JOB Function
        function_path='/html/body/div/div/section/div/div/section/div/ul/li[3]/span'
        print(job_func)
        try:
            func0 = item.find_element(By.XPATH,function_path).get_attribute('innerText')
            job_func.append(func0)
        except:
            func0=None
            job_func.append(func0)
            pass

        #__________________________________________________________________________ JOB Industry
        industry_path='/html/body/div/div/section/div/div/section/div/ul/li[4]/span'
        
        try:
            ind0 = item.find_element(By.XPATH,industry_path).get_attribute('innerText')
            job_ind.append(ind0)
        except:
            ind0=None
            job_ind.append(ind0)
            pass

        # Den Path Finden: rechtklick auf das gewünschte Objekt/ den Text >> untersuchen, 
        # dann rechtsklick auf die markierte Stelle im HTML Code >> kopieren >> gesamten XPATH kopieren
        profile_link_path = '/html/body/div[1]/div/section/div[2]/section/div/a'
        # old that worked on other file one_job : '/html/body/div[3]/div/section/div[2]/section/div/a'
        #f'/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a' #vorher anfang april
        #second: /html/body/div[3]/div/section/div[2]/section/div/a
        
        try:
            prof0 = item.find_element(By.XPATH, profile_link_path).get_attribute('href')
            prof0
            prof.append(prof0)

        except:
            prof0=None
            prof.append(prof0)
            pass
        
        intermediate_result.loc[len(intermediate_result)]=[element,jd0, seniority0,emp_type0,func0,ind0,prof0]
        intermediate_result.to_pickle('zwischenergebnis.pkl')
        del element,jd0, seniority0,emp_type0,func0,ind0,prof0
        #time.sleep(2)
        
    #print("Total time elapsed for detailed info: {}")
    return id_num, jd, seniority, emp_type, job_func, job_ind ,prof

############################################################################################
###################################################################
def page_webscraping(tuple_pair, ort):

    job_name, erfahrung = tuple_pair

    # create the URL  
    url = create_url(job_name, location, ort, erfahrung)

    # set-up the browser
    s=Service(ChromeDriverManager(version="114.0.5735.90").install())
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
    company_name_list,job_link_list,date_list,location_list,job_title_list= basic_info(rand_jobs=rand_jobs)


    # webscrape the detailed information (right panel) and saves them in list
    
    #x=0
    jd = [] #job_description
    seniority = []
    emp_type = []
    job_func = []
    job_ind = []
    prof = [] # company link
    id_num=[]


    id_num, jd,seniority,emp_type, job_func,job_ind ,prof = detail_info(start=0, end=len(rand_jobs),rand_jobs=rand_jobs,jobs=jobs, driver=driver,
                                                                        jd=[],seniority=[],emp_type=[],job_func=[],job_ind=[],prof=[],id_num=[],x=0)

    
    #intermediate save of data
    dataMerge= pd.DataFrame({
    'id_num': id_num,
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
    scraped_data= pd.merge(dataMerge,df_companies,how='left', on=['profile_Link'])
    scraped_data.to_pickle(r"data_{0}_{1}_{2}_{3}.pkl".format(job_name,jobs_num,ort,erfahrung))
    scraped_data.to_excel(r"data_{0}_{1}_{2}_{3}.xlsx".format(job_name,jobs_num,ort,erfahrung))
    driver.close()
    return scraped_data



time1=datetime.datetime.now()
df = page_webscraping(tuple_pair=tuple_pair, ort=ort)
time2=datetime.datetime.now()-time1

# set up multithreading 
mp.cpu_count()# 8 Kerne
max_worker=3
with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
    executor.map(page_webscraping,list_of_tuples)




