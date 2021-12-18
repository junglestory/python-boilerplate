import csv

FILE_ENCODING ="utf-8"
NEW_LINE = '\n'

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