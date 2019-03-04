# TopHatGraderBot2000
##### A grading script for CS200 @ UW-Madison
___

###### Usage:
1. **Download student data from TopHat in the correct format.**
    For example, if Section 1 meets on Tuesday and Thursday, the week one data should be stored as:
    `data/week1/sec1-tue.xls`
    `data/week1/sec1-thu.xls`
2. **Run convertdata.sh to convert .xls to .csv files**
3. **Edit variables at the top of tophatgrader.py** and any TODOs (optional) for your class
4. **Export the student data from Canvas as Students.csv**
5. **Run the script:**
    `python tophatgrader.py week1`
    + All previous weeks must be run before running the current week (ie week1 -> week2 -> week3, etc)
    + Once a week has been run and `intermediate/weekX-average.csv` has been generated, no need to run it again
6. **Final output data up to the week you just ran is in `overall-averages.csv`**
    + This file can be uploaded to Canvas

###### Notes:
+   `intermediate/debug.csv` contains weekly averages and final grade for each student, helpful for debugging or quickly seeing how a student's grade was calculated

