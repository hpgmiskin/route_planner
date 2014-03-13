#LaTeX Writing
import re
from string import Template

class TexDocument():
	"Class to write LaTeX documents"

	def __init__(self,filename):

		self.filename = filename
		self.document = ""
		self.header()


	def updateTex(self,content):
		"method to update the Tex Document with the given content"

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

		content = r"""\documentclass[a4paper,12pt,twoside]{article}
\usepackage[a4paper,top=20mm,bottom=20mm,inner=38mm,outer=19mm]{geometry}
\usepackage{graphicx}
\usepackage{float}
\usepackage{url}
\usepackage{listings}
\usepackage{subfigure}
\usepackage[noadjust]{cite}
\usepackage{amssymb}
\usepackage{parskip}
\usepackage{setspace}
\bibliographystyle{apalike} 
\begin{document}
\onehalfspacing
"""
		self.updateTex(content)

	def titlePage(self,title,subtitle,abstract,name="Henry Miskin",table=""):
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
\vspace{5cm}
\center
\textbf{Abstract}
\center
$abstract
\vfill
$table
\clearpage
\end{titlepage}
\tableofcontents
\clearpage
""")

		titlePage = titlePage.substitute(title=title,subtitle=subtitle,name=name,abstract=abstract,table=table)
		self.updateTex(titlePage)

	def section(self,name,sectionType=""):
		"method to add a section heading to the Tex Document"

		sectionType = "{}section".format(sectionType)
		label = name.replace(" ","_").lower()

		section = Template(r"""
\$sectionType{$name}
\label{sec:$label}
""")

		section = section.substitute(sectionType=sectionType,name=name,label=label)
		self.updateTex(section)

		sectionRef = Template(r"\ref{sec:$label}")
		sectionRef = sectionRef.substitute(label=label)

		return sectionRef

	def paragraph(self,text):
		"method to add a paragraph of text provided"

		paragraph = Template("""
$text
""")

		paragraph = paragraph.substitute(text=text)
		self.updateTex(paragraph)

	def figure(self,filename,caption=""):
		"method to add a figure to the Tex Document"

		label = filename.split("/")[1].split(".")[0]

		figure = Template(r"""
\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{$filename} 
\caption{$caption}
\label{fig:$label}
\end{figure}
""")

		figure = figure.substitute(filename=filename,caption=caption,label=label)
		self.updateTex(figure)

		figureRef = Template(r"\ref{fig:$label}")
		figureRef = figureRef.substitute(label=label)

		return figureRef

	def figures(self,filenames,caption="",captions=None):
		"method to add a 4x4 figure to the LaTeX document"

		figuresContent = Template(r"""
\begin{figure}[H]
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
			label = captions[i].replace(" ","_").lower()
			subFigures += subFigure.substitute(caption=captions[i],filename=filename,label=label,width=width)
			figureRefs.append(Template(r"\ref{fig:$label}").substitute(label=label))

		label = caption.replace(" ","_").lower()
		figuresContent = figuresContent.substitute(subFigures=subFigures,label=label,caption=caption)
		self.updateTex(figuresContent)

		figureRef= Template(r"\ref{fig:$label}").substitute(label=label)
		return figureRef,figureRefs


	def table(self,name,table,centering="c"):
		"method to add a table to the LaTeX document"

		label = name.replace(" ","_").lower()
		centering = centering*len(table[0])

		tableBody = Template(r"""
\begin{table}[width=\textwidth]
\centering
    \begin{tabular}{$centering}
    $lines
    \end{tabular}
\caption{$caption}
\label{tbl:$label}
\end{table}
""")

		lines = ""

		for row in table:
			rowLength = len(row)
			for count,item in enumerate(row):
				if (count != rowLength-1):
					lines += Template(r"$item	& ").substitute(item=item)
				else:
					lines += Template(r"""$item	\\
""").substitute(item=item)

		tableBody = tableBody.substitute(caption=name,label=label,centering=centering,lines=lines)
		self.updateTex(tableBody)

		tableRef = Template(r"\ref{tbl:$label}")
		tableRef = tableRef.substitute(label=label)

		return tableRef


	def equation(self,name,equation):
		"method to add an equation to the LaTeX document"

		label = name.replace(" ","_").lower()

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