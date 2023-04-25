import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
import datetime #to check the performance of the code
import random
from selenium.webdriver.support import expected_conditions as EC # want to continue execution of webscraping only after the detailed description has loaded
from selenium.webdriver.support.ui import WebDriverWait # wait for the data to load before continueing the loop
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options # to prevent pop-up window where Linkedin wants me to login

job_name= "Robotik"
location= "Deutschland"

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


url = "https://de.linkedin.com/jobs/search?keywords={0}&location={1}&geoId=101282230&trk=guest_homepage-basic_jobs-search-bar_search-submit&position=1&pageNum=0"
url= url.format(job_url,loc_url)
url
s=Service(ChromeDriverManager().install())
driver= webdriver.Chrome(service=s)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument("--diable-notifications") #new 16.02 
driver.get(url)

driver.maximize_window() #get Chrome full screen 
#We find how many jobs are offered.
jobs_num = driver.find_element(By.CSS_SELECTOR,"h1>span").get_attribute("innerText")

if len(jobs_num.split('.')) > 1:
    jobs_num = int(jobs_num.split('.')[0])*1000
else:
    jobs_num = int(jobs_num)

jobs_num   = int(jobs_num)
jobs_num

# durch die Jobs scrollen wird weg gelassen
job_lists = driver.find_element(By.CLASS_NAME,"jobs-search__results-list")
jobs = job_lists.find_elements(By.TAG_NAME,"li") # return a list
job_title_list = []
company_name_list = []
location_list = []
date_list = []
job_link_list = []


#We loop over every job and obtain all the wanted info.
for job in jobs[0:2]:
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



jd = [] #job_description
seniority = []
emp_type = []
job_func = []
job_ind = []
prof = [] # company link
prof_text=[] # company description
comp_size=[]

item= jobs[1] ##################change to 1 for the second job

num= jobs.index(item) 
num

job_click_path = f'/html/body/div/div/main/section/ul/li[{num+1}]'
element= WebDriverWait(driver= driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
element.click()

jd_path = '/html/body/div/div/section/div/div/section/div/div/section/div'
jd0 = item.find_element(By.XPATH,jd_path).get_attribute('innerText')
jd.append(jd0)
jd

seniority_path='/html/body/div/div/section/div/div/section/div/ul/li[1]/span'
seniority0 = item.find_element(By.XPATH,seniority_path).get_attribute('innerText')
seniority.append(seniority0)
seniority

emp_type_path='/html/body/div/div/section/div/div/section/div/ul/li[2]/span'
emp_type0 = item.find_element(By.XPATH,emp_type_path).get_attribute('innerText')
emp_type.append(emp_type0)
emp_type

function_path='/html/body/div/div/section/div/div/section/div/ul/li[3]/span'
func0 = item.find_element(By.XPATH,function_path).get_attribute('innerText')
job_func.append(func0)
job_func

industry_path='/html/body/div/div/section/div/div/section/div/ul/li[4]/span'
ind0 = item.find_element(By.XPATH,industry_path).get_attribute('innerText')
job_ind.append(ind0)
job_ind

# Den Path Finden: rechtklick auf das gewünschte Objekt/ den Text >> untersuchen, 
# dann rechtsklick auf die markierte Stelle im HTML Code >> kopieren >> gesamten XPATH kopieren
profile_link_path = '/html/body/div[3]/div/section/div[2]/section/div/a'
#f'/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a' #vorher

#second: /html/body/div[3]/div/section/div[2]/section/div/a

profile_path= '/html/body/main/section[1]/div/section[1]/div/p'

prof0 = item.find_element(By.XPATH, profile_link_path).get_attribute('href')
prof0
profile_click = WebDriverWait(driver= driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, profile_link_path)))
profile_click.click() # new tab opens!!!, 12.04 kein neuer tab
# maybe close the pre window with login recommendation
try:
    prof_text= item.find_element(By.XPATH,profile_path).get_attribute('innerText')
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

driver.back()
driver.close()
    
