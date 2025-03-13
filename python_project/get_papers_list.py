import requests  # type: ignore
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
    """Fetches PubMed IDs for a given query."""
    try:
        params = {"db": "pubmed", "term": query, "retmax": retmax, "retmode": "xml"}
        response = requests.get(SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        return [id_elem.text for id_elem in root.findall(".//Id")]
    except requests.RequestException as e:
        print(f"⚠️ Error fetching PubMed IDs: {e}")
        return []

def fetch_paper_details(pubmed_ids):
    """Fetches paper details from PubMed."""
    if not pubmed_ids:
        return None
    try:
        params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
        response = requests.get(FETCH_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"⚠️ Error fetching paper details: {e}")
        return None

def extract_email(text):
    """Extracts email addresses from a given text."""
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return emails[0] if emails else "N/A"

def fetch_email_from_crossref(doi):
    """Fetches corresponding author email from CrossRef API using DOI."""
    if not doi:
        return "N/A"
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        author_list = data.get("message", {}).get("author", [])
        for author in author_list:
            if "email" in author:
                return author["email"]
    except requests.RequestException:
        pass
    return "N/A"

def parse_papers(xml_data):
    """Parses XML data from PubMed and extracts relevant details."""
    root = ET.fromstring(xml_data)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.find(".//PMID").text if article.find(".//PMID") is not None else "N/A"
        title = article.find(".//ArticleTitle").text or "No Title"

        pub_date = article.find(".//PubDate")
        year = pub_date.find("Year").text if pub_date is not None and pub_date.find("Year") is not None else "N/A"
        month = pub_date.find("Month").text if pub_date is not None and pub_date.find("Month") is not None else ""
        day = pub_date.find("Day").text if pub_date is not None and pub_date.find("Day") is not None else ""
        publication_date = f"{year}-{month}-{day}".strip("-")

        authors, affiliations = [], []
        corresponding_email = "N/A"

        for author in article.findall(".//Author"):
            first_name = author.find("ForeName").text if author.find("ForeName") is not None else ""
            last_name = author.find("LastName").text if author.find("LastName") is not None else ""
            full_name = f"{first_name} {last_name}".strip()
            if full_name:
                authors.append(full_name)

            aff_elem = author.find(".//AffiliationInfo/Affiliation")
            if aff_elem is not None:
                affiliations.append(aff_elem.text)
                email = extract_email(aff_elem.text)
                if email != "N/A":
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
    """Saves extracted papers to a CSV file."""
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except PermissionError:
            print(f"❌ Error: Cannot write to {filename}. Close the file and try again.")
            return
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["PubMedID", "Title", "Publication Date", "Authors", "Affiliations", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(papers)
    
    print(f"✅ Papers saved to {filename}")

def print_papers(papers):
    """Prints extracted papers to the console."""
    for paper in papers:
        print("\n" + "="*80)
        print(f"📌 PubMed ID: {paper['PubMedID']}")
        print(f"📖 Title: {paper['Title']}")
        print(f"📅 Publication Date: {paper['Publication Date']}")
        print(f"👥 Authors: {paper['Authors']}")
        print(f"🏛 Affiliations: {paper['Affiliations']}")
        print(f"📧 Corresponding Author Email: {paper['Corresponding Author Email']}")

def main():
    """Main function to fetch and display PubMed papers."""
    parser = argparse.ArgumentParser(description="Fetch papers from PubMed based on a query.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Specify output CSV file (otherwise print to console)")
    
    args = parser.parse_args()

    if args.debug:
        print("🔍 Debug Mode Enabled")
        print(f"Query: {args.query}")

    print("🔄 Fetching paper list, please wait...")
    pubmed_ids = fetch_pubmed_ids(args.query)
    if not pubmed_ids:
        print("❌ No papers found.")
        return

    if args.debug:
        print(f"📜 Found {len(pubmed_ids)} papers.")

    xml_data = fetch_paper_details(pubmed_ids)
    if not xml_data:
        print("❌ Error fetching paper details.")
        return

    papers = parse_papers(xml_data)
    if not papers:
        print("❌ No relevant paper data extracted.")
        return

    if args.file:
        save_to_csv(papers, args.file)
    else:
        print_papers(papers)

if __name__ == "__main__":
    main()
