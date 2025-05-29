# school_data.py
# AUTHOR NAME
#
# A terminal-based application for computing and printing statistics based on given input.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd
import numpy as np
import re
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022

df = pd.read_csv("Assignment3Data.csv") #Reads csv into data frame
df = df.dropna(axis=1, how='all')#Removing empty spaces
unique_school_names = df['School Name'].unique() #These two used Pandas because I need to retain their original indexing.
unique_school_codes = df['School Code'].astype(str).unique()
unique_school_year = np.array(sorted(set(df['School Year'])))# Years is fine because it is naturally ordered in ascending order when loaded.
school_name_to_index = {name: i for i, name in enumerate(unique_school_names)} #Key value pairs generated for school_names where the value is their index in their respective unique collection.
school_code_to_index = {str(code): i for i, code in enumerate(unique_school_codes)}
school_year_to_index = {str(year): i for i, year in enumerate(unique_school_year)}
All_years = np.array([year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022]) #Creation of the 2D array
reshaped_years = np.array([year.reshape(20, 3) for year in All_years])#Reshaping into 3D array
Name_Code_dict = dict(zip(unique_school_names, unique_school_codes))#Zipping together the names and corresponding codes of schools into a key/value pair. The reason I need 2 of them is because sometimes someone enters only Code and I need to know what the Name is, and vice versa.
Code_Name_dict = dict(zip(unique_school_codes, unique_school_names))



def query_school_data(school_id, id_type):
    """takes in school_id, which can be either name or code(it is flexible because of validation and input parsing later on), gets assigned an id_type internally and search for each type of id separately in the corresponding array of names or codes."""
    if id_type == "name":
        if school_id not in school_name_to_index: #Checks if the name appears in our collection of school names
            raise ValueError("You must enter a valid school name or code.")# Raises VE if not found
        school_index = school_name_to_index[school_id]# is found, collects the index of the corresponding name.
    elif id_type == "code":
        school_id = str(school_id)
        if school_id not in school_code_to_index: #Checks if the code appears in our collection of school names
            raise ValueError("You must enter a valid school name or code.")# Raises VE if not found
        school_index = school_code_to_index[school_id]# is found, collects the index of the corresponding code.
    else:
        raise ValueError("id_type must be 'name' or 'code'") #This should never happen, id_type is determined internally through validation, but I put it here anyway just in case.
    
    
    return reshaped_years[:, school_index, :] # Return enrollment data for this school across all years



def extract_code_and_name(user_input):  
    """This is for processing user_input, returns the input string to two variables name and code."""
    code_match = re.search(r'\d+', user_input) #checks to see if the input only has numbers, if so returns true.
    school_code = int(code_match.group()) if code_match else None # if the above returns true, type cast input to int and asisgn to school_code.
    school_name = re.sub(r'\d+', '', user_input).strip()# if input is a combination of text and number, strip the number then assign text to school_name.
    return school_name, school_code



def find_values_over_x(arr, x):
    """This function takes an array and stores values greater than x in another array."""
    greater = arr[arr > x]
    if greater.size != 0:
        return True, greater # I need the boolean return to simplify the logical evaluation for the question output later.
    else:
        return False, greater






