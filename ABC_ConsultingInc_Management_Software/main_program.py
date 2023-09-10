# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 18:52:36 2022

@author: saidh
"""

# Importing Libraries.
import statistics
import string
import time
import os
import numpy as np

# Base Class
class Staff(object):
    
    # Getter/Accessor Functions.
    def get_eid(self):
        return self.__eid
    def get_empname(self):
        return self.__empname
    def get_basepay(self):
        return self.__basepay
    def get_emp_type(self):
        return self.__emp_type
    def get_newsales(self):
        return self.__newsales
    
    # Setter/Mutator Functions.
    def set_newsales(self, newsales):
        self.__newsales = newsales
    
    # Constructor Function.
    def __init__(self, eid, empname = "", emp_type = "", util = 0, evalscore = 0, basepay = 0, bonus = 0, newsales = 0):
        self.__eid = eid
        self.__empname = empname
        self.__emp_type = emp_type
        self.util = util
        self.evalscore = evalscore
        self.__basepay = float(basepay)
        self.bonus = float(bonus)
        self.__newsales = float(newsales)
    
    # Function to print Employee details.
    def print_emp_details(self):
        print("Employee Details:")
        print("ID:", str(self.get_eid()))
        print(self.get_emp_type() + ":", self.get_empname())
        print("Utilization:", str(self.util))
        if self.get_emp_type() == "Consultant":
            print("Evaluation score:", str(self.evalscore))
        if self.get_emp_type() == "Director":
            print("New Sales: $" + '{:,.2f}'.format(self.get_newsales()))
        print("Base pay: $" + '{:,.2f}'.format(self.get_basepay()))
        print("Bonus: $" + '{:,.2f}'.format(self.bonus))
        print(" ")
    
    # Function to Calculate Bonus. 
    def bonus_calc(self, utils, perc):
        if self.util > np.percentile(utils, 75):
            if self.evalscore >= 50:
                if ((perc/100) * self.get_basepay()) <= 50000.00:
                    return (perc/100) * self.get_basepay()
            else:
                if ((perc/100) * self.get_newsales()) <= 150000.00:
                    return (perc/100) * self.get_newsales()
                    


# Dictionary staff to hold data from file to perform operations.
staff = {}
# List of errors appearing during program run.
errors = []

# Reading Employee details from emp_beg_yr text file and storing in staff dictionary.
with open("emp_beg_yr.txt", "r") as file:
    file.readline()
    for line in file.readlines():
        temp = line.strip().split(",")
        if temp[3] == "C":
            staff[int(temp[0])] = Staff(int(temp[0]), str(temp[2]+" "+temp[1]), "Consultant", 0, 0, float(temp[4]))
        if temp[3] == "D":
            staff[int(temp[0])] = Staff(int(temp[0]), temp[2]+" "+temp[1], "Director", 0, 0, float(temp[4]))


# Reading Sales numbers of Directors from Sales Text file, updating records in staff dictionary.
with open("sales.txt", "r") as file:
    for line in file.readlines():
        temp = line.strip().split(",")
        for i in staff.keys():
            if int(temp[0]) == i:
                staff[i].set_newsales(float(temp[1])) 
            if int(temp[0]) not in staff.keys():
                errors.append(temp[0] + " in sales.txt\n")

# Reading hours worked from timesheet.txt to calculate Project Utilization Rate percentage and updating staff dictionary.
with open("timesheet.txt", "r") as file:
    for line in file.readlines():
        temp = line.strip().split(",")
        for i in staff.keys():
            if int(temp[0]) == i:
                staff[i].util = int((int(temp[1]) / 2250) * 100)
        if int(temp[0]) not in staff.keys():
            errors.append(temp[0] + " in timesheet.txt\n")

# Function to write errors stored in list errors to a error.txt file.
def write_errors():
    with open("error.txt", "w") as file:
        file.writelines(errors)

# List of negative and positive words used in calculating evaluation score of Consultants.
words = {
            "negative,s":["poor", "error", "unreliable", "late"], 
            "positive,a":["excellent", "good", "dependable"]
        }

# Function to calculate evaluation score of Consultants.
def eval_scorer(temp):
    score = 0
    count = 0
    pos_words = 0
    neg_words = 0
    for i in staff.keys():
            if int(temp[0]) == i:
                temp[1] = temp[1].translate(str.maketrans('', '', string.punctuation))
                another_temp = temp[1].split(" ")
                for j in another_temp:
                    for k in words.keys():
                        if j.lower() in words[k]:
                            if k.split(",")[1] == "a":
                                pos_words += 1
                                count += 1
                            elif k.split(",")[1] == "s":
                                neg_words += 1
                                count += 1    
                if count == 0:
                    score = 0
                    return score
                else:
                    score = int(((pos_words - neg_words) / count ) * 100)
                    return score


   
# Updating evaluation scores based on list of negative and positive words and the feedback given in evaluation.txt file.
def update_eval_score():
    with open("evaluation.txt", "r") as file:
        for line in file.readlines():
            temp = line.strip().split("#")
            if int(temp[0]) not in staff.keys():
                errors.append(temp[0] + " in evaluation.txt\n")
            else:
                staff[int(temp[0])].evalscore = eval_scorer(temp)

# Calling update_eval_score() function once to have evaluation scores calculated based on existing list of positive
# or negative words.
update_eval_score()
            
        
# Function to add or delete a category of words.  
def add_del_category():
    names = []
    comp = ""
    temp = ""
    flag = 0
    name_category = ""
    while True:
        for i in words.keys():
            temp += i.split(",")[0].title() + "," + " "
            names.append(i.split(",")[0].lower())
        temp = temp.strip().rstrip(",")
        print("Existing categories of words: ", temp)
        try:
            action_type = int(input("Enter 1 for adding or 0 for deleting a category of words: "))
        except:
            print("Wrong input given. Please try again.")
            print(" ")
            action_type = int(input("Enter 1 for adding or 0 for deleting a category of words: "))
        if (action_type == 1) or (action_type == 0):
            name_category =  input("Enter name of the category of words: ")
            name_category = name_category.lower()
            if name_category.isalpha() == True:
                if name_category in names:
                    if (action_type == 1):
                        print("Entered named category of words already exists. Please try again.")
                        print(" ")
                    elif action_type == 0:
                        flag = 1
                        break
                    else:
                        print("Wrong input given. Please try again.")
                        print(" ")
                else:
                    if action_type == 1:
                        try:
                            comp_type = int(input("Would you like to add or subtract "+ name_category +" words, encountered within the feedback for computation? (1 for add, 0 for subtract): "))
                        except:
                            print("Wrong input given. Please try again.")
                            print(" ")
                            comp_type = int(input("Would you like to add or subtract "+ name_category +" words, encountered within the feedback for computation? (1 for add, 0 for subtract): "))
                        print(" ")
                        if (comp_type == 1 or comp_type == 0):
                            if comp_type == 1:
                                comp = "a"
                                flag = 1
                                break
                            elif comp_type == 0:
                                comp = "s"
                                flag = 1
                                break
                        else:
                            print("Wrong computation type entered. Please try again.")
                            print(" ")
                    elif action_type == 0:
                        print("Entered named category of words does not exist. Please try again.")
                        print(" ")
                    else:
                        print("Wrong input given. Please try again.")
                        print(" ")
            else:
                print("Wrong input given. Please try again.")
                print(" ")
        else:
            print("Wrong input given. Please try again.")
            print(" ")
    
                 
    if action_type == 1 and flag == 1:
        try:
            num = int(input("Enter number of words to be input into this category: "))
        except:
            print("Wrong input given. Please try again.")
            print(" ")
            num = int(input("Enter number of words to be input into this category: "))
        another_temp = []
        while num != 0:
            temp_word = input("Enter new word: ")
            if temp_word not in (word for item in words.values() for word in item) and temp_word.isalpha():
                another_temp.append(temp_word.lower())
                num -= 1
            else:
                print("Wrong input/entered word already exists in another category. Please enter another word.")
                print(" ")
        if len(another_temp) > 0:
            words[name_category.lower()+","+comp]  = another_temp
            print("Words added to new category and evaluation scores updated.")
            print(" ")
            update_eval_score()
        elif len(another_temp) == 1:
            words[name_category.lower()+","+comp]  = another_temp
            print(" ")
            print("Word added to new category and evaluation scores updated.")
            print(" ")
            update_eval_score()
        else:
            print(" ")
            print("No words added due to wrong inputs. Please try again.")
            print(" ")
    elif action_type == 0 and flag == 1:
        temp_dict = words.copy()
        for j in temp_dict.keys():
            if j.split(",")[0] == name_category:
                del words[j]
        update_eval_score()
        print(" ")
        print("Category deleted and evaluation scores updated.")
        print(" ")
      

# Function to delete or add positive or negative words to existing list of positive or negative words.        
def add_del_eval_words():
    temp = ""
    names = []
    category_name = ""
    word_values = ""
    while True:
        for i in words.keys():
            temp += i.split(",")[0].title() + "," + " "
            names.append(i.split(",")[0].lower())
        temp = temp.strip().rstrip(",")
        print("Existing categories of words: ", temp)
        try:
            action_type = int(input("Enter 1 to add or 0 to delete words in a category: "))
        except:
            print("Wrong input entered. Please try again.")
            print(" ")
            action_type = int(input("Enter 1 to add or 0 to delete words in a category: "))
        if  action_type == 1 or action_type == 0:
            category_name = input("Enter category name: ")
            category_name = category_name.lower()
            if category_name.isalpha() == True:
                if action_type == 1 and (category_name in names):
                    for i in words.keys():
                        if category_name == i.split(",")[0]:
                            for j in words[i]:
                                word_values += j + "," + " "
                            print(" ")
                            print("Existing words:", word_values.strip().strip(","))
                            print(" ")
                            try:
                                num = int(input("Enter number of words to add: "))
                            except:
                                print("Wrong input entered. Please try again.")
                                print(" ")
                                num = int(input("Enter number of words to add: "))
                            while num != 0:
                                another_temp = input("Enter word: ")
                                if another_temp.lower() not in (word for item in words.values() for word in item) and another_temp.isalpha():
                                    words[i].append(another_temp.lower())
                                    print(" ")
                                    if num > 1:
                                        print("Words added.")
                                    else:
                                        print("Word added.")
                                    print(" ")
                                    num -= 1
                                        
                                else:
                                    print("Wrong input/word already exists. Please try again.")
                                    print(" ")
                            break
                    update_eval_score()
                    print("Evaluation Scores updated.")
                    print(" ")
                    break        
                elif action_type == 1 and (category_name not in names):
                    print("Entered category name, does not exist. Please try again.")
                    print(" ")
                elif action_type == 0 and (category_name in names):
                    for i in words.keys():
                        if category_name == i.split(",")[0]:
                            word_values = ""
                            for j in words[i]:
                                word_values += j + "," + " "
                            print("Existing words:", word_values.strip().strip(","))
                            try:
                                num = int(input("Enter number of words to delete: "))
                            except:
                                print("Wrong input given. Please try again.")
                                print(" ")
                                num = int(input("Enter number of words to delete: "))
                            while num != 0:
                                another_temp = input("Enter word: ")
                                if another_temp.lower() in words[i] and another_temp.isalpha():  
                                    words[i].remove(another_temp.lower())
                                    num -= 1
                                    print(" ")
                                    if num > 1:
                                        print("Words deleted.")
                                    else:
                                        print("Word deleted.")
                                    print(" ")
                                else:
                                    print("Word does not exist. Please try again.")
                                    print(" ")
                            break
                    update_eval_score()
                    print("Evaluation Scores updated.")
                    print(" ")
                    break
                else:
                    print("Entered category name, does not exist. Please try again.")
                    print(" ")
                    
            else:
                print("Wrong input given. Please try again.")
                print(" ")
        else:
            print("Wrong input entered. PLease try again.")
            print(" ")


# Calling write_errors() function to write to error.txt any errors/discrepancy that occured during reading 
# from any text file.
write_errors()
            

# Function for management to test bonuses by input of different percentages and finalize one percentage.
def mgmt_bonus_test():
    choice = "n"
    utils = []
    perc = 0
    for i in staff.values():
        utils.append(i.util)
    while choice.lower() == "n":
        try:
            perc = float(input("Enter a percentage (number only) to see bonuses: "))
        except ValueError:
            print("Wrong input given. Please try again.")
            print(" ")
            perc = float(input("Enter a percentage to see bonuses: "))
        total_consultants_bonus = 0
        total_directors_bonus = 0
        for i in staff.values():
            if i.get_emp_type() == "Consultant":
                if i.bonus_calc(utils, perc) != None:
                    total_consultants_bonus += i.bonus_calc(utils, perc)
            if i.get_emp_type() == "Director":
                if i.bonus_calc(utils, perc) != None:
                    total_directors_bonus += i.bonus_calc(utils, perc)
        
        print("Consultants Total Bonus payout: $" + '{:,.2f}'.format(total_consultants_bonus))
        print("Directors Total Bonus payout: $" + '{:,.2f}'.format(total_directors_bonus))
        print("Overall Total: $" + '{:,.2f}'.format(total_directors_bonus + total_consultants_bonus))
        while True:
            choice = input("Is this bonus percentage final? (y/n):")
            if choice.isalpha() and (choice.lower() == "y" or choice.lower() == "n"):
                break
            else:
                print("Wrong input given. Please try again.")
                print(" ")
        print(" ")
    if choice.lower() == "y":
        print("Bonus Set.")
        print(" ")
    for i in staff.values():
        if i.bonus_calc(utils, perc) != None:
            i.bonus = i.bonus_calc(utils, perc)
        else:
            i.bonus = 0


# Function to write to emp_end_yr.txt the final version of data after operations are performed.
def final_write():
   with open("emp_end_yr.txt", "w") as file:
        file.write("ID,LastName,FirstName,JobCode,BasePay,Utilization,Evaluation/Sales,Bonus\n")
        lines = []
        
        # Function to return the employee ID from a string.
        def sorter(line):
            return int(line[0:3])
        
        for i in staff.values():
            if i.get_emp_type() == "Consultant":
                line = str(i.get_eid()) + "," + ((i.get_empname()).split(" "))[1] + "," +  ((i.get_empname()).split(" "))[0] + "," +  i.get_emp_type()[0] + "," +  str(int(i.get_basepay())) + "," +  str(i.util) + "," +  str(i.evalscore) + "," +  str(int(i.bonus)) + "\n"
            elif i.get_emp_type() == "Director":
                line = str(i.get_eid()) + "," + ((i.get_empname()).split(" "))[1] + "," +  ((i.get_empname()).split(" "))[0] + "," +  i.get_emp_type()[0] + "," +  str(int(i.get_basepay())) + "," +  str(i.util) + "," +  str(int(i.get_newsales())) + "," +  str(int(i.bonus)) + "\n"
            lines.append(line)
        lines.sort(key = sorter)
        file.writelines(lines)
    


# Function to search for an employee details based on Employee ID.
def emp_search():
    choice = "y"
    while choice.lower() != "n":
        try:
            empid = int(input("Enter Employee ID to search: "))
        except:
            print("Wrong input given. Please try again.")
            print(" ")
            empid = int(input("Enter Employee ID to search: "))
        print(" ")
        for i in staff.values():
            if (empid == i.get_eid()):
                i.print_emp_details()
        if empid not in staff.keys():
            print("No Employee with entered ID present.")
            print(" ")
        while True:
            choice = input("Do you want to search another employee details? (y/n):")
            if choice.isalpha() and (choice.lower() == "y" or choice.lower() == "n"):
                break
            else:
                print("Wrong input given. Please try again.")
                print(" ")
        print(" ")


# Function to obtain descriptive analytics of project utilization rates, new sales, evaluation scores and bonuses of employees.
def desc_analytics():
    consultants_count = 0
    directors_count = 0
    for i in staff.values():
        if i.get_emp_type() == "Consultant":
            consultants_count += 1
        elif i.get_emp_type() == "Director":
            directors_count += 1
    print("Total Number of Employees (Staff):", (consultants_count + directors_count))
    print("Total Number of Directors:", directors_count)
    print("Total Number of Consultants:", consultants_count)
    print(" ")
    util_list = []
    sales_list = []
    evalscore_list = []
    bonus_list = []
    for i in staff.values():
        if (i.util != 0):
            util_list.append(i.util)
        if (i.get_newsales() != 0):
            sales_list.append(i.get_newsales())
        if (i.evalscore != 0):
            evalscore_list.append(i.evalscore)
        if (i.bonus != 0):
            bonus_list.append(i.bonus)
    
    num = 0
    while num != 5:
        print("Which metric analytics would you like to see?:")
        print("1. Utilization Rate.")
        print("2. Sales.")
        print("3. Evaluation Score.")
        print("4. Bonus.")
        print("5. Back to Main Menu.")
        print(" ")
        try:
            num = int(input("Enter option: "))    
        except:
            print("Wrong input entered. Please try again.")
            print(" ")
            num = int(input("Enter option: "))    
        print(" ")
        if num == 1:
            # Utilization Rate Desc Analytics
            print("Minimum utilization rate among employees:", min(util_list))
            print("Maximum utilization rate among employees:", max(util_list))
            print("Median utilization rate among employees:", statistics.median(util_list))
            print("Mean utilization rate among employees:", round(statistics.mean(util_list), 2))
            print("Mode utilization rate among employees:", round(statistics.mode(util_list), 2))
            print("Standard Deviation of utilization rate among employees:", round(statistics.stdev(util_list), 2))
            print(" ")
            time.sleep(1)
       
        elif num == 2:
            # Sales Desc Analytics
            print("Minimum sale among Directors: $" + '{:,.2f}'.format(min(sales_list)))
            print("Maximum sale among Directors: $" + '{:,.2f}'.format(max(sales_list)))
            print("Median sale among Directors: $" + '{:,.2f}'.format(statistics.median(sales_list)))
            print("Mean sale among Directors: $" + '{:,.2f}'.format(statistics.mean(sales_list)))
            print("Mode sale among Directors: $" + '{:,.2f}'.format(statistics.mode(sales_list)))
            print("Standard Deviation of sales among Directors: $" + '{:,.2f}'.format(statistics.stdev(sales_list)))
            print(" ")
            time.sleep(1)
    
        elif num == 3:
            # Evaluation Score Desc Analytics
            print("Minimum Evaluation Score among Consultants:", min(evalscore_list))
            print("Maximum Evaluation Score among Consultants:", max(evalscore_list))
            print("Median Evaluation Score among Consultants:", statistics.median(evalscore_list))
            print("Mean Evaluation Score among Consultants:", round(statistics.mean(evalscore_list), 2))
            print("Mode Evaluation Score among Consultants:", statistics.mode(evalscore_list))
            print("Standard Deviation of Evaluation Scores among Consultants:", round(statistics.stdev(evalscore_list), 2))
            print(" ")
            time.sleep(1)
            
        elif num == 4:
            if len(bonus_list) == 0:
                print("Bonuses not finalized by Management yet. Please contact Management to finalize bonuses in "  \
                      "order to display descriptive analytics on the same.")
                print(" ")
                time.sleep(1)
            else:
                # Bonuses Desc Analytics
                print("Minimum Bonus among employees: $" + '{:,.2f}'.format(min(bonus_list)))
                print("Maximum Bonus among employees: $" + '{:,.2f}'.format(max(bonus_list)))
                print("Median Bonus among employees: $" + '{:,.2f}'.format(statistics.median(bonus_list)))
                print("Mean Bonus among employees: $" + '{:,.2f}'.format(statistics.mean(bonus_list)))
                print("Mode Bonus among employees: $" + '{:,.2f}'.format(statistics.mode(bonus_list)))
                print("Standard Deviation of Bonuses among employees: $" + '{:,.2f}'.format(statistics.stdev(bonus_list)))
                print(" ")
                time.sleep(1)

        elif num == 5:
            break
        
# Function to provide employee(s) who deserve a letter of Recognition based on Maximum utilization rate and sales.    
def sendLOR():
        util_list = []
        sales_list = []
        temp_dict = {}
        for i in staff.values():
            if (i.util != 0) and (i.get_newsales() != 0):
                util_list.append(i.util)
                sales_list.append(i.get_newsales())
                temp_dict[i.get_eid()] = [i.util, i.get_newsales()] 
        for k, v in temp_dict.items():
            if max(util_list) == v[0]:
                if max(sales_list) == v[1]:
                    for i in staff.values():
                        if (k == i.get_eid()):
                            print(i.get_emp_type(), i.get_empname() + ", ID", str(k) + ", to be sent Letter of Recognition for Maximum utilization rate and Sales.")
                            print(" ")
                            i.print_emp_details()
                else:
                    for i in staff.values():
                        if (k == i.get_eid()):
                            print(i.get_emp_type(), i.get_empname() + ", ID", str(k) + ", to be sent Letter of Recognition for Maximum utilization rate.")
                            print(" ")
                            i.print_emp_details()
            if max(sales_list) == v[1]:
                for i in staff.values():
                    if (k == i.get_eid()):
                        print(i.get_emp_type(), i.get_empname() + ", ID", str(k) + ", to be sent Letter of Recognition for Maximum Sales.")
                        print(" ")
                        i.print_emp_details()


# Function to get a list of consultants to be put on probation.
def probation():
    poor_performers = {}
    util_list = []
    for i in staff.values():
        if i.get_emp_type() == "Consultant":
            util_list.append(i.util)
    for i in staff.values():
        if (i.util < (statistics.mean(util_list) - statistics.stdev(util_list))) and (i.evalscore < 0) and (i.get_emp_type() == "Consultant"):
            poor_performers[i.get_eid()] = i.get_empname()
    if len(poor_performers) == 0:
        print("No Consultants need to be put on probation.")
        print(" ")
    else:
        for k,v in poor_performers.items():
            print("Consultant ID:", str(k), " Name:", v)
        print(" ")


# Function to print employees information based on user input.
def print_employees_info():
    try:
        num = int(input("Enter 1 to see all employees details or enter a specific number of employees: "))
    except:
        print("Wrong input given. Please try again.")
        print(" ")
        num = int(input("Enter 1 to see all employees details or enter a specific number of employees: "))
    print(" ")
    for k in staff.keys():
        if num == 1:
            staff[k].print_emp_details()
        else:
            num -= 1
            staff[k].print_emp_details()
            if num == 1:
                num -= 1
                continue                
            if num == -1:
                break

# Menu based user interface to perform operations until user wants to exit.
n = 0
print(" ")
print("Welcome to ABC Consulting Inc.".center(int(os.get_terminal_size().columns)))
print("------------------------------------".center(int(os.get_terminal_size().columns)))
print(" ")

while n != 9:
    print("Menu:")
    print("--------")
    print("1. Set Bonus.")  #mgmt_bonus_test()
    print("2. Employee Search.")  #emp_search()
    print("3. Send Letter of Recognition.")   # sendLOR()
    print("4. Descriptive Analytics on factors.") # desc_analytics()
    print("5. Poor performing Consultants.") #probation()
    print("6. Add or delete words for evaluation score.") #add_del_eval_words()
    print("7. Add or delete a category of words.") # add_del_category()
    print("8. Print Employees Information.") #print_employees_info()
    print("9. Exit") # final_write()
    print(" ")
    try:
        n = int(input("Choose an option: "))
    except:
        print("Wrong input entered. Please try again.")
        print(" ")
        n = int(input("Choose an option: "))
    print(" ")
    print(" ")
    if n == 1:
        mgmt_bonus_test()
        time.sleep(1)
    elif n == 2:
        emp_search()
        time.sleep(1)
    elif n == 3:
        sendLOR()
        time.sleep(1)
    elif n == 4:
        desc_analytics()
        time.sleep(1)
    elif n == 5:
        probation()
        time.sleep(1)
    elif n == 6:
        add_del_eval_words()
        time.sleep(1)
    elif n == 7:
        add_del_category()
        time.sleep(1)
    elif n == 8:
        print_employees_info()
        time.sleep(1)
    elif n == 9:
        final_write()
        print("Have a great day, Goodbye!")
    else:
        print("Wrong option entered. Please try again.")
        print(" ")
        

# End of Program Code.

