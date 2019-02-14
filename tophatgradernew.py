
#-------------------------------------------------------------------------------
# tophatgradernew.py
# A TopHat grading script for CS200 at UW-Madison
# Adapted from a script by Varun Ramesh
#
# @author Jack Truskowski


# The script is a bit messy and lacking documentation, sorry
#
# USAGE:
# 1) Download student data for the week and save in the required format.
#     ie) week1/week1-sec1-tue.xls
# 2) From inside the 'week' directory, run convert.sh to convert data to .csv
# 3) Download the most recent student data from Canvas as 'Students.csv'
# 4) Run 'python tophatgradernew.py week1' (or the current week)
#     The weekXX-average.csv file must exist for all previous weeks, so
#     run the script in the order week1 -> week2 -> week3 -> week4, etc.
#     Once you're caught up, you don't need to run the previous weeks again.
# 5) Verify through the output of the program that the script correctly detected
#     any days where there were no TopHat questions and that missing students
#     are no longer in the class. Download missing files / rerun the script
#     if necessary.
# 6) The weekly data is stored in weekXX-average.csv and the combined data is
#    stored in overall_averages.csv
# 7) Visually inspect and upload overall_averages.csv to Canvas
#
#-------------------------------------------------------------------------------

import pandas as pd
import sys
import re
import os

#if the students emails don't match for some reason
aliases = {"JPJAWORSKI2@WISC.EDU": ["JAWORSKI@CS.WISC.EDU"],
           "JAJOHNSON44@WISC.EDU": ["JACK.JOHNSON@WISC.EDU"],
           "SKWON37@WISC.EDU": ["CKIM246@WISC.EDU"],
           "TMLARSON2@WISC.EDU": ["THOMAS.LARSON@WISC.EDU"]}

#--------------------------------------------------
#METHODS
#--------------------------------------------------

#searches for csv files matching a pattern and adds missing files to the ignore list
def getFileWithIgnoreListChecking(filename):
    try:
        return pd.read_csv(currweek + '/' + currweek + '-' + filename + '.csv')
    except:
        ignore_list.append(filename)
        return None
    
#Detect missing files 
def initAndDetectMissingFiles(currweek_var, df, missing_message):
    if isinstance(currweek_var, df):
        currweek_var['Username'] = currweek_var['Username'].str.upper()
        currweek_var['Email Address'] = currweek_var['Email Address'].str.upper()
        currweek_var.set_index("Email Address", inplace = True)
    else:
        print(missing_message)

#Grabs the score for a student 
def find_participation_score(df, email, studentList):

    global aliases
    
    try:
        studentList.append(df.loc[email]['Average %'])
        return True
    except KeyError:
        pass

    #If initial email fails, try aliases
    if email in aliases:
        for possibleAlias in aliases[email]:
            try:
                studentList.append(df.loc[possibleAlias]['Average %'])
                return True
            except KeyError:
                pass

    studentList.append(0)
    return False;
    
#Do some calculations to give credit to students who may have attended a different lecture
def calc_max(dayList, list1, list2):
    for score1, score2 in list(zip(list1, list2)):
        max_score = max(score1, score2)
        dayList.append(max_score)
        
#Computes the average score for the week. The boolean flags represent whether there were TopHat questions on that day
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

def average_calculation(weeks, weeks_text, email, avg_list, adjusted_avg_list, adjusted_avg_score_list):
    try:
        count = 0
        week3_count = 0
        running_avg = 0.0
        running_avg_week3 = 0.0 #average from week 3 on
        for i in range(len(weeks_text)):
            if not "week1" in weeks_text and not "week2" in weeks_text and not "week3" in weeks_text:
                running_avg_week3 += weeks[i].loc[email][weeks_text[i][:-4]]
                week3_count += 1
            running_avg += weeks[i].loc[email][weeks_text[i][:-4]]
            count += 1

        if week3_count > 0:
            avg = max(running_avg/count, running_avg_week3/week3_count)
        else:
            avg = running_avg/count
        avg_list.append(avg)
        if avg > 80:
            adjusted_avg_list.append(100)
            adjusted_avg_score_list.append(5)
        else:
            adjusted_avg_list.append(avg)
            adjusted_avg_score_list.append((avg*5)/100)
    except KeyError:
        print("ERROR: Couldn't find student with email: " + email)
        avg_list.append(0)
        adjusted_avg_list.append(0)
        adjusted_avg_score_list.append(0)
        pass

    
#--------------------------------------------------
#CODE
#--------------------------------------------------

students = pd.read_csv('Students.csv')
currweek = sys.argv[1]

ignore_list = []

# The script currently auto-detects missing days. If you would like to manually enter missing days
# the following lines may help:
#
# print("Are there any missing days this week?\n\tFormat as 'secX-DAY'\nType 'end' to finish")
# while(True):
#     usr_input = input()
#     if usr_input == 'end':
#         break
#     ignore_list.append(usr_input.lower())
# print(ignore_list)

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
initAndDetectMissingFiles(currweek_sec1_tue, pd.DataFrame, "sec1_tue")
initAndDetectMissingFiles(currweek_sec1_thu, pd.DataFrame, "sec1_thu")
initAndDetectMissingFiles(currweek_sec2_tue, pd.DataFrame, "sec2_tue")
initAndDetectMissingFiles(currweek_sec2_thu, pd.DataFrame, "sec2_thu")
initAndDetectMissingFiles(currweek_sec3_mon, pd.DataFrame, "sec3_mon")
initAndDetectMissingFiles(currweek_sec3_wed, pd.DataFrame, "sec3_wed")
initAndDetectMissingFiles(currweek_sec3_fri, pd.DataFrame, "sec3_fri")
initAndDetectMissingFiles(currweek_sec4_mon, pd.DataFrame, "sec4_mon")
initAndDetectMissingFiles(currweek_sec4_wed, pd.DataFrame, "sec4_wed")
initAndDetectMissingFiles(currweek_sec4_fri, pd.DataFrame, "sec4_fri")

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

    #Search for scores for valid days
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
        #This student has no TopHat scores, something went wrong, maybe they're not in the class
        #or this is not a row containing student data
        print("WARNING: Couldn't find scores for student: " + email)


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


avg_list = []
adjusted_avg_list = []
adjusted_avg_score_list = []
weeks_list = []
weeks_text_list = []

#detect the weeks via regex
p = re.compile('^week\d{1,2}-average.csv$')
for filename in os.listdir('.'):
    if p.match(filename):
        weeks_text_list.append(filename)
        weeks_list.append(pd.read_csv(filename))

for item in weeks_list:
    item.set_index("SIS User ID", inplace = True)

    
count = 0
for i, email in enumerate(students_final['SIS User ID']):
    average_calculation(weeks_list, weeks_text_list, str(email), avg_list, adjusted_avg_list, adjusted_avg_score_list)
    count+=1

series_avg_list = pd.Series(avg_list)
series_adjusted_avg_list = pd.Series(adjusted_avg_list)
series_adjusted_avg_score_list = pd.Series(adjusted_avg_score_list)    
    
students_final['TopHat Raw Score (477865)'] = series_avg_list.values
students_final['TopHat Participation Current Score'] = series_adjusted_avg_list.values
students_final['TopHat Participation Points (477864)'] = series_adjusted_avg_score_list.values
#students_final['adjusted-averages'] = series_adjusted_avg_list.values

students_final.to_csv('overall_averages.csv', index = False)



