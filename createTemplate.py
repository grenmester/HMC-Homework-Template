#!/usr/bin/env python

import os

################################################################################
#### TeX Class File

hmcpset = \
'''
% HMC Math dept HW class file
% v0.04 by Eric J. Malm, 10 Mar 2005
%%% IDENTIFICATION --------------------------------------------------------
\\NeedsTeXFormat{LaTeX2e}[1995/01/01]
\\ProvidesClass{hmcpset}
    [2005/03/10 v0.04 HMC Math Dept problem set class]

%%% INITIAL CODE ----------------------------------------------------------

% test whether the document is being compiled with PDFTeX
\\RequirePackage{ifpdf}


%%% DECLARATION OF OPTIONS ------------------------------------------------
%% Header Options: header*, no header
\\newif\\ifhmcpset@header

% no header block in upper right hand corner
\\DeclareOption{noheader}{%
    \\hmcpset@headerfalse%
}

% do print header block
\\DeclareOption{header}{%
    \\hmcpset@headertrue%
}

%% Font Options: palatino*, cm
\\newif\\ifhmcpset@palatino

% use palatino fonts
\\DeclareOption{palatino}{%
    \\hmcpset@palatinotrue%
}

% use compuer modern fonts
\\DeclareOption{cm}{%
    \\hmcpset@palatinofalse%
}

%% Problem Boxing: boxed*, unboxed
\\newif\\ifhmcpset@boxed

% box problem statements
\\DeclareOption{boxed}{%
    \\hmcpset@boxedtrue%
}

% don't box problem statements
\\DeclareOption{unboxed}{%
    \\hmcpset@boxedfalse%
}

% pass remaining options to article class
\\DeclareOption*{\\PassOptionsToClass{\\CurrentOption}{article}}

%%% EXECUTION OF OPTIONS --------------------------------------------------
%% default to:
% including header,
% loading mathpazo package for palatino fonts,
% boxing problem statements
\\ExecuteOptions{header,palatino,boxed}

\\ProcessOptions

%%% PACKAGE LOADING -------------------------------------------------------
%% based on std article class
\\LoadClass{article}


%% Font loading: Palatino text/math fonts
\\ifhmcpset@palatino
    \\RequirePackage{mathpazo}
\\fi

%% AMSLaTeX math environments and symbols
\\RequirePackage{amsmath}
\\RequirePackage{amssymb}

%% boxed minipage for boxed problem environment
\\RequirePackage{boxedminipage}

%%% MAIN CODE -------------------------------------------------------------
%% Tell dvips/pdflatex correct page size
\\ifpdf
  \\AtBeginDocument{%
    \\setlength{\\pdfpageheight}{\\paperheight}%
    \\setlength{\\pdfpagewidth}{\\paperwidth}%
  }
\\else
  \\AtBeginDvi{\\special{papersize=\\the\\paperwidth,\\the\\paperheight}}%
\\fi


%% Problem set environments
% boxed problem environment
\\newenvironment{problem}[1][]{%
  \\ifhmcpset@boxed\\def\\hmcpset@probenv{boxed}\\else\\def\\hmcpset@probenv{}\\fi%
  \\bigskip% put space before problem statement box %
  \\noindent\\begin{\\hmcpset@probenv minipage}{\\columnwidth}%
  \\def\\@tempa{#1}%
  \\ifx\\@tempa\\empty\\else%
    \\hmcpset@probformat{#1}\\hspace{0.5em}%
  \\fi%
}{%
  \\end{\\hmcpset@probenv minipage}%
}
% display optional argument to problem in bold
\\let\\hmcpset@probformat\\textbf

% solution environment with endmark and optional argument
\\newenvironment{solution}[1][]{%
  \\begin{trivlist}%
  \\def\\@tempa{#1}%
  \\ifx\\@tempa\\empty%
    \\item[]%
  \\else%
    \\item[\\hskip\\labelsep\\relax #1]%
  \\fi%
}{%
  \\mbox{}\\penalty10000\\hfill\\hmcpset@endmark%
  \\end{trivlist}%
}

% default endmark is small black square
\\def\\hmcpset@endmark{\\ensuremath{\\scriptscriptstyle\\blacksquare}}

%% Problem set list, for top of document
\\newcommand{\\problemlist}[1]{\\begin{center}\\large\\sffamily{#1}\\end{center}}

%% commands for upper-right id header block
\\newcommand{\headerblock}{%
\\begin{flushright}
\\mbox{\hmcpset@name}\\protect\\
\\mbox{\hmcpset@class}\\protect\\
\\mbox{\hmcpset@assignment}\\protect\\
\\hmcpset@duedate%
\\ifx\\hmcpset@extraline\\empty\\else\\protect\\\\hmcpset@extraline\\fi%
\\end{flushright}%
}

% put id header block at start of document
\\ifhmcpset@header\\AtBeginDocument{\\headerblock}\\fi

% internal state for headerblock
\\def\\hmcpset@name{}
\\def\\hmcpset@class{}
\\def\\hmcpset@assignment{}
\\def\\hmcpset@duedate{}
\\def\\hmcpset@extraline{}

% commands to set header block info
\\newcommand{\\name}[1]{\\def\\hmcpset@name{#1}}
\\newcommand{\\class}[1]{\\def\\hmcpset@class{#1}}
\\newcommand{\\assignment}[1]{\\def\\hmcpset@assignment{#1}}
\\newcommand{\\duedate}[1]{\\def\\hmcpset@duedate{#1}}
\\newcommand{\\extraline}[1]{\\def\\hmcpset@extraline{#1}}

'''

