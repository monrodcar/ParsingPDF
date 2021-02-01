## Technologies/Frameworks/Libraries

* Neo4j Cypher : for creating and querying graph database
* Streamlit : for building Machine Learning Application
* spaCy : for NLP
* Tika-Python : for parsing PDFs
* Other standard Python libraries: numpy, pandas, collections, etc.

## Step-by-step installation instructions

**Create graph database**

 1. Add a new database to your project. Set the password as "parsingpdf".

 2. Find the technologies.csv file in the [datasets](/ParsingPDF/datasets/) folder, and put it into the Neo4j database Import folder.

 3. Find the graph-technologies.cypher script in the [cypher](/ParsingPDF/cypher/) folder and execute it.

**Run the streamlit app**

 4. Start the ParsingPDF database in the Neo4j Desktop.

 5. Run the parsingpdf.py script from the [streamlit](/ParsingPDF/streamlit/) folder by executing `streamlit run parsingpdf.py`.

 6. The Streamlit Local URL will open: http: //localhost:8501 . So, please, provide the path of the resume file, for example: C: \ Users \ UserName \ Desktop \ CV.pdf.

**Note**: You can always update the  _Technologies words_ spreadsheet, rename it as _technologies.csv_ and follow the step 2. Headers of the file represent Roles, and the values in their corresponding columns represent Skills related to that Role.
