
# coding: utf-8

# In[140]:


import xlrd
import pandas as pd
import numpy as np


# In[144]:


import pandas as pd

df = pd.read_excel('youth_survey_raw.xlsx')

# get question ids from columns
question_ids = [ c for c in df.columns if 'Q' in c ]

# copy row 0 to column names
df.columns = df.iloc[0]

# delete row 0
df = df.drop(0, axis=0)

# compile list of question_columns - could be neater!
question_columns = []

for c in df.columns:
    for q_id in question_ids:
        if q_id in c:
            question_columns.append(c)


# for each Governorate and District pair...
# show how many records in this pair
# for key, df_ in df.groupby( ['M2: Governorate', 'M3: District'] ):
#     print(key)
#     print( len(df_) )


# for each Governorate and District pair...
# show answers to questions
for key, df_ in df.groupby( ['M2: Governorate', 'M3: District'] ):
#     print(key)
#     print( len(df_) )
#     print()
    
    
    for q in question_columns:
        print(key)
        print(q)
        print(df_[q].values)
        
        print()

