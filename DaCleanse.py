#!/usr/bin/env python

import nltk
import os
import re
import pandas as pd
# import numpy as np

# Filepath and file name
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = 'BL-Flickr-Images-Book.csv'

# Data cleaning
# Extract - Access CSV and extract to staging
book_df = pd.read_csv("%s\\Data\\%s" % (dir_path, filename))

# review column headers
list(book_df)

# Transform - Standardize and Clean-up
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

# Evaluate if index is unique
print("Index is unique - %s" %
      (len(df.index) == len(df.index.unique()))
      )

# Clean-up inconsistent data
# 'Date of Publication' tasks
#   - Remove Extra Characters
#   - Use first date present
#   - enforce Numeric Value

# ***Using label index to reference column***
pub_date = df.loc[:, 'Date of Publication']


# Create year extract function
def year_extract(txt):
    match = re.search(r'(\d{4})', str(txt))
    if match:
        return match.group(1)
    else:
        return('')


# Apply year_extract function
pub_date = pub_date.apply(year_extract)
# Convert to numeric
pd.to_numeric(pub_date)
# pub_date finalized ^


# 'Place of Publication' tasks
#   - Standardize each Place
#   - Remove extra Characters
# ***Using position index to reference column***
pub_place = df.iloc[:, 0]
# Extract any years from pub_place for comparing to pub_date
pub_place_date = pub_place.apply(year_extract)
# if pub_date is '' and pub_place_date is populated, use pub_place_date
pub_date.apply()

# ************ pub_place processing ************
# Remove extra characters and numeric values
pub_place_dtm = pub_place

# Apply tokenization pub_place (1-gram, 2-gram)

# Create doc term matrix

# Evaluate for terms repeating over mean frequency

# Compare 2-grams to 1-grams for each doc

# Pick 2-grams over 1-gram component within each doc

# Create finalized pub_place based on remaining tokens

# Semi-robust technique versus database lookup

# Standardize Column names

# Load - Output file with Standardized column names (.csv / .json)
