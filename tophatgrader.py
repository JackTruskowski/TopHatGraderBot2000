
#-------------------------------------------------------------------------------
# tophatgrader.py
# A TopHat grading script for CS200 at UW-Madison
#     Adapted from a script by Varun Ramesh
#
# @author Jack Truskowski
#--------------------------------------------------------------------------------
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
import numpy
import csv
import sys
import re
import os

#-------------------------------------------------------------------------------
# Modify these variables for your class

#if the students emails don't match for some reason
aliases = {"JPJAWORSKI2@WISC.EDU": ["JAWORSKI@CS.WISC.EDU"],
           "JAJOHNSON44@WISC.EDU": ["JACK.JOHNSON@WISC.EDU"],
           "SKWON37@WISC.EDU": ["CKIM246@WISC.EDU"],
           "TMLARSON2@WISC.EDU": ["THOMAS.LARSON@WISC.EDU"]}

#contains the section information
#For example,
class_list = ['sec1-tue', 'sec1-thu', 'sec2-tue', 'sec2-thu', 'sec3-mon', \
              'sec3-wed', 'sec3-fri', 'sec4-mon', 'sec4-wed', 'sec4-fri']

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Methods


# Creates a debug file that shows each weekly average and the final grade
# for each student
def createDebugCSV(student_data, week_names, outfilename):
    colnames = []

    #collect the names of all columns and prepend them
    colnames.append("Name")
    for week in week_names:
        colnames.append(week)
    colnames.append("Final Average")
    student_data.insert(0, colnames)
    
    with open(outfilename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(student_data)
    csvfile.close()
    

#searches for csv files matching a pattern and adds missing files to the ignore list
def getFileWithIgnoreListChecking(filename):
    try:
        return pd.read_csv('data/' + currweek + '/' + currweek + '-' + filename + '.csv')
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

#Given an email address, tries to find their score and add it to studentList
def found_participation_score(df, email, studentList):

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

#TODO: comment
def average_calculation(weeks, weeks_text, email, avg_list, adjusted_avg_list, adjusted_avg_score_list, student_averages):
    try:
        count = 0
        week3_count = 0
        running_avg = 0.0
        running_avg_week3 = 0.0 #average from week 3 on
        for i in range(len(weeks_text)):
            if not "week1" in weeks_text[i] and not "week2" in weeks_text[i] and not "week3" in weeks_text[i]:
                running_avg_week3 += weeks[i].loc[email][weeks_text[i][:-4]]
                week3_count += 1

            student_averages.append(weeks[i].loc[email][weeks_text[i][:-4]])
            running_avg += weeks[i].loc[email][weeks_text[i][:-4]]
            count += 1

        if week3_count > 0:
            avg = max(running_avg/count, running_avg_week3/week3_count)
        else:
            avg = running_avg/count
        avg_list.append(avg)
        
        if avg > 80:
            adjusted_avg_list.append(100)
            student_averages.append(avg)
            adjusted_avg_score_list.append(5)
        else:
            adjusted_avg_list.append(avg)
            student_averages.append(avg)
            adjusted_avg_score_list.append((avg*5)/100)
    except KeyError:
        print("ERROR: Couldn't find student with email: " + email)
        avg_list.append(0)
        adjusted_avg_list.append(0)
        adjusted_avg_score_list.append(0)
        pass


#--------------------------------------------------------------------------------    
# MAIN

students = pd.read_csv('Students.csv')
currweek = sys.argv[1]

#contains the week files <name, fileobject>
week_files = {}
#contains the score files <name, fileobject>
score_files = {}
#stores the pandas series
grade_series = {}


ignore_list = []

# The script currently auto-detects missing days. If you would like to manually
# enter missing days the following lines may help:

# print("Are there any missing days this week?\n\tFormat as 'secX-DAY'\nType 'end' to finish")
# while(True):
#     usr_input = input()
#     if usr_input == 'end':
#         break
#     ignore_list.append(usr_input.lower())
# print(ignore_list)

for curr_section in class_list:
    week_files[curr_section] = getFileWithIgnoreListChecking(curr_section)
    score_files[curr_section] = []
    grade_series[curr_section] = None

print("Couldn't find files for the following sections. Confirm that there were \
no TopHat questions for these sections this week:")

for name_text, week_file_obj in week_files.iteritems():
    initAndDetectMissingFiles(week_file_obj, pd.DataFrame, name_text)

# scores_currweek_sec1_tue = []
# scores_currweek_sec1_thu = []
# scores_currweek_sec2_tue = []
# scores_currweek_sec2_thu = []
# scores_currweek_sec3_mon = []
# scores_currweek_sec3_wed = []
# scores_currweek_sec3_fri = []
# scores_currweek_sec4_mon = []
# scores_currweek_sec4_wed = []
# scores_currweek_sec4_fri = []

currweek_average = []

for i, email in enumerate(students['SIS Login ID']):

    email = str(email)
    if not isinstance(email, basestring) and numpy.isnan(email):
        continue
    
    foundScore = False

    #Search for scores for valid days
    for name_text, week_file_obj in week_files.iteritems():
        if isinstance(week_file_obj, pd.DataFrame):
            if found_participation_score(week_file_obj, email, score_files[name_text]):
                foundScore = True

    if not foundScore:
        #This student has no TopHat scores, something went wrong, maybe they're
        #not in the class or this is not a row containing student data
        print("WARNING: Couldn't find scores for student: " + email)


max_mon = []
max_tue = []
max_wed = []
max_thu = []
max_fri = []

#TODO: for giving points to students who attended a different lecture. You can add/remove
calc_max(max_mon, score_files["sec3-mon"], score_files["sec4-mon"])
calc_max(max_tue, score_files["sec1-tue"], score_files["sec2-tue"])
calc_max(max_wed, score_files["sec3-wed"], score_files["sec4-wed"])
calc_max(max_thu, score_files["sec1-thu"], score_files["sec2-thu"])
calc_max(max_fri, score_files["sec3-fri"], score_files["sec4-fri"])

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

for name_text, score_file in score_files.iteritems():
    if name_text not in ignore_list:
        students[currweek + '-' + name_text] = pd.Series(score_file).values
currweek_average_series = pd.Series(currweek_average)

students[currweek + '-average'] = currweek_average_series
students.to_csv('./intermediate/' + currweek + '-average.csv',index = False)
students_final = pd.read_csv('Students.csv')


avg_list = []
adjusted_avg_list = []
adjusted_avg_score_list = []
weeks_list = []
weeks_text_list = []
student_averages_for_debug = []

#detect the weeks via regex
p = re.compile('^week\d{1,2}-average.csv$')
for filename in os.listdir('./intermediate'):
    if p.match(filename):
        weeks_text_list.append(filename)
        weeks_list.append(pd.read_csv('./intermediate/' + filename))

for item in weeks_list:
    item.set_index("SIS User ID", inplace = True)

    
count = 0
for i, email in enumerate(students_final['SIS User ID']):
    student_average = []
    student_average.append(students_final['SIS Login ID'][i])
    average_calculation(weeks_list, weeks_text_list, str(email), avg_list, adjusted_avg_list, adjusted_avg_score_list, student_average)
    student_averages_for_debug.append(student_average)
    count+=1

createDebugCSV(student_averages_for_debug, weeks_text_list, "./intermediate/debug.csv")

series_avg_list = pd.Series(avg_list)
series_adjusted_avg_list = pd.Series(adjusted_avg_list)
series_adjusted_avg_score_list = pd.Series(adjusted_avg_score_list)    
    
students_final['TopHat Raw Score (477865)'] = series_avg_list.values
students_final['TopHat Participation Current Score'] = series_adjusted_avg_list.values
students_final['TopHat Participation Points (477864)'] = series_adjusted_avg_score_list.values
#students_final['adjusted-averages'] = series_adjusted_avg_list.values

students_final.to_csv('overall_averages.csv', index = False)
