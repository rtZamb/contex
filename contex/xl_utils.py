# takes excel data and outputs 'copy n' paste-able' LaTex code

'''
Format:

Header Header Etc.
Data   Data
Data   Data
Etc.   Etc.

Works best
'''


# functions -----------------------------------------------------------------------

####################################################################################

# takes a workbook and turns it into a 2d list (list of lists)
def wb2list(wb, how='col'):
    # WB: a openpyxl workbook 

    # creating a list
    table = []

    if how == 'col':
        # creating a temp row to be iteratively appened to table
        col = []

        # iterating over every row in sheet
        for i in wb.columns:

            # iterating over every element in the row
            for j in i:
                # appending the value of the cell
                col.append(j.value)

            # appending the row to the list
            table.append(col.copy())

            # clearning the columne
            col.clear()

    elif how == 'row':
        # creating a temp row to be iteratively appened to table
        row = []

        # iterating over every row in sheet
        for i in wb.rows:

            # iterating over every element in the row
            for j in i:
                # appending the value of the cell
                row.append(j.value)

            # appending the row to the list
            table.append(row.copy())

            # clearning row
            row.clear()

    # returning the list of lists
    return table

###################################################################################

# function that fills in the table data with the latex commands
def maketable(table, here='', label='', caption='', newrowbar='\hline',
              align='c', col_sep='|', centered=True, tab='\t', dropempty=True,
              **kwargs):

    '''
    Parameters:

    > DATA: 2D table, either list of lists or pandas dataframe
    > HERE:
    > LABEL:
    > CAPTION:
    > NEWROWBAR:
    > ALIGN:
    > COL_SEP:
    > CENTERED:
    > TAB:
    '''

    # droping empty columns
    if dropempty:
        table = drop_empty_cols(table)

    # generating LaTeX command for number of cols
    n_cols_str = '{}{}'.format(align, col_sep) * len(table)

    # putting data into string format based on STRING_LIB dict
    table = num2str_format(table, **kwargs) # turning data into string
        
    # variable to store the number of tabs present
    ntabs = 1

    # starting to format the table -----------------------------
    tex_tab_start = ''

    # adding the begin
    tex_tab_start += '\\begin{{table}}[{}] \n'.format(here)


    # adding centering
    if centered:

        # adding a tab to the subenvironment
        if tab:
            tex_tab_start += tab * ntabs

        # adding the beginning of the centered environment
        tex_tab_start += '\\begin{center} \n'


    # adding a tab to the caption
    if tab:
        tex_tab_start += tab * ntabs
        
        # updating number of tabs
        ntabs += 1

    # adding caption
    tex_tab_start += '\caption{{}} \n'.format(caption)
    

    # creating the beginning of the LaTeX table
    if tab: # adding tab to the tabular environment
        tex_tab_start += tab * ntabs

        # updating number of tabs in environment
        ntabs += 1

    # adding the tabular environment
    tex_tab_start += '\\begin{{tabular}}{{{}{}}} \n'.format(col_sep, n_cols_str)
    
    if tab: # adding tab to the newrowbar
        tex_tab_start += tab * ntabs

    # adding the newrowbar
    tex_tab_start += '{}\n'.format(newrowbar)


    # filling in the table with data --------------------------------
    # creating middle variable
    tex_tab_mid = ''


    # filling in the table
    # adding and formatting data into a string for LaTeX (body of table)
    for i in range(len(table[0])): # iterates over rows

        # adding tab to row
        if tab:
            row = tab * ntabs + table[0][i]
        else:
            row = table[0][i]

        # iterates over columns
        for j in range(1, len(table)):
            row += ' & ' + table[j][i] # adds: & element

        # adds the ending string line to format
        tex_tab_mid += row + ' \\\\ \n'

        # adding tab to the newrowbar
        if tab:
            tex_tab_mid += tab * ntabs

        # adding the  row seperator
        tex_tab_mid += '{} \n'.format(newrowbar)

    # making the tex commands for the end --------------------------
    # creating the end of the LaTeX table

    # creating the variable to store the end of the table
    tex_tab_end = ''

    # making command to end tabular environment
    if tab: # adding tab to the caption
        ntabs -= 1 # updating for the end of the environment
        tex_tab_end += tab * ntabs

    # ending tabular environment
    tex_tab_end += '\end{tabular} \n'

    # adding a tab to the label
    if tab:
        ntabs -= 1 # updating for the end of the environment
        tex_tab_end += tab * ntabs

    # command to label the table
    tex_tab_end += '\label{{tab:{}}} \n'.format(label)

    # command to end center environment
    if centered:

        if tab: # adding tab to the end of center
            tex_tab_end += tab * ntabs

        # ending the center environment
        tex_tab_end += '\end{center} \n'

    # command to end the table environment
    tex_tab_end += '\end{table} \n'

    # returning something that you can copy and paste into you TeX editor
    return tex_tab_start + tex_tab_mid + tex_tab_end




####################################################################################


