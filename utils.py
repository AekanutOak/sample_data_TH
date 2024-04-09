import os
import json
import time
import csv
import random
import re
import numpy as np
from datetime import timedelta
from datetime import datetime

# For changing text color on console/terminal
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m' # For console/terminal default color

# Preset of colored text for displaying on console/terminal
warning_label = f"{Color.YELLOW}Warning:{Color.RESET}"
error_label = f"{Color.RED}Error:{Color.RESET}"
success_label = f"{Color.GREEN}Success:{Color.RESET}"

# Will later use to join any relative path to create absolute path to prevent file does not exist
current_directory = os.getcwd()

# load and validate config file
def load_config(keys=None):

    # stamp the time, will later use to measure execution time in cases valiadtion of config file is fail
    start_time = time.time()

    # convert to absolute path
    config_path = os.path.join(current_directory,"./config.json")
    with open(config_path,"r") as f:
        config = json.loads(f.read())

    # Handle people config
    if(keys == "people"):
        people_config = config["people"]

        # If this true, the program must be terminated until config file is all validated
        error = False

        for i in people_config.keys():

            # config value should be integer
            if(type(people_config[i]) != int):
                error = True
                print(f"{error_label} Expect {i} to be {type(10)} but get {type(people_config[i])} instead.")

            else:
                # config value should be non-zero integer
                if(people_config[i] <= 0):
                    error = True
                    print(f"{error_label} Expect {i} to be non-zero value but get {people_config[i]} instead")

                else:
                    # config value should be non-zero integer
                    if(people_config[i] <= 0):
                        error = True
                        print(f"{error_label} Expect {i} to be non-zero value but get {people_config[i]} instead")

                    else:
                    # If min age is inappropriate, raise warning instead of terminate program
                        if("min" in i):
                            if(people_config[i] < 20):
                                print(f"{warning_label} \"{i} = {people_config[i]}\" seem to be incorrect. You can ignore this error if you are sure that the age is legal")
                            
                        # If max age is inappropriate, raise warning instead of terminate program
                        elif("max" in i):
                            if(people_config[i] > 110):
                                print(f"{warning_label} \"{i} = {people_config[i]}\" seem to be incorrect. You can ignore this error if you are sure that people will be still alive at that age")

                        # If male min and max age are created appropriate age range
                        if(i == "male_min_age"):
                            if(int(people_config[i]) >= int(people_config["male_max_age"])):
                                error = True
                                print(f"{error_label} male age range is incorrect, get: ({people_config[i]} - {people_config["male_max_age"]})")

                        # If female min and max age are created appropriate age range
                        elif(i == "female_min_age"):
                            if(int(people_config[i]) >= int(people_config["female_max_age"])):
                                error = True
                                print(f"{error_label} female age range is incorrect, get: ({people_config[i]} - {people_config["female_max_age"]})")

        # If there is any error, that's mean you need to use proper value in config file first.
        if(error):
            print()
            print("The task will not continue until you have fixed error in \"people\"")
            print("-------------------------")
            print(f"{Color.BLUE}Total Execution Time:{Color.RESET} {time.time() - start_time :,.2f} s")
            print(f"{Color.BLUE}Exit code:{Color.RESET} 0")
            print("-------------------------")
            exit(0)

        # After all of config is validate, we can return config of people
        else:
            return people_config
    elif(keys == "account"):
        account_config = config["account"]
        keys = account_config.keys()
        error = False

        for i in keys:
            if(type(account_config[i]) != int):
                error = True
                print(f"{error_label} Expect {i} to be {type(10)} but get {type(account_config[i])} instead.")

            else:
                if("regis" in i and "year" in i):
                    if(len(str(account_config[i])) != 4):
                        error = True
                        print(f"{error_label} Year {account_config[i]} is invalid, should be 4 digits.")

                    elif(int(account_config["registration_min_year"]) >= int(account_config["registration_max_year"])):
                        print(f"{error_label} registration year range is incorrect, get: ({account_config["registration_min_year"]} - {account_config["registration_max_year"]})")

        if(error):
            print()
            print("The task will not continue until you have fixed error in \"account\"")
            print("-------------------------")
            print(f"{Color.BLUE}Total Execution Time:{Color.RESET} {time.time() - start_time :,.2f} s")
            print(f"{Color.BLUE}Exit code:{Color.RESET} 0")
            print("-------------------------")
            exit(0)

        else:
            return account_config
        
    # Else
    return config

load_config("account")

# Handle JSON file
def load_json(file_path,encoding):

    # If file does not exist, just terminate program
    file_path = os.path.join(current_directory,file_path)
    if(not os.path.exists(file_path)):
        print(f"{error_label} name data does not exist on {file_path }")
        exit(0)
    else:
        with open(file_path,"r",encoding=encoding) as f:
            file = json.loads(f.read())
        
        return file

# Handle CSV file
def load_csv(file_path,encoding,skip_header=True):
    # If file does not exist, just terminate program
    file_path = os.path.join(current_directory,file_path)
    if(not os.path.exists(file_path)):
        print(f"{error_label} name data does not exist on {file_path }")
        exit(0)

    rows = []
    with open(file_path,'r',encoding=encoding) as f:
        csv_reader = csv.reader(f)
        if(skip_header): next(csv_reader)
        for row in csv_reader:
            rows.append(row)

    return rows

