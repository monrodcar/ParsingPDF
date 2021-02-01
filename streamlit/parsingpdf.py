import spacy
import numpy as np
import pandas as pd
import streamlit as st
import os

from neo4j import GraphDatabase
from tika import parser
from spacy.matcher import PhraseMatcher
from collections import Counter
from pandas.io.formats.style import Styler

# --------------------------------------------------------------------------------------- #

@st.cache
def document_parser(file_path):
    """ Document tika parser """
    # Extract text from document
    content = parser.from_file(file_path)
    if 'content' in content:
        text = content['content']
    else:
        return
    # Convert to string
    text = str(text)
    return text

@st.cache
def clean_text(text):
    """ Lowercase, removes spaces and newlines """
    text = " ".join(text.strip().splitlines())
    text = text.lower()
    return text

@st.cache
def check_path(file_path):
    if file_path:
        file_path = file_path.strip('"')
        if os.path.exists(file_path):
            return file_path
        else:
            #st.error("The provided file path is invalid.")
            return None

def neo4j_connect(uri, user, password):
    """ Connect Neo4j database """
    driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
    return driver

# --------------------------------------------------------------------------------------- #

driver = neo4j_connect("bolt://localhost:7687", "neo4j", "parsingpdf")

# Get the skills from neo4j database
with driver.session() as session:
    skills = session.run("""MATCH (s:Skill) RETURN s.name as Skill""")
df = pd.DataFrame(skills.data(), columns=["Skill"])
skills = df["Skill"].to_list()

# Create patterns from skills
nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab)
keywords = list(nlp.pipe(skills))
matcher.add('keywords', None, *keywords)

st.header("Resume parser")
# Get the path
file_path = st.text_input('Please, provide the resume file path:')
path = check_path(file_path)
if path is not None:

    # Read the file and create Doc object
    resume = document_parser(path)
    text = clean_text(resume)
    with nlp.disable_pipes('tagger', 'parser'):
        doc = nlp(text)

    # Match skills in the CV
    matched_skills = []
    skills_count = 0
    matches = matcher(doc)
    for match_id, start, end in matches:
        match = doc[start:end]
        if not match.text in matched_skills:
            matched_skills.append(match.text)
            skills_count += 1

    # Count matched skills per role
    with driver.session() as session:
        count = session.run("""MATCH(s: Skill), (r: Role), (r)-[rel:REQUIRES_SKILL]->(s)
                                WHERE s.name in $skills 
                                RETURN r.name as Role, count(rel) as `Skills count`
                                ORDER BY `Skills count` DESC""",
                            skills=matched_skills)
    role_skills = pd.DataFrame(count.data(), columns=["Role", "Skills count"])
    role_skills.index = np.arange(1, len(role_skills)+1)

    # Display the role and the skills
    role = role_skills.iat[0, 0]
    st.subheader(f"Candidate is identified with the role: {role}")
    st.dataframe(role_skills.style.highlight_max(axis=0), 400, 600)
    st.subheader(f"Total number of skills identified : {skills_count}")
    show_all = st.checkbox(f"Preview all matched skills", value=True)
    if show_all:
        st.write(', '.join(matched_skills))

    # Filter matched skills by the selected role
    role_filter = st.selectbox(
        "Filter skills by role:", options=role_skills["Role"].tolist())
    with driver.session() as session:
        filtered_skills = session.run("""MATCH(s: Skill), (r: Role), (r)-[rel:REQUIRES_SKILL]->(s)
                                        WHERE s.name IN $skills AND r.name IN $filter
                                        RETURN DISTINCT s.name as Skill""",
                                      skills=matched_skills, filter=role_filter)
    filtered_skills = pd.DataFrame(filtered_skills.data(), columns=["Skill"])
    filtered_skills = filtered_skills["Skill"].to_list()
    st.write(', '.join(filtered_skills))
