# takes images in a directory and
# creates the standard latex commands to include images in a document



'''
> user gives folder or specific images
> all images are loaded and the latex commands are generated
> file types that are not latex compatible have a copy produced in a latex
compatible format

> print out the latex code to render images
'''

import os
from imageio import imread, imwrite


# list of common image formats to parse for
KNOWN_EXT = ['bmp', 'JPG', 'PNG', 'tif','eps','jpg','png']

# prefered file extensions for graphicx
GRAPHICX_EXT = ['pdf','eps']


# checks if any elements  in iterable are equal to check
def any_true(iterable, check):
    for i in iterable:
        if i == check:
            return True
    # if code gets to here then none of the elements in iterable equal check
    return False

def all_true(iterable, check):
    for i in iterable:
        if not i == check:
            return False
    # if you get here then all of the elements are true
    return True

# Proabably not the best way to do this....
# gets the file extension of a given file. must be in string format
def get_file_ext(file):
    # file is a string

    # breaking up by .
    pieces = file.split('.')

    # no file extension found
    if len(pieces) == 1:
        raise RuntimeError('No file extension for {} found'.format(file))

    # returning last element
    return pieces[-1]

# returns a string with the extension removed
def drop_file_ext(file, dot=True):

    if dot:
        return file.split('.')[0] + '.'
    else:
        return file.split('.')[0]

    return

# creates string of file name with given extension
def as_ext(string, ext='eps'):

    # droping old extension
    string = drop_file_ext(string)

    return string + ext


# parses a string to determine if string represents a file with a image file extension
def is_image(image):

    # using regular expressions to extract file extension
    image_ext = get_file_ext(image).lower()
    
    # checking if image_ext is a known_ext
    for i in KNOWN_EXT:
        if i == image_ext:
            return True
        
    # case after iterating over all the file extensions
    return False    

# convert images from one extension to another and save a copy or not
# into the cwd()
def convert_type(image, ext='eps'):

    # does nothing if ext is already the file extension
    if get_file_ext(image.path) is ext:
        return image.path

    # if the eps version exists, don't make it
    # return True
    if os.path.isfile(as_ext(image.path, ext)):
        return True
    
    # loading image
    try:
        img = imread(image.path) # imageio
    except Exception as e:
        print(e)
        print('Could not read {}'.format(image.path))
        print('Skipping Step')
        return  False

    # renaming file
    image_new_name = drop_file_ext(image.path) + ext

    # trying to convert type
    try:
        # saving image to file type
        imwrite(image_new_name, img) # imageio

    except Exception as e:
        print(e)
        print('Could not convert {} to an EPS file'.format(image.path))
        print('Skipping this image')
        return False
        

    # returning image name
    return image_new_name




# checks if images is a JPEG or PNG. if it isn't, then it is a copy of the image
# with the .jpg extension is added to cwd
def graphicx_compatible(image, make=False):
    

    # getting file extension
    image_ext = get_file_ext(image.name)

    # if the image is compatible, then
    # return it.
    if image_ext in GRAPHICX_EXT:
        return image.name

    # if make then changing file type and returning new file name
    if make:
        # coverting type
        return convert_type(image)
        
    # case after iterating over all the file extensions
    return False    



########################################################################################



# getting all files of a single type from a directory
def get_files(ext=KNOWN_EXT, file_dir=None):

    # Checks if file_dir is none. If true file_dir is cwd().
    # elis the current directory is not the file directory. cwd is changed to file_dir
    #getting cwd and changing cwd to the directory where images are
    if not file_dir:
        file_dir = os.getcwd()

    # forcing ext to be a list
    if not isinstance(ext, (list, tuple)):
        ext = [ext]
        
    # loads all files in a directory
    files = []

    # iterating over the contents of the directory
    for i in os.scandir(file_dir):

        # if the object is a file and is of correct
        # file type
        if i.is_file():

            # get file extension
            if get_file_ext(i.name) in ext:

                # adding file to 
                files.append(i)

    # returning files of proper type
    return files


########################################################################################

# update to add arbitary kwargs
# creates a latex figure with a call to graphicx
def mk_img_fig(img='', here='', centered=False,
               label='', caption='', tab='\t', **kwargs):

    # begins the figure environment
    fig = '\\begin{{figure}}[{}] \n'.format(here)

    # records the number of tabs is recorded
    ntabs = 1
    
    # creates centering environment
    if centered:

        # adds the centering environment
        # with correct number of tabs
        if tab:
            fig += tab*ntabs + '\\begin{center} \n'

            # increment number of tabs
            ntabs += 1

        else:
            fig += '\\begin{center} \n'

    
    # this is added to includegraphics
    # as teh list of kwargs that have been formatted
    fmtkwargs = ''
    
    # if there are kwargs, format this string
    if len(kwargs) != 0:
        
        fmtkwargs += '['
        
        # iterates over kwargs and passes them to includegraphics
        for k, v in kwargs.items():
            fmtkwargs += k + '=' + str(v) + ','
            
        # removing last ,
        fmtkwargs = fmtkwargs.rstrip(',')

        # adding the closing bracket
        fmtkwargs += ']'


    
    # adding the image caption and label to the figure
    if tab:
        fig += tab*ntabs + '\includegraphics{}{{{}}} \n'.format(fmtkwargs, img)
        fig += tab*ntabs + '\caption{{{}}} \n'.format(caption)
        fig += tab*ntabs + '\label{{fig:{}}} \n'.format(label)
        
    else:
        fig += '\includegraphics{}{{{}}} \n'.format(fmtkwargs, img)
        fig += '\caption{{{}}} \n'.format(caption)
        fig += '\label{{fig:{}}} \n'.format(label)


    # ending the centered environment
    if centered:
        if tab:
            # decreasing number of tabs
            ntabs -= 1
            # ending environment
            fig += tab*ntabs + '\end{center} \n'
        else:
            fig += '\end{center} \n'


    # ending the figure environment
    fig += '\end{figure} \n'

    return fig











    
            
    

        
