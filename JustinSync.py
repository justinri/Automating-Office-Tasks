import schedule, time, pyodbc
from datetime import date
from function_files.shipping import checkTracking
from function_files.send_tracking import daily_tracking_email
from function_files.accounting import AR_past_due
from function_files.receiving import PO_receiving_past_due

### Setting up the connection:
today = date.today()
# today = "2020-10-21"
print(today)
conn = pyodbc.connect('Driver={SQL Server};'
                     'Server=WIN2008SVR\JBSQL;'
                     # 'Database=TRAINING;'
                     'Database=PRODUCTION;'
                     'Trusted_Connection=yes;')     
cursor = conn.cursor()

### Getting Table Names:
# for num, rows in enumerate(cursor.tables()):
    # num += 1
    # if num < 150:# and num > 300:
        # print(rows.table_name)
# quit()

# Getting names of columns (Tables: Address, Packlist_Detail, Packlist_Header, SO_Header, SO_Detail)
# for num, row in enumerate(cursor.columns(table="PO_Header")):
    # print(num, row.column_name)
# quit()

# # cursor.execute("SELECT Address, Customer, Line1, Line2, City, State, Zip, Name, Country FROM Address")
# # table = cursor.fetchall()
# # for row in table:
    # # if row[1] == 1408:
        # # print(row)
# # # table = cursor.fetchall()
# # # print(table)

# quit()

### Scheduling jobs to run
#schedule.every(30).minutes.do(checkTracking,'It is 01:00')


### Pulling data from JobBOSS
cursor.execute("SELECT * FROM Packlist_Detail")
table_Packlist_Detail = cursor.fetchall()

cursor.execute("SELECT * FROM Packlist_Header")
table_Packlist_Header = cursor.fetchall()

cursor.execute("SELECT * FROM Address")
table_Address = cursor.fetchall()

cursor.execute("SELECT * FROM SO_Detail")
table_SO_Detail = cursor.fetchall()

if __name__ == "__main__":
#	while True:
#		schedule.run_pending()
#		time.sleep(1800) 				# wait 30 minutes

    #AR_past_due(cursor, today)
    # PO_receiving_past_due(cursor, today)
    
    # daily_tracking_email(cursor, today, table_Packlist_Detail, table_Packlist_Header, table_SO_Detail)
	# checkTracking(cursor, today, table_Packlist_Detail, table_Packlist_Header, table_Address)
    pass
