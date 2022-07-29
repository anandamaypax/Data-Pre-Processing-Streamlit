# Import libraries
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk
from nltk.stem.snowball import SnowballStemmer

# Welcome message
st.write("WELCOME TO TEXT PRE-PROCESSING 101!")

# User upload of .csv file
uploaded_csvfile = st.file_uploader("SHOW US YOUR FAVORITE CSV!")

# Columns from file to interface
def dropdowncol_names(df):
    return list(df.columns)
if uploaded_csvfile != None:
    df = pd.read_csv(uploaded_csvfile, encoding='ANSI')
    text_col = st.selectbox('CHOOSE COLUMN TO EXPERIMENT ON!', dropdowncol_names(df))

# Packages
nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")

# Clean HTML
def process_html(df, text_col):
    df[text_col]=df[text_col].astype("string")
    rev = df[text_col].tolist()
    rev_clean = []
    for text in rev:
        text = BeautifulSoup(text, 'html.parser').getText()
        rev_clean.append(text.lower())
    st.write("HTML JUNK BANISHED!")
    st.write(rev_clean)
    return rev_clean

# Tokenize and stem
def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens if t not in stopwords]
    return stems

def running_tokenizer(rev_clean):
    vocab_stem = []
    for i in rev_clean:
        all_stem = tokenize_and_stem(i)
        vocab_stem.extend(all_stem) 
    st.write("DISINTEGRATED INTO TOKENS AND STEMMED!")
    st.write(vocab_stem)
    return vocab_stem

# Preprocessing
if st.button('GO GO PROCESSING!'):
    rev_clean = process_html(df, text_col)
    vocab_stem = running_tokenizer(rev_clean)

