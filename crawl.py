import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import common.file_utils as file_utils
import common.logger as logger
from common.crawl_manager import *

PROJECT_NAME = "crawl"
RESULT_TEXT_FILE_NAME = "/Users/baltigo/workspace/python-boilerplate/result_{}.txt"
RESULT_CSV_FILE_NAME = "/Users/baltigo/workspace/python-boilerplate/result_{}.csv"
HEADER = ['제목', '작성자', '등록일', '내용']
ARGV_COUNT = 2

# Create logger
logger = logger.create_logger(PROJECT_NAME)

def create_crawl_manager(journal_id):
    # get module from module name
    mod_name = "crawl.{}_crawl".format(journal_id)    
    mod = __import__('%s' %(mod_name), fromlist=[mod_name])
    
    # get class in module
    klass = getattr(mod, "{}CrawlManager".format(journal_id.capitalize()))
    
    return klass(driver)


# 크롤링
def crawling(manager, journal_id):
    urls = []
    results = []

    urls = manager.list()
    
    for url in urls:
        results.append(manager.detail(url))

    file_utils.file_writer(RESULT_TEXT_FILE_NAME.format(journal_id), results)   
    file_utils.csv_writer(RESULT_CSV_FILE_NAME.format(journal_id), results, HEADER)
       
    
def main(args): 
    logger.info("Start crawling...")

    journal_id = args[1]

    if journal_id != None:
        manager = create_crawl_manager(journal_id)

        crawling(manager, journal_id)
        
        driver.quit()
    
    logger.info("Finished.")   
    sys.exit(1)

    
# 실행 옵션 설명
def run_info():
    print("Usage: migrator.py [OPTIONS]")
    print("")
    print("Options:")
    print("  --journal_id TEXT     [required]")


if __name__ == '__main__':
    for i in range(len(sys.argv)):
        if i > 0:
            logger.info('arg value = %s', sys.argv[i])
    print("args : " + str(len(sys.argv)))

    if len(sys.argv) >= ARGV_COUNT:    
        driver = webdriver.Chrome(ChromeDriverManager().install())

        main(sys.argv)
    else:
        logger.error("Requires at least %s argument, but only %s were passed.", ARGV_COUNT-1, len(sys.argv)-1)
        run_info()    