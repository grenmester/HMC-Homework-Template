# HMC Homework Template

This script creates a TeX template in the current directory that uses the
Harvey Mudd College class file and format. If the proper class file
`hmcpset.cls` is not found, it will ask whether you would like one to be made.
It will also make sure that no existing files will be overwritten.

## Usage

This script works in both Python 2 and Python 3. To use it, simply type the
following into your command prompt.

```bash
python create_template.py
```

Below is an example usage of the script.

```
Please enter the following information:
Name: John Doe
Course: Math 30G
Assignment Name/Number: Limits
Due Date: 9/5
Number of Problems: 5
The file "Limits.tex" has been created in the current directory.
Your current directory does not have the required "hmcpset.cls".
Create "hmcpset.cls"? [Y/n]: y
The file "hmcpset.cls" has been created in the current directory.
```

## Credits
This script was created originally by [Eyassu
Shimelis](https://github.com/eshimelis) and modified by [Jacky
Lee](https://github.com/grenmester).
