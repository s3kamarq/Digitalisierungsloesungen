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

########### The structure should look like that ############
def theBigWebscrapingFct():
    #do something 
    return #scraped data

for comb in list_of_tuples:
    for ort in ortlist:
        print(comb,ort)
        #Do Webscraping for one search request 
        theBigWebscrapingFct(list_of_tuples)
############ End of Example #######################

#for testing the inner part of the loop
#job_name= techlist[1] 
ort=ortlist[0]
job_name, erfahrung = list_of_tuples[0]















# set up multithreading 
mp.cpu_count()# 8 Kerne
max_worker=3
with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
    executor.map(theMainFunction,list_of_tuples)