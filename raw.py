
# coding: utf-8

# In[301]:


import xlrd
import pandas as pd
import numpy as np
import json


# In[302]:


df = pd.read_excel('input/youth_survey_raw.xlsx')

# get question ids from columns
question_ids = [ c for c in df.columns if 'Q' in c ]

# copy row 0 to column names
df.columns = df.iloc[0]

# delete row 0
df = df.drop(0, axis=0)
df = df.applymap(str)


# In[303]:


# compile list of question_columns - could be neater!
question_columns = []

for c in df.columns:
    for q_id in question_ids:
        if q_id in c:
            question_columns.append(c)


# In[304]:


# for each Governorate and District pair...
# show how many records in this pair
# for key, df_ in df.groupby( ['M2: Governorate', 'M3: District'] ):
#     print(key)
#     print( len(df_) )



# In[305]:


# for each Governorate and District pair...
# show answers to questions
# M2: Governorate
# M3: District

def makeJSON(group, kind):
    
    for key, df_ in df.groupby( [group] ):
        overall_data = []
        df_ = df_.fillna('N/A')

        for q in question_columns:

            values_list = []

            unique, counts = np.unique(df_[q].values, return_counts=True)

            for q_, c in zip(unique, counts):
                values = {"answer": q_, "count": str(c)}
                values_list.append(values)


            if len(q.split(':')) > 1:
                q = q.split(':')[1].strip()

            if q != "Other":
                q_dict = {
                    "gov": key,
                    "question_en": q,
                    "values": values_list
                }

                overall_data.append(q_dict)


            with open('output/'+kind+'/'+key.lower()+'.json', 'w') as outfile:
                json.dump(overall_data, outfile)
        
makeJSON('M2: Governorate', 'gov')
makeJSON('M3: District', 'district')