# function that fills in the table data with the latex commands
def dftable(df, here='', label='', caption='', newrowbar='\hline',
            align='c', col_sep='|', centered=True, tab='\t',
            dropempty=True,dropna='all',**kwargs):

    '''
    Parameters:

    > DATA: 2D table, either list of lists or pandas dataframe
    > HERE:
    > LABEL:
    > CAPTION:
    > NEWROWBAR:
    > ALIGN:
    > COL_SEP:
    > CENTERED:
    > TAB:
    '''

    # droping empty columns
    if dropempty:
        df = df.dropna(how=dropna)

    # getting headers
    headers = list(df.columns)

    # converting them to latex
    if 'formatter' in kwargs:
        # converting all headers to latex
        # commands
        for i in range(len(headers)):
            headers[i] = kwargs['formatter'].to_str(headers[i])
    
    # generating LaTeX command for number of cols
    n_cols_str = '{}{}'.format(align, col_sep) * len(headers)
    
    # putting data into string format based on STRING_LIB dict
    table = num2str_format(df.values.tolist(), **kwargs) # turning data into string
    
    # variable to store the number of tabs present
    ntabs = 1

    # starting to format the table -----------------------------
    tex_tab_start = ''

    # adding the begin
    tex_tab_start += '\\begin{{table}}[{}] \n'.format(here)


    # adding centering
    if centered:

        # adding a tab to the subenvironment
        if tab:
            tex_tab_start += tab * ntabs

        # adding the beginning of the centered environment
        tex_tab_start += '\\begin{center} \n'


    # adding a tab to the caption
    if tab:
        tex_tab_start += tab * ntabs
        
        # updating number of tabs
        ntabs += 1

    # adding caption
    tex_tab_start += '\caption{{}} \n'.format(caption)
    

    # creating the beginning of the LaTeX table
    if tab: # adding tab to the tabular environment
        tex_tab_start += tab * ntabs

        # updating number of tabs in environment
        ntabs += 1

    # adding the tabular environment
    tex_tab_start += '\\begin{{tabular}}{{{}{}}} \n'.format(col_sep, n_cols_str)
    
    if tab: # adding tab to the newrowbar
        tex_tab_start += tab * ntabs

    # adding the newrowbar
    tex_tab_start += '{}\n'.format(newrowbar)


    # filling in the table with data --------------------------------
    # creating middle variable
    tex_tab_mid = ''
    
    # adding tabs
    if tab:
        tex_tab_mid += tab * ntabs

    # adding first element
    tex_tab_mid += headers[0]
    
    # adding headers
    for i in range(1, len(headers)):
        tex_tab_mid += ' & ' + headers[i] 

    # adding line break
    tex_tab_mid += ' \\\\ \n'


    # filling in the table
    # adding and formatting data into a string for LaTeX (body of table)
    for i in range(len(table)): # iterates over rows

        # adding tab to row
        if tab:
            row = tab * ntabs + table[0][i]
        else:
            row = table[0][i]
            
        # iterates over columns
        for j in range(1, len(table[0])):
            row += ' & ' + table[i][j] # adds: & element

        # adds the ending string line to format
        tex_tab_mid += row + ' \\\\ \n'

        # adding tab to the newrowbar
        if tab:
            tex_tab_mid += tab * ntabs

        # adding the  row seperator
        tex_tab_mid += '{} \n'.format(newrowbar)

    # making the tex commands for the end --------------------------
    # creating the end of the LaTeX table

    # creating the variable to store the end of the table
    tex_tab_end = ''

    # making command to end tabular environment
    if tab: # adding tab to the caption
        ntabs -= 1 # updating for the end of the environment
        tex_tab_end += tab * ntabs

    # ending tabular environment
    tex_tab_end += '\end{tabular} \n'

    # adding a tab to the label
    if tab:
        ntabs -= 1 # updating for the end of the environment
        tex_tab_end += tab * ntabs

    # command to label the table
    tex_tab_end += '\label{{tab:{}}} \n'.format(label)

    # command to end center environment
    if centered:

        if tab: # adding tab to the end of center
            tex_tab_end += tab * ntabs

        # ending the center environment
        tex_tab_end += '\end{center} \n'

    # command to end the table environment
    tex_tab_end += '\end{table} \n'

    # returning something that you can copy and paste into you TeX editor
    return tex_tab_start + tex_tab_mid + tex_tab_end




######################################################################################


# changing the organisation of data from columns to rows
def col2row(data):

    # preallocating a list to return
    table = []
    row = []

    # creating a new row from a list
    for i in range(len(data[0])): # iterates over the rows

        # iterates over every column
        for j in range(len(data)):

            # adds the elemnet from each column to the row
            row.append(data[j][i])

        # appending the new row to table
        table.append(row.copy())

        # clearing the temp variable
        row.clear()


    return table


##################################################################################

# takes a list of list and drops columns that contain only
# empty strings
def drop_empty_cols(data):

    # creating list to return
    clean_tab = []

    # iterates over all columns in data
    for i in range(len(data)):

        # iterates over every element in column
        for j in data[i]:

            # checks if the column has any non-empty strings
            if j != '':
                # appendign column of is contains anything
                clean_tab.append(data[i])
                break

    return clean_tab


################################################################################



######################################################################################

# function that takes numerical data and formats a string given a format
def num2str_format(data, formatter=None):
    '''
    Parameters:

    DATA: input data table to be converted to a string
    FORMATTER: a texFormat object. If nothing given, then the default is used
    '''

    # a texFormat object that controls the string formatting
    if not formatter:
        # getting needed import
        from texformat import texfmt
        
        # using default format settings
        formatter = texfmt()

    # iterates over all elements in data
    # iterates of number of rows
    for i in range(len(data[0])):

        # iterates over elements in row (columns)
        for j in range(len(data)):

            # using formatter methods to convert data to string
            data[j][i] = formatter.to_str(data[j][i])
            

    return data



################################################################################
