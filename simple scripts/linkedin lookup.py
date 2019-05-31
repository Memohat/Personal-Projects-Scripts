#! python3
# Mehmet Hatip

import webbrowser, os

name = "linkedin lookups.csv"
skip = False

with open(name) as fin:

	for line in fin:
		company = line
		print(company)
		answer = input("Press enter to search for company, s to skip next, e to exit: ")
		if answer == 'e':
			exit()
		elif not answer == 's':
			linkedinURL = ("https://www.linkedin.com/search/results/companies/?keywords="
							+ company.replace('&','%26') + "&origin=SWITCH_SEARCH_VERTICAL")
			webbrowser.open(linkedinURL)
