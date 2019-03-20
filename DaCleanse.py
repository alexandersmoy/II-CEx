#!/usr/bin/env python
# encoding: utf-8

from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
from nltk.probability import FreqDist
import nltk
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ************ Read in Data ************
# Filepath and file name
dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = r'BL-Flickr-Images-Book.csv'
# ipy: full_path = r'C:\Users\atmoy\OneDrive\Desktop\Python\II-CEx\Data\BL-Flickr-Images-Book.csv'

# Extract - read CSV and extract to staging book_df
book_df = pd.read_csv("%s\\Data\\%s" % (dir_path, file_name))
# ipy: book_df = pd.read_csv(full_path)


# ************ Review Data ************
# review column headers
book_df.columns

# Evaluate if index is unique
print("Identifier is unique - %s" %
      (book_df.Identifier.is_unique)
      )


# ************ Transform/Staging ************
# Drop columns / Change index to Identifier
df = (book_df
      .drop(columns=['Edition Statement',
                     'Corporate Author',
                     'Corporate Contributors',
                     'Former owner',    # lower case owner
                     'Engraver',
                     'Contributors',
                     'Issuance type',   # lower case type
                     'Shelfmarks'])
      .set_index('Identifier')
      )

# --------------------------------------------------- #
# -- Clean-up inconsistent data --
# --------------------------------------------------- #
# 'Date of Publication' tasks:
#   - Remove Extra Characters
#   - Use first date present
#   - enforce Numeric Value
# --------------------------------------------------- #
# ***Using label index to reference column***
pub_date = df.loc[:, 'Date of Publication']

# Extract year and store numeric
pub_date = pd.to_numeric(pub_date.str.extract(r'(\d{4})', expand=False))

# --------------------------------------------------- #
# 'Place of Publication' tasks:
#   - Standardize each Place
#   - Remove extra Characters
# --------------------------------------------------- #
# ***Using position index to reference column***
pub_place = pd.DataFrame(df.iloc[:, 0])
# Extract any years from pub_place for comparing to pub_date
pub_place_date = pub_place.iloc[:, 0].str.extract(r'(\d{4})', expand=False)

# if pub_date is '' and pub_place_date is populated, use pub_place_date
pub_date2 = pd.Series(pub_date)
pub_date2[pub_date.isnull()] = pub_place_date

# pub_date.isnull().sum()
# pub_date2.isnull().sum()

# --- pub_place processing ---
# set stopwords
stopword_list = stopwords.words('english')


# Function: clean_data(row)
#   - remove non-letters and stopwords
def clean_data(record):
    # remove non-letters
    text = re.sub('[^a-zA-Z]', ' ', record)
    text = text.lower()
    words = text.split()
    words = [word for word in words if not word in stopword_list]
    return ' '.join(words)


# Clean pub_place data + store back in dataframe
pub_place['cleaned_place'] = pub_place['Place of Publication'].apply(clean_data)

# Apply tokenization to pub_place (1-gram)
pub_place['tokens'] = pub_place.cleaned_place.apply(word_tokenize)

# --- Document Length Analysis ---
# Analysis of text by number of words/tokens
len(pub_place.tokens)
(pub_place.tokens.apply(len) == 1).sum()
(pub_place.tokens.apply(len) == 2).sum()
(pub_place.tokens.apply(len) > 2).sum()

# --- Term Frequency Analysis ---
# Evaluate term frequency
pub_place_cat = pub_place.cleaned_place.str.cat(sep=' ')
fdist = FreqDist(word_tokenize(pub_place_cat))
print(fdist)
fdist.most_common(40)
# fdist.plot(50, cumulative=False)

# --- Create High Freq Word List ---
high_freq_words = [item[0] for item in fdist.most_common(40)
                   if str(item[0]) != 'nan']
# Hand prune high_freq_words
high_freq_words.remove('new')
high_freq_words.remove('york')
high_freq_words.remove('printed')
high_freq_words.remove('pp')
high_freq_words.remove('mass')
high_freq_words.remove('co')
high_freq_words.remove('w')
high_freq_words.remove('j')
high_freq_words.remove('n')
high_freq_words.remove('e')
high_freq_words.remove('enk')
high_freq_words.remove('kj')
high_freq_words.remove('buenos')
# Add to high_freq_words
high_freq_words.append('plymouth')
# print(high_freq_words)

# --- Build pub_place['final'] ---
# Evaluate if pub_place.tokens contains high_freq_words then use high_freq_words
#   else use pub_place.cleaned_place
pub_place_final = []
for index, row in pub_place.iterrows():
    words = [word for word in row['tokens'] if word in high_freq_words]
    place = ''
    if (len(words) == 0):
        place = row['cleaned_place']
    else:
        place = words[0]
    pub_place_final.append(place)

pub_place['final'] = pub_place_final

# ************ Final Staging to Output ************
# Standardize Column names
df_final = (pd.DataFrame(df)
            .rename(columns={
                'Place of Publication': 'publication_place',
                'Date of Publication': 'publication_date',
                'Publisher': 'publisher',
                'Title': 'title',
                'Author': 'author',
                'Flickr URL': 'flickr_url'
            })
            )
# Assign cleaned publication_date
df_final['publication_date'] = pub_date2
# Assign cleaned publication_place
df_final['publication_place'] = pub_place['final']


# Load - Output file with Standardized column names (.csv)
df_final.to_csv("%s\\cleaned_books.csv" % (dir_path))
# ipy: df_final.to_csv(r'C:\Users\atmoy\OneDrive\Desktop\Python\II-CEx\cleaned_books.csv')
