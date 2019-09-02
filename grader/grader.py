#-------------------------------------------------------------------------------
# grader.py
# A TopHat grading script for CS200 at UW-Madison
#     Adapted from a script by Varun Ramesh
#
# @author Jack Truskowski
#--------------------------------------------------------------------------------
#
# For usage information, refer to README.md
#
#-------------------------------------------------------------------------------

import csv
import sys
import re
import os
import pandas as pd
import numpy
import hy_param #hyperparameters

# Creates a debug file that shows each weekly average and the final grade for each student
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
        return pd.read_csv('../data/' + currweek + '/' + currweek + '-' + filename + '.csv')
    except:
        ignore_list.append(filename)
        return None

#Detect missing files
def initAndDetectMissingFiles(currweek_var):
    if isinstance(currweek_var, pd.DataFrame):
        currweek_var['Username'] = currweek_var['Username'].str.lower()
        currweek_var['Email Address'] = currweek_var['Email Address'].str.lower()
        currweek_var.set_index("Email Address", inplace = True)
        return True
    return False

#Given an email address, tries to find their score and add it to studentList
def foundParticipationScore(df, email, studentList, name_text):

    #try overrides first
    if email in hy_param.override_dict:
        for override_tup in hy_param.override_dict[email]:
            if override_tup[0] == currweek + '-' + name_text:
                print("LOG:\t\tFound an override score for student " + email + \
                      "\n\t\t\tClass: " + currweek + '-' + name_text + \
                      "\n\t\t\tNew Score: " + str(override_tup[1]))
                studentList.append(override_tup[1])
                return True

    #test hy_param.aliases for overrides too
    if email in hy_param.aliases:
        for possible_alias in hy_param.aliases[email]:
            if possible_alias in hy_param.override_dict:
                for override_tup in hy_param.override_dict[possible_alias]:
                    if override_tup[0] == currweek + '-' + name_text:
                        print("LOG:\t\tFound an override score for student " + email + \
                              "\t\t\tClass: " + currweek + '-' + name_text + \
                              "\t\t\tNew Score: " + str(override_tup[1]))
                        studentList.append(override_tup[1])
                        return True

    #if no override, do the normal searching
    try:
        studentList.append(df.loc[email]['Average %'])
        return True
    except KeyError:
        pass

    #If initial email fails, try hy_param.aliases
    if email in hy_param.aliases:
        for possible_alias in hy_param.aliases[email]:
            try:
                studentList.append(df.loc[possible_alias]['Average %'])
                return True
            except KeyError:
                pass

    studentList.append(0)
    return False


#Do some calculations to give credit to students who may have attended a different lecture
#TODO: unsure if this actually works, because TopHat doesn't seem to track it
def getMaxScoreFromSections(list1, list2):
    max_list = []
    for score1, score2 in list(zip(list1, list2)):
        max_score = max(score1, score2)
        max_list.append(max_score)
    return max_list


#Computes the average score for the week. The boolean flags represent whether there
#were TopHat questions on that day
def calculateWeeklyAverage(avg_list, max_mon, max_tue, max_wed, max_thu, max_fri,\
                           monflag, tueflag, wedflag, thuflag, friflag):
    for mon, tue, wed, thu, fri in list(zip(max_mon, max_tue, max_wed, max_thu, max_fri)):

        #In order to allow credit for attending a variety of lectures, 4 different
        #cases to test
        avg_1 = 0
        avg_2 = 0
        avg_3 = 0
        avg_4 = 0

        #Case 1: mon/wed/fri
        divisor = 3
        for flag in [monflag, wedflag, friflag]:
            if not flag:
                divisor -= 1
        if divisor > 0:
            avg_1 = (mon + wed + fri)/divisor

        #Case 2: tue/thu
        divisor = 2
        for flag in [tueflag, thuflag]:
            if not flag:
                divisor -= 1
        if divisor > 0:
            avg_2 = (tue + thu)/divisor

        #Case 3: mon/wed/thu
        divisor = 3
        for flag in [monflag, wedflag, thuflag]:
            if not flag:
                divisor -= 1
        if divisor > 0:
            avg_3 = (mon + wed + thu)/divisor


        #Case 4: tue/wed/fri
        divisor = 3
        for flag in [tueflag, wedflag, friflag]:
            if not flag:
                divisor -= 1
        if divisor > 0:
            avg_4 = (tue + wed + fri)/divisor


        best_avg = max(avg_1, avg_2, avg_3, avg_4)

        avg_list.append(best_avg)


#Computes the final average across all weeks for a given student
def calculateFinalStudentAverage(weeks, weeks_text, email, avg_list, adjusted_avg_list,
                                 adjusted_avg_score_list, student_averages):

    try:
        count = 0
        week3_count = 0
        running_avg = 0.0
        running_avg_week3 = 0.0 #average from week 3 on
        for i, _ in enumerate(weeks_text):
            if not "week1" in weeks_text[i] and not "week2" in weeks_text[i]:
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
        if isinstance(email, basestring) and email != "nan":
            print("WARNING:\tCouldn't find student with email: " + email)
        avg_list.append(0)
        adjusted_avg_list.append(0)
        adjusted_avg_score_list.append(0)


