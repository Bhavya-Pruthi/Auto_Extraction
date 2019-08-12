# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 18:46:02 2019

@author: bhavya
"""

import docx2txt
import re
from nltk.corpus import stopwords

def FindAbstract(position):
    i=0
    for tuples in position:
        if tuples[1].lower()=="abstract":
            return i
        else:
            i+=1
def FindKeyWords(position):
    i=0
    for t_key in position:
        if t_key[1].lower()=="keyword":
            return i
        elif t_key[1].lower()=="key word":
            return i         
        else:
            i+=1

def keyword_exist(keyword_order,my_text,position,keyword_pos):
    if keyword_order<len(position)-1:
        potential_keywords=my_text[keyword_pos.end():position[keyword_order+1][0]].strip()
    else:
        end=keyword_pos.end()+200
        potential_keywords=my_text[keyword_pos.end():end].strip()
    keyword_summary=potential_keywords.split("\n")[0]
    return keyword_summary
    
def lc_remove(text): 
        return ' '.join(word for word in text.split() if len(word)>4)
    
def get_top_n2_words(corpus, n=None):
    from sklearn.feature_extraction.text import CountVectorizer
    stop = stopwords.words('English')
    vec1 = CountVectorizer(ngram_range=(2,3),max_df=0.8,
                max_features=2000,stop_words=stop).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec1.vocabulary_.items()]
    words_freq =sorted(words_freq,key = lambda x: x[1],reverse=True)
    return words_freq[:n]

def none_keyword(strin):
    my_text=re.sub('[()]'," ",strin)

    my_text=my_text.split("\n")
    corpus=[]
    for abc in my_text:
        text=lc_remove(abc)
        corpus.append(re.sub('[^a-zA-Z0-9]', ' ',text).lower())
    
    keywords_list= get_top_n2_words(corpus, n=20)  
    keywords_summary=[]
    for abc in keywords_list:
        keywords_summary.append(abc[0])
    return keywords_summary[0:5]

def Extract_Abstract_Keyword(t):
    my_text = docx2txt.process(t)
    text = re.sub('[^a-zA-Z:\n-.,()1-9\'\"%:]', ' ',my_text)
    
    abstract_pos=re.search('(Abstract|ABSTRACT)( )*(\n|:|-)',text)
    intro_pos=re.search(u'(Introduction|INTRODUCTION)( )*(\n|:|-)',text)
    keyword_pos=re.search('(Key words|KEY WORDS|Key Words|Keywords|KEYWORDS)( )*(\n|:|-)',text)
    
    position=[]
    
    if type(abstract_pos) == re.Match:
        position.append((abstract_pos.end(),"Abstract"))
        
    
    if type(intro_pos) == re.Match:
       position.append((intro_pos.start(),"Introduction"))
    
    if type(keyword_pos) == re.Match:
        position.append((keyword_pos.start(),"Keyword"))
        
    position.sort()
    
    
    abstract_order=FindAbstract(position)
    if type(abstract_order)!=int:
        Abstract_Summary="Abstract not present"
    elif abstract_order==len(position)-1:
        text2=my_text[position[abstract_order][0]:].strip()
        abstr_summary=text2.split(".")[:3]
        Abstract_Summary=".".join(abstr_summary)
        Abstract_Summary=Abstract_Summary+"."
    
    else:
        Abstract_Summary=my_text[position[abstract_order][0]:position[abstract_order+1][0]].strip()
 
    keyword_order=FindKeyWords(position)

    if type(keyword_order)!=int:
        keyword_summary=none_keyword(my_text)
    else:    
        keyword_summary=keyword_exist(keyword_order,my_text,position,keyword_pos)
    
    return keyword_summary,Abstract_Summary



























