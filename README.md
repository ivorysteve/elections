# elections
Scripts for parsing PDF election results for the 2024 Election.

Developed using Python 3.

Requires installing 'pypdf' package: `pip3 install pypdf`

## How to generate CSV results for a specific county:
```
python3 bin/readFulton.py
python3 bin/readHuntingdon.py
python3 bin/readJuniata.py
...
```

## Testing
A regression test checks that any changes to common files (e.g., `readSingleDoc.py`) still generates the same results in all checked-in CSV files.

To run the test on a command line:

```
sh regression-test.sh
```

## Data Organization

Data for all counties are organized the same way:

```
<Stage_Abbreviation>/<County_Name>/<County_Data>
```

The County Data consists of the following (mandatory) organization:

* `Results_PDF`: A directory containing 1 or more original PDF files from the county website.  Only files with a `.pdf` suffix are read.
* `Results_PDF/URL_List.txt`: A text file containing a list of URLs from which the PDFs were fetched.  The filecomponent of the URL MUST match that of the corresponding file in the `Results_PDF` directory.
* `CSV`: A directory containing a single normalized CSV file for the county.  It must use a `.csv` suffix.

For example, the CSV file for `Juniata` county in Pennsylvania is: `PA/Juniata/CSV/juniata.csv`.