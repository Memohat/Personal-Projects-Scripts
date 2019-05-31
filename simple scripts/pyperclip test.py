#! python3
# Mehmet Hatip

import pyperclip

def main():
    pasted = pyperclip.paste()
    print(f"Clipboard: {pasted}")

    word = "hello!"
    copied = pyperclip.copy(word)
    print(f"Clipboard now contains {word}")

if __name__ == '__main__':
    main()
