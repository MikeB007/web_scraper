#Required to write to a csv file
import csv
import xlrd

#Needed in order to compare names
from difflib import SequenceMatcher


#This function create the Profile Object
# class UserProfile():
#     def __init__(self, name_input, linked_in_input, preferred_name_input, current_firm_input, current_address_input,current_city_input,current_province_input, current_postal_code_input, compliance_input, gender_input, number_of_jobs_input, total_tenure_input,tenure_input, registered_province_input, job_title_input, start_date_input, end_date_input, current_position_input, status_input, notes_input):
#         self.name = generate_name(name_input)
#         self.middle_name = generate_middle_name(name_input)
#         self.linked_in = linked_in_input
#         self.preferred_name = preferred_name_input
#         self.current_firm = generate_current_firm(current_firm_input)
#         self.current_address = current_address_input
#         self.current_city = current_city_input
#         self.current_province = current_province_input
#         self.current_postal_code = current_postal_code_input
#         self.compliance = compliance_input
#         self.gender = gender_input
#         self.number_of_jobs = number_of_jobs_input
#         self.total_tenure = total_tenure_input
#         self.tenure = tenure_input
#         self.registered_province = registered_province_input
#         self.job_title = job_title_input
#         self.start_date = start_date_input
#         self.end_date = end_date_input
#         self.currrent_position = current_position_input
#         self.status = status_input
#         self.notes = "null"

#This function create the Profile Object
class UserProfile():
    def __init__(self, name_input, current_firm_input):
        self.name = generate_name(name_input)
        self.middle_name = generate_middle_name(name_input)
        self.current_firm = generate_current_firm(current_firm_input)
        self.current_firm_input = current_firm_input


def generate_name(input):
    output = ""
    for char in input:
        if(char != "("):
            output += char
        else: break
    #print(output + " is the new name")


    if(output == input):
        return output    
    else:
        return output[:-1]

def generate_middle_name(input):
    output = ""
    trigger = False
    for char in input:
        if(char == "("):
            trigger = True
            output+=char
            continue
        if(char == ")"):
            output+=char
            trigger = False
        if(trigger):
            output+=char
        
    #print(output + " is the new name")
    return output

def generate_current_firm(input):
    output = ""
    for char in input:
        
        if(char != ' '):
            output += char
        else: break
    #print(output + " is the firm")
    return output

#This function creates a list of profiles based on the name of the csv file provided
def CreatProfileList(data):
    with open(data, newline='') as csv_file:
        profile_list = []

        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        line_count = 0
        last_profile = ''
        first_element = True

        for column in csv_reader:

            #Change the column numbers if data changes
            new_profile = UserProfile(column[0], column[3])
            
            #This outputs the firm and the name of a profile
            # Details(new_profile)
            #print("This is the current profile "+ new_profile.name)
            if(first_element):
                profile_list.append(new_profile)
                last_profile=new_profile
                first_element = False

            elif (last_profile.name != new_profile.name):
                last_profile=new_profile
                #print(last_profile.name + " is not the same as " +new_profile.name)
                profile_list.append(new_profile)
        print("==================================      ")    
        print("Generated " + str(len(profile_list)) + " unique user profiles.")
        print("==================================      ")  
    return profile_list



#This function will return the ratio of how similar two profiles are two each other based on their title
def ProfileSimilarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

#This function will help find itself within another csv file based on its name,
#It will use the similarity package to find itself
def FindProfile(profile_input, other_profile_list):
    profile_position=-1
    for element in range(len(other_profile_list)-1):
        if(ProfileSimilarity(profile.name,other_profile_list[element].name) > 0.9):
            profile_position = element
            
    return profile_position






    