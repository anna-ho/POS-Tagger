# This program is a most likely tagger that uses training data to assign tags to each word. Using those tags, along with five rules 
# additional rules, it tags a test data set and outputs that information into a file named 'pos-test-with-tags.txt'. 
# 
# To use: type "python tagger.py pos-train.txt pos-test.txt > [name of document containing answers]" into the terminal
# 
# Rules:  
# Digit rule: If the word contained only numbers, assign it the tag CD for cardinal numbers. 
# Adverb rule: If the last two letters of the word were ‘ly’, assign it the tag RB for adverbs. 
# Superlative rule: If the last three letters of the word were ‘est’, assign it the tag JJS for superlative adjectives. 
# Plural rule: If the last two letters were ’s’, assign it the tag NNS for plural nouns. 
# Proper noun rule: If the first letter of the word is upper case, assign it the tag NNP for singular proper nouns.
# 
# Accuracy of the most likely tagger and each individual rule: 
# Most likely tagger: 0.843214895376872
# Digit rule: 0.8451331327103462
# Adverb rule: 0.8449923446491737
# Superlative rule: 0.8433204864227514
# Plural rule: 0.8553226686376996
# Proper noun rule: 0.8824771659363286

import sys

def main ():

    word_dict = {}
    tag_dict = {}
    freq_table = {}  
    most_likely_tag = {}

    # opens and reads the training data
    train = open(sys.argv[1])
    train_string = train.read()
    
    # tokenizes the training data
    train_string = train_string.replace("[", "" )
    train_string = train_string.replace("]", "" )
    train_string = train_string.replace("\n", "")

    train_array = train_string.split(" ")
    train_array = list(filter(None, train_array)) # removes empty elements in the array

    # closes the file
    train.close()

    # loops through each element of train_array and creates the word_dict and tag_dict
    for element in train_array:
        
        # split each element of the train_array into a word and its tag
        temp = element.split("/")
        word = temp[0]
        tag = temp[1]

        # if there is a '|' that means there is more than one tag, so we split it and just use the first tag
        if ('|' in tag): 
            tag = tag.split('|', 1)[0]

        # increments the number of times we see the word overall
        if (word in word_dict): 
            word_dict[word] += 1
        else:
            word_dict[word] = 1

        # increments the number of times we see the word with that tag
        if (word in tag_dict):  
            if (tag in tag_dict[word]):  
                tag_dict[word][tag] += 1
            else: 
                tag_dict[word][tag] = 1
        else: 
            tag_dict[word] = {}
            tag_dict[word][tag] = 1
    
    # loops through each word in tag_dict and calculates the frequency of each tag
    for word in tag_dict:
        
        freq_table[word] = {} 
        
        # calculates the probability of that tag appearing and how many times the word appeared in general
        for tag in tag_dict[word]: 
            freq_table[word][tag] = tag_dict[word][tag]/word_dict[word]
    
    # assigns the most likely tag to a word based on whichever tag has the highest frequency
    for word in freq_table:
        
        freq = 0
        
        for tag in freq_table[word]: 
            if (freq_table[word][tag] > freq): 
                freq = freq_table[word][tag]
                most_likely_tag[word] = tag

    # opens and reads the test data
    test = open(sys.argv[2])
    test_string = test.read()

    # tokenizes the test data
    test_string = test_string.replace("[", "" )
    test_string = test_string.replace("]", "" )
    test_string = test_string.replace("\n", "")

    test_array = test_string.split(" ")
    test_array = list(filter(None, test_array)) # removes empty elements in the array

    # closes the file
    test.close()

    tagged_test_dict = {}
    tagged_test_string = ""

    # loops through the test array and assigns a tag to each word
    for word in test_array:
        # looks for the word in the most_likely_tag dict and assigns that word's tag to the word in test_array
        if (word in most_likely_tag):
            tagged_test_dict[word] = most_likely_tag[word]
        # if the word contains all numbers, assume it's a cardinal number
        elif (word.isdigit()):
            tagged_test_dict[word] = 'CD' 
        # if the last two letters are 'ly', assume it's an adverb
        elif (word[-2:] == 'ly'): 
            tagged_test_dict[word] = 'RB'
        # if the last three letters are 'est', assume it's a superlative adjective
        elif (word[-3:] == 'est'):
            tagged_test_dict[word] = 'JJS'
        # if the last two letters are 'es', assume it's plural
        elif (word[-1:] == 's'): 
            tagged_test_dict[word] = 'NNS'
        # if the first letter of the word is capitalized, assume it's a proper noun
        elif(word[0].isupper()): 
            tagged_test_dict[word] = 'NNP'
        # if the word isn't in the dictionary, assume it's a noun
        else: 
            tagged_test_dict[word] = 'NN'

    # formats the tagged test data to be printed
    for i in range(0, len(test_array)):
        
        word = test_array[i]
        
        # doesn't add a \n character if the word is the last word in the array
        if (i != len(test_array) - 1):    
            tagged_test_string += word + "/" + tagged_test_dict[word] + "\n"
        else: 
            tagged_test_string += word + "/" + tagged_test_dict[word]

    print(tagged_test_string)


if __name__ == '__main__':
    main()
