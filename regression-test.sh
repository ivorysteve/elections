#
# Rerun each county, making sure results are the same as what is stored in CSV directory.
#
LIST="\
Cumberland 
Fulton \
Huntingdon \
Juniata \
Lackawanna \
Lebanon \
McKean \
Mercer \
Snyder \
Tioga \
Venango"

# Not yet working
# Lycoming

for c in $LIST
do
	f="read${c}.py"
	echo $f
	python3 "bin/${f}" > foo.csv
	diff -i foo.csv PA/$c/CSV/*csv > /dev/null
	if test "$?" != "0"
	then
		echo "==> REGRESSION PROBLEM WITH $c"
		head -2 foo.csv PA/$c/CSV/*csv
	else
		echo "==> OK"
	fi
done
