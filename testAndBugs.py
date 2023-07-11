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
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options # to prevent pop-up window where Linkedin wants me to login
import numpy as np
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


############################################################################
# 1. Open LinkedIn Website in the Browser 
############################################################################

techlist=['Cloud-Computing', 'Online-Marketing','E-Commerce','Künstliche Intelligenz','AI','Analytics', 'Big Data',
          'Internet of Things (IoT)', 'IoT','Deep Tech','Digitale Transformation', 'Industrie 4.0',
          'Robotik','Fintech', 'Blockchain','3D-Druck']
ortlist= [1,2,3]
berufserfahrunglist=[1,2,3,4,5]

job_name= techlist[1] 
ort=ortlist[0]
erfahrung=berufserfahrunglist[1]
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
# f_JT=F is default filter, so only full-time jobs are considered 
url = "https://de.linkedin.com/jobs/search?keywords={0}&location={1}&geoId=101282230&trk=guest_homepage-basic_jobs-search-bar_search-submit&f_JT=F&f_WT={2}&f_E={3}&position=1&pageNum=0"
url= url.format(job_url,loc_url, ort,erfahrung)
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
scroll_time_start=datetime.datetime.now()
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

scroll_time_end=datetime.datetime.now()

job_lists = driver.find_element(By.CLASS_NAME,"jobs-search__results-list")
jobs = job_lists.find_elements(By.TAG_NAME,"li") # return a list

len(jobs)
scroll_time=scroll_time_end-scroll_time_start
scroll_time
# 2min circa



##############################################################################################
#
# 2. Get the basic information: 
# number of listed jobs, basic information of job description on the left panel of the Website 
#
###############################################################################################
# We get a list containing all jobs that we have found.

# Declare a void list to keep track of all obtaind data.
#job_title_list = []
#company_name_list = []
#location_list = []
#date_list = []
#job_link_list = []

# This function is added to avoid a certain order (1,2,3,..) when webscraping. 
# That reduces the risk to get banned, as we scan the job like e.g.(104,78,5,2006,..)
# for more see: https://levelup.gitconnected.com/if-you-are-web-scraping-dont-do-these-things-2cba2ebe5b29
def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest

rand_jobs=scrambled(jobs)

def basic_info(rand_jobs=rand_jobs,job_title_list = [],company_name_list = [],
               location_list = [],date_list = [],job_link_list = []):
    
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
    
    return company_name_list,job_link_list,date_list,location_list,job_title_list


basicinfo_time_start=datetime.datetime.now()
company_name_list,job_link_list,date_list,location_list,job_title_list= basic_info()
# 3min 30
basicinfo_time_end=datetime.datetime.now()
basicinfo_time=basicinfo_time_end-basicinfo_time_start
basicinfo_time


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

#start=0
#end=10
def detail_info(start, end,jd ,seniority,emp_type,job_func,job_ind,prof,rand_jobs=rand_jobs):

    detail_timestart= datetime.datetime.now()
    for item in rand_jobs[start:end]: #range(len(jobs)):
        num= jobs.index(item) # not rand_jobs, because the order changed there!
        print(num)
        #job_func0=[]
        #industries0=[]
        # clicking job to view job details
        
        #__________________________________________________________________________ JOB Link
        
        try: 
            job_click_path = f'/html/body/div[1]/div/main/section[2]/ul/li[{num+1}]'
            #Wait as long as required, or maximum 10 sec before for the page loading of the detailed job description on the right side of the page
            element= WebDriverWait(driver= driver, timeout=20).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
            time.sleep(random.randint(2,4)) # to ensure that the scrolling is not faster than my code on saving the data 
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
            prof.append(prof0)
            
        except:
            prof.append(None)
            pass
        detail_timeend=datetime.datetime.now() 
        #time.sleep(2)
    
    return jd,seniority,emp_type, job_func,job_ind ,prof


jd1,seniority1,emp_type1, job_func1,job_ind1 ,prof1 =detail_info(start=0, end=10, jd=[], seniority=[],emp_type=[],job_func=[], job_ind=[],prof=[])
detail_timestart= datetime.datetime.now()
jd,seniority,emp_type, job_func,job_ind ,prof =detail_info(start=10,jd=jd, seniority=seniority,emp_type=emp_type, job_func=job_func, job_ind=job_ind, prof=prof,rand_jobs=rand_jobs, end=len(rand_jobs))
detail_timeend=datetime.datetime.now() 

time_detailinfo= detail_timeend-detail_timestart
time_detailinfo

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


dataMerge.to_csv(r"df1107_{0}_{1}_{2}_{3}.csv".format(job_name,jobs_num,ort,erfahrung))
dataMerge.to_excel(r"df1107_{0}_{1}_{2}_{3}.xlsx".format(job_name,jobs_num,ort,erfahrung))

dataMerge.to_pickle(r"df1107_{0}_{1}_{2}_{3}.pkl".format(job_name,jobs_num,ort,erfahrung))

####################
#
#Check for one detailed info if there is 'Loading took too much time'
#
###################

