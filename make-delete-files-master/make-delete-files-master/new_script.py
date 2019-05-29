#! python3
# New script to make a file based on command line arguements
# asks for file name if none is given in console.
# makes python script with the name, also makes batch file for it.

import os, sys

# seeing if name is given in console, if it is no input is needed
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Please enter the new file name: ")

# put the folder name of where the scripts are going to be put
python_scripts_path = "C:\\Users\\STEM\\Desktop\\Python scripts"

#folder name of batch files
batch_path = "C:\\Users\\STEM\\Desktop\\Python scripts\\Batch files"

os.chdir(python_scripts_path)

try:
    python_file = open(f"{name}.py", "x")
    python_file.write("#! python3")
    python_file.close()
    os.chdir(batch_path)
    with open(f"{name}.bat", "x") as bat:
        bat.write(f'@py.exe "{python_scripts_path}\{name}.py" %*')
    print(f"Files \"{name}.py\" and \"{name}.bat\" have been successfully created.")
except:
    print("Error, file may already exist")
