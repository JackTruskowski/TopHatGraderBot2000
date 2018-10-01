#small script to convert the excel files from TopHat to csv files
for file in *.xls
do
    ssconvert "$file" "${file%.xls}.csv"
done
mkdir xlsfiles
mv *.xls xlsfiles/
