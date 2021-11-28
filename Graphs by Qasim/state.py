import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy

#This gives the plot of percentage of black/hispanic people in different states.
df = pd.read_csv('C:\\Users\\qasim\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\districts_info.csv')
z,k,w,p,e,r,t,l,u,i,o,p,aa,s,dd,f,g = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
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
def isnan(st):
    return st != st


stu_df = pd.DataFrame(df, columns =['state', 'pct_black/hispanic'])

for (x,y) in stu_df.iterrows():
    if (not(isnan(y[1])) and not(isnan(y[0]))):
        if(y[0] == 'Utah'):
            Utah.append(y[1])
        elif y[0] == 'Illinois':
            Illi.append(y[1])
        elif y[0] == 'Wisconsin':
            Wisco.append(y[1])
        elif y[0] == 'North Carolina':
            north.append(y[1])
        elif y[0] == 'Missouri':
            miss.append(y[1])
        elif y[0] == 'Washington':
            wash.append(y[1])
        elif y[0] == 'Connecticut':
            connect.append(y[1])
        elif y[0] == 'Massachusetts':
            mass.append(y[1])
        elif y[0] == 'New York':
            newyork.append(y[1])
        elif y[0] == 'Indiana':
            indiana.append(y[1])
        elif y[0] == 'Virginia':
            vir.append(y[1])
        elif y[0] == 'Ohio':
            ohio.append(y[1])
        elif y[0] == 'New Jersey':
            jersey.append(y[1])
        elif y[0] == 'California':
            cal.append(y[1])
        elif y[0] == 'District Of Columbia':
            dis.append(y[1])
        elif y[0] == 'Arizona':
            ari.append(y[1])
        elif y[0] == 'Texas':
            tex.append(y[1])

states = ['Utah', 'Illinois', 'Wisconsin', 'NC', 'Missouri', 'Washington', 'Connecticut', 'Massachusetts', 'NY', 'Indiana', 'Virginia', 'Ohio', 'New Jersey', 'California', 'DOC', 'Arizona','Texas']
for x, y in zip(Utah, Illi):
    z.append(float(''.join(x).replace('[', '').split(',')[0]))
    z.append(float(''.join(x).replace('[', '').split(',')[1]))

    k.append(float(''.join(y).replace('[', '').split(',')[0]))
    k.append(float(''.join(y).replace('[', '').split(',')[1]))

for a, b in zip(Wisco, north):
    w.append(float(''.join(a).replace('[', '').split(',')[0]))
    w.append(float(''.join(a).replace('[', '').split(',')[1]))

    p.append(float(''.join(b).replace('[', '').split(',')[0]))
    p.append(float(''.join(b).replace('[', '').split(',')[1]))

for c, d in zip(miss, wash):
    e.append(float(''.join(c).replace('[', '').split(',')[0]))
    e.append(float(''.join(c).replace('[', '').split(',')[1]))

    r.append(float(''.join(d).replace('[', '').split(',')[0]))
    r.append(float(''.join(d).replace('[', '').split(',')[1]))

for h, j in zip(connect, mass):
    t.append(float(''.join(h).replace('[', '').split(',')[0]))
    t.append(float(''.join(h).replace('[', '').split(',')[1]))

    l.append(float(''.join(j).replace('[', '').split(',')[0]))
    l.append(float(''.join(j).replace('[', '').split(',')[1]))

for ny, ind in zip(newyork, indiana):
    u.append(float(''.join(ny).replace('[', '').split(',')[0]))
    u.append(float(''.join(ny).replace('[', '').split(',')[1]))

    i.append(float(''.join(ind).replace('[', '').split(',')[0]))
    i.append(float(''.join(ind).replace('[', '').split(',')[1]))

for virg, oh in zip(vir, ohio):
    o.append(float(''.join(virg).replace('[', '').split(',')[0]))
    o.append(float(''.join(virg).replace('[', '').split(',')[1]))

    p.append(float(''.join(oh).replace('[', '').split(',')[0]))
    p.append(float(''.join(oh).replace('[', '').split(',')[1]))

for jer, ca in zip(jersey, cal):
    aa.append(float(''.join(jer).replace('[', '').split(',')[0]))
    aa.append(float(''.join(jer).replace('[', '').split(',')[1]))

    s.append(float(''.join(ca).replace('[', '').split(',')[0]))
    s.append(float(''.join(ca).replace('[', '').split(',')[1]))

for di, ar in zip(dis, ari):
    dd.append(float(''.join(di).replace('[', '').split(',')[0]))
    dd.append(float(''.join(di).replace('[', '').split(',')[1]))

    f.append(float(''.join(ar).replace('[', '').split(',')[0]))
    f.append(float(''.join(ar).replace('[', '').split(',')[1]))

for te in tex:
    g.append(float(''.join(te).replace('[', '').split(',')[0]))
    g.append(float(''.join(te).replace('[', '').split(',')[1]))
mean_perc.append((sum(z))/len(z))
mean_perc.append((sum(k))/len(k))
mean_perc.append((sum(w))/len(w))
mean_perc.append((sum(p))/len(p))
mean_perc.append((sum(e))/len(e))
mean_perc.append((sum(r))/len(r))
mean_perc.append((sum(t))/len(t))
mean_perc.append((sum(l))/len(l))
mean_perc.append((sum(u))/len(u))
mean_perc.append((sum(i))/len(i))
mean_perc.append((sum(o))/len(o))
mean_perc.append((sum(p))/len(p))
mean_perc.append((sum(aa))/len(aa))
mean_perc.append((sum(s))/len(s))
mean_perc.append((sum(dd))/len(dd))
mean_perc.append((sum(f))/len(f))
mean_perc.append((sum(g))/len(g))
print('------')
print(mean_perc)

plt.barh(states,mean_perc)
plt.xlabel('Percentage')
plt.ylabel('States')
plt.title('Percentage of pct_black/hispanic in states')

plt.show()