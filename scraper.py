import requests
import PyPDF2
import csv
import re
    

def scrape(file_location, office, outfile_name, election_year='2008', write_fieldnames=True):
    #file location is a url for a file, eg: https://www.ok.gov/elections/documents/08pres.pdf
    r = requests.get(file_location)
    filename = file_location.split('/')[-1]
    pdf_name = "tmp/{}".format(filename)
    with open(pdf_name, 'wb') as outfile:
        outfile.write(r.content)
    pdfFileObj = open(pdf_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    rows = []
    i = 0
    pageObj = pdfReader.getPage(i)
    while True:
        rows.extend(parse_page(pageObj, office, election_year))
        i += 1
        try:
            pageObj = pdfReader.getPage(i)
        except IndexError:
            break

    with open(outfile_name, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['county','office','district','party','candidate','votes'])
        writer.writeheader()
        writer.writerows(rows)




def parse_page(pageObj, office, election_year):
    text = pageObj.extractText()
    districts = re.findall('DISTRICT \d+', text)
    elections = text.split(election_year)[1:] #this is not a risk to find elsewhere in the doc bc all other numbers are comma-delimited
    rows = []
    for i, e in enumerate(elections):
        if len(districts) > 0:
            district = districts[i].replace('DISTRICT','').strip()
        else:
            district = ""
        rows.extend(parse_election(e, office, district))
    return rows

def parse_election(text, office, district):
    #PARSE HEADER
    #the names all come before the equals signs
    header = text.split("=")[0]
    #names occur after the election year
    header = header.replace('VOTES','')
    first_names, last_names = header.split("TOTAL")

    first_name_list = re.split('\s\s+',first_names.strip())
    last_name_list = re.split('\s\s+',last_names.strip())

    name_list = ['']*len(last_name_list)

    for i, name in enumerate(first_name_list):
        index = i % len(last_name_list)
        name_list[index] = name_list[index] + " " + name

    for i, name in enumerate(last_name_list):
        name_list[i] = name_list[i] + " " + name

    #PARSE RESULTS
    results = "\n".join(text.split("=")[1:]).strip()

    rows = []
    for line in results.split('\n'):
        if line.strip():
            #the below deals with the fact that the first 2 lines are usually glommed together
            matches = re.findall('[\D]+\s\s[0-9, ]+', line.strip())
            for m in matches:
                if not m:
                    continue
                if "STATE TOTAL" in m:
                    continue
                else:
                    rows.extend(parse_result_line(m, name_list, office, district))

    return rows

def parse_result_line(line, names, office, district_number):
    ret_lines = []
    split_line = re.split('\s\s+', line)
    for i, name in enumerate(names):
        line_dict = {}
        line_dict['county'] = split_line[0].title()
        line_dict['office'] = office
        line_dict['district'] = district_number
        if "(D)" in name or "Democrat" in name:
            line_dict['party'] = 'D'
            line_dict['candidate'] = name.replace('(D)','').replace('Democrat','').strip()

        elif "(R)" in name or "Republican" in name:
            line_dict['party'] = 'R'
            line_dict['candidate'] = name.replace('(R)','').replace('Republican','').strip()

        elif "(I)" in name or "Independent" in name:
            line_dict['party'] = 'I'
            line_dict['candidate'] = name.replace('(I)','').replace('Independent','').strip()
        else:
            line_dict['candidate'] = name.strip()

        line_dict['votes'] = split_line[i+1].replace(",","")

        ret_lines.append(line_dict)

    return ret_lines

scrape('https://www.ok.gov/elections/documents/08pres.pdf', 'President', "2008/20081104__ok__general__president__county.csv")
scrape('https://www.ok.gov/elections/documents/08ussen.pdf', 'U.S. Senate', "2008/20081104__ok__general__us_senate__county.csv")
scrape('https://www.ok.gov/elections/documents/08usrep.pdf', 'U.S. House', "2008/20081104__ok__general__us_house__county.csv")
scrape('https://www.ok.gov/elections/documents/08ss.pdf', 'State Senate', "2008/20081104__ok__general__state_senate__county.csv")
scrape('https://www.ok.gov/elections/documents/08sh.pdf', 'State House', "2008/20081104__ok__general__state_house__county.csv")
scrape('https://www.ok.gov/elections/documents/08corp.pdf', 'Corporation Commissioner', "2008/20081104__ok__general__corp_commissioner__county.csv")
