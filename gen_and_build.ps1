Set-Location build
python ..\src\assemble_tex.py -o recepty.tex
pdflatex recepty
pdflatex recepty
Set-Location ..