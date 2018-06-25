'''
TODO:

> Detect and convert pure numbers that are already strings
    and then format those
'''

# single needed import
# for scientific notation
# formatting
from math import floor, isnan, log10


# A class to store the numerical and table formatting for conversion
class texfmt:

    def __init__(self, ints='{:0.0f}', int_sci='{:0.0e}', floats='{:0.2f}', sci='{:0.2e}',
                 nan='', zero='0', none='', int2sci=1e4,float2sci=(1e-2, 1e4),
                 special_sci=True, decimals=2):
        '''
        Parameters:

        The kwargs that are of data types/values are the string formatters for
        when that data type/value is given.

        > INT2SCI: the cutoff value for when an integer should be converted
            to scientific notation.
        > FLOAT2SCI: the lower and upper bounds for when a float should be converted to
            scientific notation.
        > SPECIAL_SCI: determines if a non-python format for scientifi numbers is to be used
            See method "sci_formatter" for more details
        > DECIMALS: the number of decimals to show for the SPECIAL_SCI formatting
        '''


        # string formats to convert numbers to string
        self.num2str = {'int':ints,
                        'int_sci':int_sci,
                        'float':floats,
                        'sci':sci,
                        'nan':nan,
                        'zero':zero,
                        'none':none}

        # parameters that control when a int or float is converted to scientific notation
        self.int2sci = int2sci # controls int to scientific notation
        self.float2sci = float2sci # controls float to scientific notation

        # a dictionary of special characters and their raw forms
        self.special = {'\newline': r'\newline', '\\':r'\\', '\'': r'\'', '\"': r'\"',
                        '\a':r'\a','\b':r'\b','\f':r'\f', '\n':r'\n','\r':r'\r',
                        '\t':r'\t','\v':r'\v', '\ooo': r'\ooo'}

        # stores math related characters
        self.mathrelated = ['+', '*', '/', '-', '=', '<', '>', '{','}']

        # stores punctuation marks
        self.punc = ['.','?', '!']

        # storing decision to use standard or special scientific notation
        self.special_sci = special_sci
        self.special_dec = int(decimals)

        return


    # -----------------------------------------------------------------------------------
    # method to convert a raw data type to latex formatted string
    def to_str(self, data):
        # iterates over data, which is assumed to be either 1D or a single value,
        # and coverts it to a string based on the num2str attribute

        # checking if data is a list-like thing
        if isinstance(data, list):
            # creating an array
            to_return = []

            # iterating over all
            # elements in data
            # and recursively calling this function
            for i in data:
                to_return.append(self.to_str(i))

            return to_return

        # ---------------------------------------------------
        

        # getting type
        data_type = type(data)

        # case for none type
        if data_type == type(None):
            return self.num2str['none'].format(data)

        # Checking for strings
        elif isinstance(data, str):
            return self.str2tex(data)
        
        # checking for nan
        elif isnan(data):
            return self.num2str['nan']

        # case where input data is an integer
        elif isinstance(data,int) or data % 1.0 == 0 and data != 0:

            # determines if integer is too large and requires scientific notation
            if abs(data) > self.int2sci:

                # using special scientific notation
                if self.special_sci:
                    return self.sci_formatter(data, self.special_dec)

                # returning standard format scientific notation
                return self.num2str['int_sci'].format(data)

            else:
                # returning the integer representation
                return self.num2str['int'].format(data)

        # checking for zeros
        elif data == 0:
            return self.num2str['zero'] 

        # formatting floats
        elif isinstance(data, float):
            # determining which format is best
            if abs(data) < self.float2sci[0] or abs(data) > self.float2sci[1]:

                # using special scientific notation
                if self.special_sci:
                    return self.sci_formatter(data, self.special_dec)

                # using standard scientific notation
                return self.num2str['sci'].format(data)

            else:
                # returning simple representation of number
                return self.num2str['float'].format(data)

        else:
            raise TypeError('Unrecognized type {}'.format(data_type))

        # end of to_tex
        return


    # ---------------------------------------------------------------------------------

    # method to parse strings for latex commands
    def str2tex(self, line):
        # adds $$ signs to latex commands and converts special characters
        # into their raw form
        # line is used to refer to a line in excel 

        # removing special escape chars with their raw counterparts
        line = self.remove_special_chars(line)

        # Now that all strings are in raw format (no weird escape characters)
        # We add the $ signs where needed.

        # getting individual words from line
        words = line.split()

        # records if there is an open money sign or not
        open_money = False

        # iterating over the words in the line
        for i in range(len(words)):

            # checks if word is latex command or is a number or is a math character
            # if it is, then no closing $ sign is added and a new one is opened if
            # open_money if false

            # checking if word contains '\\\\' (really just \\) to escape latex formatting
            if '\\\\' == words[i][0:2]:
                words[i] = words[i][1:] # just removes a backslash but does not have $
                continue # escaping latex formatting
            
            # checking if word contains latex commands
            if '\\' == words[i][0] or words[i] in self.mathrelated:
                
                # if there is no open $, create a new one
                if not open_money:
                    words[i] = '$' + words[i]

                    # records there is an open money sign
                    open_money = True

                # if there is an open_money, then don't do anything and just go to next iteration
                continue
            
            # if something is a pure number
            elif self.isnumber(words[i]):

                # formatting the string in the correct number format
                words[i] =  self.num_as_str_fmt(words[i])

                # next iteration
                continue 
            
            # parsing for underscores in words
            elif '_' in words[i]:

                # breaking up into bits
                pieces = words[i].split('_')

                # iterating over all pieces to make
                # to account for escaping the _
                for j in range(1, len(pieces)):

                    # if there is an underscore escape
                    if pieces[j-1] != '' and pieces[j-1][-1] == '\\' and not pieces[j-1] in '\\\\':
                        continue # escaped, nothing to add
                    elif pieces[j-1] != '' and pieces[j-1][-1] == '\\' and pieces[j-1] in '\\\\':
                        continue # escaped, nothing to add

                    else: # no escape character
                        if not open_money:
                            # replace only the first occurance
                            pieces[j-1] += '$'

                            # recording open money
                            open_money = True

                # joining the parsed pieces together 
                words[i] = '_'.join(pieces)

                continue

            # superscript case
            elif '^' in words[i]:
                # breaking up into bits
                pieces = words[i].split('^')

                # iterating over all pieces to make
                # to account for escaping the _
                for j in range(1, len(pieces)):

                    # if there is an underscore escape
                    if pieces[j-1] != '' and pieces[j-1][-1] == '\\' and not pieces[j-1] in '\\\\':
                        continue # escaped, nothing to add
                    elif pieces[j-1] != '' and pieces[j-1][-1] == '\\' and pieces[j-1] in '\\\\':
                        continue # escaped, nothing to add

                    else:
                        
                        if not open_money:
                            # replace only the first occurance
                            pieces[j-1] += '$'

                            # recording open money
                            open_money = True

                # joining the parsed pieces together 
                words[i] = '^'.join(pieces)

                continue

            
            # Case where there is a plain word so the previous word needs a $ at the end
            else:

                # if there is no open $ then move to next word
                if not open_money:
                    continue

                # there is an open $ so close it on the previous word
                else:

                    # make sure to put the money before the punctuation
                    if words[i-1][-1] in self.punc:

                        # counter variable
                        idx = 0
                        # iterating over word backwards to ignore
                        # several punctuation marks
                        for j in range(len(words[i-1])-1, -1, -1):
                            if words[i-1][j] in self.punc:
                                continue
                            else:
                                # storing index of first punctuation mark at end of string
                                idx = j + 1
                                break

                        # putting money before punctuation
                        words[i-1] = words[i-1][0:idx] + '$' + words[i-1][idx:] 

                    # no punctuation so we just add a $ 
                    else:
                        words[i-1] = words[i-1] + '$'

                    # records there there is no open money sign
                    open_money = False

                    continue
                
        # -----------------------------------------------------
        # checking the last word to make sure that the $ is closed
        if open_money:

            # make sure to put the money before the punctuation
            if words[-1][-1] in self.punc:

                # counter variable
                idx = 0
                # iterating over word backwards to ignore
                # several punctuation marks
                for j in range(len(words[-1])-1, -1, -1):
                    if words[-1][j] in self.punc:
                        continue
                    else:
                        # storing index of first punctuation mark at end of string
                        idx = j + 1
                        break

                # putting money before punctuation
                words[-1] = words[-1][0:idx] + '$' + words[-1][idx:] 

            # no punctuation so we just add a $ 
            else:
                words[-1] = words[-1] + '$'

            # recording just for consistancy
            open_money = False


        # Joining formatted words and returning
        return ' '.join(words)


    # ---------------------------------------------------------------------------------

    # method to tell if a string is a number
    def isnumber(self, num):
        # NUM is a string.

        #print(num)

        # simple testing
        if num.isnumeric():
            return True

        # testing each char individually
        for i in num:

            # if the char is a number continue
            if i.isnumeric():
                continue

            # testing non-numeric digits that are apart of numbers
            elif i == '.' or i == '-' or i == 'e' or i == '+':
                continue
            else:
                return False

        # if no errors are found then return true
        return True

    # method to convert strings of number to their
    # formatted appearance
    def num_as_str_fmt(self, num_as_str):

        # try to make an int,
        # if that failes, make a foat and format it
        num = num_as_str.split('e')

        # only numerical values,
        # not scientific notation
        if len(num) == 1:
            try:
                num_as_num = int(num_as_str)
                
            except Exception as e:
                num_as_num = float(num_as_str)

            # formatting the converted number properly
            return self.to_str(num_as_num)

        # scientific notation case
        elif len(num) == 2:

            # getting digets
            mantissa = float(num[0])
            
            # getting power
            power = num[1]

            # decimal case
            if power[0] == '-':
                sign = '-'

                power = power.lstrip('-')

            # removing positive sign
            elif power[0] == '+':
                power = power.lstrip('+')

            # remove any beginning zeros
            power = power.lstrip('0')

            # converting string to int
            power = float(power)

            # if exponent signis negative
            # mutiply power by negative 1
            if sign == '-':
                power *= -1

            # creating actual number
            num_as_num = mantissa * 10 ** power

        return self.to_str(num_as_num)


    # -------------------------------------------------------------------------------

    # method to remove special (escape) characters in a string
    def remove_special_chars(self, line):

        # iterating over all special characters
        # see https://docs.python.org/3/reference/lexical_analysis.html
        # for string literal special characters

        for i in self.special:  # iterates over the keys

            # get index of the first time the special char appears
            idx = line.find(i)

            # if idx is -1 then there are no instances
            if idx == -1:
                continue

            # replacing special characters with their raw values
            line.replace(line[idx], self.special[i])

        return line

    
    # -------------------------------------------------------------------------------

    # a function to properly format in scientific notation
    def sci_formatter(self, x, decimals=2):
        '''
        Creates numbers formatted in non-python scientific notation

        For Example:

        IDLE output
        >>> a = 12345.098765
        >>> '{:0.2e}'.format(a)
        '1.23e+04'

        But I Much rather prefer
        '1.23e4'
        or '1.23e-4' for decimals
        
        It looks cleaner, So I wrote this formatter
        to do this for a given number
        
        '''
        
        # 
        # getting the decimal values
        mantisa = '{{:0.{}f}}'.format(decimals)

        # getting the power of the number
        power = log10(abs(x))

        # dropping to minimum poewr
        power = floor(power) # import from math
        
        # returning formatted string
        return mantisa.format(x/10**power) + 'e{}'.format(power)

    # -------------------------------------------------------------------------------


    # allows for [string] indexing.
    # returnes the string format for the index from the num2str dictionary
    def __getitem__(self, index):

        # checking over every dictionary
        if index in self.num2str: # number to string formatter dictionary
            return self.num2str[index]

        elif index in self.special: # special escaped charater dictionary
            return self.special[index]

        else:
            raise KeyError('key, {}, Not found any attribute dictionaries'.format(index))
