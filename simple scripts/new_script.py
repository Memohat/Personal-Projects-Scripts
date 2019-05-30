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

try:
    python_file = open(f"{name}.py", "x")
    python_file.write('#! python3\n# Mehmet Hatip\n\n')
    python_file.close()
    print(f"File {name}.py successfully created")
    os.startfile(f'{name}.py')
except:
    print(f"Error, {name}.py file already exists")
f"""{name}"""
try:
    os.chdir('ps1files')
    with open(f"{name}.ps1", "x") as bat:
        bat.write(
f"""cd ..
py "{name}.py"
cd ps1files""")
    print(f"File {name}.ps1 successfully created.")
except:
    print(f"Error, {name}.ps1 file already exists")
