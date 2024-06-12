import ast
import pandas as pd
df = pd.read_csv('test_retrieve.csv')
for col in ['pre_text', 'post_text', 'text_retrieved_all', 'table_retrieved_all', 'table']:
    df[col] = df[col].apply(ast.literal_eval)
for col in ['Top-1', 'Top-3', 'Top-5']:
    df[col] = ''
def Extraction(row):
    Texts = row['pre_text'] + row['post_text']
    Tables = row['table']
    retrieved_indices = [ind['ind'] for ind in sorted(row['table_retrieved_all'] + row['text_retrieved_all'], key=lambda x: x['score'], reverse=True) ][:5]
    Retrieved_facts = [Tables[int(ind.replace('table_', ''))] if 'table_' in ind else Texts[int(ind.replace('text_', ''))] for ind in retrieved_indices]
    row['Top-1'] = Retrieved_facts[:1]
    row['Top-3'] = Retrieved_facts[:3]
    row['Top-5'] = Retrieved_facts
    return row

df = df.apply(Extraction, axis=1)
df.to_csv('test_retrieve.csv')
print('done!')