#%%
import pandas as pd

df = pd.read_csv('ref/combined_output.csv')
df.columns = df.columns.str.lower()
df = df.sort_values(['page','y']).reset_index(drop=True)
df = df[df['page'] <= 565]
# print(df.head())


# %%
df['chinese_text'] = df['text'].str.replace(r'[^\u4e00-\u9fff]', '', regex=True)
df['english_text'] = df['text'].str.replace(r'[\u4e00-\u9fff]', '', regex=True)
is_word_mask = (
    (df['english_text'].str.contains(r'(\w+ *)?\w+ *[\[\(\{\（]\w+[\}\）\)\]]|[\[\]`′]', regex=True)).fillna(False)
    & (df['english_text'].str.len() <= 40)
    & (~(df['english_text'].str.contains(r'/', regex=True)).fillna(False))
    & (~(df['english_text'].str.contains(r':', regex=True)).fillna(False))
    & (~(df['english_text'].str.contains(r'(「|」)', regex=True)).fillna(False))
)
df['is_word'] = is_word_mask
df['is_chinese'] = (df['text'].str.contains(r'[\u4e00-\u9fff]', regex=True)).fillna(False)
df['is_english'] = (df['text'].str.contains(r'[a-zA-Z]', regex=True)).fillna(False)
df['english_length'] = df['text'].str.len()
df['chinese_length'] = df['chinese_text'].str.len()
df['is_chinese_sentence'] = (df['is_chinese'] & (df['chinese_length'] > 10))
df['is_english_sentence'] = (df['is_english'] & (df['english_length'] > 30))
df['is_word'] = df['is_word'] & (~df['is_chinese_sentence']) & (~df['is_english_sentence'])


df = df.assign(
    word=df['text'].str.extract(r'(\w+) *[L\[\{\(\（]', expand=False).fillna(df['text'])
)
df.to_clipboard()
df



#%%
word_indices = df.index[df['is_word']].tolist()
next_word_indices = word_indices[1:] + [len(df)]

dfs = []
for grp, start in enumerate(word_indices):
    end = start + 10
    print(df.iloc[start]['text'], '->', df.iloc[start]['word'], sep='\t')
    print(f'len({start}: {end}) = {end - start}')
    df['word_group'] = grp
    dfs.append(df.iloc[start:end])


#%%
df0 = pd.concat(dfs)
df0.to_clipboard()
df0.to_csv('word_groups.csv', index=False)
df0


#%%
cnt = 0
rows = []
for grp, df_grp in df0.groupby('word_group'):
    word = df_grp.iloc[0]['word']
    df_grp_small = df_grp[(df_grp['x'] < 170) & (df_grp.index != df_grp.index[0])]
    root1, root2 = '', ''
    if len(df_grp_small) > 0:
        root1 = df_grp_small.iloc[0]['text'] if len(df_grp_small) > 0 else ''
        x1 = df_grp_small.iloc[0]['x']
        root2 = df_grp_small.iloc[1]['text'] if len(df_grp_small) > 1 else ''
        x2 = df_grp_small.iloc[1]['x']
    df_grp_small2 = df_grp[(df_grp['x'] >= 200) & (df_grp.index != df_grp.index[0])]
    root3, x3 = '', 0
    root4, x4 = '', 0
    if len(df_grp_small2) > 0:
        root3 = df_grp_small2.iloc[0]['text']
        x3 = df_grp_small2.iloc[0]['x']
        if len(df_grp_small2) > 1:
            root4 = df_grp_small2.iloc[1]['text']
            x4 = df_grp_small2.iloc[1]['x']
    
    df_grp_small3 = df_grp[((150 < df_grp['x']) & (df_grp['x'] < 200)) & (df_grp.index != df_grp.index[0])]
    sentence1 = ''
    sx1 = 0
    if len(df_grp_small3) > 0:
        sentence1 = df_grp_small3.iloc[0]['text']
        sx1 = df_grp_small3.iloc[0]['x']
    sentence2 = ''
    sx2 = 0
    df_grp_small4 = df_grp[((100 < df_grp['x']) & (df_grp['x'] < 170)) & (df_grp.index != df_grp.index[0])]
    if len(df_grp_small4) > 3:
        sentence2 = df_grp_small4.iloc[2]['text']
        sx2 = df_grp_small4.iloc[2]['x']

    # if df_grp.iloc[4]['is_english_sentence']:
    #     root4 = ''
    rows.append({'word': word, 'root1': root1, 'root2': root2, 'root3': root3, 'root4': root4, 
        'root1': root1, 'x1': x1,
        'root2': root2, 'x2': x2,
        'root3': root3, 'x3': x3,
        'root4': root4, 'x4': x4,
        'sentence1': sentence1, 'sx1': sx1,
        'sentence2': sentence2, 'sx2': sx2,
            
    })
    cnt += 1

result_df = pd.DataFrame(rows)
result_df.to_clipboard()
result_df

#%%
df0.loc[844: 845]
# df0

