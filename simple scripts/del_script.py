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
python_scripts_path = ".."

os.chdir(python_scripts_path)

batch_path = os.path.join(".", "Batch files")

if os.path.exists(os.path.join(name + ".py")):
    os.remove(os.path.join(name + ".py"))
    print(f"File {name}.py successfully deleted")
else:
    print(f"Error, {name}.py does not exist")

if os.path.exists(os.path.join(batch_path, name + ".bat")):
    os.remove(os.path.join(batch_path, name + ".bat"))
    print(f"File {name}.bat successfully deleted")
else:
    print(f"Error, {name}.bat does not exist")
