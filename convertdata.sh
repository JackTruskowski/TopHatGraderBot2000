#small script to convert the excel files from TopHat to csv files
for subdir in data/*
do
    echo $subdir
    for file in $subdir/*.xls
    do
	ssconvert $file "${file%.xls}.csv"
    done
    mkdir $subdir/xlsfiles
    mv $subdir/*.xls $subdir/xlsfiles/
done   