#--------------------------------------------------------------------------------
# MAIN

students = pd.read_csv('../Students.csv')
currweek = sys.argv[1][8:] #chop off the filepath
print("\n" + currweek)

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

for curr_section in hy_param.class_list:
    week_files[curr_section] = getFileWithIgnoreListChecking(curr_section)
    score_files[curr_section] = []
    grade_series[curr_section] = None

missing_filenames = []
for name_text, week_file_obj in week_files.iteritems():
    if week_file_obj is not None:
        _ = initAndDetectMissingFiles(week_file_obj)
    else:
        missing_filenames.append(name_text)

if missing_filenames:
    print(("Couldn't find files for the following sections. Confirm that there "
           "were no TopHat questions for these sections this week:"))
    for filename in missing_filenames:
        print("\t" + filename)


currweek_average = []

for _, email in enumerate(students['SIS Login ID']):

    email = str(email).lower()
    if not isinstance(email, basestring) and numpy.isnan(email):
        continue

    foundScore = False

    #Search for scores for valid days
    for name_text, week_file_obj in week_files.iteritems():
        if isinstance(week_file_obj, pd.DataFrame):
            if foundParticipationScore(week_file_obj, email, score_files[name_text], name_text):
                foundScore = True
        #Check if there was no questions this week for this students section

    if not foundScore:
        #This student has no TopHat scores, something went wrong, maybe they're
        #not in the class or this is not a row containing student data
        if isinstance(email, basestring) and email != "nan":
            print("WARNING:\tCouldn't find scores for student: " + email)


#TODO: for giving points to students who attended a different lecture. You can add/remove
max_mon_list = getMaxScoreFromSections(score_files["sec3-mon"], score_files["sec4-mon"])
max_tue_list = getMaxScoreFromSections(score_files["sec1-tue"], score_files["sec2-tue"])
max_wed_list = getMaxScoreFromSections(score_files["sec3-wed"], score_files["sec4-wed"])
max_thu_list = getMaxScoreFromSections(score_files["sec1-thu"], score_files["sec2-thu"])
max_fri_list = getMaxScoreFromSections(score_files["sec3-fri"], score_files["sec4-fri"])

monflag = len(max_mon_list)!=0
tueflag = len(max_tue_list)!=0
wedflag = len(max_wed_list)!=0
thuflag = len(max_thu_list)!=0
friflag = len(max_fri_list)!=0
for day1 in [max_mon_list, max_tue_list, max_wed_list, max_thu_list, max_fri_list]:
    for day2 in [max_mon_list, max_tue_list, max_wed_list, max_thu_list, max_fri_list]:
        if not day1 and day2:
            for x in range(len(day2)):
                day1.append(0)

calculateWeeklyAverage(currweek_average, max_mon_list, max_tue_list, max_wed_list, max_thu_list, \
             max_fri_list, monflag, tueflag, wedflag, thuflag, friflag)

for name_text, score_file in score_files.iteritems():
    if name_text not in ignore_list:
        students[currweek + '-' + name_text] = pd.Series(score_file).values
currweek_average_series = pd.Series(currweek_average)

students[currweek + '-average'] = currweek_average_series
students.to_csv('../intermediate/' + currweek + '-average.csv',index = False)
students_final = pd.read_csv('../Students.csv')


avg_list = []
adjusted_avg_list = []
adjusted_avg_score_list = []
weeks_list = []
weeks_text_list = []
student_averages_for_debug = []

#detect the weeks via regex
p = re.compile('^week\d{1,2}-average.csv$')
for filename in os.listdir('../intermediate'):
    if p.match(filename):
        weeks_text_list.append(filename)
        weeks_list.append(pd.read_csv('../intermediate/' + filename))

for item in weeks_list:
    item.set_index("SIS User ID", inplace = True)
    #print(item)


for i, student_id in enumerate(students_final['SIS User ID']):
    student_average = []
    student_average.append(students_final['SIS Login ID'][i])
    #print(student_average)
    calculateFinalStudentAverage(weeks_list, weeks_text_list, str(student_id).upper(), avg_list,
                                 adjusted_avg_list, adjusted_avg_score_list,
                                 student_average)
    student_averages_for_debug.append(student_average)

#make a debug CSV for easy verification / looking up of scores
createDebugCSV(student_averages_for_debug, weeks_text_list, "../intermediate/debug.csv")

series_avg_list = pd.Series(avg_list)
series_adjusted_avg_list = pd.Series(adjusted_avg_list)
series_adjusted_avg_score_list = pd.Series(adjusted_avg_score_list)

#create and write out the final file
students_final['TopHat Raw Score (477865)'] = series_avg_list.values
students_final['TopHat Participation Current Score'] = series_adjusted_avg_list.values
students_final['TopHat Participation Points (477864)'] = series_adjusted_avg_score_list.values
students_final.to_csv('../overall_averages.csv', index = False)
