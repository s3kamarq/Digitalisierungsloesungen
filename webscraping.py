import requests
from bs4 import BeautifulSoup
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
from selenium.webdriver.chrome.options import Options # to prevent pop-up window where Linkedin wants me to login


# Code is based on the following link:
# https://blog.devgenius.io/how-to-build-a-scraping-tool-for-linkedin-in-7-minutes-tool-data-science-csv-selenium-beautifulsoup-python-a673f12ac579
# corresponding github page: https://github.com/rfeers/Medium/tree/main/Website%20Scraping/Linkedin

############################################################################
# 1. Open LinkedIn Website in the Browser 
############################################################################
# 
#  Wenn man nach dem Jobtitel und dem Standort sucht, erscheinen diese keywords auch in der URL
# somit kennt man die URL für verschiedene Jobtitel 
# ! Sollte mehr als ein String verwendet werden, wird '%20' anstatt ein Leerzeichen in der URL benutzt
start_time =datetime.datetime.now()

job_name= "Robotik" 
# Cloud-Computing 
# Online-Marketing
# E-Commerce
# Künstliche Intelligenz, AI
# Analytics, Big Data
# Internet of Things (IoT), IoT,Deep Tech
# Digitale Transformation, Industrie 4.0
# Robotik
# Fintech, Blockchain
# 3D-Druck

location= "Deutschland"

# Make sure that the job name is put correctly into the URL
job_url= "";
for item in job_name.split(" "):
    if item != job_name.split(" ")[-1]:
        job_url= job_url +item + "%20"
    else:
        job_url= job_url+ item

loc_url="";
for item in location.split(" "):
    if item != location.split(" ")[-1]:
        loc_url= loc_url+ item +"%20"
    else: 
        loc_url= loc_url+item 

# create the URL based on location and job name

url = "https://de.linkedin.com/jobs/search?keywords={0}&location={1}&geoId=101282230&trk=guest_homepage-basic_jobs-search-bar_search-submit&position=1&pageNum=0"
url= url.format(job_url,loc_url)
url

# set up the browser

s=Service(ChromeDriverManager().install())
driver= webdriver.Chrome(service=s)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument("--diable-notifications") #new 16.02 
driver.get(url)

driver.maximize_window() #get Chrome full screen 


# We find how many jobs are offered. Note: It may be a rounded number, no exact number given by LinkeIn!

jobs_num = driver.find_element(By.CSS_SELECTOR,"h1>span").get_attribute("innerText")

if len(jobs_num.split('.')) > 1:
    jobs_num = int(jobs_num.split('.')[0])*1000
else:
    jobs_num = int(jobs_num)

jobs_num   = int(jobs_num)
jobs_num


# Not all jobs are shown directly. We create a while loop to browse/ scroll down through all jobs. 

i = 2
printcounter=0
while i <= int(jobs_num/2)+1:
    #We keep scrollind down to the end of the view.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1
    print("Current at: ", i, "Percentage at: ", ((i+1)/(int(jobs_num/2)+1))*100, "%",end="\r")
    try:
        # new 24.03 
        if(printcounter==100):
            # click on every 100th job card --> to prevent error on loading new jobs
            job_click_path = f'/html/body/div/div/main/section/ul/li[{((i-2)*2+1)}]' # kleiner als jobs_num füralle i
            #Wait as long as required, or maximum 10 sec before for the page loading of the detailed job description on the right side of the page
            element= WebDriverWait(driver= driver, timeout=3).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
            element.click() 
            printcounter=0
        else:
            pass
        printcounter +=1
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

# Notiz: circa 7-8 minuten bei 8000 jobs------------------
scrolling_point= datetime.datetime.now()
# Until now we can only scroll down the website but do not have saved anything

##############################################################################################
# 2. Get the basic information: 
# number of listed jobs, basic information of job description on the left panel of the Website 
###############################################################################################
# We get a list containing all jobs that we have found.

# Declare a void list to keep track of all obtaind data.
job_title_list = []
company_name_list = []
location_list = []
date_list = []
job_link_list = []

# This function is added to avoid a certain order (1,2,3,..) when webscraping. 
# That reduces the risk to get banned, as we scan the job like e.g.(104,78,5,2006,..)
# for more see: https://levelup.gitconnected.com/if-you-are-web-scraping-dont-do-these-things-2cba2ebe5b29
def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest

rand_jobs=scrambled(jobs)

#We loop over every job and obtain all the wanted info.
for job in rand_jobs:
    #job_title
    job_title = job.find_element(By.CSS_SELECTOR,"h3").get_attribute("innerText")
    job_title_list.append(job_title)
    
    #company_name
    company_name = job.find_element(By.CSS_SELECTOR,"h4").get_attribute("innerText")
    company_name_list.append(company_name)
    
    #location
    location = job.find_element(By.CSS_SELECTOR,"div>div>span").get_attribute("innerText")
    location_list.append(location)
    
    #date
    date = job.find_element(By.CSS_SELECTOR,"div>div>time").get_attribute("datetime")
    date_list.append(date)
    
    #job_link
    job_link = job.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
    job_link_list.append(job_link)

