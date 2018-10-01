import pandas as pd
import sys
import re

students = pd.read_csv('Students.csv')
currweek = sys.argv[1]
print("Week", currweek)

#see if there are any missing days
ignore_list = []
# print("Are there any missing days this week?\n\tFormat as 'secX-DAY'\nType 'end' to finish")
# while(True):
#     usr_input = input()
#     if usr_input == 'end':
#         break
#     ignore_list.append(usr_input.lower())
# print(ignore_list)


def getFileWithIgnoreListChecking(filename):
    try:
        return pd.read_csv(currweek + '/' + currweek + '-' + filename + '.csv')
    except:
        ignore_list.append(filename)
        return None

currweek_sec1_tue = getFileWithIgnoreListChecking('sec1-tue')
currweek_sec1_thu = getFileWithIgnoreListChecking('sec1-thu')
currweek_sec2_tue = getFileWithIgnoreListChecking('sec2-tue')
currweek_sec2_thu = getFileWithIgnoreListChecking('sec2-thu')
currweek_sec3_mon = getFileWithIgnoreListChecking('sec3-mon')
currweek_sec3_wed = getFileWithIgnoreListChecking('sec3-wed')
currweek_sec3_fri = getFileWithIgnoreListChecking('sec3-fri')
currweek_sec4_mon = getFileWithIgnoreListChecking('sec4-mon')
currweek_sec4_wed = getFileWithIgnoreListChecking('sec4-wed')
currweek_sec4_fri = getFileWithIgnoreListChecking('sec4-fri')

print("Couldn't find files for the following sections. Confirm that there were no TopHat questions for these sections this week:")

if isinstance(currweek_sec1_tue, pd.DataFrame):
    currweek_sec1_tue['Username'] = currweek_sec1_tue['Username'].str.upper()
    currweek_sec1_tue['Email Address'] = currweek_sec1_tue['Email Address'].str.upper()
    currweek_sec1_tue.set_index("Email Address", inplace = True)
else:
    print("sec1_tue")
    
if isinstance(currweek_sec1_thu, pd.DataFrame):
    currweek_sec1_thu['Username'] = currweek_sec1_thu['Username'].str.upper()
    currweek_sec1_thu['Email Address'] = currweek_sec1_thu['Email Address'].str.upper()
    currweek_sec1_thu.set_index("Email Address", inplace = True)
else:
    print("sec1_thu")
    
if isinstance(currweek_sec2_tue, pd.DataFrame):
    currweek_sec2_tue['Username'] = currweek_sec2_tue['Username'].str.upper()
    currweek_sec2_tue['Email Address'] = currweek_sec2_tue['Email Address'].str.upper()
    currweek_sec2_tue.set_index("Email Address", inplace = True)
else:
    print("sec2_tue")

if isinstance(currweek_sec2_thu, pd.DataFrame):
    currweek_sec2_thu['Username'] = currweek_sec2_thu['Username'].str.upper()
    currweek_sec2_thu['Email Address'] = currweek_sec2_thu['Email Address'].str.upper()
    currweek_sec2_thu.set_index("Email Address", inplace = True)
else:
    print("sec2_thu")

if isinstance(currweek_sec3_mon, pd.DataFrame):
    currweek_sec3_mon['Username'] = currweek_sec3_mon['Username'].str.upper()
    currweek_sec3_mon['Email Address'] = currweek_sec3_mon['Email Address'].str.upper()
    currweek_sec3_mon.set_index("Email Address", inplace = True)
else:
    print("sec3_mon")
    
if isinstance(currweek_sec3_wed, pd.DataFrame):
    currweek_sec3_wed['Username'] = currweek_sec3_wed['Username'].str.upper()
    currweek_sec3_wed['Email Address'] = currweek_sec3_wed['Email Address'].str.upper()
    currweek_sec3_wed.set_index("Email Address", inplace = True)
else:
    print("sec3_wed")

if isinstance(currweek_sec3_fri, pd.DataFrame):
    currweek_sec3_fri['Username'] = currweek_sec3_fri['Username'].str.upper()
    currweek_sec3_fri['Email Address'] = currweek_sec3_fri['Email Address'].str.upper()
    currweek_sec3_fri.set_index("Email Address", inplace = True)
else:
    print("sec3_fri")
    
if isinstance(currweek_sec4_mon, pd.DataFrame):
    currweek_sec4_mon['Username'] = currweek_sec4_mon['Username'].str.upper()
    currweek_sec4_mon['Email Address'] = currweek_sec4_mon['Email Address'].str.upper()
    currweek_sec4_mon.set_index("Email Address", inplace = True)
else:
    print("sec4_mon")

if isinstance(currweek_sec4_wed, pd.DataFrame):
    currweek_sec4_wed['Username'] = currweek_sec4_wed['Username'].str.upper()
    currweek_sec4_wed['Email Address'] = currweek_sec4_wed['Email Address'].str.upper()
    currweek_sec4_wed.set_index("Email Address", inplace = True)
else:
    print("sec4_wed")

