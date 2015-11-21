import json

from dataset.models import Dataset, Investigator, Link, PublicationDocument, \
    PublicationPubMedLink, Task


def data_import():
    fp = open("kimonoData.json")
    pubmed_fp = open("pubmed_links.json")
    
    old_json = json.load(fp)
    pubmed_json = json.load(pubmed_fp)

    for col_1 in old_json['results']['collection1']:
        url = col_1['url']
        col_2 = [x for x in old_json['results']['collection2'] if url == x['url']]
        col_3 = [x for x in old_json['results']['collection3'] if url == x['url']]
        col_4 = [x for x in old_json['results']['collection4'] if url == x['url']]
        new_dataset = Dataset()
        new_dataset.curated = col_1.get('property12')
        new_dataset.project_name = col_1.get('title')
        new_dataset.sample_size = col_1.get('sample_size')
        new_dataset.scanner_type = col_1.get('scanner')
        new_dataset.accession_number = col_1.get('accession_number')
        new_dataset.acknowledgements = col_1.get('acknowlegments')
        new_dataset.license_title = col_1.get('license').get('text')
        new_dataset.license_url = col_1.get('license').get('href')
        
        summary = ""
        for x in col_2:
            summary += x.get('description')
        new_dataset.summary = summary

        new_dataset.save()

        pubmed_link = PublicationPubMedLink()
        for inv in col_3:
            investigator = Investigator()
            investigator.investigator = inv['investigators']
            investigator.dataset = new_dataset
            investigator.save()

        for l in col_4:
            link = Link()
            link.title = l['aws']['text']
            link.url = l['aws']['href']
            link.dataset = new_dataset
            link.save()

        for pubmed in pubmed_json['results']['collection1']:
            if pubmed.get('url') == url:
                print(url)
                pubmed_link = PublicationPubMedLink()
                pubmed_link.title = pubmed.get('pubmedlink').get('text')
                pubmed_link.url = pubmed.get('pubmedlink').get('href')
                pubmed_link.dataset = new_dataset
                pubmed_link.save()
   
'''
['acknowlegments', 'pubmedlink', 'property12', 'index', 'sample_size', 'url', 'accession_number', 'scanner', 'license', 'document', 'title', 'task']
'''