################################################################################
#### TeX Template Fragments

begin = \
'''\\documentclass[11pt,letterpaper,boxed]{{hmcpset}}
\\usepackage[margin=1in,headheight=14pt]{{geometry}}
\\usepackage{{amsfonts, amsmath, amssymb, enumerate, fancyhdr, gensymb, lastpage, mathtools}}

\\pagestyle{{fancy}}
\\lhead{{{0}}}
\\chead{{{1}}}
\\rhead{{{2}}}
\\lfoot{{}}
\\cfoot{{}}
\\rfoot{{Page\\ \\thepage\\ of\\ \\pageref{{LastPage}}}}

\\linespread{{1.1}}

\\newcommand\\blankpage{{
    \\thispagestyle{{empty}}
    \\addtocounter{{page}}{{-1}}
    \\newpage}}
\\renewcommand\\footrulewidth{{0.4pt}}

\\begin{{document}}

\\problemlist{{{1}}}
'''

problem = \
'''
%------------------------- Problem {0} -----------------------

\\begin{{problem}}[{0}]
    \\hfill
\\end{{problem}}

\\begin{{solution}}
    \\vfill
\\end{{solution}}

\\newpage
'''

end = \
'''
\\end{document}
'''

################################################################################
#### Main Function

def main():
    # query inputs
    print('Please enter the following information:')
    name = raw_input('Name: ')
    course = raw_input('Course: ')
    assignment = raw_input('Assignment Name/Number: ')
    dueDate = raw_input('Due Date: ')
    while True:
        try:
            numProblems = raw_input('Number of Problems: ')
            if numProblems == "":
                numProblems = 0
            numProblems = int(numProblems)
            if numProblems < 0:
                raise ValueError
            break
        except ValueError:
            print('Please enter a valid number of problems')

    # name title
    title = course
    if assignment:
        if course:
            title += ': '
        try:
            if int(assignment):
                title += 'HW '
        except:
            pass
        title += assignment

    # name homework file
    counter = 0
    fileName = 'hw{0}.tex'.format(assignment)
    while os.path.exists(fileName):
        counter += 1
        fileName = 'hw{0} ('.format(assignment) + str(counter) + ').tex'

    # create homework file
    with open(fileName,'w') as templateFile:
        templateFile.write(begin.format(name, title, dueDate))
        for i in range(numProblems):
            templateFile.write(problem.format(i+1))
        templateFile.write(end)
        print('\nThe file "' + fileName + '" has been created in the current directory.')

    # ask to add hmcpset.cls if not found
    if not os.path.exists('hmcpset.cls'):
        createPset = raw_input('\nYour current directory does not contain the required hmcpset.cls \nCreate hmcpset.cls? [(y)/n]: ')
        if createPset in ['Y','y','Yes','yes', '']:
            with open('hmcpset.cls','w') as psetFile:
                psetFile.write(hmcpset)
                print('\nThe file "hmcpset.cls" has been created in the current directory.')

    # ask if user wants to open assignment
    openFile = raw_input('\nAll done, would you like to open your assignment? [y/(n)]: ')
    if openFile in ['Y','y','Yes','yes']:
        print('Opening your assignment!')
        os.system('open ' + templateFile.name)

if __name__ == '__main__':
    main()
