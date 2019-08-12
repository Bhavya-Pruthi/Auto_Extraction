# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 21:12:36 2019

@author: bhavya
"""

import Abstract_Keywords 
import Pages_Table_Fig 
import Details
import Extract_Email_Title
file_name="CM_for_DD_DSP_Main_Document_10_xyz10868197e8315.docx"
t=file_name
Table,Figure,Pg_no=Pages_Table_Fig.No_Pages_Tables_Figs(file_name)

Key_words,Abstract_summary=Abstract_Keywords.Extract_Abstract_Keyword(file_name)
Name,Org=Details.Extract_Details(file_name)

Email=Extract_Email_Title.email(file_name)
title=Extract_Email_Title.title(file_name)


tag=Details.check_tags(file_name)




