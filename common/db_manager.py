import pymysql
import logging

class DatabaseManager:
    conn = None
    logger = logging.getLogger()
    
    def __init__(self, datasource, journal_id):
        self.datasource = datasource
        self.journal_id = journal_id


    def connection(self):
        try:
            self.conn = pymysql.connect(host=self.datasource['host'], port=self.datasource['port'], 
                                        user=self.datasource['username'], passwd=self.datasource['password'], 
                                        db=self.datasource['database'],charset='utf8',autocommit=False)
            self.logger.info("Connected to %s ." % self.datasource['host'])
        except Exception as e:
            self.logger.error("Failed connect to %s ." % self.datasource['host'])
            self.logger.error(e)


    def close(self):
        if self.conn != None:
            self.conn.close()    


    def execute_query(self, query, value):
        cs = self.conn.cursor()
        result = 0

        try:
            cs.executemany(query, value)
            self.conn.commit()
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
            result = -1
        finally:
            cs.close()
            return result


    def select_query(self, query):
        cs = self.conn.cursor()
        
        try:
            cs.execute(query)
            return cs.fetchall()
        except Exception as e:
            self.logger.error(e)
        finally:
            cs.close()


                