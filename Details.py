# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 21:24:45 2019

@author: bhavy
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:32:01 2019

@author: bhavy
"""
import Extract_Email_Title
import docx2txt
import re
import en_core_web_sm

def Extract_Details(t):
    nlp = en_core_web_sm.load()
    
    my_text = docx2txt.process(t)
    doc=nlp(my_text)

    
    out = [[X.text, X.label_] for X in doc.ents]
    
    email=Extract_Email_Title.email(t)
    k=0           
    i=0
    j=0
    person_name=[]
    org_name=[]
    if len(email)>2:
        while j<len(out):
            if out[j][1]=="PERSON":
                if i<len(email):
                    person_name.append(out[j][0])
                    j+=1
                    i+=1
                else:
                    j+=1
            elif out[j][1]=="ORG":
                if k<len(email):
                    org_ext=[]
                    org_ext.append(out[j][0])
                    while out[j+1][1]=="ORG":                
                        org_ext.append(out[j+1][0])
                        j+=1
                    org_name.append(",".join(org_ext))
                    j+=1
                    k+=1
                else:
                    j+=1
            else:
                j+=1
    else:
        while j<len(out):
            if out[j][1]=="PERSON":
                if i<2:
                    person_name.append(out[j][0])
                    j+=1
                    i+=1
                else:
                    j+=1
            elif out[j][1]=="ORG":
                if k<2:
                    org_ext=[]
                    org_ext.append(out[j][0])
                    while out[j+1][1]=="ORG":                
                        org_ext.append(out[j+1][0])
    
                        j+=1
                    org_name.append(",".join(org_ext))
                    j+=1
                    k+=1
                else:
                    j+=1
            else:
                j+=1
    return person_name ,org_name

def check_tags(t):
    nlp = en_core_web_sm.load()
    
    my_text = docx2txt.process(t)
    doc=nlp(my_text)
    
    out = [[X.text, X.label_] for X in doc.ents]
    
    return out
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    