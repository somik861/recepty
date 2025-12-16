#! /bin/bash
mkdir -p build
cd build
python ../src/assemble_tex.py -o recepty.tex
pdflatex recepty.tex
pdflatex recepty.tex
pdflatex recepty.tex
cd ..