#! python3
# New script to delete a file based on command line arguements
# asks for file name if none is given in console.

import os, sys

# seeing if name is given in console, if it is no input is needed
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Please enter the file to be deleted: ")

# python scripts path
python_scripts_path = "C:\\Users\\STEM\\Desktop\\Python scripts"

os.chdir(python_scripts_path)

if os.path.exists(f"{name}.py"):
    os.remove(f"{name}.py")
    print(f"\"{name}.py\" successfully deleted")
else:
    print(f"Error, \"{name}.py\" does not exist")

if os.path.exists(f"Batch files\\{name}.bat"):
    os.remove(f"Batch files\\{name}.bat")
    print(f"\"{name}.bat\" successfully deleted")
else:
    print("Error, \"{name}.bat\" does not exist")
