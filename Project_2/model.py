# ------------------------------------------------------- # Assignment 2
# Written by Michel Rahme 40038465
# For COMP 472 Section IX – Summer 2020
# --------------------------------------------------------

import collections


class Model:
    vocab_path = "vocabulary.txt"
    removed_words_path = "removed_words.txt"
    model_path = "model-2018.txt"

    vocab_file = open(vocab_path, 'w')
    removed_words_file = open(removed_words_path, 'w')
    model_file = open(model_path, 'w')

    # # Task 2 ----------------------------------------------------------------------------------------------
    # stopword_model = "stopword_model.txt"
    # stopword_file = open(stopword_model, 'w')

    # # Task 3 ----------------------------------------------------------------------------------------------
    # wordlength_model = "wordlength_model.txt"
    # wordlength_file = open(wordlength_model, 'w')

    def __init__(self, counts, vocab):
        self.counts = counts
        self.vocab = collections.OrderedDict(sorted(vocab.items()))
        self.counter = 0
        self.print_vocab()
        self.print_model()

    def print_vocab(self):
        for word in self.vocab.keys():
            self.vocab_file.write(word + "\n")
        self.vocab_file.close()

    def print_model(self):
        for word in self.vocab.keys():
            model_entry = [str(self.counter), word]

            for g, v in self.counts.items():

                if word not in v.keys():
                    model_entry.append(g)
                    model_entry.append("{")
                    model_entry.append("0")
                    model_entry.append(str(round(0.5 / (len(v) + (len(self.vocab.keys()) * 0.5)), 8)))
                    model_entry.append("}")
                else:
                    for k, i in v.items():
                        if word == k:
                            model_entry.append(g)
                            model_entry.append("{")
                            model_entry.append(str(i))
                            model_entry.append(str(round((i + 0.5) / (len(v) + (len(self.vocab.keys()) * 0.5)), 8)))
                            model_entry.append("}")
            self.counter += 1

            # Task 1 ----------------------------------------------------------------------------------------------
            for i in model_entry:
                self.model_file.write(i + "  ")
            self.model_file.write("\n")

            # # Task 2 ----------------------------------------------------------------------------------------------
            # for i in model_entry:
            #     self.stopword_file.write(i + "  ")
            # self.stopword_file.write("\n")

            # # Task 3 ----------------------------------------------------------------------------------------------
            # for i in model_entry:
            #     self.wordlength_file.write(i + "  ")
            # self.wordlength_file.write("\n")

        self.model_file.close()

    def print_removed(self):
        self.removed_words_file.write("! @ # $ % % ^ & * ( ) + _ { } [ ] \ | ' \" : ; ? / > . < , ` ~ • ¥ € 1 2 3 4 5 "
                                      "6 7 8 9 -")
        self.removed_words_file.close()
