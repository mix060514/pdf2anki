#%%
import pandas as pd

# Read the CSV file
df = pd.read_csv('combined_output.csv')
# Convert column names to lowercase
df.columns = df.columns.str.lower()
df = df.sort_values(['page','y']).reset_index(drop=True)
# Display the first few rows of the data
print(df.head())
# (df.head(100).to_clipboard())
# %%
# df['is_word'] = (df['text'].str.contains(r'(\w+ *)?\w+ *[\[(]\w+[\])]|[\[\]`′]', regex=True)).fillna(False)
# df['is_word'] = df['is_word'] & (df['text'].str.len() <= 40)
# df['is_word'] = df['is_word'] & (~(df['text'].str.contains(r'/', regex=True)).fillna(False))
# df['is_word'] = df['is_word'] & (~(df['text'].str.contains(r':', regex=True)).fillna(False))
# df['is_word'] = df['is_word'] & (~(df['text'].str.contains(r'(「|」)', regex=True)).fillna(False))
df['text_without_chinese'] = df['text'].str.replace(r'[\u4e00-\u9fff]', '', regex=True)
is_word_mask = (
    (df['text_without_chinese'].str.contains(r'(\w+ *)?\w+ *[\[\(\{\（]\w+[\}\）\)\]]|[\[\]`′]', regex=True)).fillna(False)
    & (df['text_without_chinese'].str.len() <= 40)
    & (~(df['text_without_chinese'].str.contains(r'/', regex=True)).fillna(False))
    & (~(df['text_without_chinese'].str.contains(r':', regex=True)).fillna(False))
    & (~(df['text_without_chinese'].str.contains(r'(「|」)', regex=True)).fillna(False))
)
df['is_word'] = is_word_mask
# df['is_mp3'] = (df['text'].str.contains(r'MP3 *\d+', regex=True)).fillna(False)
# df['is_reading'] = (df['text'].str.contains(r'(Reading|LedaandtheSwan)', regex=True)).fillna(False)
# df.loc[df[df['is_mp3']].index + 1, 'is_word'] = True
df['is_chinese'] = (df['text'].str.contains(r'[\u4e00-\u9fff]', regex=True)).fillna(False)
df['is_english'] = (df['text'].str.contains(r'[a-zA-Z]', regex=True)).fillna(False)
df['remove_non_chinese_text'] = df['text'].str.replace(r'[^\u4e00-\u9fff]', '', regex=True)
df['sentence_length'] = df['text'].str.len()
df['remove_non_chinese_sentence_length'] = df['remove_non_chinese_text'].str.len()
# df['word_group'] = df['is_word'].astype(int).cumsum()
# df['is_chinese_group'] = (df['is_chinese'] != df['is_chinese'].shift(fill_value=False)).cumsum()
# df['is_english_group'] = (df['is_english'] != df['is_english'].shift(fill_value=False)).cumsum()
df['is_sentence'] = (df['is_english'] & (df['sentence_length'] > 40)) | (df['is_chinese'] & (df['remove_non_chinese_sentence_length'] > 10))


# df['word'] = df['text'].str.split(' ?[\[(L].*$', regex=True).str[0]
df = df.assign(
    # word=df['text'].str.extract(r'(\w+ *)?\w+ *[\[(]\w+[\])]|[\[\]`′]', expand=False).fillna(df['text'])
    word=df['text'].str.extract(r'(\w+) *[\[\{\(\（]', expand=False).fillna(df['text'])
)
df



#%%
# Compute the indices where is_word is True
word_indices = df.index[df['is_word']].tolist()

# Create a list of "next word" indices,
# using the DataFrame length as the final boundary.
next_word_indices = word_indices[1:] + [len(df)]

dfs = []
for grp, (start, next_start) in enumerate(zip(word_indices, next_word_indices)):
    # Define end as the minimum between start+20 and the next word index
    # find next sentence idx start
    next_sentence_idx_start = df.query('is_sentence').index[df.query('is_sentence').index > start].min()
    # find next sentence idx end
    # next_sentence_idx_end = df.query('is_sentence').index[df.query('is_sentence').index > next_sentence_idx_start].min()
    next_sentence_idx_end = next_sentence_idx_start + 1
    end = min(start + 20, next_start, next_sentence_idx_end) + 1
    # Print the current word and its group length
    print(df.iloc[start]['text'], '->', df.iloc[start]['word'], sep='\t')
    print(f'len({start}: {end}) = {end - start}')
    df['word_group'] = grp
    dfs.append(df.iloc[start:end])
    
#%%
dfs[0]
    
#%%
df0 = pd.concat(dfs)
df0.to_clipboard()
df0


#%%
cnt = 0
for grp, df_grp in df0.groupby('word_group'):
    df_grp['is_root'] = (df_grp['text'].str.contains(r'/', regex=True).astype(bool)).fillna(False)
    # df_grp[df_grp['is_root']]
    if (df_grp[df_grp['is_root']].shape[0] != 2):
        print(df_grp[df_grp['is_root']])
        print(df_grp)
        cnt += 1
        break

df_grp.to_clipboard()
print(cnt/len(df0['word_group'].unique()))

#%%
df0.loc[348: 355]
# df0



#%%
filtered_df = df[df.groupby('word_group')['is_word'].transform('any')]
filtered_df.groupby('word_group').size().sort_values(ascending=False).head(15)

#%%

start = 344
end = 346
filtered_df.query(f"word_group >= {start} and word_group <= {end}").to_clipboard()
filtered_df.query(f"word_group >= {start} and word_group <= {end}").head(21)












# %%
filtered_df.to_pickle('filtered_df.pkl')

# %%
