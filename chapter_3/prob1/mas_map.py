import pandas as pd

map_path = 'chapter_3/prob1/area_map.csv'
struct_path = 'chapter_3/prob1/area_struct.csv'
category_path = 'chapter_3/prob1/area_category.csv'

map_df = pd.read_csv(map_path)
struct_df = pd.read_csv(struct_path)
category_df = pd.read_csv(category_path)

category_map = category_df.set_index('category')['struct']

struct_df['category'] = struct_df['category'].map(category_map)

print(struct_df[struct_df['area'] == 1])