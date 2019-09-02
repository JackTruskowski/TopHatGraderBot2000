rm intermediate/week*;
for subdir in $(find ../data/ -type d -name "week*" | sort -V)
do
    if [ "${subdir:7}" != "week15" ]; then
	python grader.py $subdir
    fi
done
