import pandas as pd
import json
import csv

# detail formatting
question_cols = ['id', 'governorate', 'question_tag', 'question_tag_order', 'question_raw', 'question_en', 'question_ar']
answer_cols = ['answer_raw', 'answer_en', 'answer_ar', 'answer_rank', 'answer_count', 'answer_pct']

def build_detail_dict(df_):
    df_ = df_.fillna('')
    result = {
        c: df_[c].values[0] for c in question_cols
    }

    result['values'] = []
    for _, row in df_.groupby('answer_raw'):
        result['values'].append({
            c: row[c].values[0] for c in answer_cols        
        })

    return result


inFile = 'output/ypc_edit.csv'
detailPath = 'output/gov/'
mapFile = 'output/map.json'

detailpage_df = pd.read_csv(inFile)

for key, df_ in detailpage_df.groupby( ['id'] ):
    results = []
    for id_, df__ in df_.groupby('question_raw'): 
        results.append( build_detail_dict(df__) )
   
    with open(detailPath + 'gov_'+str(key)+'.json', 'w') as outfile:
        print (detailPath + 'gov_'+str(key)+'.json')
        json.dump(results, outfile, default=str)







# map formatting     
map_df = detailpage_df[detailpage_df['question_map'] == 'y']

def build_map_dict(df_):
    answer_ranks = []
    answer_pcts = []
    
    for _, row in df_.groupby('answer_raw'):
        if row['answer_rank'].values[0] != 'dk':
            answer_ranks.append(int(row['answer_rank'].values[0]))
            answer_pcts.append(row['answer_pct'].values[0])
    
    max_rank = df_['question_scale'].values[0]   
    multiplier = (100/max_rank) / 100
    multiply_func = lambda x: (x * multiplier) / 100
    multiplied_list = list(map(multiply_func, answer_ranks))
    answer_pct_multiplied = [a*b for a,b in zip(answer_pcts, multiplied_list)]
    rank = sum(answer_pct_multiplied)
    
    return rank
    
      
results = []
for key, df_ in map_df.groupby( ['id'] ):
    df_ = df_.fillna('')
    for id_, df__ in df_.groupby('question_raw'):   
        redict = {
            'id': key,
            'gov': df__['governorate'].values[0],
            'question_en': df__['question_en'].values[0],
            'question_ar': df__['question_ar'].values[0],
            'tag': df__['question_tag'].values[0], 
            'rank': build_map_dict(df__),
            'scale_upper_en': 'more',
            'scale_lower_en': 'less',
            'scale_upper_ar': 'أكثر',
            'scale_lower_ar': 'أقل'
        }
        
        results.append(redict)
    
with open(mapFile, 'w') as outfile:
    print (mapFile)
    json.dump(results, outfile)
