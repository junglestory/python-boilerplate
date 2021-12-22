from common.crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://news.jtbc.joins.com/section/list.aspx?scode=" # JTBC 뉴스
ROOT_URL = "https://news.jtbc.joins.com"

class JtbcCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver
       
        
    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
        bsObject = bs(self.driver.page_source, 'html.parser')

        root = bsObject.find("ul", {"id":"section_list"})
        items = root.find_all("li")

        results = []

        for item in items:
            data = item.find("dt", {"class":"title_cr"})
            link = data.find("a")
            
            results.append(link.get("href"))

        return results


    # 상세 내용
    def detail(self, url):
        full_detail_url = ROOT_URL + url

        self.logger.info("Detail Url : %s", full_detail_url) 

        self.driver.get(full_detail_url)

        bsObject = bs(self.driver.page_source, 'html.parser')
        
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