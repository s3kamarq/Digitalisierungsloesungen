# create URL with predefined characteristics

def create_url(job_name, location, ort, erfahrung):

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
    return url