if isinstance(currweek_sec4_fri, pd.DataFrame):
    currweek_sec4_fri['Username'] = currweek_sec4_fri['Username'].str.upper()
    currweek_sec4_fri['Email Address'] = currweek_sec4_fri['Email Address'].str.upper()
    currweek_sec4_fri.set_index("Email Address", inplace = True)
else:
    print("sec4_fri")


def find_participation_score(df, email, studentList):
    try:
        studentList.append(df.loc[email]['Average %'])
        return True
    except KeyError:
        studentList.append(0)
        return False

scores_currweek_sec1_tue = []
scores_currweek_sec1_thu = []
scores_currweek_sec2_tue = []
scores_currweek_sec2_thu = []
scores_currweek_sec3_mon = []
scores_currweek_sec3_wed = []
scores_currweek_sec3_fri = []
scores_currweek_sec4_mon = []
scores_currweek_sec4_wed = []
scores_currweek_sec4_fri = []
max_mon = []
max_tue = []
max_wed = []
max_thu = []
max_fri = []
currweek_average = []

for i, email in enumerate(students['SIS Login ID']):
    email = str(email)
    
    foundScore = False
    if isinstance(currweek_sec1_tue, pd.DataFrame):
        result = find_participation_score(currweek_sec1_tue, email, scores_currweek_sec1_tue)
        if result:
            foundScore = True
    if isinstance(currweek_sec1_thu, pd.DataFrame):
        result = find_participation_score(currweek_sec1_thu, email, scores_currweek_sec1_thu)
        if result:
            foundScore = True
    if isinstance(currweek_sec2_tue, pd.DataFrame):
        result = find_participation_score(currweek_sec2_tue, email, scores_currweek_sec2_tue)
        if result:
            foundScore = True
    if isinstance(currweek_sec2_thu, pd.DataFrame):
        result = find_participation_score(currweek_sec2_thu, email, scores_currweek_sec2_thu)
        if result:
            foundScore = True
    if isinstance(currweek_sec3_mon, pd.DataFrame):
        result = find_participation_score(currweek_sec3_mon, email, scores_currweek_sec3_mon)
        if result:
            foundScore = True
    if isinstance(currweek_sec3_wed, pd.DataFrame):
        result = find_participation_score(currweek_sec3_wed, email, scores_currweek_sec3_wed)
        if result:
            foundScore = True
    if isinstance(currweek_sec3_fri, pd.DataFrame):
        result = find_participation_score(currweek_sec3_fri, email, scores_currweek_sec3_fri)
        if result:
            foundScore = True
    if isinstance(currweek_sec4_mon, pd.DataFrame):
        result = find_participation_score(currweek_sec4_mon, email, scores_currweek_sec4_mon)
        if result:
            foundScore = True
    if isinstance(currweek_sec4_wed, pd.DataFrame):
        result = find_participation_score(currweek_sec4_wed, email, scores_currweek_sec4_wed)
        if result:
            foundScore = True
    if isinstance(currweek_sec4_fri, pd.DataFrame):
        result = find_participation_score(currweek_sec4_fri, email, scores_currweek_sec4_fri)
        if result:
            foundScore = True
    if not foundScore:
        print("Couldn't find scores for student", email)
    
    
def calc_max(dayList, list1, list2):
    for score1, score2 in list(zip(list1, list2)):
        max_score = max(score1, score2)
        dayList.append(max_score)

calc_max(max_mon, scores_currweek_sec3_mon, scores_currweek_sec4_mon)
calc_max(max_tue, scores_currweek_sec1_tue, scores_currweek_sec2_tue)
calc_max(max_wed, scores_currweek_sec3_wed, scores_currweek_sec4_wed)
calc_max(max_thu, scores_currweek_sec1_thu, scores_currweek_sec2_thu)
calc_max(max_fri, scores_currweek_sec3_fri, scores_currweek_sec4_fri)

monflag = len(max_mon)!=0
tueflag = len(max_tue)!=0
wedflag = len(max_wed)!=0
thuflag = len(max_thu)!=0
friflag = len(max_fri)!=0
for day1 in [max_mon, max_tue, max_wed, max_thu, max_fri]:
    for day2 in [max_mon, max_tue, max_wed, max_thu, max_fri]:
        if not day1 and day2:
            for x in range(len(day2)):
                day1.append(0)


def calc_average(avg_list, max_mon, max_tue, max_wed, max_thu, max_fri, monflag, tueflag, wedflag, thuflag, friflag):
    for mon, tue, wed, thu, fri in list(zip(max_mon, max_tue, max_wed, max_thu, max_fri)):

        divisor = 3
        if not monflag:
            divisor -= 1
        if not wedflag:
            divisor -= 1
        if not friflag:
            divisor -= 1

        if divisor > 0:
            avg_1 = (mon + wed + fri)/divisor
        else:
            avg_1 = 0

        divisor = 2
        if not tueflag:
            divisor -= 1
        if not thuflag:
            divisor -= 1

        if divisor > 0:
            avg_2 = (tue + thu)/divisor
        else:
            avg_2 = 0

        divisor = 3
        if not monflag:
            divisor -= 1
        if not wedflag:
            divisor -= 1
        if not thuflag:
            divisor -= 1

        if divisor > 0:
            avg_3 = (mon + wed + thu)/divisor
        else:
            avg_3 = 0

        divisor = 3
        if not tueflag:
            divisor -= 1
        if not wedflag:
            divisor -= 1
        if not friflag:
            divisor -= 1
        if divisor > 0:
            avg_4 = (tue + wed + fri)/divisor
        else:
            avg_4 = 0

        best_avg = max(avg_1, avg_2, avg_3, avg_4)
        avg_list.append(best_avg)

