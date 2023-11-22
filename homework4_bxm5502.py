############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Ben Mashkevich"

############################################################
# Imports
############################################################

import email
from email.iterators import body_line_iterator
from collections import defaultdict
import math
import os
import heapq

############################################################
# Section 1: Spam Filter
############################################################


def load_tokens(email_path):
    toke = []
    try:
        with open(email_path, 'r', encoding='utf-8', errors='ignore') as f:
            mess = email.message_from_file(f)
            for line in email.iterators.body_line_iterator(mess):
                toke.extend(line.split())
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return toke


def log_probs(email_paths, smoothing):
    counter = defaultdict(int)
    total = 0
    for email_path in email_paths:
        tokens = load_tokens(email_path)
        for token in tokens:
            counter[token] += 1
            total += 1
    size = len(counter)
    probs = {}
    for word, count in counter.items():
        perc = (count + smoothing) / (total + smoothing * (size + 1))
        probs[word] = math.log(perc)
    unk = smoothing / (total + smoothing * (size + 1))
    probs["<UNK>"] = math.log(unk)
    return probs


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        s_paths = [os.path.join(spam_dir, email) for email in os.listdir(spam_dir)]
        h_paths = [os.path.join(ham_dir, email) for email in os.listdir(ham_dir)]
        self.s_probs = log_probs(s_paths, smoothing)
        self.h_probs = log_probs(h_paths, smoothing)
        total_emails = len(s_paths) + len(h_paths)
        self.p_spam = len(s_paths) / total_emails
        self.p_ham = len(h_paths) / total_emails

    def is_spam(self, email_path):
        tokes = load_tokens(email_path)
        s_prob = math.log(self.p_spam)
        h_prob = math.log(self.p_ham)
        for toke in tokes:
            if toke in self.s_probs:
                s_prob += self.s_probs[toke]
            else:
                s_prob += self.s_probs["<UNK>"]
            if toke in self.h_probs:
                h_prob += self.h_probs[toke]
            else:
                h_prob += self.h_probs["<UNK>"]
        return s_prob > h_prob

    def most_indicative_spam(self, n):
        indic = []
        for word in self.s_probs:
            if word in self.h_probs:
                func = (math.exp(self.s_probs[word]) * self.p_spam + math.exp(self.h_probs[word]) * self.p_ham) / (self.p_spam + self.p_ham)
                value = self.s_probs[word] - math.log(func)
                indic.append((value, word))
        top = heapq.nlargest(n, indic)
        return [word for _, word in top]

    def most_indicative_ham(self, n):
        indic = []
        for word in self.h_probs:
            if word in self.s_probs:
                func = (math.exp(self.s_probs[word]) * self.p_spam + math.exp(self.h_probs[word]) * self.p_ham) / (self.p_spam + self.p_ham)
                value = self.h_probs[word] - math.log(func)
                indic.append((value, word))
        top = heapq.nlargest(n, indic)
        return [word for _, word in top]


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Around 8-10 hours
"""

feedback_question_2 = """
Nothing was too challenging here. It was definitely the shortest code to write 
this semester and I really didn't struggle with much here.
"""

feedback_question_3 = """
Similar to the others I just liked seeing the output of Spam Filter. I never feel
like I've truly learned anything until I can create and see a correct output.
"""
