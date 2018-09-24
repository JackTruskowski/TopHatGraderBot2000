import pandas as pd
import sys

students = pd.read_csv('../Students.csv')
currweek = sys.argv[1]
print("Week", currweek)

week2_sec1_tue = pd.read_csv('./week2-sec1-tue.csv')
week2_sec1_thu = pd.read_csv('./week2-sec1-thu.csv')
week2_sec2_tue = pd.read_csv('./week2-sec2-tue.csv')
week2_sec2_thu = pd.read_csv('./week2-sec2-thu.csv')
#week2_sec3_mon = pd.read_csv('./week2-sec3-mon.csv')
week2_sec3_wed = pd.read_csv('./week2-sec3-wed.csv')
week2_sec3_fri = pd.read_csv('./week2-sec3-fri.csv')
week2_sec4_mon = pd.read_csv('./week2-sec4-mon.csv')
week2_sec4_wed = pd.read_csv('./week2-sec4-wed.csv')
week2_sec4_fri = pd.read_csv('./week2-sec4-fri.csv')

week2_sec1_tue.set_index("Email Address", inplace = True)
week2_sec1_thu.set_index("Email Address", inplace = True)
week2_sec2_tue.set_index("Email Address", inplace = True)
week2_sec2_thu.set_index("Email Address", inplace = True)
#week2_sec3_mon.set_index("Email Address", inplace = True)
week2_sec3_wed.set_index("Email Address", inplace = True)
week2_sec3_fri.set_index("Email Address", inplace = True)
week2_sec4_mon.set_index("Email Address", inplace = True)
week2_sec4_wed.set_index("Email Address", inplace = True)
week2_sec4_fri.set_index("Email Address", inplace = True)

def find_participation_score(df, email, studentList):
    try:
        print(email)
        print(df.loc[email])
        studentList.append(df.loc[email]['Average %'])
    except KeyError:
        print("couldn't find participation score")
        studentList.append(0)                                 
        pass

scores_week2_sec1_tue = []
scores_week2_sec1_thu = []
scores_week2_sec2_tue = []
scores_week2_sec2_thu = []
scores_week2_sec3_mon = []
scores_week2_sec3_wed = []
scores_week2_sec3_fri = []
scores_week2_sec4_mon = []
scores_week2_sec4_wed = []
scores_week2_sec4_fri = []
max_mon = []
max_tue = []
max_wed = []
max_thu = []
max_fri = []
week2_average = []

for i, email in enumerate(students['SIS Login ID']):
    print(i, email)
    find_participation_score(week2_sec1_tue, str(email), scores_week2_sec1_tue)
    find_participation_score(week2_sec1_thu, str(email), scores_week2_sec1_thu)
    find_participation_score(week2_sec2_tue, str(email), scores_week2_sec2_tue)
    find_participation_score(week2_sec2_thu, str(email), scores_week2_sec2_thu)
    #find_participation_score(week2_sec3_mon, str(email), scores_week2_sec3_mon)
    find_participation_score(week2_sec3_wed, str(email), scores_week2_sec3_wed)
    find_participation_score(week2_sec3_fri, str(email), scores_week2_sec3_fri)
    find_participation_score(week2_sec4_mon, str(email), scores_week2_sec4_mon)
    find_participation_score(week2_sec4_wed, str(email), scores_week2_sec4_wed)
    find_participation_score(week2_sec4_fri, str(email), scores_week2_sec4_fri)
    
def calc_max(dayList, list1, list2):
    for score1, score2 in list(zip(list1, list2)):
        max_score = max(score1, score2)
        dayList.append(max_score)

calc_max(max_mon, scores_week2_sec4_mon, scores_week2_sec4_mon)
calc_max(max_tue, scores_week2_sec1_tue, scores_week2_sec2_tue)
calc_max(max_wed, scores_week2_sec3_wed, scores_week2_sec4_wed)
calc_max(max_thu, scores_week2_sec1_thu, scores_week2_sec2_thu)
calc_max(max_fri, scores_week2_sec3_fri, scores_week2_sec4_fri)

