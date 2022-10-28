# -*- coding: utf-8 -*-

# =============================================================================
# https://www.ncbi.nlm.nih.gov/books/NBK3828/
# #https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/
# =============================================================================


# Part 1, get publications through pubmed API
#!pip install biopython
from Bio import Entrez
import pandas as pd
import re

#open text file in read mode
text_file = open("C:/Users/Desktop/RedCap/Publications project/members list Aug.txt", "r")
#read whole file to a string 
# https://stackoverflow.com/questions/8369219/how-to-read-a-text-file-into-a-string-variable-and-strip-newlines
members = text_file.read().split('\n')
#count how many members in the file
Counter = 0 
for i in members:
    if i:
        Counter += 1          
print("Total members in the file:", Counter)
#close file
text_file.close() 
#print(members)


# The search_text can be input any text, either author name or PMID or others. It function like searching in pubmed
def search(query):
    Entrez.email = email
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax = maxpaper,
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results
 
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

publication_dict = {"record_id":[],"author":[],"articleTitle":[], "month":[], "year":[], "details":[],"PMID":[], 'PMCID':[],"affiliations":[]}

# input your email for Pubmed to track     
email = 'abc@gmail.com'
maxpaper = '300000'
for line in members:
    #In my project I search publications of GU and 
    search_text = line +  " and (DC or D.C. or District of Columbia or New Jersey or NJ or Georgetown or Hackensack)"
    print(line)
                
    
    if __name__ == '__main__': 
        results = search(search_text)
        #print(results)
        id_list = results['IdList']
        #print(len(id_list))
        try:
            papers = fetch_details(id_list)
            print(len(papers['PubmedArticle']))
        except:
            print(0)       
        #print(papers['PubmedArticle'])
 
    
        for i, paper in enumerate(papers['PubmedArticle']):
            # check duplicates in publication_dict by PMID
            if paper['MedlineCitation']['PMID'] in publication_dict['PMID']:
                i+1
            else: 
                page = None
                doi = None
                print_ahead = ""
                year = None
                month = None
                day = None
                #the last elements may be pmcid. start with PMC7971554
                #print(paper['PubmedData']['ArticleIdList'][-1])
                if 'Pagination' in paper['MedlineCitation']['Article']:
                    page = paper['MedlineCitation']['Article']['Pagination']['MedlinePgn']
                if len(paper['MedlineCitation']['Article']['ELocationID'])==1:
                    doi = paper['MedlineCitation']['Article']['ELocationID'][0]
                elif len(paper['MedlineCitation']['Article']['ELocationID'])==2: 
                    doi = paper['MedlineCitation']['Article']['ELocationID'][1] 
                #print(paper['PubmedData']['PublicationStatus'])
                if paper['PubmedData']['PublicationStatus'] == "aheadofprint":
                    print_ahead = ". Epub ahead of print"
                else: print_ahead = ""
                    #print_ahead = ". Epub " + str(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Year','')) + " " + str(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Month','')) + " " + str(paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Day',''))
                publication_dict['record_id'].append(i+1)
                publication_dict['PMID'].append(paper['MedlineCitation']['PMID'])
                if len(paper['PubmedData']['ArticleIdList'])>=3 and re.search("^PMC", paper['PubmedData']['ArticleIdList'][-1]):
                    publication_dict['PMCID'].append(paper['PubmedData']['ArticleIdList'][-1])
                elif len(paper['PubmedData']['ArticleIdList'])>=3 and re.search("^PMC", paper['PubmedData']['ArticleIdList'][-2]):
                    publication_dict['PMCID'].append(paper['PubmedData']['ArticleIdList'][-2])
                else: publication_dict['PMCID'].append('N/A')
                if 'Year' in paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']:
                    year = paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Year','')
                elif len(paper['MedlineCitation']['Article']['ArticleDate']) != 0:
                    year = paper['MedlineCitation']['Article']['ArticleDate'][0]['Year']
                if 'Month' in paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']:
                    month = paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Month']
                    day = paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Day','')
                elif len(paper['MedlineCitation']['Article']['ArticleDate']) != 0: 
                    month = paper['MedlineCitation']['Article']['ArticleDate'][0]['Month']
                    day = paper['MedlineCitation']['Article']['ArticleDate'][0]['Day']
                #print(month)
                #print(paper['MedlineCitation']['PMID'])
                publication_dict['articleTitle'].append(paper['MedlineCitation']['Article']['ArticleTitle'])
                publication_dict['details'].append("{}. {} {} {}; {}({}):{} doi: {}{}".format(#paper['MedlineCitation']['Article']['Journal']['Title'],
                                                   paper['MedlineCitation']['Article']['Journal']['ISOAbbreviation'],                                      
                                                   year,
                                                   month,
                                                   day,
                                                   #paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Year',''),
                                                   #paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Month',''),
                                                   #paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Day',''),
                                                   paper['MedlineCitation']['Article']['Journal']['JournalIssue'].get('Volume', ''),
                                                   paper['MedlineCitation']['Article']['Journal']['JournalIssue'].get('Issue',''),
                                                   page,
                                                   doi,
                                                   print_ahead
                                                   ))
                publication_dict['month'].append(month)                                   
                publication_dict['year'].append(year)
        
                author=[]
                affiliations =[]
                if 'AuthorList' in paper['MedlineCitation']['Article']:
                    for i, name in enumerate(paper['MedlineCitation']['Article']['AuthorList']):
                        #print("{}) {} {},".format(i+1, name.get('ForeName',''), name.get('LastName','')))
                        author.append("{} {}".format(name.get('ForeName',''), name.get('LastName','')))
                    publication_dict['author'].append(author)
                
                    
                    
                    # some AffiliationInfo':[] are empty, some have more than one affiliations inside
                    duplicate_check={}
                    i=0  # final affiliations without duplicates
                    m= 0 # all affiliations including duplicates
                    n=0  # duplicate affiliations
                    for j, place in enumerate(paper['MedlineCitation']['Article']['AuthorList']):
                        af_array = place['AffiliationInfo']
                        if len(af_array)==0:
                            continue
                        
                        for affiliation in af_array:
                            m=m+1
                            aff_key = affiliation['Affiliation']
                            if aff_key in duplicate_check:
                                duplicate_check[aff_key]+=1
                                #print("{}) {},".format(j, place['AffiliationInfo'][0]['Affiliation']))
                                n=n+1
                                continue
                            
                            #print("{}) {},".format(i, place['AffiliationInfo'][0]['Affiliation']))
                            affiliations.append(aff_key)
                            duplicate_check[aff_key]=1
                            i=i+1
                                               
                    #print(m,n,i)
                    #print(duplicate_check)
                    publication_dict['affiliations'].append(affiliations)
                else: 
                    publication_dict['author'].append("")
                    publication_dict['affiliations'].append("")
            

