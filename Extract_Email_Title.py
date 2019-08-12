# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:21:36 2019

@author: bhavy
"""
import re
import docx2txt
import en_core_web_sm
import docx
from nltk import Tree
import nltk
from nltk.corpus import stopwords


def email(t):
    my_text = docx2txt.process(t)
    text = re.sub('[^a-zA-Z:\n-.,()1-9\'\"%:]', ' ',my_text)
    abstract_pos=re.search('(Abstract|ABSTRACT)( )*(\n|:|-)',text)
    if type(abstract_pos)==re.Match:
        my_text=my_text[:abstract_pos.start()]
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+[.a-z]+", my_text)
        emails = list(dict.fromkeys(emails))
    else:
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+[.a-z]+", my_text)
        emails = list(dict.fromkeys(emails))
    
    return emails
    
def position_of_name(my_text):
    
    my_text=my_text.split("\n")
    
    while("" in my_text) :    
        my_text.remove("") 
        
    sentences = [nltk.word_tokenize(sent) for sent in my_text]
    
    pos_in_new_words = [nltk.pos_tag(sent) for sent in sentences]
        
    grammar = "NAM: {<NNP><NNP>+}"
    cp = nltk.RegexpParser(grammar)
    
    result=[]
    i=0
    while i <len(pos_in_new_words):
        result.append(cp.parse(pos_in_new_words[i]))
        i+=1

    names = []
    for w in result:
        for abc in w:
            if type(abc) == nltk.tree.Tree:
                names.append(' '.join([c[0] for c in abc]))
    my_text="\n".join(my_text)
    if len(names)>0:
        s="("+names[0]+")( )*(\w){,1}(\*){,1}(,)"
        pos=re.search(s,my_text)
    else:
        pos=""
    if type(pos)==re.Match:
        title=my_text[:pos.start()]
        return title
    else:
        return my_text

def title(file_name):
    def getText(filename):
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    my_text=getText(file_name)
    text = re.sub('[^a-zA-Z:\n-.,()1-9\'\"%:]', ' ',my_text)
    text = re.sub('[1-9]\*', '',my_text)
    
    abstract_pos=re.search('(Abstract|ABSTRACT)( )*(\n|:|-)',text)
    intro_pos=re.search(u'(Introduction|INTRODUCTION)( )*(\n|:|-)',text)
    if type(abstract_pos)==re.Match:
        my_text=text[:abstract_pos.start()]
    elif type(intro_pos)==re.Match:
        my_text=text[:intro_pos.start()]
    else:
        my_text=my_text.split("\n")[:3]
        my_text="\n".join(my_text)
    authors_pos=re.search(u'(AUTHOR|Author)(s|S){,1}( )*(\n|:|-)',my_text)
    if type(authors_pos)==re.Match:
        my_text=text[:authors_pos.start()]
    title=position_of_name(my_text)
    return title
