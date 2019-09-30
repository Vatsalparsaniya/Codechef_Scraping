import os
import re
import urllib.request
from bs4 import BeautifulSoup
import os
import time
import requests
from urllib.request import Request, urlopen
import argparse

print("\nRunning...\n")


#Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--Contest_name", required=True, help="Contest name , Ex : JULY19B ")
ap.add_argument("-u", "--User_name", required=True, help="User name , Ex : vatsal1999 ")
args = vars(ap.parse_args())


#initialize variable
Contest_name = args["Contest_name"]
User_name = args["User_name"]
Contest_URL = "https://www.codechef.com/{}/".format(Contest_name)
Contest_page = requests.get(Contest_URL)


#Beautify HTML code
Contest_page_content = BeautifulSoup(Contest_page.content,'html.parser')
data = [['Name','Code','Successful Submissions','Accuracy']]
Problem_code_URL = []


# Fatching Main content of competition
for row in Contest_page_content.findAll('tr',attrs={'class':'problemrow'}):
    #print(row)
    row_data =[]
    problem_name = row.findAll('b')[0].text
    problem_code = row.findAll('td')[1].text
    problem_Successful_Submission = row.findAll('div')[2].text
    problem_Accuracy = row.findAll('a')[1].text
    row_data.append(problem_name)
    row_data.append(problem_code)
    row_data.append(problem_Successful_Submission)
    row_data.append(problem_Accuracy)
    Problem_code_URL.append(problem_code)
    data.append(row_data)


# Printing Table of All content competition 
dash = '-'*90
for i in range(len(data)):
    if i == 0:
        print(dash)
        print('{:<40s}{:<15s}{:<25s}{:<10s}'.format(data[i][0],data[i][1],data[i][2],data[i][3]))
        print(dash)
    else:
        print('{:<40s}{:<15s}{:<25s}{:<10s}'.format(data[i][0],data[i][1],data[i][2],data[i][3]))


# tacking Choice from user
time.sleep(5)
print("\n\n\nScraping Problem Statement...\n\n")
print("Select: ")
print("\t\t1) Problem_Statement + Solution")
print("\t\t2) Problem_Statement")
print("\t\t3) Solution")
choice = int(input("Select (1/2/3) :"))


# Function for Get Problem statment by Contest name , user name, and url
def Problem_S(Contest_name,User_name,Problem_code_URL):
    print("\n\nProblem Statement Scraping...")
    # for every Problem statment URL
    for url_code in Problem_code_URL:
        time.sleep(2)
        print(url_code + " Working...")
        problem_page_url = Contest_URL + 'problems/' + url_code+'/'
        page = requests.get(problem_page_url)
        page_contest = BeautifulSoup(page.content,'html.parser')
        statement = page_contest.findAll('div',attrs={'class':'content'})
        a = statement[1].text
        b = re.sub('[$]', '', a)
        # Can't fatch All Special character so replacing them by replace function
        b = b.replace("\le","<").replace("\ldots","...").replace("\in","∈").replace("\oplus","⊕").replace("\{","{")
        b =b.replace("\}","}").replace("\sum_{i=1}^{N-1}","i=1∑N−1").replace("**","").replace("`","").replace("\neq","≠")
        b =b.replace("*","").replace("\rightarrow","->").replace("\ge",">").replace(" \cdot ","*").replace("\neq","≠")
        file_name = filename = "Problem_Statement/{}/".format(url_code)+"{}.txt".format(url_code)
        # Macking Folder for Problem statment
        if not os.path.exists(os.path.dirname(file_name)):
                try:
                    os.makedirs(os.path.dirname(file_name))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
        f= open(file_name,"w+",encoding='utf-8')
        f.write(str(b))
        f.close()
        print("{} Problem_Statement Done...\n".format(url_code))


# Function for Get Solution by Contest name , user name, and url
def Solution_s(Contest_name,User_name,Problem_code_URL):
    print("\n\nSolutions Scraping...")
    # for every Problem page url
    for url_code in Problem_code_URL:
        time.sleep(2)
        print("\n"+url_code +"  working...")
        # make url by solution status
        Sloution_Status_url = Contest_URL + "status/" +url_code+","+User_name
        page_content = requests.get(Sloution_Status_url)
        page = BeautifulSoup(page_content.content,'html.parser')
        ID = page.findAll('td',attrs={'width':'60'})
        j=1
        # for every solution ID getting information
        for sub_id in ID:
            solution_view_url = "https://www.codechef.com/viewplaintext/" + sub_id.text
            req = Request(solution_view_url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            webpage = BeautifulSoup(webpage,'html.parser')
            z = webpage.find('pre').text

            # Macking New Folder for every New Problem statment
            filename = "{}_Solutions/{}/".format(User_name,url_code)+"{}_{}.txt".format(url_code,j)
            j=j+1
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            f= open(filename,"w+",encoding='utf-8')
            f.write(z)
            f.close()
            print("{}) {} Solution Done...".format(j-1,url_code))


if(choice == 1):
    Problem_S(Contest_name,User_name,Problem_code_URL)
    Solution_s(Contest_name,User_name,Problem_code_URL)
elif(choice == 2):
    Problem_S(Contest_name,User_name,Problem_code_URL)
elif(choice == 3):
    Solution_s(Contest_name,User_name,Problem_code_URL)
else:
    print("\nchoice Proper Option\n\n")
