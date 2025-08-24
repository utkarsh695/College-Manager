from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview

# import face_recognition
import pymysql
from tkcalendar import DateEntry
from PIL import Image,ImageTk

class CreateAdminClass:
    defaultname="default_image.png"
    def __init__(self):
        self.window = Tk()
        self.window.title("My College Manager\Create Admin")

        # ------------- settings ------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()

        w1 = int(w/2)
        h1 = int(h/2)+200
        x1 = int(w/4)
        y1 = int(h/4)-100
        self.window.minsize(w1,h1)
        self.window.geometry("%dx%d+%d+%d"%(w1,h1,x1,y1))#wxh+x+y

        # ------------- widgets ----------------------------------
        mycolor1 = '#EDE8F5'
        mycolor2 = '#7091E6'
        myfont1 = ('Cambria',13,'bold')
        self.window.config(background=mycolor1)

        self.hdlbl = Label(self.window,text='Welcome to My college Manager',background=mycolor2,font=('Cambria',20,'bold'))


        self.L1 = Label(self.window,text='Username',background=mycolor1,font=myfont1)
        self.L2 = Label(self.window,text='Password',background=mycolor1,font=myfont1)
        self.L3 = Label(self.window,text='Usertype',background=mycolor1,font=myfont1)
        self.L4 = Label(self.window,text='Pic',background=mycolor1,font=myfont1)

        self.t1 = Entry(self.window,font=myfont1)
        self.t2 = Entry(self.window,font=myfont1,show='*')
        self.v1 = StringVar()
        self.v2 = StringVar()
        self.c1 = Combobox(self.window,values=['Admin','Employee'],
                           textvariable=self.v1,font=myfont1,state='disable')
        self.c1.current(0)


        #----------------- buttons ---------------------
        self.b1 = Button(self.window,text='Save',font=myfont1,background=mycolor2,command=self.saveData)
        self.b7 = Button(self.window,text='Reset',font=myfont1,background=mycolor2,command=self.clearPage)
        self.b6 = Button(self.window,text='Choose',font=myfont1,background=mycolor2,command=self.selectImage)

        self.imglbl = Label(self.window,relief='groove',borderwidth=1)

        # ------------placement -----------------
        self.hdlbl.place(x=0,y=0,width=w1,height=70)
        x1 = 10
        y1 =100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L4.place(x=x1,y=y1)
        self.imgsize=150
        self.imglbl.place(x=x1+x_diff,y=y1,width=self.imgsize,height=self.imgsize)
        self.b6.place(x=x1+x_diff,y=y1+self.imgsize,width=self.imgsize,height=40)
        y1+=self.imgsize
        y1+=y_diff
        self.b1.place(x=x1,y=y1,width=150,height=40)
        y1+=y_diff
        self.b7.place(x=x1,y=y1,width=150,height=40)



        #------call required functions ----------
        self.databaseConnection()
        self.clearPage()

        self.window.mainloop()

    def selectImage(self):
        filename = askopenfilename(filetypes=[ ("All Pictures","*.jpg;*.png;*.jpeg") , ("PNG Images","*.png"),
                                               ("JPG Images",'*.jpg')],parent=self.window)

        if filename!="":
            #show image
            self.img1 = Image.open(filename).resize((self.imgsize,self.imgsize))
            self.pimg1= ImageTk.PhotoImage(self.img1)
            self.imglbl.config(image=self.pimg1)

            #make name
            import time
            path=filename.split("/")
            name = path[-1]
            unique= str(int(time.time()))
            self.actualname = unique+name

            # # detect face
            # image = face_recognition.load_image_file(filename)
            # face_locations = face_recognition.face_locations(image)
            # if len(face_locations) != 1:
            #     messagebox.showwarning("Input Error", "Please Select One Face Image ", parent=self.window)
            #     self.actualname = self.defaultname
            #     self.img1 = Image.open(self.actualname).resize((self.imgsize, self.imgsize))
            #     self.photoimg1 = ImageTk.PhotoImage(self.img1)
            #     self.imglbl.config(image=self.photoimg1)
            #     return False

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
            #	username	password	usertype	pic

            qry = 'insert into usertable values(%s,%s,%s,%s)'
            rowcount = self.curr.execute(qry ,(self.t1.get(), self.t2.get(), self.v1.get(),self.actualname) )
            self.conn.commit()
            if rowcount==1:
                uname=self.t1.get()
                #--------- save image ---------------
                if self.actualname!=self.defaultname: # new image is given
                    self.img1.save("user_images//"+self.actualname)
                #---------------------------------------

                messagebox.showinfo("Success","Admin Created successfully",parent=self.window)
                self.window.destroy()
                from Homepage import HomepageClass
                HomepageClass(uname,"Admin")
            else:
                messagebox.showwarning("Failure","User Record not Saved y",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)


    def clearPage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        # show image
        self.actualname=self.defaultname
        self.img1 = Image.open("user_images//"+self.actualname).resize((self.imgsize, self.imgsize))
        self.pimg1 = ImageTk.PhotoImage(self.img1)
        self.imglbl.config(image=self.pimg1)

        self.b1['state']='normal'



    def validationCheck(self):
        return True



#--------- for testing only ------------
if __name__ == '__main__':
   CreateAdminClass()