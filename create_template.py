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
\\usepackage[margin=1in,headheight=14pt]{{geometry}} % set page layout
\\usepackage{{amssymb}} % AMS symbols
\\usepackage{{enumerate}} % enumerate environment
\\usepackage{{fancyhdr}} % fancy header
\\usepackage{{gensymb}} % generic symbols for text and math mode
\\usepackage{{lastpage}} % get the page count
\\usepackage{{mathtools}} % useful symbols and tools
\\usepackage{{parskip}} % fix paragraph indentation

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

\\problemlist{{{3}}}
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


def determine_title(course, assignment):
    '''Determines the title of the problem set.'''
    title = course
    if assignment and assignment is not 'hw':
        if course:
            title += ': '
        if assignment.isdigit():
            title += 'HW '
        title += assignment
    return title


def query_inputs(advanced):
    '''Gets information about problem set.'''
    click.echo('Please enter the following information:')
    name = click.prompt('Name')
    course = click.prompt('Course')
    assignment = click.prompt('Assignment Name/Number', default='hw',
                              show_default=False)
    due_date = click.prompt('Due Date')
    # Limit maximum number of problems to 50.
    num_problems = click.prompt('Number of Problems', default=0,
                                show_default=False,
                                type=click.IntRange(0, 50, clamp=True))
    title = determine_title(course, assignment)
    problem_list = click.prompt('Problem List', default=title,
                                show_default=False) if advanced else title
    return name, course, assignment, due_date, num_problems, title, \
        problem_list


def determine_homework_file_name(assignment):
    '''Determines the name of the file.'''
    # Strip '/' characters since they can't be used in file names.
    assignment = assignment.replace('/', '')
    counter = 0
    file_name = ''
    if assignment.isdigit():
        file_name += 'hw'
    file_name += '{0}.tex'.format(assignment)
    while os.path.exists(file_name):
        counter += 1
        file_name = ''
        if assignment.isdigit():
            file_name += 'hw'
        file_name += '{0} ({1}).tex'.format(assignment, counter)
    return file_name


def create_homework_file(file_name, name, title, due_date, problem_list,
                         num_problems):
    '''Creates the file in the current directory.'''
    with click.open_file(file_name, 'w') as template_file:
        template_file.write(begin.format(
            name, title, due_date, problem_list).lstrip())
        for i in range(1, num_problems+1):
            template_file.write(problem.format(i))
        template_file.write(end)
        click.echo('The file "' + file_name +
                   '" has been created in the current directory.')


def verify_hmcpset():
    '''
    Determines whether hmcpset is in the current directory and asks to add it
    if it is not found.
    '''
    if not os.path.exists('hmcpset.cls'):
        click.echo('Your current directory does not have the required '
                   '"hmcpset.cls".')
        if click.confirm('Create "hmcpset.cls"?', default=True):
            with click.open_file('hmcpset.cls', 'w') as pset_file:
                pset_file.write(hmcpset.lstrip())
                click.echo('The file "hmcpset.cls" has been created in the '
                           'current directory.')

################################################################################
#### Main Function


@click.command()
@click.option('-a', '--advanced', default=False, is_flag=True,
              help='Advanced options.')
def main(advanced):
    '''Create a ready-to-compile tex file using the hmcpset class.'''
    if advanced:
        click.echo('Entering advanced mode.')
    name, course, assignment, due_date, num_problems, title, problem_list \
        = query_inputs(advanced)
    file_name = determine_homework_file_name(assignment)
    create_homework_file(file_name, name, title, due_date,
                         problem_list, num_problems)
    verify_hmcpset()


if __name__ == '__main__':
    main()
