import requests
import xml.etree.ElementTree as ET
import csv
import os
import re
import argparse

# PubMed API Base URLs
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SEARCH_URL = BASE_URL + "esearch.fcgi"
FETCH_URL = BASE_URL + "efetch.fcgi"

def fetch_pubmed_ids(query, retmax=20):
    params = {"db": "pubmed", "term": query, "retmax": retmax, "retmode": "xml"}
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        return [id_elem.text for id_elem in root.findall(".//Id")]
    else:
        print("Error fetching PubMed IDs:", response.status_code)
        return []

def fetch_paper_details(pubmed_ids):
    params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
    response = requests.get(FETCH_URL, params=params)
    return response.text if response.status_code == 200 else None

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "N/A"

def fetch_email_from_crossref(pubmed_id):
    try:
        url = f"https://api.crossref.org/works/{pubmed_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            author_list = data.get("message", {}).get("author", [])
            for author in author_list:
                if "email" in author:
                    return author["email"]
    except:
        return "N/A"
    return "N/A"

def parse_papers(xml_data):
    root = ET.fromstring(xml_data)
    papers = []

    for article in root.findall(".//PubmedArticle"):  
        pubmed_id = article.find(".//PMID").text if article.find(".//PMID") is not None else "N/A"
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
        
        pub_date = article.find(".//PubDate")
        year = pub_date.find("Year").text if pub_date is not None and pub_date.find("Year") is not None else "N/A"
        month = pub_date.find("Month").text if pub_date is not None and pub_date.find("Month") is not None else ""
        day = pub_date.find("Day").text if pub_date is not None and pub_date.find("Day") is not None else ""
        publication_date = f"{year}-{month}-{day}".strip("-")

        authors, affiliations, corresponding_email = [], [], "N/A"

        for author in article.findall(".//Author"):
            lastname = author.find("LastName")
            firstname = author.find("ForeName")
            name = f"{firstname.text if firstname is not None else ''} {lastname.text if lastname is not None else ''}".strip()
            authors.append(name)
            
            aff_elem = author.find(".//AffiliationInfo/Affiliation")
            if aff_elem is not None:
                affiliations.append(aff_elem.text)
                email = extract_email(aff_elem.text)
                if email:
                    corresponding_email = email

        if corresponding_email == "N/A":
            corresponding_email = fetch_email_from_crossref(pubmed_id)

        papers.append({
            "PubMedID": pubmed_id,
            "Title": title,
            "Publication Date": publication_date,
            "Authors": "; ".join(authors),
            "Affiliations": "; ".join(affiliations),
            "Corresponding Author Email": corresponding_email
        })

    return papers

def save_to_csv(papers, filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except PermissionError:
            print(f"Error: Permission denied for {filename}. Close the file and try again.")
            return
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["PubMedID", "Title", "Publication Date", "Authors", "Affiliations", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"✅ Papers saved to {filename}")

def print_papers(papers):
    for paper in papers:
        print("\n" + "="*80)
        print(f"📌 PubMed ID: {paper['PubMedID']}")
        print(f"📖 Title: {paper['Title']}")
        print(f"📅 Publication Date: {paper['Publication Date']}")
        print(f"👥 Authors: {paper['Authors']}")
        print(f"🏛 Affiliations: {paper['Affiliations']}")
        print(f"📧 Corresponding Author Email: {paper['Corresponding Author Email']}")

def main():
    parser = argparse.ArgumentParser(description="Fetch COVID-19 vaccine papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Specify output CSV file (otherwise print to console)")
    
    args = parser.parse_args()

    if args.debug:
        print("🔍 Debug Mode Enabled")
        print(f"Query: {args.query}")

    pubmed_ids = fetch_pubmed_ids(args.query)
    if not pubmed_ids:
        print("No papers found.")
        return

    if args.debug:
        print(f"Found {len(pubmed_ids)} papers.")

    xml_data = fetch_paper_details(pubmed_ids)
    if not xml_data:
        print("Error fetching paper details.")
        return

    papers = parse_papers(xml_data)
    if not papers:
        print("No relevant paper data extracted.")
        return

    if args.file:
        save_to_csv(papers, args.file)
    else:
        print_papers(papers)

if __name__ == "__main__":
    main()
