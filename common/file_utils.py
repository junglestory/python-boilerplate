import os
import csv
import yaml

FILE_ENCODING ="utf-8"
NEW_LINE = '\n'
CONFIG_PATH = "config"
SITE_INFO_FILE = "site.yml"


# 사이트 정보 읽기
def read_site_info(site_id):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    doc = yaml.load(open(os.path.join(root_dir, CONFIG_PATH, SITE_INFO_FILE), "r", encoding = FILE_ENCODING), Loader=yaml.SafeLoader)

    return doc[site_id]

# 텍스트 파일 생성
def file_writer(file_path, datas):
    f = open(file_path, "w", encoding=FILE_ENCODING)

    for data in datas:
        for i in range(len(data)):
            f.write(data[i] + NEW_LINE)
            
        f.write(NEW_LINE)

    f.close()
    
    
# csv 파일 생성
def csv_writer(file_path, datas, header):
    f = open(file_path,'w', newline='', encoding=FILE_ENCODING)

    r = csv.writer(f)
    r.writerow(header)

    for data in datas:
        r.writerow(data)