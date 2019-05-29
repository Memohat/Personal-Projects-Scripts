import pyperclip

pasted = pyperclip.paste()
print(f"Clipboard: {pasted}")

word = "hello!"
copied = pyperclip.copy(word)
print(f"Clipboard now contains {word}")
