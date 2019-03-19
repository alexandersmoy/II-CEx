#!/usr/bin/env python

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import os
import re
import pandas as pd
# import numpy as np

# Filepath and file name
dir_path = os.path.dirname(os.path.realpath(__file__)
filename='BL-Flickr-Images-Book.csv'
# ipy: full_path = r'C:\Users\atmoy\OneDrive\Desktop\Python\II-CEx\Data\BL-Flickr-Images-Book.csv'


# Data cleaning
# Extract - Access CSV and extract to staging
book_df=pd.read_csv("%s\\Data\\%s" % (dir_path, filename))
# ipy: book_df = pd.read_csv(full_path)

# review column headers
book_df.columns

# Evaluate if index is unique
print("Identifier is unique - %s" %
      (book_df.Identifier.is_unique)
      )


# Transform - Standardize and Clean-up
# Drop columns / Change index to Identifier
df=(book_df
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


# Clean-up inconsistent data
# 'Date of Publication' tasks
#   - Remove Extra Characters
#   - Use first date present
#   - enforce Numeric Value

# ***Using label index to reference column***
pub_date=df.loc[:, 'Date of Publication']

# Extract year and store numeric
pub_date=pd.to_numeric(pub_date.str.extract(r'(\d{4})', expand=False))
# pub_date finalized ^


# 'Place of Publication' tasks
#   - Standardize each Place
#   - Remove extra Characters
# ***Using position index to reference column***
pub_place=df.iloc[:, 0]
# Extract any years from pub_place for comparing to pub_date
pub_place_date=pub_place.str.extract(r'(\d{4})', expand=False)

# if pub_date is '' and pub_place_date is populated, use pub_place_date
pub_date2=pd.Series(pub_date)
pub_date2[pub_date.isnull()]=pub_place_date

# pub_date.isnull().sum()
# pub_date2.isnull().sum()

# ************ pub_place processing ************
# Remove extra characters and numeric values
pub_place_dtm=pd.DataFrame(pub_place)

# set stopwords
stopword_list=stopwords.words('english')
pub_place_dtm['cleaned_place']=None

# Create DTM
for i in range(0, len(pub_place_dtm)-1):
    # remove non-letters
    exclusions='[^a-zA-Z]'
    text=re.sub(exclusions, ' ', pub_place_dtm[i])
    text=text.lower()
    words=text.split()
    words=[word for word in words if not word in stopword_list]
    pub_place_dtm.iloc[i, 1]=' '.join(words)


# Apply tokenization pub_place (1-gram, 2-gram)

# Create doc term matrix

# Evaluate for terms repeating over mean frequency

# Compare 2-grams to 1-grams for each doc

# Pick 2-grams over 1-gram component within each doc

# Create finalized pub_place based on remaining tokens

# Semi-robust technique versus database lookup

# Standardize Column names

# Load - Output file with Standardized column names (.csv / .json)
