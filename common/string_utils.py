import re

# 태그 제거
def relace_tag(content):
    cleaner = re.compile('<.*?>')
    cleantext  = re.sub(cleaner, '', content)     
    
    return cleantext    