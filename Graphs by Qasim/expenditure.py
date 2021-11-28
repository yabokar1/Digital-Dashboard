import pandas as pd
import math
import statistics
import matplotlib.pyplot as plt
import numpy

Utah = []
Illi = []
Wisco = []
mean_perc = []
north = []
miss = []
wash = []
connect = []
mass = []
newyork = []
indiana = []
vir = []
ohio = []
jersey = []
cal = []
dis = []
ari = []
tex = []
avg_expenditure_for_states = []
states = ['Utah', 'Illinois', 'Wisconsin', 'NC', 'Missouri', 'Washington', 'Connecticut', 'Massachusetts', 'NY', 'Indiana', 'Virginia', 'Ohio', 'New Jersey', 'California', 'DOC', 'Arizona','Texas']

#Helper method for checking nan
def isnan(st):
    return st != st

#This class gives us the mean expenditure per pupil in different states. When storing the field pp_total_raw in database make sure to store the actual numbers and not the string. Retrieval from database will be easier this way.

#Read the file districts_info.csv from correct path
df = pd.read_csv('C:\\Users\\qasim\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\districts_info.csv')

#read the columns of file in a dataframe
stu_df = pd.DataFrame(df, columns =['state', 'pp_total_raw'])

for (x,y) in stu_df.iterrows():
    if not(isnan(y[1])) and not(isnan(y[0])):
        if y[0] == 'Utah':
            ut1 = float(''.join(y[1]).replace('[', '').split(',')[0])    #The number before the comma
            ut2 = float(''.join(y[1]).replace('[', '').split(',')[1])    #The number after the comma
            Utah.append(statistics.median([ut1, ut2]))                   #Median of the two numbers and append it to each state.
        elif y[0] == 'Illinois':
            illi1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            illi2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            Illi.append(statistics.median([illi1, illi2]))
        elif y[0] == 'Wisconsin':
            wis1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            wis2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            Wisco.append(statistics.median([wis1, wis2]))

        elif y[0] == 'North Carolina':
            nc1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            nc2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            north.append(statistics.median([nc1, nc2]))
        elif y[0] == 'Missouri':
            mi1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            mi2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            miss.append(statistics.median([mi1, mi2]))
        elif y[0] == 'Washington':
            wa1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            wa2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            wash.append(statistics.median([wa1, wa2]))
        elif y[0] == 'Connecticut':
            con1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            con2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            connect.append(statistics.median([con1, con2]))
        elif y[0] == 'Massachusetts':
            mas1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            mas2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            mass.append(statistics.median([mas1, mas2]))
        elif y[0] == 'New York':
            ny1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            ny2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            newyork.append(statistics.median([ny1, ny2]))
        elif y[0] == 'Indiana':
            ind1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            ind2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            indiana.append(statistics.median([ind1, ind2]))
        elif y[0] == 'Virginia':
            vi1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            vi2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            vir.append(statistics.median([vi1, vi2]))
        elif y[0] == 'Ohio':
            oh1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            oh2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            ohio.append(statistics.median([oh1, oh2]))
        elif y[0] == 'New Jersey':
            nj1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            nj2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            jersey.append(statistics.median([nj1, nj2]))
        elif y[0] == 'California':
            cal1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            cal2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            cal.append(statistics.median([cal1, cal2]))
        elif y[0] == 'District Of Columbia':
            doc1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            doc2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            dis.append(statistics.median([doc1, doc2]))
        elif y[0] == 'Arizona':
            ari1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            ari2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            ari.append(statistics.median([ari1, ari2]))
        elif y[0] == 'Texas':
            tex1 = float(''.join(y[1]).replace('[', '').split(',')[0])
            tex2 = float(''.join(y[1]).replace('[', '').split(',')[1])
            tex.append(statistics.median([tex1, tex2]))
def avg(li):
    j = 0
    for i in li:
        j = j + i
    return (j/len(li))

if len(Utah) > 0:
    avg_expenditure_for_states.append(avg(Utah))
else:
    avg_expenditure_for_states.append(0)
if len(Illi) > 0:
    avg_expenditure_for_states.append(avg(Illi))
else:
    avg_expenditure_for_states.append(0)
if len(Wisco) > 0:
    avg_expenditure_for_states.append(avg(Wisco))
else:
    avg_expenditure_for_states.append(0)
if len(north) > 0:
    avg_expenditure_for_states.append(avg(north))
else:
    avg_expenditure_for_states.append(0)
if len(miss) > 0:
    avg_expenditure_for_states.append(avg(miss))
else:
    avg_expenditure_for_states.append(0)
if len(wash) > 0:
    avg_expenditure_for_states.append(avg(wash))
else:
    avg_expenditure_for_states.append(0)
if len(connect) > 0:
    avg_expenditure_for_states.append(avg(connect))
else:
    avg_expenditure_for_states.append(0)
if len(mass) > 0:
    avg_expenditure_for_states.append(avg(mass))
else:
    avg_expenditure_for_states.append(0)
if len(newyork) > 0:
    avg_expenditure_for_states.append(avg(newyork))
else:
    avg_expenditure_for_states.append(0)
if len(indiana) > 0:
    avg_expenditure_for_states.append(avg(indiana))
else:
    avg_expenditure_for_states.append(0)
if len(vir) > 0:
    avg_expenditure_for_states.append(avg(vir))
else:
    avg_expenditure_for_states.append(0)
if len(ohio) > 0:
    avg_expenditure_for_states.append(avg(ohio))
else:
    avg_expenditure_for_states.append(0)
if len(jersey) > 0:
    avg_expenditure_for_states.append(avg(jersey))
else:
    avg_expenditure_for_states.append(0)
if len(cal) > 0:
    avg_expenditure_for_states.append(avg(cal))
else:
    avg_expenditure_for_states.append(0)
if len(dis) > 0:
    avg_expenditure_for_states.append(avg(dis))
else:
    avg_expenditure_for_states.append(0)
if len(ari) > 0:
    avg_expenditure_for_states.append(avg(ari))
else:
    avg_expenditure_for_states.append(0)
if len(tex) > 0:
    avg_expenditure_for_states.append(avg(tex))
else:
    avg_expenditure_for_states.append(0)


plt.barh(states,avg_expenditure_for_states)
plt.xlabel('Average Expenditure per pupil in dollars')
plt.ylabel('States')
plt.title('Average Expenditure per Pupil in different states')

for index, value in enumerate(avg_expenditure_for_states):
    plt.text(value, index, int(value))

plt.show()