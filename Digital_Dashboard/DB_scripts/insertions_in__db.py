import glob

import mysql.connector
import pandas as pd
import statistics
import stats_can
from stats_can import StatsCan

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


def labour_force_status():
    df = stats_can.sc.zip_table_to_dataframe('3710010701')
    df.columns = [c.replace(' ', '_').replace("-", "_") for c in df.columns]
    df = (df[((df.REF_DATE == "2020/2021") | (df.REF_DATE == "2019/2020") |
              (df.REF_DATE == "2018/2019"))])

    for index, row in df.iterrows():
        val = (row.REF_DATE, row.Age_group, row.Labour_force_status_of_students_and_non_students, row.VALUE)
        if not np.isnan(
                row.VALUE) and row.Labour_force_status_of_students_and_non_students != "Total labour Force status":
            print(val)
            mycursor.execute(
                "INSERT INTO labour_force (ReferenceDate,AgeGroup,LabourForceStatus,Value) VALUES (%s,%s,%s,%s)",
                val)
            mydb.commit()

    df = df[['REF_DATE', 'Age_group', 'Labour_force_status_of_students_and_non_students', 'VALUE']]
    print("\n Labour Force \n", df['Labour_force_status_of_students_and_non_students'])


# just make it total registration status and put the countries
def post_secondary_enrollment():
    df = stats_can.sc.zip_table_to_dataframe('3710001801')
    df.columns = [c.replace(' ', '_').replace("(", "").replace(")", "") for c in df.columns]
    print(df.columns)

    df = (df[(df.Gender == 'Total, gender') &
             (df.Status_of_student_in_Canada == "Total, status of student in Canada") &
             (df.International_Standard_Classification_of_Education_ISCED ==
              'Total, International Standard Classification of Education (ISCED)') &
             (df.Field_of_study == 'Total, field of study') &
             (df.Registration_status == "Total, registration status") &
             (df.UOM == 'Number') &
             ((df.REF_DATE == "2020/2021") | (df.REF_DATE == "2019/2020") | (df.REF_DATE == "2018/2019"))])

    for index, row in df.iterrows():
        val = (row.REF_DATE, row.GEO, row.Institution_type, row.Gender, row.VALUE)
        print(val)
        mycursor.execute(
            "INSERT INTO postsecondary_enrollment (ReferenceDate, GEO, InstitutionType,Gender, Value) VALUES (%s,%s,%s,%s,%s)",val)
        mydb.commit()

    df = df[['REF_DATE', 'Institution_type', 'Registration_status',
             'International_Standard_Classification_of_Education_ISCED',
             'Field_of_study', 'Gender', 'Status_of_student_in_Canada', 'VALUE']]
    print("\n Enrollment \n", df)


def expenditure_by_colleges():
    df = stats_can.sc.zip_table_to_dataframe('3710002901')
    df.columns = [c.replace(' ', '_').replace("(", "").replace(")", "") for c in df.columns]
    print(df.columns)
    df = (df[(df.Types_of_funds_and_functions == 'Total funds') &
             ((df.REF_DATE == "2020/2021") | (df.REF_DATE == "2019/2020") | (df.REF_DATE == "2018/2019"))])
    for index, row in df.iterrows():
        val = (row.REF_DATE, row.GEO, row.Types_of_expenditures,
               row.VALUE)
        print(val)
        mycursor.execute(
            "INSERT INTO expenditure_colleges (ReferenceDate,Geo,Types,Value) VALUES (%s,%s,%s,%s)", val)
        mydb.commit()

    df = df[['REF_DATE', 'GEO', 'Types_of_expenditures', 'Types_of_funds_and_functions', 'VALUE']]
    print("\n Expenditure by College \n", df)


