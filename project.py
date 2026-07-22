import mysql.connector as m
import customtkinter as ctk
import pandas as pd

con = m.connect(host="localhost", user="root", passwd="student")
c = con.cursor()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

def welcomepage(): 
    global app, entry, entry1
    
    app = ctk.CTk()
    app.geometry("700x500")
    app.title('Timetable Entry')
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    
    label = ctk.CTkLabel(app, text="Welcome to Timetable Entry", font=('Arial', 23))
    label.grid(row=0, column=0, columnspan=3, pady=20)
    
    entry = ctk.CTkEntry(app, placeholder_text="Type in your Name", width=280)
    entry.grid(row=1, column=0, padx=30, pady=20, sticky="e")
    
    entry1 = ctk.CTkEntry(app, placeholder_text="Type in your Code", width=280)
    entry1.grid(row=1, column=1, padx=30, pady=20, sticky="w")
    

    def on_submit():
        global code, name
        name = entry.get()
        code = entry1.get()
        
        if not code.strip():
            print("Please fill out the code field.")
            return

        c.execute("USE user1")
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS `{code}` (
                Day VARCHAR(15), 
                P1 VARCHAR(4), P2 VARCHAR(4), P3 VARCHAR(4), P4 VARCHAR(4), 
                P5 VARCHAR(4), P6 VARCHAR(4), P7 VARCHAR(4), P8 VARCHAR(4)
            )
        """)
        con.commit()

        entry.delete(0, 'end')
        entry1.delete(0, 'end')
        showedit()

    button = ctk.CTkButton(app, text="Enter", command=on_submit)
    button.grid(column=0, row=4, pady=10, padx=10, columnspan=3)
    
    app.mainloop()

def showedit():
    tablewin = ctk.CTkToplevel(app)
    tablewin.title("Create/Edit")
    tablewin.geometry("450x200")
    tablewin.transient(app)
    
    cb = ctk.CTkButton(tablewin, text="Create Timetable", command=lambda: insertval(tablewin))
    eb = ctk.CTkButton(tablewin, text="Show existing table", command=lambda: showtable(tablewin))
    cb.grid(row=1, column=0, padx=30, pady=20, sticky="e")
    eb.grid(row=1, column=2, padx=30, pady=20, sticky="w")
    
    tablewin.focus()
    tablewin.lift()

def insertval(tablewin):
    tablewin.destroy()
    inserttable = ctk.CTkToplevel(app)
    inserttable.title("Create Table")
    inserttable.geometry("950x600")
    inserttable.focus()
    inserttable.lift()
    
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods_list = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
    entry_matrix = {}

    table_frame = ctk.CTkScrollableFrame(inserttable, height=400)
    table_frame.pack(padx=20, pady=20, fill="both", expand=True)

    day_header = ctk.CTkLabel(table_frame, text="Day", font=("Arial", 13, "bold"), text_color="#1f538d")
    day_header.grid(row=0, column=0, padx=8, pady=8, sticky="w")

    for col_idx, col_name in enumerate(periods_list, start=1):
        header = ctk.CTkLabel(table_frame, text=col_name, font=("Arial", 13, "bold"), text_color="#1f538d")
        header.grid(row=0, column=col_idx, padx=8, pady=8, sticky="ew")

    for row_idx, day_name in enumerate(days_list, start=1):
        day_label = ctk.CTkLabel(table_frame, text=day_name, font=("Arial", 12, "bold"))
        day_label.grid(row=row_idx, column=0, padx=8, pady=6, sticky="w")
        
        entry_matrix[day_name] = []
        for col_idx in range(1, len(periods_list) + 1):
            entry_field = ctk.CTkEntry(table_frame, placeholder_text="-", width=80)
            entry_field.grid(row=row_idx, column=col_idx, padx=6, pady=6, sticky="ew")
            entry_matrix[day_name].append(entry_field)

    def handle_save():
        c.execute("USE user1")
        for day, entries in entry_matrix.items():
            tasks = [entry_field.get() for entry_field in entries]
            query = f"REPLACE INTO `{code}` (Day, P1, P2, P3, P4, P5, P6, P7, P8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = [day] + tasks
            c.execute(query, values)
            
        con.commit()
        print("Weekly Schedule Saved Successfully!")
        inserttable.destroy()

    save_btn = ctk.CTkButton(inserttable, text="Save Weekly Schedule", command=handle_save)
    save_btn.pack(pady=(0, 20))

def showtable(tablewin):
    tablewin.destroy()
    c.execute("USE user1")
    
    # Check if table has data safely
    try:
        c.execute(f"SELECT 1 FROM `{code}` LIMIT 1")
        has_data = c.fetchone() is not None
    except:
        has_data = False

    if has_data:
        query = f"SELECT * FROM `{code}`"
        df = pd.read_sql_query(query, con)
        
        shtable = ctk.CTkToplevel(app)
        shtable.geometry("950x600")
        shtable.title("Weekly Timetable")
        for col_idx, column in enumerate(df.columns):
            header = ctk.CTkLabel(shtable,text=str(column), font=("Consolas",24,"bold"))
            header.grid(row=0,column=col_idx, padx=15, pady=10,sticky='w')
        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                cell = ctk.CTkLabel(shtable,text=str(value), font=("Consolas",20))
                cell.grid(row=row_idx + 1, column=col_idx,padx=15,pady=5,sticky='w')
        
    else:
        dialog_box = ctk.CTkToplevel(app)
        dialog_box.geometry("680x200")
        label1 = ctk.CTkLabel(dialog_box, text="TIMETABLE DOESNT EXIST!",font=('Arial',20),text_color="white")
        label1.grid(row=1, column=1, padx=30, pady=20)   
        
        btn1 = ctk.CTkButton(dialog_box, text="Make a new one", command=lambda: insertval(dialog_box))
        btn2 = ctk.CTkButton(dialog_box, text="Close", command=lambda: dialog_box.destroy()) 
        btn1.grid(row=2, column=0, padx=10, pady=20, sticky="e")   
        btn2.grid(row=2, column=2, padx=10, pady=20, sticky="w")


welcomepage()
con.close()
