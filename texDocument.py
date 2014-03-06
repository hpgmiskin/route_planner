#LaTeX Writing

from string import Template

class TexDocument():
	"Class to write LaTeX documents"

	def __init__(self,filename):

		self.filename = filename
		self.document = ""

	def updateTex(self,content):
		"method to update the Tex Document with the given content"

		self.document += content

		with open(filename,'w') as openFile:
			openFile.write(self.document)

	def section(self,name):
		"method to add a section heading to the Tex Document"

		label = name.replace(" ","_").lower()

		template = Template(r"""
			\subsection{$name}
			\label{$label}
			""")

		template.substitute(name=name,label=label)

	def figure(self,name,src,caption):
		"method to add a figure to the Tex Document"

		content = r"""
			\begin{figure}[H]
			\centering
			\includegraphics[width=0.4\textwidth]{Figures/tangent_binormal_normal.png} 
			\caption{Tangent, Binormal and Normal Vectors}
			\label{fig:tangent_binormal_normal}
			\end{figure}
			"""

		print(content)

		self.updateTex(content)