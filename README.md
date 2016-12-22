# HMC Homework Template
This script creates a TeX template in the current directory that uses the Harvey Mudd College class file and format. If the proper class file `hmcpset.cls` is not found, it will ask whether you would like one to be made. It will also make sure that no existing files will be overwritten.

## Python Version
This code is written for Python 3 but is backwards compatible with Python 2.

### Python 2
To run this script with Python 2, the `future` package needs to be installed. To do this, run the following command.
```{bash}
pip install future
```
Once the `future` package is installed, the script may be run in Python 2.
```{bash}
python createTemplate.py
```

### Python 3
Nothing additional needs to be done for Python 3. Simply run the following command.
```{bash}
python3 createTemplate.py
```

## Credits
This script was created originally by [Eyassu Shimelis](https://github.com/eshimelis).

