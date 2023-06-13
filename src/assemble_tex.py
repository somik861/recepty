from argparse import ArgumentParser
from common import loader
from pathlib import Path
from typing import TextIO

_ARG_OUT = Path('out.tex')


def _write_header(stream: TextIO) -> None:
    stream.write(
        r'''
\documentclass[a4paper]{article}

% Set title page
\author{Jan Juračka}
\title{Recepty}

% set content page title
\renewcommand{\contentsname}{Obsah}
% make content table clickable
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=blue,
    urlcolor=blue
}

% section centering
\usepackage{sectsty}
\sectionfont{\centering}
\subsectionfont{\centering}

% degree symbol
\usepackage{gensymb}

% whole paragraph indent
\usepackage{changepage}

% make paragraph indent 0
\setlength{\parindent}{0pt}

% portions
\newcommand{\porce}[1]{\begin{center}\small(Porce: #1)\end{center}}

\begin{document}
\maketitle
\newpage

\tableofcontents\label{toc}
\newpage
''')


def _write_footer(stream: TextIO) -> None:
    stream.write(r'''
\end{document}
''')


def _write_recipe(stream: TextIO, recipe: loader.Recipe) -> None:
    stream.write(
        f'''
\\subsection{{{recipe.name}}}
\\begin{{flushright}} \\hyperref[toc]{{obsah}} \\end{{flushright}}
\\porce{{{'?' if recipe.portions is None else recipe.portions}}}
\\vspace{{10px}}
\\textbf{{Suroviny:}}
\\begin{{itemize}}

''')
    for item in recipe.items:
        stream.write(f'\\item {item.text} \n')

    stream.write('''
\\end{itemize}

\\vspace{10px}
\\textbf{Postup:}
\\begin{enumerate}
''')

    for step in recipe.procedure:
        stream.write(f'\\item {step} \n')

    stream.write('\\end{enumerate}\n')

    if recipe.note is not None:
        stream.write(f'''
\\vspace{{10px}}
\\textbf{{poznamka}}
\\begin{{adjustwidth}}{{1cm}}
{recipe.note}
\\end{{adjustwidth}}
''')


def _write_block(stream: TextIO, recipes: list[loader.Recipe], name: str) -> None:
    stream.write(f'''
\\section{{{name}}}
''')
    for recipe in recipes:
        _write_recipe(stream, recipe)


def _write_recipes(stream: TextIO, recipes: dict[str, list[loader.Recipe]]) -> None:
    for name, recipe_list in recipes.items():
        _write_block(stream, recipe_list, name)


def main() -> None:
    with open(_ARG_OUT, mode='w', encoding='utf-8', newline='\n') as out_file:
        recipes = loader.load_all()

        _write_header(out_file)
        _write_recipes(out_file, recipes)
        _write_footer(out_file)


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--out', '-o', type=Path,
                        help=f'Output path; default: {_ARG_OUT}', default=_ARG_OUT)

    args = parser.parse_args()
    _ARG_OUT = args.out

    main()