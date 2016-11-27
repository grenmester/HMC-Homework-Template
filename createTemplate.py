# createTemplate.py
# Author: Eyassu Shimelis
# Date: Sept. 4, 2016
#
# Automated creation of blank homework TeX files.

import time
import os

packages = """\documentclass[11pt,letterpaper,boxed]{../../hmcpset}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx, enumerate, amsmath, mathtools, amssymb, cancel, mathrsfs, fancyhdr, lastpage, extramarks, amsfonts, tabularx, gensymb}
\usepackage[breakable,skins]{tcolorbox} % yellowness

\setlength{\parskip}{6pt}
\setlength{\parindent}{0pt}

% Margins
\\topmargin=-0.45in
\\evensidemargin=0in
\\oddsidemargin=0in
\\textwidth=6.5in
\\textheight=9.0in
\headsep=0.25in

\\linespread{1.1} % Line spacing

% Set up the header and footer
\pagestyle{fancy}
\lhead{\hmwkAuthorName} % Top left header
\chead{\hmwkClass\ (\hmwkClassInstructor\ \hmwkClassTime): \hmwkTitle} % Top center header
\chead{\hmwkClass: \hmwkTitle} % Top center header
\\rhead{\\firstxmark\ \hmwkDueDate} % Top right header
\lfoot{\lastxmark} % Bottom left footer
\cfoot{} % Bottom center footer
\\rfoot{Page\ \\thepage\ of\ \pageref{LastPage}} % Bottom right footer
\\renewcommand\headrulewidth{0.4pt} % Size of the header rule
\\renewcommand\\footrulewidth{0.4pt} % Size of the footer rule
\\newcommand{\ind}{\hspace{4em}}
"""



def main():

    finished = False

    while not finished:
        print "\nHi there, ready to start an assignment?"
        time.sleep(.5)

        # Get file information
        name = raw_input("Your name: ")
        className = raw_input("Course name: ")
        assignmentNumber = raw_input("Assignment number: ")
        dueDate = raw_input("Due date (any format you prefer): ")
        numberProblems = raw_input("Number of problems: ")
        createHMCpset = raw_input("Create HMCpset.cls (Y/N): ")

        filename = className.replace(" ", "") + "Assignment" + assignmentNumber + ".tex"

        overwrite = "pending"

        # Check if file already exists
        if os.path.exists(filename):
            overwrite = raw_input("\nWARNING: This file already exists in this directory, \nwould you like to overwrite it? (Y/N): ")


        if (overwrite != 'N' and overwrite != 'n'):

            # Create, open template file, and add header
            templateFile = open(filename, "w")
            header = createHeader(name, className, assignmentNumber, dueDate)
            templateFile.write(packages + header)

            # Start document
            templateFile.write("""
\\begin{document} {
\\vspace{-1.5cm}
\\begin{flushleft}
Collaborators:
\end{flushleft}""")

            # Add problems
            for i in range(int(numberProblems)):
                templateFile.write("""

%------------------------- Problem """ + str(i+1) + """ -----------------------

\\begin{problem}[""" + str(i+1) + """]
% Problem goes here...
\end{problem}


\\begin{solution}
% Solution goes here...
\end{solution}

\\newpage

        """)

            # End document
            templateFile.write("""
        \\end{document}""")

            # Close template file
            templateFile.close();

            # Open completed file.
            os.system("open " + templateFile.name)

            HMCpset(createHMCpset)

            print "All done, opening your assignment!\n"
            finished = True


# Creates and returns a header with information provided by user
def createHeader(name, className, assignmentNumber, dueDate):

    remainingHeader = """

%----------------------------------------------------------------------------------------
%	NAME AND CLASS SECTION
%----------------------------------------------------------------------------------------
\\newcommand{\hmwkTitle}{Assignment\ """ + assignmentNumber + """ } % Assignment title
\\newcommand{\hmwkDueDate}{""" + dueDate + """} % Due date
\\newcommand{\hmwkClass}{""" + className + """} % Course/class
\\newcommand{\hmwkAuthorName}{""" + name + """} % Your name
\usepackage{afterpage}
\\newcommand{\half}{\\tfrac{1}{2}}
\\newcommand\\blankpage{%
    \\thispagestyle{empty}%
    \\addtocounter{page}{-1}%
    \\newpage}


    """

    return remainingHeader


