#! python3
# Mehmet Hatip
"""
Program functions to get search queries from the specified file in the directory,
get the html page of a google search for each of the searches, and return the
first result on google of each search in a new csv file.
"""


import os, csv, requests, bs4, time, re
"""
- os: change directory
- csv: writing and reading csv
- requests: gets html page from internet
- bs4: makes html request into easily searchable and usable format
- time: delaying the program so it doesn't request too much at once
- re: Regex to get portion of URL
"""

path = os.getcwd() #insert path of input/output here

source = "source.txt" #insert name of input file here
output = "output.csv" #insert name of output file here

os.chdir(path)

search_url = []
# list will store tuples in the form of (search query, google url)

with open(source, encoding="utf-8") as fin:
    try:
        for query in fin:
            if query:
                search_url.append((query, "https://www.google.com/search?q="
                                    + query.replace(' ', '+')))
    except UnicodeDecodeError as error:
        print(f"\nOne of the queries could not be read properly.")
        if input("Press e for error message: ") == 'e':
            print(error)
        exit()
    # try statement catches error, prints out in console, and exits program
try:
    with open(output, 'a+', newline='') as fout:
        # opening output file
        
        writer = csv.writer(fout)
        # using csv module
        
        i = 1
        # counter for number of queries done
        
        headers = ['Query', 'Website']

        with open(f"{name}.csv", newline='') as fout2:
            topline = fout2.readline()
            if topline.strip() != ','.join(headers):
                writer.writerow(headers)
        
        for query, google_url in search_url:
            
            i += 1            

            while True:
                try:
                    request = requests.get(google_url)
                    # get html file with google url with requests

                    request.raise_for_status()
                    # make sure file was successfully obtained
                    
                    soup = bs4.BeautifulSoup(request.text, features='html.parser')
                    # make new BeautifulSoup object using request.text
                                 
                    info = soup.select('.r a')[0]
                    """
                    specification to get the first search result on google using bs4.
                    in '.r a', .r specifies to look for the class attribute r, while
                    a specifies to look for the element named a.
                    """

                    url = info.get('href')
                    break
                except:
                    print("Trying again")

            Regex = re.compile(r'https?://.*(?=/)')

            mo = Regex.search(url)

            url = mo.group()
            
            writer.writerow([query, url])
            # write the query and its url into the output file.

            print(f"{i} {query}")
            #print the counter and query on the console

            time.sleep(30)
            # delaying for 30 seconds so program is not requesting too much at once            

    print(f"File stored in {path}")
    # end message saying file was stored

except PermissionError:
    print(f"Error, {name} is open\nClose the file and try again")

    
