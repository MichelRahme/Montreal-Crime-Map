# ------------------------------------------------------- # Assignment 2
# Written by Michel Rahme 40038465
# For COMP 472 Section IX – Summer 2020
# --------------------------------------------------------

import math
from decimal import Decimal
import operator


class Classifier:

    # Task 1 ------------------------------------------------------------------------------------------------
    baseline_path = "baseline-result.txt"
    baseline_file = open(baseline_path, 'w')
    model_path = "model-2018.txt"
    model_file = open(model_path, 'r')

    # # Task 2 ------------------------------------------------------------------------------------------------
    # stopword_file = "stopword-result.txt"
    # stopword = open(stopword_file, 'w')
    # model_path = "stopword_model.txt"
    # model_file = open(model_path, 'r')

    # # Task 3 ------------------------------------------------------------------------------------------------
    # wordlength_file = "wordlength-result.txt"
    # wordlength = open(wordlength_file, 'w')
    # model_path = "wordlength_model.txt"
    # model_file = open(model_path, 'r')

    def __init__(self, list_posts, set_posts, testing_set, stopwords):
        self.true_count = 0  # Count of correctly classified posts
        self.false_count = 0  # Count of wrong classified posts
        self.post_probabilities = {}  # Probability of each type of post: {"story":0.9, "ask-hn":0.3.....}
        self.counter = 0  # Line counter
        self.model_data = []  # Store data from model after reading the file
        for row in self.model_file:
            self.model_data.append(row)
        for p in set_posts:  # Calculate each post probability
            self.post_probabilities[p] = list_posts.count(p) / len(list_posts)
        for title, title_type in testing_set.items():  # Iterate each entry in the testing data
            score = {}
            line_to_print = [str(self.counter), title]
            title = title.split()

            # # Task 2 ------------------------------------------------------------------------------------------------
            # for word in stopwords:
            #     if word in title:
            #         title[:] = (value for value in title if value != word)

            # # Task 3 ------------------------------------------------------------------------------------------------
            # title = [word for word in title if 2 < len(word) < 9]

            for model_type, probability in self.post_probabilities.items():  # Calculate probability of each post type
                score[model_type] = math.log10(probability)
                for word in title:
                    for entry in self.model_data:
                        data = entry.split()
                        if word == data[1]:
                            index = data.index(model_type)
                            d = Decimal(float(data[index + 3]))
                            score[model_type] = score[model_type] + float(d.log10())
            self.counter += 1
            expected_value = next(iter(score.values()))  # check for an empty dictionary first if that's possible
            all_equal = all(value == expected_value for value in score.values())
            if all_equal:
                result = title_type
            else:
                result = max(score.items(), key=operator.itemgetter(1))[0]
            line_to_print.append(result)
            for entry_type, score in score.items():
                line_to_print.append(entry_type + "{" + str(score) + "}")
            line_to_print.append(title_type)
            if result == title_type:
                self.true_count += 1
                line_to_print.append("True")
            else:
                self.false_count += 1
                line_to_print.append("False")

            # Task 1 ----------------------------------------------------------------------------------------------
            for i in line_to_print:
                self.baseline_file.write(i + "  ")
            self.baseline_file.write("\n")

            # # Task 2 ----------------------------------------------------------------------------------------------
            # for i in line_to_print:
            #     self.stopword.write(i + "  ")
            # self.stopword.write("\n")

            # # Task 3 ----------------------------------------------------------------------------------------------
            # for i in line_to_print:
            #     self.wordlength.write(i + "  ")
            # self.wordlength.write("\n")

        print("True Classifications: " + str(self.true_count))
        print("False Classifications: " + str(self.false_count))
        self.model_file.close()
