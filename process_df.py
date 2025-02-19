#%%
import pandas as pd

# Read the CSV file
df = pd.read_csv('combined_output.csv')
# Convert column names to lowercase
df.columns = df.columns.str.lower()
df = df.sort_values(['page','y']).reset_index(drop=True)
# Display the first few rows of the data
print(df.head())
# %%

df['is_word'] = df['text'].str.contains('[', regex=False) | df['text'].str.contains(']', regex=False)
df
# %%
df['word_group'] = df['is_word'].astype(int).cumsum()
df.iloc[20:].head(10)
# %%
filtered_df = df[df.groupby('word_group')['is_word'].transform('any')]
filtered_df.query("word_group == 3").head(15)
# %%
filtered_df.to_pickle('filtered_df.pkl')

# %%