calc_average(currweek_average, max_mon, max_tue, max_wed, max_thu, max_fri, monflag, tueflag, wedflag, thuflag, friflag)

series_currweek_sec1_tue = pd.Series(scores_currweek_sec1_tue)
series_currweek_sec1_thu = pd.Series(scores_currweek_sec1_thu)
series_currweek_sec2_tue = pd.Series(scores_currweek_sec2_tue)
series_currweek_sec2_thu = pd.Series(scores_currweek_sec2_thu)
series_currweek_sec3_mon = pd.Series(scores_currweek_sec3_mon)
series_currweek_sec3_wed = pd.Series(scores_currweek_sec3_wed)
series_currweek_sec3_fri = pd.Series(scores_currweek_sec3_fri)
series_currweek_sec4_mon = pd.Series(scores_currweek_sec4_mon)
series_currweek_sec4_wed = pd.Series(scores_currweek_sec4_wed)
series_currweek_sec4_fri = pd.Series(scores_currweek_sec4_fri)
series_currweek_average = pd.Series(currweek_average)

if 'sec1-tue' not in ignore_list:
    students[currweek + '-sec1-tue'] = series_currweek_sec1_tue.values
if 'sec1-thu' not in ignore_list:
    students[currweek + '-sec1-thu'] = series_currweek_sec1_thu.values
if 'sec2-tue' not in ignore_list:
    students[currweek + '-sec2-tue'] = series_currweek_sec2_tue.values
if 'sec2-thu' not in ignore_list:
    students[currweek + '-sec2-thu'] = series_currweek_sec2_thu.values
if 'sec3-mon' not in ignore_list:
    students[currweek + '-sec3-mon'] = series_currweek_sec3_mon.values
if 'sec3-wed' not in ignore_list:
    students[currweek + '-sec3-wed'] = series_currweek_sec3_wed.values
if 'sec3-fri' not in ignore_list:
    students[currweek + '-sec3-fri'] = series_currweek_sec3_fri.values
if 'sec4-mon' not in ignore_list:
    students[currweek + '-sec4-mon'] = series_currweek_sec4_mon.values
if 'sec4-wed' not in ignore_list:
    students[currweek + '-sec4-wed'] = series_currweek_sec4_wed.values
if 'sec4-fri' not in ignore_list:
    students[currweek + '-sec4-fri'] = series_currweek_sec4_fri.values
students[currweek + '-average'] = series_currweek_average

students.to_csv('./' + currweek + '-average.csv',index = False)

students_final = pd.read_csv('Students.csv')


#TODO
#exit(0)


avg_list = []
adjusted_avg_list = []
weeks_list = ['week1', 'week2', 'week3', 'week4']

week1_average = pd.read_csv('week1-average.csv')
week2_average = pd.read_csv('week2-average.csv')
week3_average = pd.read_csv('week3-average.csv')
#week4_average = pd.read_csv('../week4-average.csv')

week1_average.set_index("SIS User ID", inplace = True)
week2_average.set_index("SIS User ID", inplace = True)
week3_average.set_index("SIS User ID", inplace = True)
#week4_average.set_index("SIS User ID", inplace = True)

def average_calculation(week1, week2, week3, email, avg_list, adjusted_avg_list):
    try:
        w1 = week1.loc[email]['week1-average']
        w2 = week2.loc[email]['week2-average']
        w3 = week3.loc[email]['week3-average']
        #w4 = week4.loc[email]['week4-average']
        avg = (w1 + w2 + w3)/3
        avg_list.append(avg)
        if avg > 80:
            adjusted_avg_list.append(100)
        else:
            adjusted_avg_list.append(avg)
    except KeyError:
        print("ERROR: Couldn't find student with email: " + email)
        avg_list.append(0)
        adjusted_avg_list.append(0)
        pass

count = 0
for i, email in enumerate(students_final['SIS User ID']):
    average_calculation(week1_average, week2_average, week3_average, str(email), avg_list, adjusted_avg_list)
    count+=1

series_avg_list = pd.Series(avg_list)
series_adjusted_avg_list = pd.Series(adjusted_avg_list)

    
students_final['TopHat Raw Score (377375)'] = series_avg_list.values
students_final['TopHat Participation Current Score'] = series_adjusted_avg_list.values
#students_final['adjusted-averages'] = series_adjusted_avg_list.values

students_final.to_csv('overall_averages.csv', index = False)
