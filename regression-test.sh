#
# Rerun each county, making sure results are the same as what is stored in CSV directory.
#
LIST="\
Chester \
Cumberland \
Elk \
Fulton \
Huntingdon \
Indiana \
Juniata \
Lackawanna \
Lawrence \
Lebanon \
McKean \
Mercer \
Mifflin \
Montour \
Northampton \
Perry \
Potter \
Snyder \
Tioga \
Venango \
Wayne"

# Submitted by Nicole, not these programs:
# Crawford
# Jefferson
# Lycoming
# Somerset

for c in $LIST
do
	f="read${c}.py"
	echo $f
	python3 "bin/${f}" > foo.csv
	diff -i -b foo.csv PA/$c/CSV/*csv > /dev/null
	if test "$?" != "0"
	then
		echo "==> REGRESSION PROBLEM WITH $c"
		head -2 foo.csv PA/$c/CSV/*csv
	else
		echo "==> OK"
	fi
done