item=rand_jobs[5]

num= jobs.index(item) # not rand_jobs, because the order changed there!
print(num)
#job_func0=[]
#industries0=[]
# clicking job to view job details

#__________________________________________________________________________ JOB Link

try: 
    job_click_path = f'/html/body/div[1]/div/main/section[2]/ul/li[{num+1}]'
    #Wait as long as required, or maximum 10 sec before for the page loading of the detailed job description on the right side of the page
    element= WebDriverWait(driver= driver, timeout=20).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
    time.sleep(random.randint(2,4)) # to ensure that the scrolling is not faster than my code on saving the data 
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
    prof.append(prof0)
    
except:
    prof.append(None)
    pass
detail_timeend=datetime.datetime.now() 
#time.sleep(2)

##############################################################################################################
#
# Get the information from the profiles 
#
########################################################################################################

#driver.back()
#driver.close()
# Only webscrape the profile page of a company ONCE. One company often has multiple job offers

df= pd.DataFrame([prof,rand_jobs]).transpose()
#u_prof= [*set(df[0])]

unique=df.drop_duplicates(subset=[0], keep='first') # Company link + corresponding WebElement 
u_webelem= unique[1]

#unique_prof= [*set(prof)]
#len(unique_prof) # for 1 example 329.. that is one third! a lot of time saving by avoiding duplicates

driver.current_window_handle # In welchem Tab befinde ich mich?
#driver.switch_to.new_window()
# Lets open https://www.facebook.com/ in the third tab
#driver.execute_script("window.open('about:blank','thirdtab');")
driver.switch_to.window("thirdtab")
#driver.get('https://www.facebook.com/')
driver.window_handles # Welche und wieviele Tabs habe ich offen?
driver.close()
#driver._switch_to.window(driver.window_handles[1])
#driver.close()
driver.switch_to.window(driver.window_handles[0])

driver.execute_script("window.open('about:blank','thirdtab');")
#driver.switch_to.window('thirdtab')
#driver.get(prof[0])
#driver.close()

## Test version: Open 30 Tabs in total, but after the 5th tab, close them. So 6 times there are 5 tabs open.
# As I do not want 1000 tabs open when webscraping the company description, I webscrape 5 profiles at a time, close the tabs, open the next five and so on..
# Note: The Company description is at an new URL, thus new page on LinkedIn
for i in range(1,31):
    print(i)
    time.sleep(1)
    if i%5 ==0:
        driver.switch_to.new_window()
        #scraping
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        driver.switch_to.new_window()
        #scraping
    

#close tabs that are not needed anymore, all except the first tab
for handle in driver.window_handles[1:]:
    driver.switch_to.window(handle)
    driver.close()

driver.switch_to.window(driver.window_handles[0])

prof_text=[]
comp_size=[]

#item=rand_jobs[0]


#fixed values
maxtab=10
i=0
starttime= datetime.datetime.now()
no_profilepage=0

