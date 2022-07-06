# This program calculates the accuracy of tagger.py by comparing the generated answers to the key. It creates a confusion matrix and then outputs the accuracy and
# confusion matrix to a file
# 
# To use: type "python scorer.py [name of document containing answers] pos-test-key.txt" into the terminal.

import sys
from sklearn.metrics import confusion_matrix
import pandas as pd
import re

def main ():

    # opens and reads the key
    key = open(sys.argv[2])
    key_string = key.read()

    key_string = re.sub(r"[\[\]\n]", "", key_string)

    # tokenizes the key
    key_array = key_string.split()

    # removes empty elements in the array
    key_array = list(filter(None, key_array)) 

    # closes the file
    key.close()

    # opens and reads the tagged test data 
    tagged = open(sys.argv[1])
    tagged_string = tagged.read()
    
    # tokenizes the tagged test data
    tagged_array = tagged_string.split("\n")

    # removes empty elements in the array
    tagged_array = list(filter(None, tagged_array)) 

    # closes the file
    tagged.close()

    total_correct = 0
    total_words = 0

    actual_tags = []
    predicted_tags = []
    tags = []

    # loops through elements in key_array looking for ambiguous tags
    for i in range(0, len(key_array)): 
        
        # if there's an ambiguous tag, get rid of everything after the first tag
        if ('|' in key_array[i]):    
            element = key_array[i].split('|', 1)[0]
            key_array[i] = element

    # loops through the tagged array 
    for i in range(0, len(tagged_array)): 

        # compares the element from the tagged array to the element of key_array and if it's the same, add one to total_correct words
        if (tagged_array[i] == key_array[i]): 
            total_correct += 1
        
        total_words += 1 # increment total number_words

        # creates list of tags for confusion matrix
        tag = tagged_array[i].rsplit("/", 1)[1]
        predicted_tags.append(tag)
        
        tag = key_array[i].rsplit("/", 1)[1]  
        actual_tags.append(tag)

        # if the tag is not already in tags, append to array in order to create a list of tags for the labels of the confusion matrix
        if (tag not in tags):
            tags.append(tag) 

    # calculates the accuracy
    accuracy = total_correct/total_words

    # creates the confusion matrix
    matrix = confusion_matrix(actual_tags, predicted_tags, labels = tags)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    matrix = pd.DataFrame(matrix, index=tags, columns=tags)

    # prints the accuracy and model
    print(str(accuracy)) 
    print(str(matrix))



if __name__ == '__main__':
    main()