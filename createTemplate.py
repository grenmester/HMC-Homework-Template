import click
import os

################################################################################
#### TeX Class File

hmcpset = '''
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

begin = '''
\\documentclass[11pt,letterpaper,boxed]{{hmcpset}}
\\usepackage[margin=1in,headheight=14pt]{{geometry}}
\\usepackage{{amsfonts, amsmath, amssymb, enumerate, fancyhdr, gensymb, lastpage, mathtools, parskip}}

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

problem = '''
%------------------------- Problem {0} -----------------------

\\begin{{problem}}[{0}]
    \\hfill
\\end{{problem}}

\\begin{{solution}}
    \\vfill
\\end{{solution}}

\\newpage
'''

end = '''
\\end{document}
'''

################################################################################
#### Helper Functions


def query_inputs():
    '''Gets information about problem set.'''
    click.echo('Please enter the following information:')
    name = click.prompt('Name')
    course = click.prompt('Course')
    assignment = click.prompt('Assignment Name/Number')
    dueDate = click.prompt('Due Date')
    # Limit maximum number of problems to 50.
    numProblems = click.prompt('Number of Problems', default=0,
                               show_default=False,
                               type=click.IntRange(0, 50, clamp=True))
    return name, course, assignment, dueDate, numProblems


def is_number(num):
    '''Determines whether parameter is a number.'''
    try:
        int(num)
    except ValueError:
        return False
    return True


def determine_title(course, assignment):
    '''Determines the title of the problem set.'''
    title = course
    if assignment:
        if course:
            title += ': '
        if is_number(assignment):
            title += 'HW '
        title += assignment
    return title


def determine_homework_file_name(assignment):
    '''Determines the name of the file.'''
    # Strip '/' characters since they can't be used in file names.
    assignment = assignment.replace('/', '')
    counter = 0
    fileName = ''
    if is_number(assignment) or assignment == '':
        fileName += 'hw'
    fileName += '{0}.tex'.format(assignment)
    while os.path.exists(fileName):
        counter += 1
        fileName = ''
        if is_number(assignment) or assignment == '':
            fileName += 'hw'
        fileName += '{0} ({1}).tex'.format(assignment, counter)
    return fileName


def create_homework_file(fileName, name, title, dueDate, numProblems):
    '''Creates the file in the current directory.'''
    with click.open_file(fileName, 'w') as templateFile:
        templateFile.write(begin.format(name, title, dueDate).lstrip())
        for i in range(1, numProblems+1):
            templateFile.write(problem.format(i))
        templateFile.write(end)
        click.echo('The file "' + fileName +
                   '" has been created in the current directory.')


def verify_hmcpset():
    '''
    Determines whether hmcpset is in the current directory and asks to add it
    if it is not found.
    '''
    if not os.path.exists('hmcpset.cls'):
        click.echo('Your current directory does not have the required ' +
                   '"hmcpset.cls".')
        if click.confirm('Create "hmcpset.cls"?', default=True):
            with click.open_file('hmcpset.cls', 'w') as psetFile:
                psetFile.write(hmcpset.lstrip())
                click.echo('The file "hmcpset.cls" has been created in the '
                           'current directory.')

################################################################################
#### Main Function


def main():
    name, course, assignment, dueDate, numProblems = query_inputs()
    title = determine_title(course, assignment)
    fileName = determine_homework_file_name(assignment)
    templateName = create_homework_file(
        fileName, name, title, dueDate, numProblems)
    verify_hmcpset()


if __name__ == '__main__':
    main()
