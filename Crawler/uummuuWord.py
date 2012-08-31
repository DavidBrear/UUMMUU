import MySQLdb;
import re;
#from nltk import PorterStemmer;
from copy import copy;

def append_word(my_list, word):
    '''
        This function is to assume that the word is not in my_list.
        This function does a binary search of the my_list and inserts
        the word into the correct location.
        @author: David Brear.
        @date: 07/29/08.
        @version 29.07.08.1.
    '''
    if(len(my_list) ==0):
        my_list.append(word);
    else:
        start = 0;
        end = len(my_list);
        mid = int(end/2);
        while start+1 < end:
            if(my_list[mid] > word):
                end = mid;
                mid = start + int((end-start)/2);
            else:
                start = mid;
                mid = mid + int((end-start)/2);

        if(my_list[start] > word):
            pos = my_list.index(my_list[start]);
            my_list.insert(pos, word);
        else:
            pos = my_list.index(my_list[start]);
            if(pos == len(my_list)):
                my_list.append(word);
            else:
                my_list.insert(pos+1, word);  
                
def in_array(my_list, word,  type='str'):
    '''
        A boolean function that determines if word is in my_list.
        This function does a boolean search for the word in my_list.
        If the word is in the array, the function returns true.
        Otherwise, the function returns false.

        @author: David Brear.
        @date: 07/29/08.
        @version: 20.10.08.3.
    '''
    if (type == 'int'):
        start = 0;
        end = len(my_list);
        mid = int(end/2);

        if(end==0):
            return False;
        if(int(my_list[mid]) == word):
            return True;
        while(start+1 < end):
            if(int(my_list[mid]) == word):
                return True;
            elif(int(my_list[mid]) > word):
                end = mid;
                mid = start + int((end-start)/2);
            else:
                start = mid;
                mid = mid + int((end-start)/2);
        if(int(my_list[start]) == word):
            return True;
        return False;
    elif(type == 'str'):
        start = 0;
        end = len(my_list);
        mid = int(end/2);

        if(end==0):
            return False;
        if(my_list[mid] == word):
            return True;
        while(start+1 < end):
            if(my_list[mid] == word):
                return True;
            elif(my_list[mid] > word):
                end = mid;
                mid = start + int((end-start)/2);
            else:
                start = mid;
                mid = mid + int((end-start)/2);
        if(my_list[start] == word):
            return True;
        return False;
'''
def get_stem(my_list):
    returned_list = [];
    stemmer = PorterStemmer();
    if(isinstance(my_list, str)):
        my_list = my_list.split();
    for item in my_list:
        returned_list.append(stemmer.stem(item));
    return returned_list;
'''

def create_unique_array(my_list):
    words = [];
    word_weights = {};
    word_freqs = {};
    sorted_list = [];
    if(isinstance(my_list, str)):
        my_list = my_list[1:-1];
        my_list = my_list.split("><");
    for word in my_list:
        term, weight, freq = word.split(',');
        words.append(term);
        word_weights[term] = weight;
        word_freqs[term] = freq;
        #print 'the term is:', term, 'the weight is:', weight, 'it occurs:', freq, 'times.';
        '''
        word = word.replace('\\',  ' ');
        if re.search(r'([^a-z|^A-Z|^0-9|^\\|^/]+)', word):
            temp_word = word;
            matches = re.findall(r'([^a-z|^A-Z|^0-9|^\\|^/]+)', word);
            for match in matches:
                for char in match:
                    temp_word = temp_word.replace(char, '');
            if temp_word.endswith('-'):
                temp_word = temp_word[:-1];
            if temp_word.startswith('-'):
                temp_word = temp_word[1:];
                
            if(len(temp_word) > 1):
                if not in_array(words, temp_word):
                    append_word(words, temp_word);
                    unique_words[temp_word] = 1;
                else:
                    unique_words[temp_word] += 1;
                append_word(sorted_list, temp_word);
        else:
            if word.startswith('-'):
                word = word[1:];
            if word.endswith('-'):
                word = word[:-1];
            if(len(word) > 1):
                if not in_array(words, word):
                    append_word(words, word);
                    unique_words[word] = 1;
                else:
                    unique_words[word] += 1;
                append_word(sorted_list, word);
    return words, unique_words, sorted_list;
        '''
    return words,  word_weights,  word_freqs;

