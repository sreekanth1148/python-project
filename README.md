#  python project:PubMed Paper Fetcher
 
 ## Overview
 
 PubMed Paper Fetcher is a Python-based tool designed to fetch research papers from PubMed based on a given query. It extracts relevant details such as title, publication date, authors, affiliations, and corresponding author emails. The extracted data can be displayed on the console or saved as a CSV file.
 
 ## Code Organization
 
 The project structure is as follows:
 

 python_project/
 │── get_paper_list.py   # Main script for fetching papers
 │── main.py             # Entry point for running the script
 │── __init__.py         # Package initialization
 │── README.md           # Project documentation
 │── requirements.txt    # Dependencies list
 │── poetry.lock         # Poetry dependency lock file
 │── pyproject.toml      # Poetry configuration file

 
 ## Main Components
 
 - `fetch_pubmed_ids(query, retmax)`: Fetches PubMed IDs based on the search query.
 - `fetch_paper_details(pubmed_ids)`: Retrieves paper details from PubMed.
 - `extract_email(text)`: Extracts email addresses from text.
 - `fetch_email_from_crossref(doi)`: Fetches corresponding author email using CrossRef API.
 - `parse_papers(xml_data)`: Parses XML data from PubMed and extracts relevant details.
 - `save_to_csv(papers, filename)`: Saves extracted papers to a CSV file.
 - `print_papers(papers)`: Prints extracted paper details to the console.
 - `main()`: Handles user input and execution flow.
 
 ## Installation and Execution
 
 
  ### 1️⃣ Install Poetry (If Not Already Installed)
 
 If you haven't installed Poetry, install it using the following command:
 
 Windows (PowerShell):
 
 (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
 
 
 ### 2️⃣ Install Dependencies
 
 Ensure you have **Python 3.7+** installed. Then, install the required dependencies using
 
 #### 🔹Using pip:
 
 pip install -r requirements.txt
 
 #### 🔹Using Poetry:
 
 poetry install
 
 #### 🔹Test the Script
 
 poetry run get-papers-list
 
 
 ### 3️⃣ Run the Program
 
 The script has been **tested and executed** with the following query:
 
 python main.py "COVID-19 Vaccine"
 
 ### 4️⃣ Save Results to a CSV File
 
 To fetch papers and save the results in a CSV file, run:
 
 
 poetry run get-papers-list -f results.txt
 
 
 ### 5️⃣ Enable Debug Mode
 
 For **detailed logging**, use the `--debug` flag:
 
  poetry run get-papers-list -d
  
  6️⃣ Common Issues & Fixes
 
 🔹 Command 'poetry' not found
 
 Restart your terminal and try running poetry --version.
 If it still doesn’t work, try pipx ensurepath, then restart your terminal.
 
 🔹 Error: No file/folder found for package
 
 Check if pyproject.toml is correctly configured with the [tool.poetry] section.
 Ensure your project name is valid (no spaces).
 
 🔹 Error: 'get-papers-list' not recognized
 
 Check if pyproject.toml has the correct script entry under [tool.poetry.scripts]:
 
 [tool.poetry.scripts]
 get-papers-list = "python_project.get_papers:main"
 
 🔹  Run poetry install again.

 7️⃣ Clone the Repository
First, download the project to your local system:

git clone https://github.com/sreekanth1148/python-project.git

cd python-project
 
 ## Tools and Libraries Used
 
 # Python Project
 
 This project uses **Poetry** for dependency management and packaging.
 
 ## **Tools & Technologies Used**
 The following tools and libraries were used to build and manage this project:
 
 ### **Programming Language**
 - **Python**: The core programming language used in this project.
   - 🔗 [Python Official Website](https://www.python.org/)
   - 🔗 [Python Documentation](https://docs.python.org/3/)
 
 ### **Dependency Management & Packaging**
 - **Poetry**: Used for dependency management and packaging.
   - 🔗 [Poetry Official Site](https://python-poetry.org/)
   - 🔗 [Poetry Documentation](https://python-poetry.org/docs/)
 
 ### **Version Control & Collaboration**
 - **Git**: Used for version control.
   - 🔗 [Git Official Site](https://git-scm.com/)
   - 🔗 [Git Documentation](https://git-scm.com/doc)
 - **GitHub**: Used for hosting and collaborating on the project.
   - 🔗 [GitHub](https://github.com/)
   - 🔗 [GitHub Docs](https://docs.github.com/)
 
 ### **Libraries Used**
 - **Requests**: Used for making HTTP requests to fetch data.
   - 🔗 [Requests Documentation](https://docs.python-requests.org/en/latest/)
 - **Pandas**: Used for handling and analyzing data.
   - 🔗 [Pandas Documentation](https://pandas.pydata.org/docs/)
 
 
 
 ## Contribution
 
 Contributions are welcome! Feel free to fork the repository, create issues, or submit pull requests.
 
