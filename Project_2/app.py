# ------------------------------------------------------- # Assignment 2
# Written by Michel Rahme 40038465
# For COMP 472 Section IX – Summer 2020
# --------------------------------------------------------

import csv
from post import *
from model import *
from classifier import *
from collections import Counter

data_path = "hns_2018_2019.csv"

data_file = open(data_path, newline='')

reader = csv.reader(data_file)
header = next(reader)  # First line in the file

stopwords_path = "stopwords.txt"
stopwords_file = open(stopwords_path, 'r')

data = []  # Store data read from CSV file. Used to read CSV file only once.
set_types_2018 = set()  # Store different post types
list_types_2018 = []
vocab = Counter()  # Store Vocabulary
word_counts = {}  # Store counts of words in each type
posts_2019 = {}
stopwords = []

# loop through file, save the data, get all different Post Types
for row in reader:
    data.append(row)
    if int(row[5][0:4]) == 2018:
        set_types_2018.add(row[3])
        list_types_2018.append(row[3])

# initialize counter for each Post Type
for post_type in set_types_2018:
    word_counts[post_type] = Counter()

for word in stopwords_file:
    word_clean = re.sub(r'\n', '', word).lower()
    stopwords.append(word_clean)

# loop through data, get posts, then populate vocabulary and counts
for row in data:
    post = Post(row[2], row[3], row[5])

    # # Task 2 ------------------------------------------------------------------------------------------------
    # for word in stopwords:
    #     if word in post.title:
    #         post.title[:] = (value for value in post.title if value != word)

    # # Task 3 ------------------------------------------------------------------------------------------------
    # post.title = [word for word in post.title if 2 < len(word) < 9]

    if post.date == 2018:
        vocab.update(post.title)
        word_counts[post.post_type].update(post.title)
    if post.date == 2019:
        posts_2019[re.sub(r'[^a-zA-Z\s]', '', row[2]).lower()] = post.post_type

Model(word_counts, vocab)
Classifier(list_types_2018, set_types_2018, posts_2019, stopwords)

data_file.close()
