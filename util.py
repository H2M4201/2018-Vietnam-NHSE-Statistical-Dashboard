import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def load_caching_information():
    # load provinces 
    with open(os.environ.get("PROVINCE_INFO"), 'r', encoding='utf-8') as json_file:
        provinces = json.load(json_file)
    json_file.close()

    # load caching stat about participation
    with open(os.environ.get("PARTICIPATION_INFO"), 'r', encoding='utf-8') as json_file:
        attendant_stat = json.load(json_file)
    json_file.close()

    # load caching stat score distribution
    with open(os.environ.get("SCORE_DISTRIBUTION_INFO"), 'r', encoding='utf-8') as json_file:
        score_distribution_stat = json.load(json_file)
    json_file.close()

    return provinces, attendant_stat,score_distribution_stat

provinces, attendant_stat,score_distribution_stat = load_caching_information()

def find_attendant_stat_by_province(province_code):
    result = next((item for item in attendant_stat if item['province_code'] == province_code), None)
    return result

def find_score_distribution_stat_by_province(province_code):
    result = next((item for item in score_distribution_stat if item['province_code'] == province_code), None)
    return result