def calc_average(avg_list, max_mon, max_tue, max_wed, max_thu, max_fri):
    for mon, tue, wed, thu, fri in list(zip(max_mon, max_tue, max_wed, max_thu, max_fri)):
        avg_1 = (mon + wed + fri)/3
        avg_2 = (tue + thu)/2
        avg_3 = (mon + wed + thu)/3
        avg_4 = (tue + wed + fri)/3
        best_avg = max(avg_1, avg_2, avg_3, avg_4)
        avg_list.append(best_avg)

calc_average(week2_average, max_mon, max_tue, max_wed, max_thu, max_fri)

series_week2_sec1_tue = pd.Series(scores_week2_sec1_tue)
series_week2_sec1_thu = pd.Series(scores_week2_sec1_thu)
series_week2_sec2_tue = pd.Series(scores_week2_sec2_tue)
series_week2_sec2_thu = pd.Series(scores_week2_sec2_thu)
#series_week2_sec3_mon = pd.Series(scores_week2_sec3_mon)
series_week2_sec3_wed = pd.Series(scores_week2_sec3_wed)
series_week2_sec3_fri = pd.Series(scores_week2_sec3_fri)
series_week2_sec4_mon = pd.Series(scores_week2_sec4_mon)
series_week2_sec4_wed = pd.Series(scores_week2_sec4_wed)
series_week2_sec4_fri = pd.Series(scores_week2_sec4_fri)
series_week2_average = pd.Series(week2_average)

students['week2-sec1-tue'] = series_week2_sec1_tue.values
students['week2-sec1-thu'] = series_week2_sec1_thu.values
students['week2-sec2-tue'] = series_week2_sec2_tue.values
students['week2-sec2-thu'] = series_week2_sec2_thu.values
#students['week2-sec3-mon'] = series_week2_sec3_mon.values
students['week2-sec3-wed'] = series_week2_sec3_wed.values
students['week2-sec3-fri'] = series_week2_sec3_fri.values
students['week2-sec4-mon'] = series_week2_sec4_mon.values
students['week2-sec4-wed'] = series_week2_sec4_wed.values
students['week2-sec4-fri'] = series_week2_sec4_fri.values
students['week2-average'] = series_week2_average

students.to_csv('./week2-average.csv',index = False)

students_final = pd.read_csv('../Students.csv')

avg_list = []
adjusted_avg_list = []

week1_average = pd.read_csv('../week1-average.csv')
week2_average = pd.read_csv('../week2-average.csv')
week3_average = pd.read_csv('../week3-average.csv')
week4_average = pd.read_csv('../week4-average.csv')

week1_average.set_index("SIS User ID", inplace = True)
week2_average.set_index("SIS User ID", inplace = True)
week3_average.set_index("SIS User ID", inplace = True)
week4_average.set_index("SIS User ID", inplace = True)

def average_calculation(week1, week2, week3, week4, email, avg_list, adjusted_avg_list):
    try:
        w1 = week1.loc[email]['week1-average']
        w2 = week2.loc[email]['week2-average']
        w3 = week3.loc[email]['week3-average']
        w4 = week4.loc[email]['week4-average']
        avg = (w1 + w2 + w3 + w4)/4
        avg_list.append(avg)
        if avg > 80:
            adjusted_avg_list.append(5)
        else:
            adjusted_avg_list.append((avg * 0.05))
    except KeyError:                                 
        pass

for i, email in enumerate(students_final['Emails']):
    average_calculation(week1_average, week2_average, week3_average, week4_average, str(email), avg_list, adjusted_avg_list)

series_avg_list = pd.Series(avg_list)
series_adjusted_avg_list = pd.Series(adjusted_avg_list)

students_final['raw-averges'] = series_avg_list.values
students_final['adjusted-averages'] = series_adjusted_avg_list.values

students_final.to_csv('../overall_averages.csv', index = False)
