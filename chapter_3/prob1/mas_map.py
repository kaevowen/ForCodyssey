import pandas as pd
import csv

map_path = 'chapter_3/prob1/area_map.csv'
struct_path = 'chapter_3/prob1/area_struct.csv'
category_path = 'chapter_3/prob1/area_category.csv'

map_df = pd.read_csv(map_path)
struct_df = pd.read_csv(struct_path)
category_df = pd.read_csv(category_path)

category_map = category_df.set_index('category')['struct']
struct_df['category'] = struct_df['category'].map(category_map)
area_counts = struct_df.groupby('area')['category'].count()
print(f'area별 구조물 개수\n{area_counts.to_string(header=False, name=False, dtype=False)}')

final_df = struct_df[struct_df['area'] == 1]

with open('chapter_3/prob2/map.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(final_df.columns)
    writer.writerows(final_df.values)

merge_map = pd.read_csv('chapter_3/prob2/map.csv')
print('\nstruct_category의 상위 5개 값')
print(merge_map.head())