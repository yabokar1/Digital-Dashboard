import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy
import glob
from pathlib import Path

path = r'C:\\Users\\qasim\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\engagement_data\\' # use your path
all_files = glob.glob(path + "/*.csv")
ids = []
li = []
did_value = {}
lp_id = []
percentage_access = []
district_name = ''
top_ten_products = []
top_ten_product_names = []
top_ten_percentage_access = []
top_ten_product_categories = []

def isnan(st):
    return st != st

def select_specific_district(d):
    tmp_array = []
    for index, key in enumerate(did_value):
        if(did_value[key] == d):
            tmp_array.append(key)
    return (tmp_array)


for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

i = 0
while(i <= len(li) -1 ):
    stu_df = pd.DataFrame(li[i], columns =['lp_id','pct_access'])
    ids.append(Path(all_files[i]).name.strip('.csv'))
    i = i + 1



districtdf = pd.read_csv('C:\\Users\\qasim\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\districts_info.csv')
district_stu_df = pd.DataFrame(districtdf, columns =['district_id', 'state'])

for(x,y) in district_stu_df.iterrows():
    for item in ids:
        if y[0] == int(item):
            did_value.update({y[0] : y[1]})

print(did_value)
specific_district = []
district_name = 'New York'
specific_district = select_specific_district(district_name)                      ## place to enter district
paths = []
non_existing_product_ids = {}

print(specific_district)

correct_path = 'C:\\Users\\qasim\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\engagement_data\\'
for k in specific_district:
    paths.append(correct_path + str(k) + ".csv")


print(paths)
# vtemp = ((str(paths).strip('[]')))
# print(vtemp)


combined_csv = pd.concat([pd.read_csv(f) for f in paths ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

# print(combined_csv)


final_dataframe = pd.DataFrame(combined_csv, columns =['lp_id', 'pct_access'])

# print(final_dataframe['lp_id'])

series = final_dataframe.groupby('lp_id')['pct_access'].mean()

print(series)
# fdf = pd.DataFrame([series]).T
print('hello')
print(series.index)
fdf = pd.DataFrame({'lp_id':series.index, 'pct_access':series.values})

print('******')
print(fdf)
# print(fdf.columns.str.match("pct_access"))

for (r,t) in fdf.iterrows():
    lp_id.append(t[0])
    percentage_access.append(t[1])



N = 10                 # Can be used as user input
column_name = 0
# topdf = (pd.DataFrame(percentage_access).nlargest(N, ['ind', 'pct_val']))

top_10_largest = fdf.nlargest(N, 'pct_access', keep='all')

print(top_10_largest)

print("HERE")
for (f,g) in top_10_largest.iterrows():
    top_ten_percentage_access.append(g[1])
    top_ten_products.append(int(g[0]))



print(top_ten_percentage_access)
print(top_ten_products)

productdf = pd.read_csv('C:\\Users\\qasim\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\products_info.csv')
product_stu_df = pd.DataFrame(productdf, columns =['LP ID', 'Product Name' , 'Primary Essential Function'])




f = 0
while(f <= len(top_ten_products)-1):
    for (p, q) in product_stu_df.iterrows():
        if q[0] == int(top_ten_products[f]) and not isnan(q[0]):
            top_ten_product_names.append(q[1])
            top_ten_product_categories.append(q[2])
    f = f + 1


z = 0
for h in top_ten_products:
    if h not in product_stu_df.values:
        non_existing_product_ids.update({top_ten_products.index(h) : h })

for key, value in non_existing_product_ids.items():
    top_ten_products.remove(value)
    top_ten_percentage_access.remove(top_ten_percentage_access[key])




print(top_ten_product_names)
print(top_ten_product_categories)


plt.barh(top_ten_product_names,top_ten_percentage_access)
plt.xlabel('Percentage Access (%)')
plt.ylabel('Product Name')
plt.title('Percentage Access of Products for {}'.format(district_name))



for index, value in enumerate(top_ten_percentage_access):
    plt.text(value, index, round(value,3))

plt.show()