# Text cleaning
def clean_text(text):
    # Remove unusual characters
    cleaned_text = re.sub(r'[\x00-\x1F\x7F-\x9F\xa0\n\r\t\b]', '', text)

    if cleaned_text != text:
        print(f"{warning_label} detect non-printable ASCII on {text}, cleaning...")

    cleaned_text = cleaned_text.lower()
    cleaned_text_temp = cleaned_text.strip()
    
    cleaned_text = cleaned_text_temp.replace("/n","")
    cleaned_text = cleaned_text.replace("/b","")
    cleaned_text = cleaned_text.replace("/r","")
    cleaned_text = cleaned_text.replace("/t","")

    if cleaned_text != cleaned_text_temp:
        print(f"{warning_label} detect special ASCII on {text}, cleaning...")
        
    html_pattern = re.compile(r'<.*?>')
    cleaned_text = html_pattern.sub('', cleaned_text)
    if cleaned_text != cleaned_text_temp:
        print(f"{warning_label} detect HTML tag on {text}, cleaning...")

    return cleaned_text

# random Thai phone number
def random_phone(sample):
    phone_numbers = []
    for _ in range(sample):
        
        # Thai number should start with 09 or 08
        prefix = random.choice(['09', '08'])
        
        # Generate 8 random digits for the remaining part of the phone number
        number = ''.join(random.choices('0123456789', k=8))
        
        # Concatenate the prefix and number to form the complete phone number
        phone_number = prefix + number
        phone_numbers.append(phone_number)
    
    return phone_numbers

# Remove any duplicate element in list (when value is unhashable)
def remove_duplicates(input_list):
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

# Random valid thai ID
def random_id(sample):
    thai_ids = []
    for _ in range(sample):

        # Generate 2nd and 3rd digits between 10 and 96
        second_third_digits = random.randint(10, 96)
        
        # Generate 4th and 5th digits between 00 and 15
        fourth_fifth_digits = random.randint(0, 15)
        
        # Convert to string and fill with leading zeros if necessary
        second_third_digits_str = str(second_third_digits).zfill(2)
        fourth_fifth_digits_str = str(fourth_fifth_digits).zfill(2)
        
        # Focus on common prefix number
        first_digit = random.choice('12345')  # Randomly choose a digit from 1 to 5
        
        # Concatenate first digit, 2nd and 3rd digits, 4th and 5th digits, and 7 random digits
        id_number = first_digit + second_third_digits_str + fourth_fifth_digits_str + ''.join(random.choices('0123456789', k=7)) 
        
        # Generate proper last digit or checksum
        checksum = sum(int(digit) * (13 - i) for i, digit in enumerate(id_number)) % 11
        checksum = 1 if checksum == 0 else 11 - checksum
        id_number += str(checksum)
        thai_ids.append(id_number)
    return thai_ids

# Handle writing CSV
def write_csv(data,filename):
    filepath = os.path.join(current_directory,f"./data/{filename}")
    with open(filepath,mode="w",newline='',encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

# Random date
def random_dates(start_year, end_year, sample_size):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year + 1, 1, 1) - timedelta(days=1)  # Subtract 1 day to include the end year
    days_difference = (end_date - start_date).days
    
    random_dates_list = []
    for _ in range(sample_size):
        random_days = random.randint(0, days_difference)
        random_date = start_date + timedelta(days=random_days)
        random_dates_list.append(random_date.strftime("%Y/%m/%d"))  # Append the random date in "YYYY-MM-DD" format
    
    return random_dates_list

# Random bank account
def generate_bank(num_samples, num_digits):
    # Define the string containing all digits
    digits = '0123456789'
    
    random_strings = []
    for _ in range(num_samples):
        # Generate a random sample of num_digits digits from the string
        random_digits = random.choices(digits, k=num_digits)
        
        # Concatenate the random digits to form a string
        random_digits_string = ''.join(random_digits)
        random_strings.append(random_digits_string)
    
    return random_strings

def random_int_stats(min_val, max_val, std_dev, avg, num_samples):
    # Calculate the mean value to be used with normal distribution
    mean_val = (avg - min_val) / (max_val - min_val)
    
    # Calculate the standard deviation to be used with normal distribution
    std_val = std_dev / (max_val - min_val)
    
    # Generate random numbers from a normal distribution
    random_numbers = np.random.normal(loc=mean_val, scale=std_val, size=num_samples)
    
    # Clip the random numbers to fit within the specified range
    clipped_numbers = np.clip(random_numbers, 0, 1)
    
    # Scale the clipped numbers back to the desired range
    scaled_numbers = clipped_numbers * (max_val - min_val) + min_val
    
    # Round the numbers to the nearest multiple of 100
    rounded_numbers = np.round(scaled_numbers, -2)
    
    # Convert rounded numbers to integers
    random_integers = rounded_numbers.astype(int)
    
    return list(random_integers)
