#LaTeX Writing
import os,re,subprocess
from string import Template

#use to change between listings and minted code packages
MINTED = True

class TexDocument(object):
	"Class to write LaTeX documents"

	def __init__(self,filename):

		self.filename = filename
		self.document = ""
		self.wordCount = 0
		self.abreviations = {}
		self.nomeclature = {}
		self.labels = []
		self.header()

	def updateTex(self,content=None):
		"method to update the Tex Document with the given content"

		if content:
			content = re.subn(r"([^\\])%",r"\1\%",content)[0]
			self.document += content

		fileContent = Template(r"""
$document
\end{document}
""")

		fileContent = fileContent.substitute(document=self.document)

		with open(self.filename,'w') as openFile:
			openFile.write(fileContent)


	def header(self):
		"method to add the required header to a latex file"

		#\renewcommand{\rmdefault}{phv}
		#\renewcommand{\sfdefault}{phv}

		if MINTED:
			self.package = "minted"
		else:
			self.package = "listings"

		content = Template(r"""\documentclass[a4paper,12pt,twoside]{article}
\usepackage[a4paper,top=20mm,bottom=20mm,inner=38mm,outer=19mm]{geometry}
\usepackage{graphicx}
\usepackage{float}
\usepackage{url}
\usepackage{subfigure}
\usepackage[noadjust]{cite}
\usepackage{amssymb}
\usepackage{parskip}
\usepackage{setspace}
\usepackage{$package}
\usepackage{etoolbox}
\patchcmd{\thebibliography}{\section*}{\section}{}{}
\bibliographystyle{apalike} 

\begin{document}
\onehalfspacing
""")

		content = content.substitute(package=self.package)
		self.updateTex(content)

	def title(self,title,subtitle,abstract,other="",name="Henry Miskin"):
		"method to add a title page"

		titlePage = Template(r"""
\begin{titlepage}
\clearpage
\vspace*{\fill}
\begin{center}
\begin{minipage}{.6\textwidth}
\centerline{\textbf{\huge $title}}
\centerline{\textbf{\large $subtitle}}
\centerline{\textit{$name}}
\centerline{\textit{\today}}
\end{minipage}
\end{center}
\vspace{2em}
\centering
\vfill
\textbf{\large Abstract}
\\
$abstract
\vfill
$other
\clearpage
\end{titlepage}""")

		titlePage = titlePage.substitute(title=title,subtitle=subtitle,name=name,abstract=abstract,other=other)
		self.updateTex(titlePage)

	def contents(self,figures=False,tables=False):
		"method to add the contents page"

		content = Template(r"""
\tableofcontents
\vfill
\begin{center}
Word Count: WORD-COUNT-HERE
\end{center}
\vfill
\clearpage
$figures
$tables
\section*{Abreviations}
ABREVIATIONS-HERE
\section*{Nomeclature}
NOMECLATURE-HERE
\clearpage""")

		if figures:
			figures = r"\listoffigures \clearpage"
		else:
			figures = ""

		if tables:
			tables = r"\listoftables \clearpage"
		else:
			tables = ""

		content = content.substitute(tables=tables,figures=figures)
		self.updateTex(content)

	def section(self,name,sectionType=""):
		"method to add a section heading to the Tex Document"

		self.wordCount += len(name.split())
		label = self.formatLabel(name)

		if (sectionType == "*"):
			sectionType = "section*"
		elif ("sub" in sectionType):
			sectionType = "{}section".format(sectionType)
		else:
			sectionType = "section"

		section = Template(r"""
\$sectionType{$name}
\label{sec:$label}
""")

		section = section.substitute(sectionType=sectionType,name=name,label=label)
		self.updateTex(section)

		sectionRef = Template(r"\ref{sec:$label}")
		sectionRef = sectionRef.substitute(label=label)


		return sectionRef

	def code(self,filename,name=None,description=""):
		"adds code to the LaTeX document"

		if self.package == "minted":
			command = "inputminted[tabsize=2,fontsize=\scriptsize]{python}"
		else:
			command = "lstinputlisting[tabsize=2]"

		code = Template(r"""
\subsection*{$name}
$description
\vspace{1em}
\$command{../$filename}
\vspace{2em}
""")

		if not name:
			name = filename.split(".")[0]

		code = code.substitute(filename=filename,name=name,command=command,description=description)
		self.updateTex(code)

	def paragraph(self,text):
		"method to add a paragraph of text provided"

		self.wordCount += len(text.split())

		paragraph = Template("""
$text
""")

		paragraph = paragraph.substitute(text=text)
		self.updateTex(paragraph)

	def figure(self,filename,caption="",width=0.6,position=""):
		"method to add a figure to the Tex Document"

		label = filename.split("/")[1].split(".")[0]
		label = self.formatLabel(label)

		self.wordCount += len(caption.split())

		figure = Template(r"""
\begin{figure}$position
\centering
\includegraphics[width=$width\textwidth]{$filename} 
\caption{$caption}
\label{fig:$label}
\end{figure}
""")

		figure = figure.substitute(position=position,width=width,filename=filename,caption=caption,label=label)
		self.updateTex(figure)

		figureRef = Template(r"\ref{fig:$label}")
		figureRef = figureRef.substitute(label=label)

		return figureRef

	def figures(self,filenames,caption="",captions=None):
		"method to add a 4x4 figure to the LaTeX document"

		self.wordCount += len(caption.split())

		figuresContent = Template(r"""
\begin{figure}
	\centering
	$subFigures
	\caption{$caption}
	\label{fig:$label}
\end{figure}
""")

		subFigure = Template(r"""
	\subfigure[$caption]{
		\includegraphics[width=$width\textwidth]{$filename} 
		\label{fig:$label}
	}""")

		if not (len(filenames)%2):
			width = 0.44
		elif not (len(filenames)%3):
			width = 0.3
		else:
			width = 0.8

		subFigures = ""
		figureRefs = []

		if (captions == None):
			captions = [""]*len(filenames)

		for i,filename in enumerate(filenames):
			self.wordCount += len(captions[i].split())
			label = self.formatLabel(captions[i])
			subFigures += subFigure.substitute(caption=captions[i],filename=filename,label=label,width=width)
			figureRefs.append(Template(r"\ref{fig:$label}").substitute(label=label))

		label = self.formatLabel(caption)
		figuresContent = figuresContent.substitute(subFigures=subFigures,label=label,caption=caption)
		self.updateTex(figuresContent)

		figureRef= Template(r"\ref{fig:$label}").substitute(label=label)
		return figureRef,figureRefs


	def table(self,name,table,centering="l"):
		"method to add a table to the LaTeX document"

		label = self.formatLabel(name)

		tableBody = Template(r"""
\begin{table}[width=\textwidth]
\centering
$tabular
\caption{$caption}
\label{tbl:$label}
\end{table}
""")

		tabular = self.tabular(table,centering)
		tableBody = tableBody.substitute(tabular=tabular,caption=name,label=label)
		self.updateTex(tableBody)

		tableRef = Template(r"\ref{tbl:$label}")
		tableRef = tableRef.substitute(label=label)

		return tableRef

	def tabular(self,table,centering="l"):
		"method to add a tabular section to the report"

		centering = centering*len(table[0])

		tabularBody = Template(r"""
    \begin{tabular}{$centering}
    $lines
    \end{tabular}""")

		lines = ""

		for row in table:
			rowLength = len(row)
			for count,item in enumerate(row):
				if type(item)==str: self.wordCount += len(item.split())
				if (count != rowLength-1):
					lines += Template(r"$item	& ").substitute(item=item)
				else:
					lines += Template(r"""$item	\\
""").substitute(item=item)

		tabularBody = tabularBody.substitute(centering=centering,lines=lines)
		return tabularBody

	def equation(self,name,equation):
		"method to add an equation to the LaTeX document"

		label = self.formatLabel(name)

		equationContent = Template(r"""
\begin{equation}
\label{eq:$label}
$equation
\end{equation}
""")

		equationContent = equationContent.substitute(label=label,equation=equation)
		self.updateTex(equationContent)

		equationRef = Template(r"\ref{eq:$label}")
		equationRef = equationRef.substitute(label=label)

		return equationRef

	def list(self,items,listType="itemize"):
		"method to add a list to the Latex document"

		self.wordCount += sum([len(item.split()) for item in items])

		listContent = Template(r"""
\begin{$listType}
\setlength{\itemsep}{-12pt}
$listItems
\end{$listType}
""")

		listItems = ""

		for item in items:
			listItems += Template(r"""\item $item
""").substitute(item=item)

		listContent = listContent.substitute(listType=listType,listItems=listItems)
		self.updateTex(listContent)

	def bibliography(self):
		"method to insert a bibliography into the tex document"

		content = r"""\newpage
\bibliographystyle{unsrt}
\bibliography{references}
\newpage"""

		self.updateTex(content)

	def addAbreviations(self):
		"method to add abreviations to the document"

		items = sorted(self.abreviations.items(), key=lambda x:x[0])
		table = [[r"{}".format(name),"{}".format(value)] for name,value in items]
		table.insert(0,["Abreviation","Name"])
		abreviations = self.tabular(table)

		self.document = self.document.replace("ABREVIATIONS-HERE",abreviations)
		self.updateTex()

	def addNomeclature(self):
		"method to add nomeclature to the document"

		items = sorted(self.nomeclature.items(), key=lambda x:x[0])
		table = [[r"${}$".format(name),"{}".format(value[0]),r"${}$".format(value[1])] for name,value in items]
		table.insert(0,["Symbol","Name","Unit"])
		nomeclature = self.tabular(table)

		self.document = self.document.replace("NOMECLATURE-HERE",nomeclature)
		self.updateTex()

	def addWordCount(self,wordCount=None):
		"method to count the number of words in the document and add it to title page"

		if not wordCount:
			wordCount = self.wordCount

		self.document = self.document.replace("WORD-COUNT-HERE",str(wordCount))
		self.updateTex()

	def formatLabel(self,label):
		"function to format label and if there is the same label from before add _1"

		label = label.replace(" ","_").lower()
		label = re.subn(r"[^\w\d_]","",label)[0]
		label = label.replace("__","_")
		newLabel = label

		i=0
		while True:
			if newLabel in self.labels:
				newLabel = "{}_{}".format(label,i)
				i += 1
			else:
				break

		self.labels.append(newLabel)

		return newLabel

	def compile(self,show=False):
		"method to compile the report and open the pdf if show == true"

		# self.addAbreviations()
		# self.addNomeclature()
		#self.addWordCount()

		print("----------------------------------------------")

		cwd = os.getcwd()
		reportPath = os.path.join(cwd,self.filename)
		reportName = os.path.basename(reportPath).split(".")[0]
		reportDirectory = os.path.dirname(reportPath)
		#print(reportName,reportDirectory)
		os.chdir(reportDirectory)

		# try:
		# 	os.unlink("{}.pdf".format(reportName))
		# except IOError:
		# 	None

		print("Writing LaTeX Document")

		FNULL = open(os.devnull, 'w')
		subprocess.call("pdflatex -shell-escape {}.tex".format(reportName),
			stdout=FNULL)

		subprocess.call("bibtex {}".format(reportName),
			stdout=FNULL)

		subprocess.call("pdflatex -shell-escape {}.tex".format(reportName),
			stdout=FNULL)

		subprocess.call("pdflatex -shell-escape {}.tex".format(reportName),
			stdout=FNULL)

		for extension in ["log","aux","toc","bbl","blg","pyg"]:
			try:
				os.unlink("{}.{}".format(reportName,extension))
			except:
				None

		if show:
			os.system("start {}.pdf".format(reportName))
		os.chdir(cwd)
