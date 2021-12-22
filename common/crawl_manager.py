import os
import logging
import common.file_utils as file
import re
import requests
import shutil

from abc import *
from urllib.request import urlopen

class CrawlManager(metaclass=ABCMeta):
    driver = None
    logger = logging.getLogger()
    
    # 회원 데이터 수집
    @abstractmethod
    def list(self):
        pass
    
    
    # 게시물 수집
    @abstractmethod
    def detail(self, url):
        pass
    
    
    # 게시물 번호 생성
    def create_board_post_id(self, post_id, board_id):
        return str((int(board_id) * 100000) + int(post_id))
    
    
    # 게시물 정보 생성
    def create_board_content_info(self, site_id, crawl_datas):
        datas = []
        
        for data in crawl_datas:        
            datas.append(dict(board_post_id=data[0], board_id=data[1], parent_id="", author_name=data[3], subject=data[2], message=data[9], 
                                is_notice=data[7], password="", is_secret="0", views=data[5], add_date=data[4], edit_date="", use_at="Y"))
        
        if len(datas):                                                                                                                                                  
            file.write_xml(site_id, datas, "content")    
            

    # 첨부파일 정보 생성                
    def create_attach_info(self, site_id, datas):
        attach_datas = []

        for data in datas:
            if data[3] != "":
                attach_datas.append(dict(board_post_id=data[0], board_id=data[1], file_name=data[3], file_path=data[4], add_date=data[2], edit_date="",  use_at="Y"))
        
        if len(attach_datas):                                                                                                                                                  
            file.write_xml(site_id, attach_datas, "attach")    


    # 첨부파일 다운로드
    def download_attach_file(self, site_id, datas):
        count = 0
        
        for data in datas:
            if data[5] != "":    
                download_path = os.path.join(os.path.dirname(__file__), "..", "download", site_id, data[1])
                file.create_directory(download_path)
                    
                response = requests.get(data[5])
                
                with open(os.path.join(download_path, data[4]),'wb') as f:
                    f.write(response.content)
                    
                    if count % 10 == 0:
                        print("[{0}]".format(str(count)), end='', flush=True)
                            
                    count += 1

        print("")        
        self.logger.info("Total download count : %s", count)


    # 첨부파일 복사
    def copy_attach_file(self, site_id, datas):
        count = 0
        
        for data in datas:
            if data[5] != "":                
                source_file = os.path.join(data[5], data[3].replace('&#44;', ',').strip())
                
                if source_file != "":                        
                    if os.path.exists(source_file):
                        download_path = os.path.join(os.path.dirname(__file__), "..", "download", site_id, data[1])
                        
                        file.create_directory(download_path)                    
                        shutil.copyfile(source_file, os.path.join(download_path, data[4]))
                        
                        count += 1                            

        print("")        
        self.logger.info("Total file count : %s", count)
        
        
    # 날짜 형식 변경
    def convert_date(self, s):
        return re.sub("[-:\s+]", "", s)
    

    # 특수문자 확인
    def getType(self, s):
        pattern = re.compile("^[0-9a-zA-Z가-힣]*$")
        return pattern.findall(s);


    # html tag 변환
    def escapeHtml(self, tag):
        result = []
        
        for i in range(len(tag)):
            if self.getType(tag[i]) == "" or tag[i] == '"' or tag[i] == '<' or tag[i] == '>' or tag[i] == '&':
                result.append("&#")
                result.append(str(ord(tag[i])))
                result.append(';')
            else:
                result.append(tag[i]);
        
        return ''.join(result)
    
    
    # 태그에서 주석 제거
    def delete_comment(self, word):
        result = []     
        words = word.split('<!--')
        
        for w in words:            
            end = w.find('-->')

            if end > -1:
                result.append(w[end+3:])        

        if len(result) > 0:
            return ''.join(result)
        else:
            return word