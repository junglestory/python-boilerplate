import sys
import common.logger as logger
import common.file_utils as file_utils

PROJECT_NAME = "boilerplate"
ARGV_COUNT = 2

# Create logger
logger = logger.create_logger(PROJECT_NAME)

def main(args):
    file_utils.file_writer()
    file_utils.csv_writer()

# 실행 옵션 설명
def run_info():
    print("Usage: main.py [OPTIONS]")
    print("")
    print("Options:")
    print("  --site_id TEXT     [required]")
    print("  --type TEXT      [optional : member/board] ")


if __name__ == '__main__':    
    for i in range(len(sys.argv)):
        if i > 0:
            logger.info('arg value = %s', sys.argv[i])
   
    if len(sys.argv) >= ARGV_COUNT:
        main(sys.argv)
    else:
        logger.error("Requires at least %s argument, but only %s were passed.", ARGV_COUNT-1, len(sys.argv)-1)
        run_info()    