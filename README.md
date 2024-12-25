# elections
Scripts for parsing PDF election results for the 2024 Election.

Developed using Python 3.

Requires installing 'pypdf' package: `pip3 install pypdf`

## How to generate CSV results:
```
python3 readFulton.py
python3 readHuntingdon.py
python3 readJuniata.py
python3 readLebanon.py
python3 readLackawanna.py
python3 readLebanon.py
python3 readMcKean.py
python3 readMercer.py
python3 readSnyder.py
python3 readTioga.py
```

## Testing
A regression test checks that any changes to common files (e.g., `readSingleDoc.py`) still generates the same results in all checked-in CSV files.

To run the test on a command line:

```
sh regression-test.sh
```