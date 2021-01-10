#This is the main LinkedIn Scrapper python file

#Importing the required elements
import pandas as pd
import sqlalchemy
import getpass
import pyodbc
import numpy as np

import requests
import urllib.request 
import re
from requests import get

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from parsel import Selector
from lxml import html
from webdriver_manager.chrome import ChromeDriverManager

#Importing custom profile class
import UserProfile
#Declaring the driver
driver = webdriver.Chrome(ChromeDriverManager().install())


#This will be used as the logging in function for the driver
def login():
    print("LOGGING IN.")
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    # locate email form by_class_name
    username = driver.find_element_by_id('username')
    print("LOGGING IN..")
    # send_keys() to simulate key strokes
    username.send_keys('')
    # locate password form by_class_name
    password = driver.find_element_by_id('password')
    # send_keys() to simulate key strokes
    password.send_keys('')
    # locate submit button by_xpath
    log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    print("LOGGING IN...")
    # .click() to mimic button click
    log_in_button.click()
    driver.get('https://www.linkedin.com/talent/home')
    print("Success!")

#This function is used to search for a profile given a series of inputs
#Please note this is not the main searching function, the actual one is given below
def search_profile(*search_inputs):

    #Declaring the var which will be used as the search input
    search_input = ''
    for element in search_inputs:
        #print("Current element", element)
        search_input  += element + ' '

    #Getting the webpage for the search input
    driver.get('https://www.linkedin.com/talent/search?searchKeyword='+search_input+'&start=0')
    #Waiting for the page to load
    time.sleep(4)

    #Elements will return the number of search results on a page
    elements = driver.find_element_by_tag_name('a')
    #print(elements)
    results = driver.find_elements_by_xpath("//*[div]//*[@class='artdeco-entity-lockup__title ember-view']")
    #print('Number of results', len(results))


    #retrieving links and names for the given name
    Name = []
    Link = []

    #Generating the links and the names for the list of results on the page
    for result in results:
        product_name = result.text
        link = result.find_element_by_tag_name('a')
        product_link = link.get_attribute("href")
        
        # append dict to array
        Name.append(product_name)
        Link.append(product_link)

    #Creating the data frame
    df = pd.DataFrame({"Link" : Link, "Name" : Name})

    #Delcaring the list of urls that need to be accessed
    url_list = df['Link'].values.tolist()

    #Declaring all the arrays which will store the names, titles etc for each search
    names = []
    titles = []
    companies = []
    tenures = []
    locations = []

    #This function will return the taxt, given a tag
    def retrieve(tag):
        try:
            txt = tag.text
            # needs some cleaning here
        except:
            txt = "None"  
        return txt
    
    #For each url in the url list, it will get the user profile and write to the arrays
    for linkedin_url in url_list:
            # get the profile URL 
            driver.get(linkedin_url)

        #add a 5 second pause loading each URL
        #sleep(5)
        # assigning the source code for the webpage to variable sel
            sel = Selector(text=driver.page_source) 

            name = sel.xpath('//*[starts-with(@class,"artdeco-entity-lockup__title ember-view")]/text()').extract_first()
            if name:
                name = name.strip()

            # xpath to extract the text from the class containing the job title
            job_title = sel.xpath('//*[starts-with(@class, "position-item__position-title-link ember-view")]/text()').extract_first()

            if job_title:
                job_title = job_title.strip()

            # xpath to extract the text from the class containing the company
            company = sel.xpath('//*[starts-with(@class, "position-item__company-link")]/text()').extract_first()

            if company:
                company = company.strip()

            job_tenure = sel.xpath('//*[starts-with(@class, "background-entity__duration")]/text()').extract_first()

            if job_tenure:
                job_tenure = job_tenure.strip()
                
                # xpath to extract the text from the class containing the location
            location = sel.xpath('//*[starts-with(@class, "background-entity__summary-definition--location")]/text()').extract_first()

            if location:
                location = location.strip()
            
            if company != None:
                if search_inputs[1].upper() in company.upper():
                    names.append(name)
                    titles.append(job_title)
                    companies.append(company)
                    tenures.append(job_tenure)
                    locations.append(location)



    # creating a dataframe with the data we have scraped
    advisors = pd.DataFrame({"Name" : names, "Job Title" : titles, "Company" : companies, "Tenure" : tenures,"Location" : locations})

    #additional step concatinating links with the rest of the data
    result = pd.concat([advisors, df], axis=1, sort=False)
    result.to_csv('./Output/Profile_result_' + search_input+'.csv')


