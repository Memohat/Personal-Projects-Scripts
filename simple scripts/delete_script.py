#! python3
# Mehmet Hatip
"""
New script to delete a file based on command line arguements
asks for file name if none is given in console.
"""

import os, sys

def main():

    # seeing if name is given in console, if it is no input is needed
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = input("Please enter the file to be deleted: ")

    if os.path.isfile(name + ".py"):
        os.remove(os.path.join(name + ".py"))
        print(f"File {name}.py successfully deleted")
    else:
        print(f"Error, {name}.py does not exist")

    os.chdir('ps1files')

    if os.path.isfile(name + ".ps1"):
        os.remove(name + ".ps1")
        print(f"File {name}.ps1 successfully deleted")
    else:
        print(f"Error, {name}.ps1 does not exist")

if __name__ == '__main__':
    main()
