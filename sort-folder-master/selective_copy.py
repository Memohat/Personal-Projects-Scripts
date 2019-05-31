#! python3
# Mehmet Hatip

import shutil, os, re

def main():
    extensionRegex = re.compile(r"\.\w+$")

    for folder, subfolders, files in os.walk(os.path.join(os.getcwd(), 'data')):
        for file in files:
            mo = extensionRegex.search(file)
            if mo:
                ext = mo.group()
                if os.path.isdir(ext):
                    file = os.path.join(folder, file)
                    shutil.copy(file, ext)
                    print(f"Copying from {file} to {ext}")
                else:
                    os.mkdir(ext)

if __name__ == '__main__':
    main()