print(len(publication_dict['PMID']))
#print(publication_dict)


# Part 2, import publications through pubmed API to RedCap through RedCap API
#!pip install pycap
from redcap import Project
api_url= "https://redcap.XXX/redcap/api/" #REDCap project api url
api_key = 'XXXXXXXXXXXXXXXXXXX' #REDcap project api key
project = Project(api_url, api_key)


#check the forms and the field names
#print(project.field_names)

x = 0
to_import = []
while x < len(publication_dict['record_id']):
    record_id = publication_dict['record_id'][x]
    program = 0
    inter_intra = 0
    location= 0
    authors = publication_dict['author'][x]
    authors_string = ", ".join(authors)
    title = publication_dict['articleTitle'][x]
    month = publication_dict['month'][x]
    year = publication_dict['year'][x]
    detail = publication_dict['details'][x]
    pmid = publication_dict['PMID'][x]
    pmcid = publication_dict['PMCID'][x]
    impf= ''
    source = ''
    othcancercentr= publication_dict['affiliations'][x]
    affiliations_string = "\n".join(othcancercentr)
    dept = 0
    supplement=''
    devfund= ''
    needattach= ''
    attached = ''

    
    # append a dictionary to to_import list 
    to_import.append({'record_id':record_id, 'authors':authors_string, 'title': title, 'month': month,'year': year, 'detail': detail, 'pmid': pmid,'pmcid': pmcid, 'othcancercentr': affiliations_string}. copy())
    #print(record_id, month, authors_string)
    #print(to_import)
    x+=1

#print(to_import[0])
print(len(to_import))
# filter a list of dictionary by specific month and year of publications: https://blog.finxter.com/how-to-filter-a-list-in-python/   
sub_import = [pub for pub in to_import if (pub['month']=="09" or pub['month']=="Sep") and pub['year']=="2022"]  
# re-assign the record_id
for i, pub in enumerate(sub_import):
    #print(i)
    pub["record_id"]= i+1
      
print(len(sub_import))
#print(sub_import)


response = project.import_records(sub_import, overwrite='overwrite')
#print(response)



        

