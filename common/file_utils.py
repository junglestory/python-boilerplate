import os
import csv

FILE_ENCODING ="utf-8"
NEW_LINE = '\n'

# 텍스트 파일 생성
def file_writer(file_path, datas):
    f = open(file_path, "w", encoding=FILE_ENCODING)

    for data in datas:
        for key, value in data.items():
            f.write(value + NEW_LINE)
            
        f.write(NEW_LINE)

    f.close()
    
    
# csv 파일 생성
def csv_writer(file_path, datas, titles):
    f = open("C:/hm_py/crawling/result/rawling_hw3.csv",'w', newline='', encoding="utf-8")

    r = csv.writer(f)
    r.writerow([titles])

    for data in datas:
        r.writerow([data])