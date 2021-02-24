# ------------------------------------------------------- # Assignment 2
# Written by Michel Rahme 40038465
# For COMP 472 Section IX – Summer 2020
# --------------------------------------------------------

import re


class Post:

    # Class representing each POST
    def __init__(self, title, post_type, date):
        self.title = re.sub(r'[^a-zA-Z\s]', '', title).lower().split()  # Clean titles. Keep letters only
        self.post_type = post_type  # Post Type
        self.date = int(date[0:4])  # Store Year of post (int, ex: 2018)
