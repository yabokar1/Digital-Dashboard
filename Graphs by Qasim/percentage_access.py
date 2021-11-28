import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy
import glob
from pathlib import Path

states = []
district_id = []
percentage_access = []
def isnan(st):
    return st != st


def percentage_access_in_district(d):
    tmp = []
    tmp_value = []
    j = 0
    while j <= len(states) - 1:
        if states[j] == d:
            tmp.append(district_id[j])
            tmp_value.append(percentage_access[j])
        j = j + 1
    print(tmp)
    print(tmp_value)
    plot2 = plt.figure(2)
    plt.bar(tmp, tmp_value)
    plt.xlabel('District ID')
    plt.ylabel('Percentage Access in %')
    plt.title('Percentage Access in '+ d)
    plt.xticks(rotation=45)


path = r'C:\\Users\\qasim\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\engagement_data\\' # use your path
all_files = glob.glob(path + "/*.csv")
mydict = {}
li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)


i = 0
while(i <= len(li) -1 ):
    stu_df = pd.DataFrame(li[i], columns =['pct_access'])
    mydict.update({Path(all_files[i]).name.strip('.csv') : stu_df.pct_access.mean(axis=0)})
    i = i + 1

# print(stu_df.pct_access.mean(axis=0))
# print(Path(all_files[1]).name.strip('.csv'))

print("------------------")
print(mydict)

districtdf = pd.read_csv('C:\\Users\\qasim\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\districts_info.csv')
district_stu_df = pd.DataFrame(districtdf, columns =['district_id', 'state'])


for k, v in mydict.items():
    for (x, y) in district_stu_df.iterrows():
        if y[0] == int(k) and not(isnan(y[1])):
            states.append(y[1])
            district_id.append(k)
            percentage_access.append(v)


print('----')
print(states)
print(percentage_access)
print(district_id)

plot1 = plt.figure(1)
plt.barh(states,percentage_access)
plt.xlabel('Percentage Access (%)')
plt.ylabel('States')
plt.title('Percentage Access in states')
percentage_access_in_district('Illinois')

plt.show()