#This will serve as the main function for search the profiles
def search_profiles(profiles):
    
    #Declaring the arrays for getting the information about the profiles provided
    names = []
    titles = []
    companies = []
    tenures = []
    locations = []
    linkedin_urls= []
    public_linkedin_urls= []  
    search_inputs = []
    languages = []
    education = []
    personalwebsite = []
    opentoworkflag = []
    firm_input = []

    #Used to count the number of profiles and which profile it is currently on
    length = len(profiles)
    profile_count = 0


    for profile in profiles:
        profile_count+=1
        search_input = profile.name + " " +  profile.current_firm  + " "
        print("Profile ", profile_count, "of", length, " \t - Searching for", profile.name)

    
        driver.get('https://www.linkedin.com/talent/search?searchKeyword='+search_input+'&start=0')
        time.sleep(4)
        # we check how many links we have got here, should be 12 or 6
        elements = driver.find_element_by_tag_name('a')
        
        results = driver.find_elements_by_xpath("//*[div]//*[@class='artdeco-entity-lockup__title ember-view']")
        


        #retrieving links and names for the given name
        Name = []
        Link = []


        for result in results:
            product_name = result.text
            link = result.find_element_by_tag_name('a')
            product_link = link.get_attribute("href")
            
            # append dict to array
            Name.append(product_name)
            Link.append(product_link)
        #print(Link)
        #print(Name)
        ## In[22]:

        df = pd.DataFrame({"Link" : Link, "Name" : Name})


        url_list = df['Link'].values.tolist()
        
    

        def retrieve(tag):
            try:
                txt = tag.text
                # needs some cleaning here
            except:
                txt = "None"  
            return txt
       
        #Note: the program only gets the first element of the url list 
        #       - the assumption is that the first profile is the correct one

        if(len(url_list) != 0):
            linkedin_url = url_list[0]

            # get the profile URL 
            driver.get(linkedin_url)
            #add a 5 second pause loading each URL
            #sleep(5)

            # assigning the source code for the webpage to variable sel
            sel = Selector(text=driver.page_source) 

            #Getting the name
            name = sel.xpath('//*[starts-with(@class,"artdeco-entity-lockup__title ember-view")]/text()').extract_first()
            if name:
                name = name.strip()

            #Getting the job title
            job_title = sel.xpath('//*[starts-with(@class, "position-item__position-title-link ember-view")]/text()').extract_first()

            if job_title:
                job_title = job_title.strip()

            #Getting the company
            company = sel.xpath('//*[starts-with(@class, "position-item__company-link")]/text()').extract_first()

            if company:
                company = company.strip()


            #Getting the job tenure
            job_tenure = sel.xpath('//*[starts-with(@class, "background-entity__duration")]/text()').extract_first()

            if job_tenure:
                job_tenure = job_tenure.strip()
                        
            #Getting the location of the profile
            location = sel.xpath('//*[starts-with(@class, "background-entity__summary-definition--location")]/text()').extract_first()

            if location:
                location = location.strip()

            #Getting the linkedin url
            public_linkedin_url = sel.xpath('//*[starts-with(@class, "topcard-condensed__public-profile-hovercard t-14")]').extract_first()
            
            #Parsing the linked_in url
            if (public_linkedin_url):  
                public_linkedin_url = (get_url(public_linkedin_url))   

            #Getting the language of the profile
            language = sel.xpath('//*[(@data-test-language-name = "")]/text()').extract()

            #Getting the education of 
            educat = sel.xpath('//*[(@data-test-education-entity-school-link = "")]/text()').extract()
            #data-test-education-entity-school-name   school name
            #print(educat)
            
            if educat:
                for count in range(len(educat)):
                    educat[count] = remove_space(educat[count])
                    #print(educat[count])
               

            else:
                educat = sel.xpath('//*[(@data-test-education-entity-school-name = "")]/text()').extract()
                if educat:
                    for count in range(len(educat)):
                        educat[count] = remove_space(educat[count])
                    
                    
            opentowork = sel.xpath('//*[starts-with(@class, "summary-card__header")]/text()').extract_first()
            
            if opentowork:
                opentowork = opentowork.strip()
            
            # xpath to extract the text from the class containing the location
            personal_website = sel.xpath('//*[starts-with(@class, "personal-info__link personal-info__link--website")]').extract_first()

            #print(personal_website)    
            

            if personal_website:  
                personal_website = (get_url(personal_website))

            
            if company != None:
                if profile.current_firm.upper() in company.upper():
                    print("Profile found! "+ profile.name+ "'s profile has been extracted \n")
                    
                    #print(profile.current_firm.upper() +" contains" + company.upper())
                    names.append(name)
                    titles.append(job_title)
                    companies.append(company)
                    tenures.append(job_tenure)
                    locations.append(location)
                    linkedin_urls.append(linkedin_url)
                    languages.append(language)
                    education.append(educat)
                    opentoworkflag.append(opentowork)
                    personalwebsite.append(personal_website)
                    search_inputs.append(profile.name + " " +  profile.middle_name)
                    public_linkedin_urls.append(public_linkedin_url)
                    firm_input.append(profile.current_firm_input)

                else:
                    #print(profile.current_firm.upper() +" does not contain " + company.upper())
                    names.append("Null")
                    titles.append("Null")
                    companies.append("Null")
                    tenures.append("Null")
                    locations.append("Null")
                    linkedin_urls.append("Null")
                    public_linkedin_urls.append("Null")
                    languages.append("Null")
                    education.append("Null")
                    opentoworkflag.append("Null")
                    personalwebsite.append("Null")
                    search_inputs.append(profile.name + " " +  profile.middle_name)
                    firm_input.append(profile.current_firm_input)
            else:
                #print(profile.name + " " +  profile.middle_name)
                names.append("Null")
                titles.append("Null")
                companies.append("Null")
                tenures.append("Null")
                locations.append("Null")
                linkedin_urls.append("Null")
                languages.append("Null")
                education.append("Null")
                opentoworkflag.append("Null")
                public_linkedin_urls.append("Null")
                personalwebsite.append("Null")
                firm_input.append(profile.current_firm_input)
                search_inputs.append(profile.name + " " +  profile.middle_name)
        else:
            #print(profile.name + " " +  profile.middle_name)
            names.append("Null")
            titles.append("Null")
            companies.append("Null")
            tenures.append("Null")
            locations.append("Null")
            linkedin_urls.append("Null")
            languages.append("Null")
            education.append("Null")
            opentoworkflag.append("Null")
            public_linkedin_urls.append("Null")
            personalwebsite.append("Null")  
            search_inputs.append(profile.name + " " +  profile.middle_name)
            firm_input.append(profile.current_firm_input)

    # creating a dataframe with the data we have scraped
    advisors = pd.DataFrame({
        "Name" : names, 
        "Job Title" : titles, 
        "Company" : companies, 
        "Tenure" : tenures,
        "Location" : locations, 
        "Recruiter LinkedIn" : linkedin_urls,
        "Languages" : languages, 
        "Education" : education,
        "Open to work" : opentoworkflag, 
        "Personal website" : personalwebsite, 
        "Public LinkedIn" : public_linkedin_urls, 
        "Name Input": search_inputs,
        "Firm Input": firm_input
        })

    #additional step concatinating links with the rest of the data

    #result = pd.concat([advisors, df], axis=1, sort=False)

    result = advisors

    
    result.to_csv('./Output/ProfileSearch.csv')



