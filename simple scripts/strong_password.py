#! python3
# Mehmet Hatip

import re

def find_regex(regex, text, error, valid):
    NewRegex = re.compile(regex)
    if NewRegex.search(text) == None:
        print(error)
        valid = False
    return valid

def main():
    while True:
        valid = True
        text = input("Password: ")
        """
        valid = find_regex(r".{8,}", text, "Password is too short", valid)
        valid = find_regex(r".*[a-z].*", text, "Lowercase letter is missing", valid)
        valid = find_regex(r".*[A-Z].*", text, "Uppercase letter is missing", valid)
        valid = find_regex(r".*[0-9].*", text, "Number is missing", valid)
        """
        valid = find_regex(r"^(?=\D*\d)(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z]).{8,}$", text, "Invalid", valid)
        if valid:
            if not input("Password is accepted\nenter to exit"):
                break

if __name__ == '__main__':
    main()