def main():
    
    print("ENSF 692 School Enrollment Statistics")
    print("Shape of full data array:", reshaped_years.shape)
    print("dimensions of full data array:", reshaped_years.ndim)
    user_input = input("Enter the school name and/or school code (e.g. 'Centennial High School 1224'): ") #prompts user.
    school_name, school_code = extract_code_and_name(user_input)#user_input is passed to the function defined above for parsing and value separation.
    found = False #initializes a found boolean to false at the start of program execution.
    if school_name: #this basically says if there's a text portion in input, since unless school_name is None this will return True.
        try:
            result = query_school_data(school_name, id_type="name")# passes the text portion of user_input to query, id_type is manually set to 'name' because we are passing a name to the function, not a code.
            found = True #In this branch we did find something, otherwise the above statement will fail.
        except ValueError as e: #This is kind of redundant since the function already protects against invalid input, but we'll never know if someone gets really creative with their inputs.
            print("You must enter a valid school name or code.")

    if school_code is not None: #There is a numerical portion of input.
        try:
            result = query_school_data(school_code, id_type="code")# passes the numerical portion of user_input to query, id_type is manually set to 'code' because we are passing a code to the function, not a name.
            found = True #In this branch we did find something, otherwise the above statement will fail.
        except ValueError as e:
            print("You must enter a valid school name or code.") 
    #Note: I did consider the case where both parts of the input are present, however in that case executing either branch will be sufficient since they produce the same result.
    print("\n***Requested School Statistics***\n")
    if found: #This just avoids any unpredictable behaviour and saves runtime in the case of false execution, all of the following will only print if the query found something matching the input.
        if school_name:
            print("School Name: ", school_name, "School Code: ", Name_Code_dict[school_name]) #This is where the dictionary I zipped together earlier comes into action, if there's a name portion, using the name value as a key will return the corresponding code and vice versa, so I only need to know 1 of the 2 to know both.
        if not school_name:
            print("School Name: ", Code_Name_dict[str(school_code)], "School Code: ", school_code)


        """The rest are mostly just simply answering questions, nothing too notable."""


        print("Mean enrollment for Grade 10 across all years: ","{:.0f}".format(np.nanmean(result[:,0]))) #Nanmean calculates mean while ignoring nan, aka it's a masking operation.
        print("Mean enrollment for Grade 11 across all years: ", "{:.0f}".format(np.nanmean(result[:,1]))) #Worth while to mention for criteria satisfication, result[:,1] returns a slice, which means it's a subarray view.
        print("Mean enrollment for Grade 12 across all years: ", "{:.0f}".format(np.nanmean(result[:,2])))
        print("Highest enrollment for a single grade within the entire time period: ", "{:.0f}".format(np.nanmax(result)))
        print("Lowest enrollment for a single grade within the entire time period: ", "{:.0f}".format(np.nanmin(result)))
        print("Total enrollment for each year from 2013 to 2022: ")
        year = 2013
        yearlysum = [] #Used to collect individual sums across 10 years.
        for i in range (len(result)):
            print(year, ": ", "{:.0f}".format(np.nansum(result[i])))
            yearlysum.append(np.nansum(result[i]))
            year+=1

        print("Total ten year enrollment: ", "{:.0f}".format(np.nansum(result)))
        print("Mean total yearly enrollment over 10 years: ", "{:.0f}".format(np.nanmean(yearlysum)))
        greater_than_500, G500_array = find_values_over_x(result, 500)
        if greater_than_500:
            Median = np.nanmedian(G500_array)
            print("For enrollments over 500, the median was: ", "{:.0f}".format(Median))
        else:
            print("No enrollments over 500.")



    # Print Stage 3 requirements here
    print("\n***General Statistics for All Schools***\n")
    print("The mean enrollment in 2013: ", "{:.0f}".format(np.nanmean(year_2013)))# Note this normally woudln't be possible, it so happens we have the data ordered by year and the individual arrays are named with year number.
    print("The mean enrollment in 2022: ", "{:.0f}".format(np.nanmean(year_2022)))# This is one instance why my year to index dictionary will be useful, however in this case analyzing individual year arrays is far easier.
    print("Total graduating class of 2022 across all schools: ", "{:.0f}".format(np.nansum(reshaped_years[school_year_to_index['2022'], :, 2])))#Useful implementation of school_year_to_index in order to find data slice under year 2022.
    print("Highest enrollment for a single grade within the entire time period (across all schools): ", "{:.0f}".format(np.nanmax(reshaped_years)))
    print("Lowest enrollment for a single grade within the entire time period (across all schools): ", "{:.0f}".format(np.nanmin(reshaped_years)))
if __name__ == '__main__':
    main()

