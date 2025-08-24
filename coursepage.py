from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview
import pymysql
from tkcalendar import DateEntry
from PIL import Image,ImageTk

class CourseClass:
    def __init__(self,hwindow):
        self.window = Toplevel(hwindow)
        self.window.title("My College Manager\Course")

        # ------------- settings ------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()

        x1 = 200
        w1 = w-x1
        y1 = 50
        h1 = h-y1-100
        self.window.minsize(w1,h1)
        self.window.geometry("%dx%d+%d+%d"%(w1,h1,x1,y1))#wxh+x+y

        # ------------- widgets ----------------------------------
        mycolor1 = '#EDE8F5'
        mycolor2 = '#7091E6'
        myfont1 = ('Cambria',13,'bold')
        self.window.config(background=mycolor1)

        self.hdlbl = Label(self.window,text='Course',background=mycolor2,font=('Cambria',20,'bold'))


        self.L1 = Label(self.window,text='Department',background=mycolor1,font=myfont1)
        self.L2 = Label(self.window,text='Course Name',background=mycolor1,font=myfont1)
        self.L3 = Label(self.window,text='Fee(Rs) ',background=mycolor1,font=myfont1)
        self.L4 = Label(self.window,text='Duration',background=mycolor1,font=myfont1)

        self.v1 = StringVar()
        self.c1 = Combobox(self.window,values=['IT','Science'],textvariable=self.v1,font=myfont1,state='readonly')
        self.t2 = Entry(self.window,font=myfont1)
        self.t3 = Entry(self.window,font=myfont1)
        self.t4 = Entry(self.window,font=myfont1)
        self.v2 = StringVar()
        self.c2 = Combobox(self.window,values=['Year(s)',"Month(s)","Day(s)"],textvariable=self.v2,font=myfont1,state='readonly')

        # ------------------ table ---------------------
        self.mytable1 = Treeview(self.window, columns=['c1', 'c2', 'c3', 'c4', 'c5'], height=10)

        self.mytable1.heading('c1', text='Department')
        self.mytable1.heading('c2', text='Course')
        self.mytable1.heading('c3', text='Fee')
        self.mytable1.heading('c4', text='Duration')
        self.mytable1.heading('c5', text='Units')
        self.mytable1['show'] = 'headings'

        self.mytable1.column('c1', width=100, anchor='center')
        self.mytable1.column('c2', width=100, anchor='center')
        self.mytable1.column('c3', width=100, anchor='center')
        self.mytable1.column('c4', width=100, anchor='center')
        self.mytable1.column('c5', width=100, anchor='center')
        self.mytable1.bind("<ButtonRelease-1>",lambda e: self.getSelectedRow())

        #----------------- buttons ---------------------
        self.b1 = Button(self.window,text='Save',font=myfont1,background=mycolor2,command=self.saveData)
        self.b2 = Button(self.window,text='Update',font=myfont1,background=mycolor2,command=self.updateData)
        self.b3 = Button(self.window,text='Delete',font=myfont1,background=mycolor2,command=self.deleteData)
        self.b4 = Button(self.window,text='Fetch',font=myfont1,background=mycolor2,command=self.fetchData)
        self.b5 = Button(self.window,text='Search',font=myfont1,background=mycolor2,command=self.showAllData)
        # ------------placement -----------------
        self.hdlbl.place(x=0,y=0,width=w,height=70)
        x1 = 10
        y1 =100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)
        self.b5.place(x=x1+x_diff*2+80,y=y1,width=100,height=25)
        self.mytable1.place(x=x1+x_diff*3+32,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        self.b4.place(x=x1+x_diff*2+80,y=y1,width=100,height=25)
        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.t3.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L4.place(x=x1,y=y1)
        self.t4.place(x=x1+x_diff,y=y1,width=50)
        self.c2.place(x=x1+x_diff+70,y=y1,width=100)

        y1+=y_diff
        self.b1.place(x=x1,y=y1,width=150,height=40)
        self.b2.place(x=x1+x_diff,y=y1,width=150,height=40)
        self.b3.place(x=x1+x_diff*2,y=y1,width=150,height=40)

        #------call required functions ----------
        self.databaseConnection()
        self.getAllDepartments()
        self.clearPage()

        self.window.mainloop()



    def databaseConnection(self):

        try:
            self.conn = pymysql.connect(host='localhost',db='mycollegemanager_db',user='root',password='')
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Error in Database Connection : \n"+str(e),parent=self.window)

    def saveData(self):
        if self.validationCheck()==False:
            return # end this function now
        try:
            #rollno	name	phone	gender	dob	address	department	course
            qry = 'insert into course values(%s,%s,%s,%s,%s)'
            rowcount = self.curr.execute(qry ,(self.v1.get(), self.t2.get(),self.t3.get(),
                    self.t4.get(),self.v2.get()) )
            self.conn.commit()
            if rowcount==1:

                messagebox.showinfo("Success","Course Record Saved successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","Course Record not Saved y",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def updateData(self):
        if self.validationCheck()==False:
            return # end this function now
        try:
            qry = 'update course set dname=%s, fee=%s, duration=%s, units=%s where cname=%s'
            rowcount = self.curr.execute(qry ,(self.v1.get(),self.t3.get(),
                    self.t4.get(),self.v2.get(), self.t2.get()) )
            self.conn.commit()
            if rowcount==1:

                messagebox.showinfo("Success","Course Record Updated successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","Course Record not Updated ",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def deleteData(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to delete??",parent=self.window)
        if ans=='yes':
            try:
                qry = 'delete from course where cname=%s'
                rowcount = self.curr.execute(qry ,(self.t2.get()) )
                self.conn.commit()
                if rowcount==1:
                    messagebox.showinfo("Success","Course  Record Deleted successfully",parent=self.window)
                    self.clearPage()
                else:
                    messagebox.showwarning("Failure","Course  Record not Deleted ",parent=self.window)
            except Exception as e:
                messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def getSelectedRow(self):
        id = self.mytable1.focus()
        row_record = self.mytable1.item(id)
        row = row_record['values']
        col0 = row[1]
        self.fetchData(col0)

    def fetchData(self,pcolumn=None):
        if pcolumn==None:
            col = self.t2.get()
        else:
            col = pcolumn
        try:
            #rollno	name	phone	gender	dob	address	department	course
            qry = 'select * from course where cname=%s'
            rowcount = self.curr.execute(qry ,(col) )
            rowdata = self.curr.fetchone()
            self.clearPage()
            if rowdata:
                # set data in fields
                self.v1.set(rowdata[0])
                self.t2.insert(0,rowdata[1])
                self.t3.insert(0,rowdata[2])
                self.t4.insert(0,rowdata[3])
                self.v2.set(rowdata[4])
            else:
                messagebox.showwarning("Empty","No Record Found",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def clearPage(self):
        self.t2.delete(0,END)
        self.t3.delete(0,END)
        self.t4.delete(0,END)
        self.c1.set("Choose Department")
        self.c2.current(0)
        self.showAllData()

    def showAllData(self):
        try:
            self.mytable1.delete(*self.mytable1.get_children())
            #rollno	name	phone	gender	dob	address	department	course

            dept=self.v1.get()
            if dept=="Choose Department":
                dept=""

            qry = 'select * from course where dname like %s'
            rowcount = self.curr.execute(qry,(dept+"%") )
            rowdata = self.curr.fetchall()
            if rowdata:
                for row in rowdata:
                    self.mytable1.insert('',END,values=row)
            else:
                messagebox.showwarning("Empty","No Record Found",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def validationCheck(self):
        return True

    def getAllDepartments(self):
        try:
            qry = 'select * from department'
            rowcount = self.curr.execute(qry )
            rowdata = self.curr.fetchall()
            self.dept_list=[]
            if rowdata:
                self.c1.set("Choose Department")
                for row in rowdata:
                     self.dept_list.append(row[0])
            else:
                self.c1.set("No Department")
            self.c1.config(values=self.dept_list)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

#--------- for testing only ------------
if __name__ == '__main__':
    dummy_home=Tk()
    CourseClass(dummy_home)
    dummy_home.mainloop()