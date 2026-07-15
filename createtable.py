import mysql.connector

# 1. Establish database connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='student',
    database='school'
)
cursor = connection.cursor()

# 2. Create the timetable table structure
create_table_query = """
CREATE TABLE IF NOT EXISTS timetable (
    day VARCHAR(10) PRIMARY KEY,
    P1 VARCHAR(50),
    P2 VARCHAR(50),
    P3 VARCHAR(50),
    P4 VARCHAR(50),
    P5 VARCHAR(50),
    P6 VARCHAR(50),
    P7 VARCHAR(50),
    P8 VARCHAR(50)
);
"""
cursor.execute(create_table_query)
print("Database and 'timetable' table verified/created successfully.\n")

# 3. Collect input data from the user
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
schedule_data = []

print("--- TIMETABLE DATA ENTRY ---")
for day in days:
    print(f"\nEntering periods for {day.upper()}:")
    p1 = input("  Period 1: ")
    p2 = input("  Period 2: ")
    p3 = input("  Period 3: ")
    p4 = input("  Period 4: ")
    p5 = input("  Period 5: ")
    p6 = input("  Period 6: ")
    p7 = input("  Period 7: ")
    p8 = input("  Period 8: ")
    
    schedule_data.append((day, p1, p2, p3, p4, p5, p6, p7, p8))

# 4. Save/Update records in the MySQL table
insert_query = """
INSERT INTO timetable (day, P1, P2, P3, P4, P5, P6, P7, P8) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    P1=VALUES(P1), P2=VALUES(P2), P3=VALUES(P3), P4=VALUES(P4), 
    P5=VALUES(P5), P6=VALUES(P6), P7=VALUES(P7), P8=VALUES(P8);
"""
cursor.executemany(insert_query, schedule_data)
connection.commit()
print(f"\nSuccessfully saved the timetable to the database.")

# -------------------------------------------------------------
# FIXED SECTION: FETCH AND DISPLAY IN CHRONOLOGICAL DAY ORDER
# -------------------------------------------------------------
print("\n--- RETRIEVED TIMETABLE (CORRECT DAY ORDER) ---")

# FIELD() forces MySQL to output Mon, then Tue, Wed, Thu, Fri
select_ordered_query = """
SELECT * FROM timetable 
ORDER BY FIELD(day, 'Mon', 'Tue', 'Wed', 'Thu', 'Fri');
"""
cursor.execute(select_ordered_query)
rows = cursor.fetchall()

# Print the layout table header cleanly
print("Day    | P1       | P2       | P3       | P4       | P5       | P6       | P7       | P8       ")
print("-" * 95)

# Print each row matching your grid view format
for row in rows:
    print(f"{row[0]:<6} | {row[1]:<8} | {row[2]:<8} | {row[3]:<8} | {row[4]:<8} | {row[5]:<8} | {row[6]:<8} | {row[7]:<8} | {row[8]:<8}")

# 5. Safely close database connections
cursor.close()
connection.close()
print("\nMySQL connection closed.")
