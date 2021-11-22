import glob

import mysql.connector
import pandas as pd
import statistics

df_1 = pd.read_csv('C:\\Users\\yabok\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\districts_info.csv')

df_2 = pd.read_csv('C:\\Users\\yabok\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\products_info.csv')

district_df = pd.DataFrame(df_1, columns=['district_id', 'state', 'locale', 'pct_black/hispanic',
                                          'county_connections_ratio', 'pp_total_raw'])

product_df = pd.DataFrame(df_2, columns=['LP ID', 'URL', 'Product Name', 'Provider/Company Name',
                                         'Sector(s)', 'Primary Essential Function'])

engagement_df = pd.DataFrame(df_2, columns=['LP ID', 'URL', 'Product Name', 'Provider/Company Name',
                                         'Sector(s)', 'Primary Essential Function'])

# district_df.dropna(inplace=True)
#print(district_df.to_string)

mydb = mysql.connector.connect(
    host="data.czjngffm4iwg.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Messenger1",
    db="dashboard"
)
mycursor = mydb.cursor()


def isnan(st):
    return st != st


def insert_district_data():
    for (x, y) in district_df.iterrows():

        if not (isnan(y[1])) and not (isnan(y[2])) and not (isnan(y[2])) and not (isnan(y[3])) and \
                not (isnan(y[4])) and not (isnan(y[5])):
            temp = y[2]
            pct_num1 = float(''.join(y[3]).replace('[', '').split(',')[0])
            pct_num2 = float(''.join(y[3]).replace('[', '').split(',')[1])
            county_c1 = float(''.join(y[4]).replace('[', '').split(',')[0])
            county_c2 = float(''.join(y[4]).replace('[', '').split(',')[1])
            total_r1 = int(''.join(y[5]).replace('[', '').split(',')[0])
            total_r2 = int(''.join(y[5]).replace('[', '').split(',')[1])
            ppt_total_raw = list(range(total_r1, total_r2))
            median_value = statistics.median(ppt_total_raw)

            ratio = county_c1 / county_c2
            avg = (pct_num1 + pct_num2) / 2
            print("The pct black avg", avg)
            print("The county connection", ratio)
            print("The median value is", median_value)
            sql = "INSERT INTO district_info (DistrictID,State,Locale,Pct_ethnicity,County_connection,PP_total_raw) " \
                  "VALUES (%s,%s,%s,%s,%s,%s) "
            val = (y[0], y[1], y[2], avg, ratio, median_value)

            mycursor.execute(sql, val)
            mydb.commit()

# The product info is inserted
def insert_product_data():
    for (x, y) in product_df.iterrows():
        if (isnan(y[5])):
            y[5] = "Empty"
        if (isnan(y[4])):
            y[4] = "Empty"
        if (isnan(y[3])):
            y[3] = "Empty"
        if (isnan(y[2])):
            y[2] = "Empty"
        if (isnan(y[1])):
            y[1] = "Empty"
        if (isnan(y[0])):
            y[0] = "Empty"

        sql = "INSERT INTO products_info (Lpid,Product_Name,Provider,Sector,Primary_Essential_Function,URL) " \
              "VALUES (%s,%s,%s,%s,%s,%s)"
        val = (y[0], y[2], y[3], y[4], y[5],y[1])
        print("The", val)

        mycursor.execute(sql, val)
        mydb.commit()

def insert_engagement_data():
    path = r'C:\\Users\\yabok\\Downloads\\learnplatform-covid19-impact-on-digital-learning\\engagement_data\\'  # use your path
    all_files = glob.glob(path + "/*.csv")
    mydict = {}
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)


    i = 0
    while (i <= len(li) - 1):
        district_df = pd.DataFrame(li[i], columns=['time', 'lp_id', 'pct_access', 'engagement_index'])
        for (x, y) in district_df.iterrows():
            sql = "INSERT INTO engagement_info (Time,Lp_id,Pct_access,Engagement_index) " \
                  "VALUES (%s,%s,%s,%s)"
            if (isnan(y[0])):
                y[0] = "Empty"
            if (isnan(y[1])):
                y[1] = 0.0
            if (isnan(y[2])):
                y[2] = 0.0
            if (isnan(y[3])):
                y[3] = 0.0

            val = (y[0], y[1], y[2], y[3])
            print("The", val)
            mycursor.execute(sql, val)
            mydb.commit()
            i = i + 1



insert_product_data()
#insert_engagement_data()