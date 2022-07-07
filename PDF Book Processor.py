# -*- coding: utf-8 -*-
"""
This document processes PDF files.
1- The book is found in the local directory, then ensures there is just 1 book
2- Open and store PDF book contents into Python using PyPDF2
3- Extracts book pages into array
4- Array turned into lower-case string
5- Counts words by breaking up the book string into a list of words
6- Counts letters by removing whitespace from book string
7- Counts characters by keeping whitespace from book string
8- Counts most common word 
9- Counts most common letter
10-Calculates frequency of desired word
"""

import os
import PyPDF2 
import re
from collections import Counter


def file_search():
    global PDF_read, number_of_pages

    directory = os.getcwd() #gets current directory name
    files = os.listdir(directory) #gets all files in directory

    desired_file = [i for i in files if not '.py' in i] #find items that are not python files
    if len(desired_file) == 1:
        book_name = "".join(desired_file) #turn list to string since we have 1 file
    else:
        quit() #if we have >1 viable files, stop running this code
    print("The book is: \"{}\" \n".format(  book_name  )) #prints the book name
    
    bookhandle = open(book_name, 'rb') #creates a book handle (not text yet)
    PDF_read = PyPDF2.PdfFileReader(bookhandle) #reads the handle (not text yet)
    number_of_pages = len(PDF_read.pages) #gets the number of pages
    print('Loading book... \n')

def book_processing(number_of_pages):
    global book_no_space, book_by_words, book_string
    
    page_handle = [None] * number_of_pages #initializes the variable
    page_text = [None] * number_of_pages #initializes the variable
    
    for i in range( number_of_pages ):#number_of_pages
        page_handle[i] = PDF_read.pages[i] #creates page handle (not text yet)
        page_text[i] = page_handle[i].extractText().replace("\n", " ") #extracts text from page handle. Replaces newlines with a space
    
    book_string = ' '.join(page_text).lower() #gives the entire book in one lower case string, separates pages with a space
    book_no_space = book_string.replace(' ', '') #remove whitespace from book
    book_by_words = re.findall(r'\w+', book_string) #turns book string into list of words, considers punctuation
    print('Book successfully copied to Python!')
    print('Book has:')
    print('- {} pages'.format( number_of_pages ))
    # return(book_no_space, book_by_words)

def number_words(book_by_words):
    # book_by_words = book_string.split(' ') #splits the book into individual words, does NOT consider punctuation
    number_of_words = len(book_by_words) #how many words in the book
    print('- {} words'.format( number_of_words )) #number of words

def number_letters(book_no_space):
    number_of_letters = len(book_no_space) #gives number of letters
    print('- {} letters'.format( number_of_letters )) #number of letters

def number_characters(book_string):
    number_of_characters = len(book_string) #gives number of characters
    print('- {} characters'.format( number_of_characters )) #number of characters

def common_words_letters(number_words, number_letters, book_by_words, book_no_space):
    common_words_occur = Counter(book_by_words).most_common(number_words) # gives (top word, frequency) tuple
    top_words = [ i[0] for i in common_words_occur ] #change to top word (removes the frequency)
    print('Most common words: {}'.format( ", ".join(top_words) )) #put common words in sentence
    
    common_letters_occur = Counter(book_no_space).most_common(number_letters) # gives (letter, frequency) tuple
    top_letters = [ i[0] for i in common_letters_occur ] #change to top letter (removes the frequency)
    print('Most common letters: {}'.format( ", ".join(top_letters) )) #put common letter in sentence

def word_frequency(book_string, desired_word):
    desired_word.lower() # we made the book in all lower case previously
    instance = book_string.count(desired_word)  #counts from a string
    # instance2= Counter(book_by_words).get(desired_word) #counts from a list (does not work)
    # print(instance2)
    print('The word \'{}\' is mentioned {} times'.format( desired_word.capitalize(), instance))


file_search()
book_processing(number_of_pages)
number_words(book_by_words)
number_letters(book_no_space)
number_characters(book_string)
common_words_letters(5, 5, book_by_words, book_no_space)
word_frequency(book_string, 'mate')