from pprint import pprint
import pandas as pd

ds_path = r"C:\Users\dolgo\OneDrive\Desktop\Dataset\RAW_recipes.csv"

df = pd.read_csv(ds_path, encoding='utf-8')

for column in df:
    print(column)
    if column == 'minutes' or column == 'contributor_id' or column == 'nutrition' or column == 'n_steps' or \
            column == 'n_ingredients' or column == 'id':
        continue
    df[column] = df[column].str.replace('"', "")
    df[column] = df[column].str.replace("'", "")

df['description'] = df['description'].str.replace('"', "")
df['description'] = df['description'].str.replace("'", "")
print(df['description'])
df['steps'] = df['steps'].str.replace("'", "")
df['steps'] = df['steps'].str.replace('"', "")
df['steps'] = df['steps'].str.replace('[', "")
df['steps'] = df['steps'].str.replace(']', "")
df['steps'] = df['steps'].str.replace(',', " ")


df['ingredients'] = df['ingredients'].str.replace("'", "")
df['ingredients'] = df['ingredients'].str.replace('"', "")
df['ingredients'] = df['ingredients'].str.replace("[", "")
df['ingredients'] = df['ingredients'].str.replace("]", "")

df['nutrition'] = df['nutrition'].str.replace('[', "")
df['nutrition'] = df['nutrition'].str.replace(']', "")

r_id_ingrid_pair_lst = []
r_id_nutrition_lst = []


for r_id, ingrid, nutrition in zip(df['id'], df['ingredients'], df['nutrition']):
    for item in ingrid.split(','):
        r_id_ingrid_pair_lst.append([r_id, item.strip()])
    lcl_list = [r_id]
    for value in nutrition.split(','):
        lcl_list.append(value)
    r_id_nutrition_lst.append(lcl_list)


df.drop('ingredients', inplace=True, axis=1)
df.drop('nutrition', inplace=True, axis=1)
r_id_ingrid_csv = pd.DataFrame(r_id_ingrid_pair_lst, columns=["recipe_id", "ingredient"])
r_id_nutrition_csv = pd.DataFrame(r_id_nutrition_lst, columns=['recipe_id', 'calories', 'total fat', 'sugar', 'sodium','protein', 'saturated fat', 'carbohydrates'])

r_id_nutrition_csv.to_csv('recipe_id_nutrition_table.csv', index=False)

r_id_ingrid_csv.to_csv('recipe_id_ingredient_table.csv', index=False)

df.to_csv('main_recipe_table.csv', index=False)