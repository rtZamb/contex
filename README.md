# Contex #

This package contains functions to read excel sheets, images, text files, and other python raw datatypes into latex commands. My inspiration came from
getting tired of typing excel tables into latex tables so I automated the procedure (an extra bonus was that I avoided typing a 20x12 excel sheet for an assignment).
I hope this saves you a lot of time!

## Basic Usage ##

### Text Files ###
To convert a file into latex command doesn't save a lot of time but can be useful.
Regardless, this text demo shows the string conversion rules that are the same for every conversion you do!

Here is the contents of a text file to convert
> This is some text. I like symbols \lambda. And div is cool \del. But I want a new line here: \\\newline. Small font is f_o_o_o. of this^i^i^i. Some more complex cases are \lambda \cdot \hbar = E. Or ^o C or X_o.

The python code to convert the file is as follows:
```python
from contex import totex

# reads in the text
file = 'demo/demo.txt'

# create an instance of the converter
converter = totex() # default formatting values

# this converts the text and saves this into a new file
converter.txt(file, 'save_demo.txt')
```

The output is text file is:
> This is some text. I like symbols $\lambda$. And div is cool $\del$. But I want a new line here: \\newline. Small font is f$_o_o_o$. of this$^i^i^i$. Some more complex cases are $\lambda \cdot \hbar =$ E. Or $^o$ C or X$_o$.

As you can see, a single \ tells the parser to put $$ around the mathmatical phrase. but a double \\\ escapes this and returns just a single \ without $$. This allows for typing regular latex and math commands simultaneously. These same rules apply to Excel spreadsheet and string conversions as well!


### Sheets ###
To read from a spreadsheet, the table should look something like this:

|\latex| is | \lambda|
|------|----|--------|
|This is a word   | 1000000  | 0.0000313|
|234.5  | \pi  | A word \del  |
|\\newline |	\this + 2 is 3| |

To convert this into a latex table, the code is:

```python
# an excel spreadsheet
file = 'demo/demo.xlsx'
file1 = './demo/demo.csv'

# gives a list of the formatted latex commands
tables = converter.xl(file) # this reader uses openpyxl
tables1 = converter.csv(file1, delimiter='\t') # this read with built-in csv

# can copy and paste this output into your
# tex editor
print(tables[0])
print tables1
```

You can control the string formatting by passing kwargs to `totex()` when you first initalize it. Those kwargs are the string formatters as described [here](https://docs.python.org/3/library/string.html).

There is another option for reading spreadsheets, which would be to use pandas to read the spreadsheet.
The method is `totex.xldf()`. This produces almost identical results as
the example above but uses `pandas.read_excel()` to read the spreadsheet. Pandas defaults to 64-bit representation of strings so this is not preferred for long strings.


The output is:
```latex
\begin{table}[]
	\begin{center}
	\caption{}
		\begin{tabular}{|c|c|c|}
			\hline
			$\latex$ & is & $\lambda$ \\
			\hline
			This is a word & 1.00e6 & 3.13e-5 \\
			\hline
			234.50 & $\pi$ & A word $\del$ \\
			\hline
			$\\newline$ & $\this + 2$ is 3 &  \\
			\hline
		\end{tabular}
	\label{tab:}
	\end{center}
\end{table}
```

### Images ###
This tool is still in the works but behaves as follows:
```python
# Either the paths to specific files are needed or
# the path to a directory
directory = 'demo/'

# this converts images to .eps type
# which is preferred by the latex package, graphicx
# It works best for jpg files, png files seem to fail
image_cmd = converter.img(directory)

# printing the first image
print(images_cmd[0])
```

The output is:
```latex
\begin{figure}[]
	\begin{center}
		\includegraphics{demo.eps}
		\caption{}
		\label{fig:}
	\end{center}
\end{figure}
```


### Generic Conversions ###

To convert raw python data types use the method `totex.raw()` and pass your raw data type. This will format is according to the formatting rules set
when the `totex()` instance was created.



## Project Details ##


### Goals ###
* Convert more file types to tex commands
* More style controls
* Ask for features!


### Dependencies ###
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/) or pandas for reading spreadsheets
* [imageio](https://github.com/imageio/imageio) for converting image types

### Optional Dependencies ###
* [pandas](https://pandas.pydata.org/) to convert DataFrames and read Excel from them.
