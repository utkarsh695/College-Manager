from tkinter import *
from tkinter import messagebox
import pymysql

class MainClass:
    def __init__(self):
        self.databaseConnection()
        try:
            qry = 'select * from usertable'
            rowcount = self.curr.execute(qry  )
            rowdata = self.curr.fetchone()
            if rowdata:
                from Loginpage import LoginClass
                LoginClass()
            else:
                from createAdminPage import CreateAdminClass
                CreateAdminClass()

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e))


    def databaseConnection(self):

        try:
            self.conn = pymysql.connect(host='localhost',db='mycollegemanager_db',user='root',password='')
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Error in Database Connection : \n"+str(e))


if __name__ == '__main__':
    MainClass()