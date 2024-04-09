import time
import random
from utils import Color, warning_label,error_label,success_label
from utils import load_config, load_json, remove_duplicates, random_phone,random_id,write_csv

print("-------------------------")
start_time = time.time()

def generate_people():

    # Load necessary file
    people_config = load_config("people")
    name_data = load_json(file_path="./data/name_data.json",encoding="utf-8-sig")
    occupation = load_json(file_path="./data/occupation_data.json",encoding="utf-8-sig")

    # Retrieve occupation name and weight, so that we can random it properly
    occupation_list = []
    occpuation_weight = []
    for i in occupation.keys():
        occupation_list.append(i)
        occpuation_weight.append(occupation[i]["weight"])

    # This list will be useed to store all people data and returned
    people_data = [["National-ID","Prefix-TH","Prefix-EN","Nickname-TH","Nickname-EN","Firstname-TH","Firstname-EN","Lastname-TH","Lastname-EN","Age","Occupation","Phone"]]

    # We need to make sure that the total number of people we can provide is sufficient to the config parameter
    total_male = len(name_data["firstnameMale"]) * len(name_data["lastname"])
    total_female = len(name_data["firstnameFemale"]) * len(name_data["lastname"])

    # Round down, if requested sample is too much
    if(people_config["male_population"] > total_male):
        print(f"{warning_label} specified male amount ({people_config["male_population"]:,}) exceeds total possible people from name list ({total_male:,})")
        print(f"Total male is changed to {total_male:,} people")
        people_config["male_population"] = total_male
        print("-------------------------")

    if(people_config["female_population"] > total_female):
        print(f"{warning_label} specified female amount ({people_config["female_population"]:,}) exceeds total possible people from name list ({total_female:,})")
        print(f"Total female is changed to {total_female:,} people")
        people_config["female_population"] = total_female
        print("-------------------------")

    # This variable will use to track if the number of sample is cut off due to the duplication
    truncate_female = people_config["female_population"]
    truncate_male = people_config["male_population"]

    # Random male data
    random_male_firstname = random.choices(name_data["firstnameMale"],k=people_config["male_population"])
    random_male_lastname = random.choices(name_data["lastname"],k=people_config["male_population"])
    random_male_nickname = random.choices(name_data["nicknameMale"],k=people_config["male_population"])
    random_male_age = [random.randint(people_config["male_min_age"], people_config["male_max_age"]) for _ in range(people_config["male_population"])]
    random_male_occupation = random.choices(occupation_list, weights=occpuation_weight, k=people_config["male_population"])
    random_male_phone = remove_duplicates(random_phone(people_config["male_population"]))
    random_male_id = remove_duplicates(random_id(people_config["male_population"]))

    # Random female data
    random_female_phone = remove_duplicates(random_phone(people_config["female_population"]))
    random_female_id = remove_duplicates(random_id(people_config["female_population"]))
    random_female_firstname = random.choices(name_data["firstnameFemale"],k=people_config["female_population"])
    random_female_lastname = random.choices(name_data["lastname"],k=people_config["female_population"])
    random_female_nickname = random.choices(name_data["nicknameFemale"],k=people_config["female_population"])
    random_female_age = [random.randint(people_config["female_min_age"], people_config["female_max_age"]) for _ in range(people_config["female_population"])]
    random_female_occupation = random.choices(occupation_list, weights=occpuation_weight, k=people_config["female_population"])

    # Make sure that phone number will not be duplicated
    for number in random_male_phone:
        if number in random_female_phone:
            del random_male_phone[random_male_phone.index(number)]

    for number in random_female_phone:
        if number in random_male_phone:
            del random_female_phone[random_female_phone.index(number)]

    # Make sure that ID will not be duplicated
    for id in random_male_id:
        if id in random_female_id:
            del random_male_id[random_male_id.index(id)]

    for id in random_female_id:
        if id in random_male_id:
            del random_female_id[random_female_id.index(id)]

    # If any duplication is detected, we should cut off
    if(len(random_male_phone) < people_config["male_population"]):
        truncate_male  = len(random_male_phone)
        
    if(len(random_female_phone) < people_config["female_population"]):
        truncate_female  = len(random_female_phone)

    if(len(random_male_id) < truncate_male):
        truncate_male  = len(random_male_id)
        
    if(len(random_female_id) < truncate_female):
        truncate_female  = len(random_female_id)

    # Use to store construct fullname
    fullname_male = []
    fullname_female = []
    
    # Append male information to people data
    for i in range(people_config["male_population"]):
        fullname = [
            "นาย",
            "Mr.",
            random_male_nickname[i]["th"],
            random_male_nickname[i]["en"],
            random_male_firstname[i]["th"],
            random_male_firstname[i]["en"],
            random_male_lastname[i]["th"],
            random_male_lastname[i]["en"]    
        ]

        fullname_male.append(fullname)

    if(len(fullname_male) < truncate_male):
        truncate_male = len(fullname_male)
        fullname_male = fullname_male[:truncate_male]
        random_male_age = random_male_age[:truncate_male]
        random_male_occupation = random_male_occupation[:truncate_male]
        random_male_phone = random_male_occupation[:truncate_male]
        random_male_id = random_male_id[:truncate_male]
        print(f"{warning_label} Duplication is found during random in male, male population is truncated to {truncate_male}")

    # Append female information to people data
    for i in range(people_config["female_population"]):
        # Don't forget that female can either be Mrs. or Ms.
        prefix = random.choice([["นาง","Mrs."],["นางสาว","Ms."]])
        fullname = [
            prefix[0],
            prefix[1],
            random_female_nickname[i]["th"],
            random_female_nickname[i]["en"],
            random_female_firstname[i]["th"],
            random_female_firstname[i]["en"],
            random_female_lastname[i]["th"],
            random_female_lastname[i]["en"]    
        ]

        fullname_female.append(fullname)

    # Make sure to remove duplicate
    fullname_male = remove_duplicates(fullname_male)
    fullname_female = remove_duplicates(fullname_female)

    # If duplication is detected, they will be cut off properly
    if(len(fullname_female) < truncate_female):
        truncate_female = len(fullname_female)
        fullname_female = fullname_female[:truncate_female]
        random_female_age = random_female_age[:truncate_female]
        random_female_occupation = random_female_occupation[:truncate_female]
        random_female_phone = random_female_occupation[:truncate_female]
        random_female_id = random_female_id[:truncate_female]
        print(f"{warning_label} Duplication is found during random in female, female population is truncated to {truncate_female}")

    # Append all data
    for i in range(truncate_female):
        full_list = [random_female_id[i]] + fullname_female[i] + [random_female_age[i]] + [random_female_occupation[i]] + [random_female_phone[i]]
        people_data.append(full_list)

    for i in range(truncate_male):
        full_list = [random_male_id[i]] + fullname_male[i] + [random_male_age[i]] + [random_male_occupation[i]] + [random_male_phone[i]]
        people_data.append(full_list)

    # Shuffle to make it feel more randomness
    random.shuffle(people_data)

    # save to csv data
    write_csv(data=people_data,filename="people.csv")
    print()
    print(f"{success_label} Generate {truncate_male+truncate_female} people successfully ( duplicated rate = {100 - (truncate_female+truncate_male)*100/(people_config["male_population"]+people_config["female_population"]):.2f}% )")
    print(f"{success_label} people list is saved to data/people.csv")
    print("-------------------------")
    # Don't forget to mention performance
    print(f"{Color.BLUE}Total Execution Time:{Color.RESET} {time.time() - start_time :,.2f} s")
    print(f"{Color.BLUE}Exit code:{Color.RESET} 0")
    print("-------------------------")
    exit(0)

if __name__ == "__main__":
    generate_people()