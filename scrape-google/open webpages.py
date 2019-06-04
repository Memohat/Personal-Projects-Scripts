#! python3
# Mehmet Hatip

def main():
    #!python3
    # Mehmet Hatip
    """
    Program functions to get company names from the specified file in the directory,
    get the html page of a google search for each of the companies, and return the
    first result on google of each search in a new csv file, that also has the
    company name in the next column.
    """
    
    
    import os, csv, requests, bs4
    """
    Very important modules, os lets you change directory so the file can be
    accessed from another folder. csv is a module for writing and reading csv
    files. requests gets an html page from the internet using a URL. bs4, or
    beautifulsoup4, makes the request txt into an easily searchable and usable
    format, one in which finding the right URL is no problem
    """
    
    path = "C://Users//ithatim//Documents"
    # path of company names file
    
    name = "SAP+ASUG19 Company Name Report as of 4.12 with URLs" 
    # name of company names file
    
    os.chdir(path)
    # changing directory
    
    company_url = []
    # list will store tuples in the form of (company name, google search url)
    
    with open(f"{name} source.csv") as fin:
        # opening company names file
    
        fin.readline()
        # skipping header
    
        reader = csv.reader(fin)
        # using csv module
    
        for company, url in reader:
            company_url.append((company, "https://www.google.com/search?q="
                                + company.replace(' ', '+')))
        # for every company listed on the file, add the name and the google search
        # url to the list.
    
    with open(f"{name}.csv", 'a+', newline='') as fout:
        # opening output file
        
        writer = csv.writer(fout)
        # using csv module
        
        i = 1
        # counter for number of companies done
        
        for company, google_url in company_url:
            # using the complete list from above
            
            request = requests.get(google_url)
            # get html file with google url with requests
    
            request.raise_for_status()
            # make sure file was successfully obtained
            
            soup = bs4.BeautifulSoup(request.text)
            # make new BeautifulSoup object using request.text
            
            info = soup.select('.r a')[0]
            """
            specification to get the first search result on google using bs4.
            in '.r a', .r specifies to look for the class attribute r, while
            a specifies to look for the element named a. This is where all the
            searches are stored, so getting the first element off of the list
            produced by this would require the [0] at the end.
            """
            
            url = info.get('href')
            # url is stored in 'href' attribute. We get the url using get
            
            start_index = str.find(url, 'http')
            # we define start index of url to be where http is in the string.
    
    
            domain_index = str.find(url, '//') + 2
            """
            all urls have a // before the domain name begins.
            this index finds the // and adds two to get the index of the string
            where the domain starts
            """
            
            end_index = str.find(url[domain_index:], '/') + domain_index
            """
            the index of the first /, which is where the base website ends after 
            .com or .org or whatever. We add domain and / index to get
            the end index of the part of the url we are interested in.
            """
            
            url = url[start_index:end_index]
            # very simple, change url so that it is from the start to end index.
            
            writer.writerow([company, url])
            # write the company name and its url into the output file.
    
    
            i += 1
            # add 1 to the counter
            
            print(i)
            #print the counter on the console
            
    print(f"File stored in {path}")
    # end message saying file was stored
    

if __name__ == '__main__':
    main()