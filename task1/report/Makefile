TARGET := report

all: wordcount
	echo "done"
	#@evince $(TARGET).pdf

pdf: wordcount

report: clean
	xelatex $(TARGET)
	#bibtex  $(TARGET)
	xelatex $(TARGET)
	xelatex $(TARGET)

wordcount: report
	pdftotext $(TARGET).pdf

clean:
	@rm -vfr *.out *.log *.toc *.aux *.bak *.bbl *.blg *.txt
