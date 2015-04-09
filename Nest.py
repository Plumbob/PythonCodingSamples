

def findChIndex(c, str_in):
    """
    Version 1: Manually, as an exercise.
    
    Write a python function that returns the first index of a character 'c' in string
    'str_in'.
    
    If the character was not found it returns -1.

    Ex:
        findChIndex('a', 'dddabbb') will return 3

        findChIndex('f', 'ddddabbb') will return -1

    """
    found_index = -1
    
    for indx, char in enumerate(str_in):
        if char == c:
            found_index = indx

    return found_index


def findChIndex(c, str_in):
    """
    Version 2: Using built-in methods.
    
    Write a python function that returns the first index of a character 'c' in string
    'str_in'.
    
    If the character was not found it returns -1.

    Ex:
        findChIndex('a', 'dddabbb') will return 3

        findChIndex('f', 'ddddabbb') will return -1

    """
    return_val = str_in.find(c)

    return return_val


class Reporter():
    """
    Receive a file name, open it for write and provide a method to write a string to the file.
    Close the file when needed.

    Will overwrite the file if already exist.

    Usage example:
    
        with Reporter("MyLogFile.log") as myReporter:
        
        myReporter.writeStr("My 1st log in my reporter\n")
        
        myReporter.writeStr("My 2nd log in my reporter\n")

    """

    def __init__(self, filename):
        """
        Initialize a Reporter class.

        """
        self.filename = filename

        self.file_obj = None

        
    def __enter__(self):
        """
        Open the output file for writing and create a Reporter class context.

        """
        self.file_obj = open(self.filename, 'w')
        
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the output file and the Reporter context.

        Let any raised exceptions propogate up unchanged.

        """
        self.file_obj.close()
        

    def writeStr(self, str_to_write):
        """
        Write 'str_to_write' to the output file.

        """
        self.file_obj.write(str_to_write)


 
def splitMyString(c, str_in):
    """
    Version 1: Manually as an exercise.
    
    Returns a list of strings separated by character 'c' where 'c' is the
    "splitter" character and 'str_in' is the string.

    Example Usage:

    splitMyString('*', 'aaa*sss*fff') returns: ['aaa', 'sss', 'fff']

    splitMyString('a', 'abbacfa') will returns: ['', 'bb', 'cf, '']

    """
    return_list = []

    sub_str = ""

    for char in str_in:
        if char == c:
            return_list.append(sub_str)
            sub_str = ""
        else:
            sub_str += char

    return_list.append(sub_str)

    return return_list

        
def splitMyString(c, str_in):
    """
    Version 2: Using built-in methods
    
    Returns a list of strings separated by character 'c' where 'c' is the
    "splitter" character and 'str_in' is the string.

    Example Usage:

    splitMyString('*', 'aaa*sss*fff') returns: ['aaa', 'sss', 'fff']

    splitMyString('a', 'abbacfa') will returns: ['', 'bb', 'cf, '']

    """
    return_val = str_in.split(c)

    return return_val