def find_difference(doc_id, repos, updated):
    '''
        find_differences is a function that determines what index entries need to be changed.
        The function checks the words currently in the repository of words associated with
        this document and compares the words that were in the document to the words that
        are in the document.
            This is necessary because certain words will appear and/or disappear as the site is
        updated.

            @param: repos - array - a sorted array of the words this page had at last update.
            @param: updated - array - a sorted array of the words this page currently has.
            @author: David  Brear
            @date: 08/10/2008 9:14PM
            @version: 10.08.08.2
    '''
    if type(repos) == str:
        repos = repos.split();
    if type(updated) == str:
        updated = updated.split();
    add_list = [];
    remove_list = [];
    if len(repos) > len(updated):
        long_list = copy(repos);
        short_list = copy(updated);
        for item in short_list:
            if item in long_list:
                long_list.remove(item);
            else:
                add_list.append(item);
        for item in long_list:
            remove_list.append(item);
    else:
        long_list = copy(updated);
        short_list = copy(repos);
        for item in short_list:
            if item in long_list:
                long_list.remove(item);
            else:
                remove_list.append(item);
        for item in long_list:
            add_list.append(item);
    return add_list, remove_list;

def add_to_index(entry, doc_id, weight, occ, in_title):
    if(re.search(r'<'+str(doc_id)+',(\d)*,(\d)*,(\d)*>',  entry)):
        return entry;
    my_entry = copy(entry[1:-1]).split('><');
    mid = int(len(my_entry)/2);
    end = len(my_entry);
    start = 0;
    if(end == 0 or len(entry)==0):
        entry = '<'+str(doc_id)+','+str(weight)+','+str(occ)+','+str(in_title)+'>';
        return entry;
    while start+1 < end:
        if(int(my_entry[mid].split(',')[0]) > doc_id):
            if(int(my_entry[mid-1].split(',')[0]) < doc_id):
                entry = entry.replace('<'+str(my_entry[mid])+'>', '<'+str(doc_id)+','+str(weight)+','+str(occ)+','+str(in_title)+'><'+str(my_entry[mid])+'>');
                return entry;
            else:
                end = mid;
                mid = int(end/2);
        else:
            if mid+1 < end:
                if(int(my_entry[mid+1].split(',')[0]) > doc_id):
                   entry = entry.replace('<'+str(my_entry[mid])+'>', '<'+str(my_entry[mid])+'><'+str(doc_id)+','+str(weight)+','+str(occ)+','+str(in_title)+'>');
                   return entry;
                else:
                    start = mid;
                    mid = start + int((end-start)/2);
            else:#if(int(my_entry[mid].split(',')[0]) > doc_id):
                entry = entry.replace('<'+str(my_entry[mid])+'>', '<'+str(my_entry[mid])+'><'+str(doc_id)+','+str(weight)+','+str(occ)+','+str(in_title)+'>');
                return entry;
    if(int(my_entry[start].split(',')[0]) < doc_id):
        return entry+'<'+str(doc_id)+','+str(weight)+','+str(occ)+','+str(in_title)+'>';
    else:
        return '<'+str(doc_id)+','+str(weight)+','+str(occ)+','+str(in_title)+'>'+entry;

def overlap_list(list1,  list2):
    '''
        overlap_list returns a list of the documents that have two terms in them
        @param: list1 is a list of the documents that have word1 in them.
        @param: list2 is a list of the documents that have word2 in them.
    '''
    overlapped_list = '';
    if len(list1) < len(list2):
        new_list = list1[1:-1];
        split_list = new_list.split('><');
        for ele in split_list:
            doc_num = ele.split(',')[0];
            exists = re.search('<'+str(doc_num)+',(\d)*>', list2);
            if exists and int(exists.group(1)) > 0:
                overlapped_list = overlapped_list + '<'+str(doc_num)+'>';
    else:
        new_list = list2[1:-1];
        split_list = new_list.split('><');
        for ele in split_list:
            doc_num = ele.split(',')[0];
            exists = re.search('<'+str(doc_num)+',(\d)*>', list1);
            if exists and int(exists.group(1)) > 0:
                overlapped_list = overlapped_list + '<'+str(doc_num)+'>';
            
    return overlapped_list;

#a simple holding class#
class Document:
    def __init__(self):
        self.id = -1;
        self.words = [];
        self.unique_words = {};
        self.sorted_words = [];
        self.url = '';