def apprentice_registration():
    df = stats_can.sc.zip_table_to_dataframe('3710002301')
    df.columns = [c.replace(' ', '_').replace("(", "").replace(")", "") for c in df.columns]
    print(df.columns)
    df = (df[(df.Age_groups == "Total age groups") & (df.Sex == 'Both sexes') &
             (df.Registration_status == 'Total registration status') &
             ((df.REF_DATE == "2020") | (df.REF_DATE == "2019") | (df.REF_DATE == "2018"))])

    for index, row in df.iterrows():
        if not np.isnan(row.VALUE):
            val = (row.REF_DATE, row.GEO, row.Age_groups, row.Sex, row.Major_trade_groups,
                   row.Registration_status, row.VALUE)
            print(val)
            mycursor.execute(
                "INSERT INTO apprenticeship_registration (ReferenceDate,Geo,AgeGroups,Sex,TradeGroups, RegistrationStatus, Value) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                val)
            mydb.commit()

    df = df[['REF_DATE', 'GEO', 'Age_groups', 'Sex', 'Major_trade_groups', 'Registration_status', 'VALUE']]
    print("\n apprentice \n", df)


# 15 year old test scores
def avg_test_score_registration():
    df = stats_can.sc.zip_table_to_dataframe('3710014901')
    df.columns = [c.replace(' ', '_').replace("(", "").replace(")", "") for c in df.columns]
    print("The columns", df.columns)
    df = (df[(df.REF_DATE == '2018') | (df.REF_DATE == '2015')])
    print("The", df)
    for index, row in df.iterrows():
        val = (row.REF_DATE, row.Domain,
               row.Selected_Characteristics, row.Gender,
               row.VALUE)
        print("The value is", val)
        mycursor.execute(
            "INSERT INTO average_test_scores (ReferenceDate,Domain,Characteristics,Gender, Value) VALUES (%s,%s,%s,%s,%s)",
            val)
        mydb.commit()

    df = df[['REF_DATE', 'GEO', 'Domain', 'Selected_Characteristics', 'Gender', 'VALUE']]
    print("\n test_scores \n", df)


def participation_rate_in_education_by_age():
    df = stats_can.sc.zip_table_to_dataframe('3710010101')
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = (df[(df.REF_DATE == '2020/2021')])
    for index, row in df.iterrows():
        if not np.isnan(row.VALUE):
            val = (row.REF_DATE, row.Age, row.Type_of_institution_attended,
                   row.VALUE)
            print(val)
            mycursor.execute(
                "INSERT INTO participation_rate (ReferenceDate,Age,Institution,Percentage) VALUES (%s,%s,%s,%s)", val)
            mydb.commit()

    df = df[['REF_DATE', 'Age', 'Type_of_institution_attended', 'VALUE']]
    print(df)


def unemployment_rates_of_population_aged_15_and_over():
    df = stats_can.sc.zip_table_to_dataframe('1410036101')
    df.columns = [c.replace(' ', '_') for c in df.columns]
    print(df.columns)
    df = (df[((df.REF_DATE == '2018-01-01') | (df.REF_DATE == '2019-01-01') | (df.REF_DATE == '2020-01-01'))])
    for index, row in df.iterrows():
        val = (row.REF_DATE, row.Characteristics_of_the_population_aged_15_and_over,
               row.Educational_attainment,
               row.VALUE)
        print(val)
        mycursor.execute(
            "INSERT INTO unemployment_rate (ReferenceDate,Characteristics,Educationalattainment,Percentage) VALUES (%s,%s,%s,%s)",
            val)
        mydb.commit()

    df = df[['REF_DATE', 'Characteristics_of_the_population_aged_15_and_over', 'Educational_attainment', 'VALUE']]
    print(df)



def generate_data_for_online_activities_by_gender_from_stats_canada():
    # This method should be invoked only when there is a change to this table for today's date.
    df = stats_can.sc.zip_table_to_dataframe('2210013701')
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = (df[(df.Gender == 'Total, gender') & (
            (df.COORDINATE == '1.1.1.1.1') | (df.COORDINATE == '1.2.1.1.1') | (df.COORDINATE == '1.3.1.1.1') | (
            df.COORDINATE == '1.4.1.1.1') | (df.COORDINATE == '1.5.1.1.1') | (df.COORDINATE == '1.6.1.1.1') | (
                    df.COORDINATE == '1.13.1.1.1') | (df.COORDINATE == '1.12.1.1.1') | (
                    df.COORDINATE == '1.23.1.1.1') | (df.COORDINATE == '1.26.1.1.1') | (
                    df.COORDINATE == '1.28.1.1.1'))])
    print(df.columns)
    df = df[['REF_DATE', 'Online_activities', 'Gender', 'Age_group', 'VALUE']]
    print(df)

