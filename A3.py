# -*- coding: utf-8 -*-
"""A3

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xriOBNu2Koyhs81nw8_mOYdM2cCQKSb7
"""

import pandas as pd
import re
import os

path = "/content/drive/MyDrive/PRML A-3/SMSSpamCollection"
dataset = pd.read_csv(path, sep='\t',
header=None, names=['Label', 'Email'])

print(dataset.shape)

ds = dataset.sample(frac=1, random_state=1)
idx = round(len(ds)*0.8)
train_data = ds[:idx].reset_index(drop=True)
test_data = ds[idx:].reset_index(drop=True)

train_data['Email'] = train_data['Email'].str.replace('\W', ' ')
train_data['Email'] = train_data['Email'].str.lower()
print(train_data.head(5))

train_data['Email'] = train_data['Email'].str.split()
unique_words = []

for email in train_data['Email']:
  for word in email:
    unique_words.append(word)

unique_words = list(set(unique_words))

print(len(unique_words))

word_cnt = {word : [0]*len(train_data['Email']) for word in unique_words}

for i,email in enumerate(train_data['Email']):
  for word in email:
    word_cnt[word][i] += 1
word_cnt = pd.DataFrame(word_cnt)

cleaned_train = pd.concat([train_data, word_cnt], axis=1)
print(cleaned_train.head())

spam = cleaned_train[cleaned_train['Label']=='spam']
ham = cleaned_train[cleaned_train['Label']=='ham']

p_spam = len(spam)/len(cleaned_train)
p_ham = len(ham)/len(cleaned_train)

num_spam = spam['Email'].apply(len).sum()
num_ham = ham['Email'].apply(len).sum()
num_unique_words = len(unique_words)

a = 1
param_spam = {word:0 for word in unique_words}
param_ham = {word:0 for word in unique_words}
for word in unique_words:
  param_spam[word] = (spam[word].sum() + a)/(num_spam + a*num_unique_words)
  param_ham[word] = (ham[word].sum() + a)/(num_ham + a*num_unique_words)

def classify(email):
   email = re.sub('\W', ' ', email)
   email = email.lower().split()

   p_spam_given_email = p_spam
   p_ham_given_email = p_ham

   for word in email:
      if word in param_spam:
         p_spam_given_email *= param_spam[word]
      if word in param_ham: 
         p_ham_given_email *= param_ham[word]

  #  print('P(Spam|Email):', p_spam_given_email)
  #  print('P(Ham|Email):', p_ham_given_email)

   if p_ham_given_email > p_spam_given_email:
      return 'ham'
   else:
      return 'spam'

test_data['prediction'] = test_data['Email'].apply(classify)
print(test_data.head())

cnt_correct = 0
total = test_data.shape[0]
for row in test_data.iterrows():
   row = row[1]
   if row['prediction'] == row['Label'] :
      cnt_correct += 1
print('Accuracy:', cnt_correct/total)

test_path = "/content/drive/MyDrive/PRML A-3/test"    #path to 'test' folder
os.chdir(test_path)

for file in os.listdir():
  if file.endswith(".txt"):
    file_path = f"{test_path}/{file}"
    with open(file_path, 'r') as f:
      s = f.read()
      # print(s)
      if classify(s) == 'spam':
        print("1(Spam)")
      else:
        print("0(Ham)")