company_name_list # list of strings
job_link_list # list of strings containing the link
date_list #list of strings with format yyyy-mm-dd
location_list # list of str
job_title_list #list of str

##########################################################################################
# 3. Get detailed Information
# 3.1 Detailed information for every job posting
# 3.2 Click on the company's LinkedIn page to scrape their profile and company size
##########################################################################################

jd = [] #job_description
seniority = []
emp_type = []
job_func = []
job_ind = []
prof = [] # company link
prof_text=[] # company description
comp_size=[]

for item in rand_jobs: #range(len(jobs)):
    num= jobs.index(item) # not rand_jobs, because the order changed there!
    # print(item)
    #job_func0=[]
    #industries0=[]
    # clicking job to view job details
    
    #__________________________________________________________________________ JOB Link
    
    try: 
        job_click_path = f'/html/body/div/div/main/section/ul/li[{num+1}]'

        #Wait as long as required, or maximum 10 sec before for the page loading of the detailed job description on the right side of the page
        element= WebDriverWait(driver= driver, timeout=3).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
        element.click() 


        #job_click = item.find_element(By.XPATH,job_click_path).click() # The URL changes when clicking on a certain job offer

        time.sleep(random.randint(1,3)) # to ensure that the scrolling is not faster than my code on saving the data 
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
        jd.append(None)
        pass
    
    #__________________________________________________________________________ JOB Seniority
    seniority_path='/html/body/div/div/section/div/div/section/div/ul/li[1]/span'
    
    try:
        seniority0 = item.find_element(By.XPATH,seniority_path).get_attribute('innerText')
        seniority.append(seniority0)
    except:
        seniority.append(None)
        pass

    #__________________________________________________________________________ JOB Time
    emp_type_path='/html/body/div/div/section/div/div/section/div/ul/li[2]/span'
    
    try:
        emp_type0 = item.find_element(By.XPATH,emp_type_path).get_attribute('innerText')
        emp_type.append(emp_type0)
    except:
        emp_type.append(None)
        pass
    
    #__________________________________________________________________________ JOB Function
    function_path='/html/body/div/div/section/div/div/section/div/ul/li[3]/span'
    
    try:
        func0 = item.find_element(By.XPATH,function_path).get_attribute('innerText')
        job_func.append(func0)
    except:
        job_func.append(None)
        pass

    #__________________________________________________________________________ JOB Industry
    industry_path='/html/body/div/div/section/div/div/section/div/ul/li[4]/span'
    
    try:
        ind0 = item.find_element(By.XPATH,industry_path).get_attribute('innerText')
        job_ind.append(ind0)
    except:
        job_ind.append(None)
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
        profile_click = WebDriverWait(driver= driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, profile_link_path)))
        profile_click.click() # new tab opens!!!, 12.04 kein neuer tab, 26.04, change existing tab
        # maybe close the pre window with login recommendation
        try:
            descr_path='/html/body/main/section[1]/div/section[1]/div/p'
            prof1= driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/p').get_attribute('innerText')
            prof2= driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd').get_attribute('innerText')
        except:
            close_popup='//*[@id="organization_guest_contextual-sign-in"]/div/section/button' #XPath des Buttons funktioniert!
            #//button[@class=]
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,close_popup))).click() #Pop-up Fenster schließt sich! :)

            #store the information -profile description + company size
            
            descr_path='/html/body/main/section[1]/div/section[1]/div/p'
            prof1= driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/p').get_attribute('innerText')
            prof2= driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd').get_attribute('innerText')
            
            prof.append(prof0)
            prof_text.append(prof1)
            comp_size.append(prof2)
    except:
        prof.append(None)
        prof_text.append(None)
        comp_size.append(None)
        pass
    driver.back()
    time.sleep(2)
    
    

driver.back()
driver.close()

jd#job_description
seniority 
emp_type 
job_func 
job_ind 
prof  # company link
prof_text # company description
comp_size



job_SUBdata = pd.DataFrame({
    'Date': date_list,
    'Company': company_name_list,
    'Title': job_title_list,
    'Location': location_list,
    'Link': job_link_list
})
len(job_SUBdata)
job_SUBdata.to_csv(r"230426_{0}_{1}_.csv".format(job_name,jobs_num))



job_SUB2data= pd.DataFrame({
    'Description': jd,
    'Level': seniority,
    'Type': emp_type,
    'Function': job_func,
    'Industry': job_ind,
})

job_SUB2data.to_csv(r"26042023_{0}_.csv".format(job_name))
