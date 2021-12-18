from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import common.file_utils as file_utils
import common.logger as logger

PROJECT_NAME = "crawl"
BASE_URL = "https://news.jtbc.joins.com/section/list.aspx?scode=" # JTBC 뉴스
ROOT_URL = "https://news.jtbc.joins.com"
RESULT_TEXT_FILE_NAME = "/Users/baltigo/workspace/python-boilerplate/crawling.txt"
RESULT_CSV_FILE_NAME = "/Users/baltigo/workspace/python-boilerplate/crawling.csv"
HEADER = ['제목', '작성자', '등록일', '내용']

# Create logger
logger = logger.create_logger(PROJECT_NAME)

driver = webdriver.Chrome(ChromeDriverManager().install())

# 목록
def crawling():
    driver.get(BASE_URL)
    bsObject = bs(driver.page_source, 'html.parser')

    root = bsObject.find("ul", {"id":"section_list"})
    items = root.find_all("li")

    results = []

    for item in items:
        data = item.find("dt", {"class":"title_cr"})
        link = data.find("a")
        
        results.append(detail(link.get("href")))

    file_utils.file_writer(RESULT_TEXT_FILE_NAME, results)   
    file_utils.csv_writer(RESULT_CSV_FILE_NAME, results, HEADER)
       

# 상세 내용
def detail(detail_url):
    full_detail_url = ROOT_URL + detail_url

    logger.info("Detail Url : %s", full_detail_url) 

    driver.get(full_detail_url)

    bsObject = bs(driver.page_source, 'html.parser')
    
    title = bsObject.find("h3", {"id" : "jtbcBody"}).text # 제목
    writer = bsObject.find("dd", {"class" : "name"}).text # 작성자
    content = bsObject.find("div", {"class" : "article_content"}).text # 본문
    date_tag =bsObject.find("span" , {"class" : "artical_date"})  # 작성일 
    reg_dates =date_tag.find_all("span")
    
    if len(reg_dates) > 1:
        reg_date = reg_dates[1].text  # 수정일
    else:
        reg_date = reg_dates[0].text  # 입력일

    return [title, writer, reg_date, content]
            
    
def main(): 
    logger.info("Start crawling...")

    crawling()
    
    driver.quit()
    
    logger.info("End")

    
if __name__ == '__main__':
    main()