for item in u_webelem[0:20]: #range(len(jobs)):
    num= jobs.index(item) # not rand_jobs, because the order changed there!
    print(num)
    i+=1

    if i%maxtab==0:
        #__Scraping block__________________________________________________
        try: 
            job_click_path = f'/html/body/div[1]/div/main/section[2]/ul/li[{num+1}]'
            #Wait as long as required, or maximum 10 sec before for the page loading of the detailed job description on the right side of the page
            element= WebDriverWait(driver= driver, timeout=3).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
            element.click() 


            #job_click = item.find_element(By.XPATH,job_click_path).click() # The URL changes when clicking on a certain job offer

            time.sleep(random.randint(2,4)) # to ensure that the scrolling is not faster than my code on saving the data 
            # random waiting time to avoid a certain structure,so I do not get banned
            #job_click = item.find_element(By.XPATH,'.//a[@class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"]')
        except TimeoutException:
            print(r"Loading took too much time")
            pass 
        
        try:
            profile_click = WebDriverWait(driver= driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/a')))
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL)
            actions.click(on_element=profile_click)
            # New Tab opens
            actions.perform() # here can occur: ElementNotInteractableException: Message: element not interactable --> if the detailed info does not load 
            driver.switch_to.window(driver.window_handles[-1]) # always open the last tab
            try:
                time.sleep(1)
                try:
                    prof1= driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/p').get_attribute('innerText')
                    prof2= driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd').get_attribute('innerText')
                except NoSuchElementException: 
                    prof1= np.nan
                    prof2=np.nan
            # maybe close the pre window with login recommendation
            except:
                time.sleep(1)
                print('pop-up')
                close_popup='//*[@id="organization_guest_contextual-sign-in"]/div/section/button' #XPath des Buttons funktioniert!
                #//button[@class=]
                wait=WebDriverWait(driver,5)
                wait.until(EC.visibility_of_element_located((By.XPATH,close_popup))).click() #Pop-up Fenster schließt sich! :)

                #store the information -profile description + company size
                try:
                    prof1= driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/p').get_attribute('innerText')
                    prof2= driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd').get_attribute('innerText')

                except NoSuchElementException: #special case: The company has no profile description on their page, then save them as np.nan
                    prof1= np.nan 
                    prof2=np.nan
            finally:
                prof_text.append(prof1) #append the "About us" for each job posting in a list
                comp_size.append(prof2) #append the company size for each job posting in a list
            for handle in driver.window_handles[1:]:
                driver.switch_to.window(handle)
                driver.close()
            driver.switch_to.window(driver.window_handles[0]) # after each iteration, switch to the "main tab"/ the LinkedIn job offer website 
        except TimeoutException: #special case: the company has no profile page at LinkedIn
            no_profilepage+=1 #count how many job postings have limited information
            pass
    
    else:
        #__Scraping block__________________________________________________
        try: 
            job_click_path = f'/html/body/div[1]/div/main/section[2]/ul/li[{num+1}]'
            #Wait as long as required, or maximum 10 sec before for the page loading of the detailed job description on the right side of the page
            element= WebDriverWait(driver= driver, timeout=3).until(EC.presence_of_element_located((By.XPATH, job_click_path)))
            element.click() 


            #job_click = item.find_element(By.XPATH,job_click_path).click() # The URL changes when clicking on a certain job offer

            time.sleep(random.randint(2,4)) # to ensure that the scrolling is not faster than my code on saving the data 
            # random waiting time to avoid a certain structure,so I do not get banned
            #job_click = item.find_element(By.XPATH,'.//a[@class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"]')
        except TimeoutException:
            print(r"Loading took too much time")
            pass 

        try:
            profile_click = WebDriverWait(driver= driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/div[2]/section/div/a')))
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL)
            actions.click(on_element=profile_click)
            # New Tab opens
            actions.perform()
            driver.switch_to.window(driver.window_handles[-1]) # always open the last tab
            try:
                time.sleep(1)
                try:
                    prof1= driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/p').get_attribute('innerText')
                    prof2= driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd').get_attribute('innerText')

                except NoSuchElementException: #special case: The company has no profile description on their page, then save them as np.nan
                    prof1= np.nan
                    prof2=np.nan
            # maybe close the pre window with login recommendation
            except:
                time.sleep(1)
                print('pop-up')
                close_popup='//*[@id="organization_guest_contextual-sign-in"]/div/section/button' #XPath des Buttons funktioniert!
                #//button[@class=]
                wait=WebDriverWait(driver,5)
                wait.until(EC.visibility_of_element_located((By.XPATH,close_popup))).click() #Pop-up Fenster schließt sich! :)

                #store the information -profile description + company size
                try:
                    prof1= driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[1]/div/p').get_attribute('innerText')
                    prof2= driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]/dd').get_attribute('innerText')
                except NoSuchElementException: 
                    prof1= np.nan
                    prof2=np.nan
                
            finally:
                prof_text.append(prof1) #append the "About us" for each job posting in a list
                comp_size.append(prof2) #append the company size for each job posting in a list

            driver.switch_to.window(driver.window_handles[0]) # after each iteration, switch to the "main tab"/ the LinkedIn job offer website 
        except TimeoutException: #special case: the company has no profile page at LinkedIn
            no_profilepage+=1 #count how many job postings have limited information/no separate profile page
            pass

endtime=datetime.datetime.now()    

links= unique[0]
df_profiles= pd.DataFrame({
    'ID':links[0:148],
    'description': prof_text,
    'company size': comp_size
    }
)

df_profiles.to_pickle(r"testdatProfiles.pkl")
df_profiles.to_csv(r"testdata_profiles.csv")


i=0
for item in u_webelem[0:40]: #range(len(jobs)):
    num= jobs.index(item) # not rand_jobs, because the order changed there!
    #print(num)
    #print(u_webelem)
    i+=1
    print(i)
    #if i%maxtab==0:
    #    print("close tab")
    #    driver.switch_to.new_window()
    #    #scraping
    #    for handle in driver.window_handles[1:]:
    #        driver.switch_to.window(handle)
    #        driver.close()
    #    driver.switch_to.window(driver.window_handles[0])
    #else:
    #    driver.switch_to.new_window()


####################################################################################
# 
# open saved data
#
####################################################################################

jobdata= pd.read_pickle(r'df0407_Online-Marketing_1000_1_2.pkl')
jobdata.columns
jobdata.head()

firmdata= pd.read_pickle(r'testdatProfiles.pkl')
firmdata.columns
firmdata.head()


len(jobdata.profile_Link) # length of 1000
len(firmdata.ID) #length of 148 not all were scraped?
jobdata= jobdata.rename(columns={'profile_Link':'ID'})
jobdata.columns
#len(jobdata['profile_Link'])-len(jobdata['profile_Link'].drop_duplicates()) #520 unique

results= jobdata.merge(firmdata, how='outer', on='ID' , validate='many_to_one')

results.shape

results.to_excel("JobFirmsExample.xlsx")
len(results['ID'])-len(results['ID'].drop_duplicates()) 