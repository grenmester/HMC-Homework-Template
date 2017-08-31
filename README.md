# HMC Homework Template
This script creates a TeX template in the current directory that uses the Harvey Mudd College class file and format. If the proper class file `hmcpset.cls` is not found, it will ask whether you would like one to be made. It will also make sure that no existing files will be overwritten.

If you want to use Python 3, replace all instances of `raw_input` with `input`.

## Usage
This script is written for Python 2.7. To use it, simply type the following into your command prompt.
```bash
python createTemplate.py
```
Below is an example usage of the script.
```
Please enter the following information:
Name: John Doe
Course: MATH 30G
Assignment Name/Number: Limits
Due Date: 9/5
Number of Problems: 5

The file "Limits.tex" has been created in the current directory.

Your current directory does not contain the required hmcpset.cls
Create hmcpset.cls? [(y)/n]: y

The file "hmcpset.cls" has been created in the current directory.

All done, would you like to open your assignment? [y/(n)]: n
```

## Credits
This script was created originally by [Eyassu Shimelis](https://github.com/eshimelis) and modified by [Jacky Lee](https://github.com/grenmester).
