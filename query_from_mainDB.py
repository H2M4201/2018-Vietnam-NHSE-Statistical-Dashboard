import pymysql
import json
from decimal import Decimal
import pandas as pd
import numpy as np
import pytest


# MySQL connection details
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DB = 'thpt'
MYSQL_PORT = 3306

# get province code
with open('./caching/province.json', 'r', encoding='utf-8') as json_file:
    province_code = list(json.load(json_file).keys())
json_file.close()

#csv caching filepath
attendant_cache = './caching/attendant_stat.json'
score_distribution_cache = './caching/score_distribution_stat.json'


# done debugging and cleaning
def connect_to_sql():
    # Connect to MySQL
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT
    )

    return connection

# done debugging and cleaning
def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)

    return cursor.fetchall()

# done debugging and cleaning
def get_actual_student_distribution():
    conn = connect_to_sql()
    total_student_by_province = []

    core_query = """
    SELECT COUNT(DISTINCT(sbd)) FROM Y2018
    """

    for pCode in province_code:
        if pCode != '00':
            # filter by province 
            province_conditioning = f""" 
            WHERE sbd LIKE '{pCode}%'
            """
            query = core_query + ' ' + province_conditioning #concat the filter condition
            number_of_students = execute_query(conn, query)
        else:
            number_of_students = execute_query(conn, core_query)
        
        total_student_by_province.append(number_of_students[0][0])

    conn.close()

    return total_student_by_province

# done debugging and cleaning
def get_student_categorization_by_province():
    conn = connect_to_sql()

    query_for_science_and_social_attendant = """
    SELECT COUNT(DISTINCT(sbd)) FROM Y2018 WHERE 
    toan IS NOT NULL
        AND van IS NOT NULL
        AND vatLy IS NOT NULL
        AND hoaHoc IS NOT NULL
        AND sinhHoc IS NOT NULL
        AND lichSu IS NOT NULL
        AND diaLy IS NOT NULL
        AND gdcd IS NOT NULL
    """

    query_for_science_attendant = """
    SELECT COUNT(DISTINCT(sbd)) FROM Y2018 WHERE 
        toan IS NOT NULL
        AND van IS NOT NULL
        AND vatLy IS NOT NULL
        AND hoaHoc IS NOT NULL
        AND sinhHoc IS NOT NULL
    """

    query_for_social_attendant = """
    SELECT COUNT(DISTINCT(sbd)) FROM Y2018 WHERE 
         toan IS NOT NULL
        AND van IS NOT NULL
        AND lichSu IS NOT NULL
        AND diaLy IS NOT NULL
        AND gdcd IS NOT NULL
    """

    query_for_independent_attendant = """
    SELECT COUNT(DISTINCT(sbd))
    FROM y2018
    WHERE 
    ( toan IS NULL OR van IS NULL
        OR ( vatLy IS NULL OR hoaHoc IS NULL OR sinhHoc IS NULL)
        AND (lichSu IS NULL OR diaLy IS NULL OR gdcd IS NULL)
    )
    """

    core_queries = [query_for_science_attendant, query_for_social_attendant, \
               query_for_science_and_social_attendant, query_for_independent_attendant]

    student_categorization = []
    for pCode in province_code:
        # constructing appropriate queries
        queries = core_queries
        if pCode != '00':
            # filter by province
            province_conditioning = f""" 
            AND sbd LIKE '{pCode}%'
            """
            queries = [query + ' ' + province_conditioning for query in core_queries]

        categories = [execute_query(conn, query)[0][0] for query in queries]
        print(categories)

        student_categorization.append({
            'province_code': pCode, 
            'science': categories[0] - categories[2], 
            'social': categories[1] - categories[2], 
            'both': categories[2], 
            'independent': categories[3]
        })

    conn.close()

    return student_categorization

# done debugging and cleaming
def get_expected_students_distribution():
    conn = connect_to_sql()
    expected_total_students = []
    core_query = """
        SELECT MAX(sbd) FROM Y2018  
    """

    for pCode in province_code:
        if pCode == '00':
            continue
            # filter by province 
        else:
            province_conditioning = f""" 
            WHERE sbd LIKE '{pCode}%'
            """
            query = core_query + ' ' + province_conditioning #concat the filter condition
            number_of_students = execute_query(conn, query)
        
        expected_total_students.append(int(number_of_students[0][0][2:]))

    conn.close()

    expected_total_students.insert(0, sum(expected_total_students))

    return expected_total_students


# done debugging and cleaning
def get_basic_attendant_stat_and_save_to_json():
    # getting data for provinces
    expected_attendant = get_expected_students_distribution()
    actual_attendant = get_actual_student_distribution()
    classify_by_type = get_student_categorization_by_province()

    for i in range(len(classify_by_type)):
        classify_by_type[i]['expected'] = expected_attendant[i]
        classify_by_type[i]['actual'] = actual_attendant[i]
        classify_by_type[i]['participation_percentage'] = \
            round(100*classify_by_type[i]['actual']/classify_by_type[i]['expected'], 2)
        

    with open(attendant_cache, 'w', encoding='utf-8') as f:
        json.dump(classify_by_type, f)
    f.close()

# done debugging and cleaning
def get_province_score_distribution_by_subject(pCode, subject):
    conn = connect_to_sql()
    if pCode == '00':
        pCode = ''

    query = f"""
        SELECT {subject}, COUNT(*)
        FROM y2018
        WHERE sbd LIKE '{pCode}%'
        GROUP BY {subject}
        ORDER BY {subject}
    """
    

    score_distribution = execute_query(conn, query)

    # post-query processing:
    # Create a full range of scores from 0 to 10 with a step of 0.2 or 0.25
    if subject == 'toan' or subject == 'ngoaiNgu':
        all_possible_score = np.arange(0, 10.2, 0.2).round(1)
    else:
        all_possible_score = np.arange(0, 10.25, 0.25).round(2)
    
    # convert fetched data to appropriate data form
    score_distribution = {float(score): count for score, count in score_distribution if score is not None}

    # Merge with the full range and fill missing scores with 0
    score_counting = []
    for score in all_possible_score:
        if score not in score_distribution.keys():
            score_counting.append(0)
        else:
            score_counting.append(score_distribution[score])

    # return object
    distribution_by_subject = {
        'score': list(all_possible_score),
        'count': score_counting
    }

    return distribution_by_subject

def get_score_distribution_of_all_provinces_and_saves_to_json():
    score_distribution_by_province = []
    for pCode in province_code:
        province_score_distribution = {"province_code": pCode}
        for subject in ['toan', 'van', 'ngoaiNgu', 'vatLy', 'hoaHoc', 'sinhHoc', 'lichSu', 'diaLy', 'gdcd']:
            subject_score_distribution = get_province_score_distribution_by_subject(pCode, subject)
            province_score_distribution[subject] = subject_score_distribution

        score_distribution_by_province.append(province_score_distribution)

    with open(score_distribution_cache, 'w') as json_file:
        json.dump(score_distribution_by_province, json_file)
    json_file.close()




if __name__ == "__main__":
    get_basic_attendant_stat_and_save_to_json()

