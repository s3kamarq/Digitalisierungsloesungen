# Function to webscrape all company profiles 
from selenium.webdriver.support.ui import WebDriverWait # wait for the data to load before continueing the loop
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # want to continue execution of webscraping only after the detailed description has loaded
import time 
import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
import numpy as np
import pandas as pd



#st values
#maxtab=10
##starttime= datetime.datetime.now()
#

#df= pd.DataFrame([prof,rand_jobs]).transpose()
#u_prof= [*set(df[0])]

#unique=df.drop_duplicates(subset=[0], keep='first') # Company link + corresponding WebElement 
#u_webelem= unique[1]

def scrape_profiles(webelements,unique, maxtab, jobs,driver):
    i=0
    no_profilepage=0
    starttime= datetime.datetime.now()
    
    prof_text=[]
    comp_size=[]

    for item in webelements: #range(len(jobs)):
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
    print(r"Excecution time for profiles: {}".format(endtime-starttime))
    links= unique[0]
    df_profiles= pd.DataFrame({
    'prof':links,
    'description': prof_text,
    'company size': comp_size
    })
    return  df_profiles   

