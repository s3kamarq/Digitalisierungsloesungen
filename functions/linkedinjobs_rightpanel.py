import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # wait for the data to load before continueing the loop
from selenium.webdriver.support import expected_conditions as EC # want to continue execution of webscraping only after the detailed description has loaded
import time
import random



def threadfunc(item,x=x,jd=jd, seniority=seniority,emp_type=emp_type,job_func=job_func, job_ind=job_ind,prof=prof, id_num=id_num, driver=driver,number_jobs=len(rand_jobs),detail_timestart= detail_timestart):
    num= jobs.index(item) # not rand_jobs, because the order changed there!
    x=x+1
    print(x)
    print("Scraping Status: {} %  _________________ Time elapsed: {} minutes ".format(x/number_jobs, int((datetime.datetime.now()-detail_timestart).seconds/60)))
    id_num.append(num)
    #job_func0=[]
    #industries0=[]
    # clicking job to view job details
    
    #__________________________________________________________________________ JOB Link
    
    try: 
        job_click_path = f'/html/body/div[1]/div/main/section[2]/ul/li[{num+1}]'
        #Wait as long as required, or maximum 10 sec before for the page loading of the detailed job description on the right side of the page
        element= WebDriverWait(driver= driver, timeout=20).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
        time.sleep(random.randint(2,3)) # to ensure that the scrolling is not faster than my code on saving the data 
        element.click() 


        #job_click = item.find_element(By.XPATH,job_click_path).click() # The URL changes when clicking on a certain job offer

        # random waiting time to avoid a certain structure,so I do not get banned
        #job_click = item.find_element(By.XPATH,'.//a[@class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"]')
    except TimeoutException:
        print(r"Loading took too much time")
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
    
    del element,jd0, seniority0,emp_type0,func0,ind0,prof0
    #time.sleep(2)
    return id_num,jd,seniority,emp_type, job_func,job_ind ,prof,x
