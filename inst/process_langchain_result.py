#%%
import pickle 
import pandas as pd
from PydanticWord import Word, WordRoot, ChineseMeaning, DerivedWords, Sentence

with open('word_groups_results.json', 'rb') as f:
    all_result = pickle.load(f)
    

# %%
all_result
# %%
all_result.keys()
# %%
rows = []
for grp, re_ in all_result.items():
    print(grp, re_.word)
    row = {}
    row['word'] = re_.word
    row['chinese_meaning'] = re_.chinese_meaning
    row['word_root_word_split'] = re_.word_root.word_split
    row['word_root_split_meaning'] = re_.word_root.split_meaning
    try:
        dw1 = re_.derived_words[0]
        row['derived_word'] = dw1.word
        try:
            dw2 = re_.derived_words[1]
            row['derived_word2'] = dw2.word
        except Exception as e:
            pass
    except Exception as e:
        pass
    try:
        se1 = re_.sentences[0]
        row['sentence1_eng'] = se1.eng
        row['sentence1_chi'] = se1.chi
        try:
            se2 = re_.sentences[1]
            row['sentence2_eng'] = se2.eng
            row['sentence2_chi'] = se2.chi
        except Exception as e:
            pass
    except Exception as e:
        pass

    # for k, v in row.items():
    #     print(k, v)
    rows.append(row)
# %%
pd.DataFrame(rows)



# %%
re_.model_dump()
# %%
all_result[60].model_dump()
