from selenium.webdriver.common.by import By

def get_numberOfJobs(driver):
    jobs_num = driver.find_element(By.CSS_SELECTOR,"h1>span").get_attribute("innerText")

    if len(jobs_num.split('.')) > 1:
        jobs_num = int(jobs_num.split('.')[0])*1000
    else:
        jobs_num = int(jobs_num)

    jobs_num   = int(jobs_num)
    return jobs_num