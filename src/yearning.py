# _*_ coding:utf-8 _*_

import pymysql


class YearningDb():
    def __init__(self,host='10.10.10.1111',username='yunwei',port=3306,password='w2nbw@tyuYPa9jbn',database='Yearning'):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        try:
            self.conn=pymysql.connect(host=self.host,port=self.port,user=self.username,password=self.password,database=self.database)
            self.cursor=self.conn.cursor()
        except Exception as e:
            print(e)        
            
    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def query(self,sql):
        '''查询数据,返回元组类型'''
        try:
            self.cursor.execute(sql)
            results=self.cursor.fetchall()
            return results
        except Exception as e:
            print(e)
            return False
            
    def run(self,sql):
        #sql= "select * from core_sql_orders where status='2'"
        results=self.query(sql)
        if results:
            for row in results:
                work_id=row[1]
                username=row[2]
                date=row[10]
                sql=row[11].split(';')
                text=row[12]
                assigned=row[13]
                real_name=row[16]
                executor=row[17]
                return work_id,username,date,sql,text,assigned,real_name,executor
        else:
            return '','','','','','','',''
            
# if __name__ == "__main__":
    #ydb=YearningDb()
    # sql= "select * from core_sql_orders where status='2'"   
    # result=ydb.query(sql)
    # print(result)
    # ydb.close()
    # for row in result:
        # work_id=row[1]
        # username=row[2]
        # date=row[10]
        # sql=row[11]
        # text=row[12]
        # assigned=row[13]
        # real_name=row[16]
        # print(work_id,username,date,sql,text,assigned,real_name)
    # ydb.run()
    
    

