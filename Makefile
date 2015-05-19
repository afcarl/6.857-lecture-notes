MD_SRCS=$(wildcard *.md)
TEX_SRCS=$(wildcard *.tex)

HTMLS=$(MD_SRCS:.md=.html)
PDFS=$(TEX_SRCS:.tex=.pdf)

%.html: %.md
	@echo "Markdown compiling $< -> $*.html"
	markdown $< >$*.html

all: $(HTMLS) $(PDFS)
	@echo "MDs: $(MD_SRCS)"
	@echo "TeXs: $(TEX_SRCS)"

%.pdf: %.tex
	@echo "TeX compiling $< -> $*.pdf"
	texi2pdf $<

pdf: *.pdf
