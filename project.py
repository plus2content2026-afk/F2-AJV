import mysql.connector as m
import customtkinter as ctk
con = m.connect(host="localhost",user="root",passwd="student")
c=con.cursor()
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.geometry("700x500")
app.title(' Timetable Entry')
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
label = ctk.CTkLabel(app,text="Welcome to Timetable Entry", font=('Arial',23))
label.grid(row=0,column=0,columnspan=3)
entry = ctk.CTkEntry(app,placeholder_text="Type in your Name",state="normal",width=280)
entry.grid(row=1,column=0,padx=30,pady=20,sticky="e")
entry1 = ctk.CTkEntry(app,placeholder_text="Type in your Code",state="normal",width=280)
entry1.grid(row=1,column=1,padx=30,pady=20,sticky="w")
def createtable():
    name= entry.get()
    global code
    code = entry1.get()
    c.execute("USE user1")
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {code} (
            Day VARCHAR(8), 
            P1 VARCHAR(10), 
            P2 VARCHAR(10), 
            P3 VARCHAR(10), 
            P4 VARCHAR(10), 
            P5 VARCHAR(10), 
            P6 VARCHAR(10), 
            P7 VARCHAR(10), 
            P8 VARCHAR(10)
            )
        """)

    entry.delete(0, 'end')
    entry1.delete(0, 'end')
    showedit()
def showedit():
    tablewin = ctk.CTkToplevel(app)
    tablewin.title("Create/Edit")
    tablewin.geometry("450x200")
    cb = ctk.CTkButton(tablewin,text="Create Timetable",command= lambda: insertval(tablewin),)
    eb = ctk.CTkButton(tablewin,text="Show existing table",command= lambda :showtable(tablewin))
    cb.grid(row=1,column=0,padx=30,pady=20,sticky="e")
    eb.grid(row=1,column=2,padx=30,pady=20,sticky="w")
    tablewin.focus()
    tablewin.lift()
    print("working")
def insertval(tablewin):
    tablewin.destroy()
    inserttable = ctk.CTkToplevel(app)
    inserttable.title("Create Table")
    inserttable.geometry("800x800")
    inserttable.focus()
    inserttable.lift()
    print("Ivade vare working")
def showtable():
    tablewin.destroy()
    
    print("Ivadeyum working aan")
button = ctk.CTkButton(app, text="Enter", command=createtable)
button.grid(column=0,row=4,pady=10,padx=10,columnspan=3)
app.mainloop()
