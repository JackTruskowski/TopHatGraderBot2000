
for subdir in $(find ./data/ -type d -name "week*" | sort -V)
do
    python tophatgrader.py $subdir
done
