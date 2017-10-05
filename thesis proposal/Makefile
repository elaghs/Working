Src=Main

all : dirs eps bib tex bib textex bib done

one : dirs eps tex bib done

done :
	@printf "\n\n\n==============================================\n"
	@printf       "see output in $(HOME)/tmp/$(Src).pdf\n"
	@printf       "==============================================\n\n\n"
#	- rm arrt.pdf

dirs : 
	if [ ! -d $(HOME)/tmp ];  then mkdir $(HOME)/tmp; fi

eps :
#	- epstopdf arrt.eps

tex :
	- pdflatex -output-directory=$(HOME)/tmp $(Src)
	
bib : 
	- bibtex $(HOME)/tmp/$(Src)

textex :
	- pdflatex -output-directory=$(HOME)/tmp $(Src)
	- pdflatex -output-directory=$(HOME)/tmp $(Src)

