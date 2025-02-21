#%%
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import numpy as np

filtered_df = pd.read_pickle('filtered_df.pkl')

#%%

def create_text_visualization(df, page_size=(800, 1000), bg_color='white'):
    # Create a blank image
    img = Image.new('RGB', page_size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try different fonts that support Chinese characters
    chinese_fonts = [
        'C:/Windows/Fonts/msyh.ttc',  # Microsoft YaHei (Windows)
        'C:/Windows/Fonts/simsun.ttc', # SimSun (Windows)
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',  # Linux
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Linux
    ]
    
    font = None
    for font_path in chinese_fonts:
        try:
            font = ImageFont.truetype(font_path, 12)
            break
        except:
            continue
    
    if font is None:
        print("Warning: Could not load a Chinese font, falling back to default")
        font = ImageFont.load_default()

    # Draw each text item
    for _, row in df.iterrows():
        x = row['x']
        y = row['y']
        text = row['text']
        
        # Draw the text
        draw.text((x, y), text, fill='black', font=font)
        
        # Draw a small point at the coordinate for reference
        draw.ellipse([x-2, y-2, x+2, y+2], fill='red')

    return img

# Create and display the visualization
group = 938
df = filtered_df.query(f"word_group == {group}")
img = create_text_visualization(df)
img.show()
word_y = df['y'].iloc[0]
df.loc[:, 'diff'] = word_y - df['y']
df

# Optionally save the image
# img.save('text_visualization.png')

#%%
for group in range(1, 10):
    df = filtered_df.query(f"word_group == {group}")
    img = create_text_visualization(df)
    img.show()
    df

#%%
# Count the rate of finding Chinese meaning
total_groups = 0
groups_with_chinese_meaning = 0

for group in range(1, 1000):
    df = filtered_df.query(f"word_group == {group}")
    total_groups += 1
    word = df['text'].str.strip().iloc[0].split(' ')[0].split('[')[0]
    
    try: 
        chinese_meaning = '     '.join(df.query("x > 220")['text'].str.strip().tolist())
        if chinese_meaning and chinese_meaning.strip():
            groups_with_chinese_meaning += 1
    except:
        pass
    print(group, word, chinese_meaning)

print(f"Total groups: {total_groups}")
print(f"Groups with Chinese meaning: {groups_with_chinese_meaning}")
print(f"Rate of finding Chinese meaning: {groups_with_chinese_meaning/total_groups*100:.2f}%")

#%%
for group in range(1, 1000):
    df = filtered_df.query(f"word_group == {group}")
    word = df['text'].str.strip().iloc[0].split(' ')[0].split('[')[0]
    word_y = df['y'].iloc[0]
    chinese_meaning = None
    try: 
        chinese_meaning_query = df.query("(x > 200 and x < 300) and (y - @word_y < 50)")
        chinese_meaning = '     '.join(chinese_meaning_query['text'].str.strip().tolist())
    except:
        pass
    print(group, word, chinese_meaning, sep='\t')

#%%
'joint (dsont]'.split(' ')[0].split('[')[0]

filtered_df.query(f"word_group == 176")['text']
# .iloc[0]