# Create hmcpset file in same directory
def HMCpset(createFile):

    if createFile == 'Y' or createFile == 'y':
        psetFile = open("hmcpset.cls", "w")
        psetFile.write("""
% HMC Math dept HW class file
% v0.04 by Eric J. Malm, 10 Mar 2005
%%% IDENTIFICATION --------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}[1995/01/01]
\ProvidesClass{hmcpset}
    [2005/03/10 v0.04 HMC Math Dept problem set class]

%%% INITIAL CODE ----------------------------------------------------------

% test whether the document is being compiled with PDFTeX
\RequirePackage{ifpdf}


%%% DECLARATION OF OPTIONS ------------------------------------------------
%% Header Options: header*, no header
\\newif\ifhmcpset@header

% no header block in upper right hand corner
\DeclareOption{noheader}{%
    \hmcpset@headerfalse%
}

% do print header block
\DeclareOption{header}{%
    \hmcpset@headertrue%
}

%% Font Options: palatino*, cm
\\newif\ifhmcpset@palatino

% use palatino fonts
\DeclareOption{palatino}{%
    \hmcpset@palatinotrue%
}

% use compuer modern fonts
\DeclareOption{cm}{%
    \hmcpset@palatinofalse%
}

%% Problem Boxing: boxed*, unboxed
\\newif\ifhmcpset@boxed

% box problem statements
\DeclareOption{boxed}{%
    \hmcpset@boxedtrue%
}

% don't box problem statements
\DeclareOption{unboxed}{%
    \hmcpset@boxedfalse%
}

% pass remaining options to article class
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

%%% EXECUTION OF OPTIONS --------------------------------------------------
%% default to:
% including header,
% loading mathpazo package for palatino fonts,
% boxing problem statements
\ExecuteOptions{header,palatino,boxed}

\ProcessOptions

%%% PACKAGE LOADING -------------------------------------------------------
%% based on std article class
\LoadClass{article}


%% Font loading: Palatino text/math fonts
\ifhmcpset@palatino
    \RequirePackage{mathpazo}
\\fi

%% AMSLaTeX math environments and symbols
\RequirePackage{amsmath}
\RequirePackage{amssymb}

%% boxed minipage for boxed problem environment
\RequirePackage{boxedminipage}

%%% MAIN CODE -------------------------------------------------------------
%% Tell dvips/pdflatex correct page size
\ifpdf
  \AtBeginDocument{%
    \setlength{\pdfpageheight}{\paperheight}%
    \setlength{\pdfpagewidth}{\paperwidth}%
  }
\else
  \AtBeginDvi{\special{papersize=\\the\paperwidth,\\the\paperheight}}%
\\fi


%% Problem set environments
% boxed problem environment
\\newenvironment{problem}[1][]{%
  \ifhmcpset@boxed\def\hmcpset@probenv{boxed}\else\def\hmcpset@probenv{}\\fi%
  \\bigskip% put space before problem statement box %
  \\noindent\\begin{\hmcpset@probenv minipage}{\columnwidth}%
  \def\@tempa{#1}%
  \ifx\@tempa\empty\else%
    \hmcpset@probformat{#1}\hspace{0.5em}%
  \\fi%
}{%
  \end{\hmcpset@probenv minipage}%
}
% display optional argument to problem in bold
\let\hmcpset@probformat\\textbf

% solution environment with endmark and optional argument
\\newenvironment{solution}[1][]{%
  \\begin{trivlist}%
  \def\@tempa{#1}%
  \ifx\@tempa\empty%
    \item[]%
  \else%
    \item[\hskip\labelsep\\relax #1]%
  \\fi%
}{%
  \mbox{}\penalty10000\hfill\hmcpset@endmark%
  \end{trivlist}%
}

% default endmark is small black square
\def\hmcpset@endmark{\ensuremath{\scriptscriptstyle\\blacksquare}}

%% Problem set list, for top of document
\\newcommand{\problemlist}[1]{\\begin{center}\large\sffamily{#1}\end{center}}

%% commands for upper-right id header block
\\newcommand{\headerblock}{%
\\begin{flushright}
\mbox{\hmcpset@name}\protect\\
\mbox{\hmcpset@class}\protect\\
\mbox{\hmcpset@assignment}\protect\\
\hmcpset@duedate%
\ifx\hmcpset@extraline\empty\else\protect\\\hmcpset@extraline\\fi%
\end{flushright}%
}

% put id header block at start of document
\ifhmcpset@header\AtBeginDocument{\headerblock}\\fi

% internal state for headerblock
\def\hmcpset@name{}
\def\hmcpset@class{}
\def\hmcpset@assignment{}
\def\hmcpset@duedate{}
\def\hmcpset@extraline{}

% commands to set header block info
\\newcommand{\\name}[1]{\def\hmcpset@name{#1}}
\\newcommand{\class}[1]{\def\hmcpset@class{#1}}
\\newcommand{\\assignment}[1]{\def\hmcpset@assignment{#1}}
\\newcommand{\duedate}[1]{\def\hmcpset@duedate{#1}}
\\newcommand{\extraline}[1]{\def\hmcpset@extraline{#1}}

        """)

        psetFile.close

# Automatically start main function
if __name__ == "__main__":
    main()