def get_url(input):
    
    output = ""
    previous_char = ''
    
    trigger = False
    for char in input:
        #print(char)
        if(char == "\"" and previous_char == '='):
            trigger = True
            continue

        if(char == "\"" and previous_char != '='):
            #print("Current char is " + char + " while the previous char is " + previous_char)
            break

        if(trigger):
            output+=char
            previous_char = char

        previous_char = char
    #print(output + " is the new name")
    return output

def remove_space(input):
    #Declaring vars
    output = ""
    previous_char = ' '
    trigger = False

    for char in input[2:]:
        #This will be used to determine if it hits a \n
        current_string = char+previous_char

        #Once the emppty spaces at the begginning end, it will trigger true to start getting the chars
        if(char != " " and previous_char == " "):
            trigger = True   

        #If it hits \n, it will break
        if("\n" in current_string):
            break

        #If its triggered it will add the output and change the previous char
        if(trigger):
            output+=char
            previous_char = char

        previous_char = char
    return output



#Defining the main method
def main():

    #Logging in
    login()

    #Creating list of profile for first lines
    profile_list = UserProfile.CreatProfileList("SampleData.csv")
    
    #Searching the profiles based on the given list
    search_profiles(profile_list)
    
    print("========================")
    print("Profile search complete!")
    print("========================")
   

#unning the main method
if __name__ == "__main__":main()