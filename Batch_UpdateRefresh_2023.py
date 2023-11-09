import pandas as pd
import teradata
import datetime
import time
import os
import tkinter as tk
from sys import exit

#Selects the size of the batch (number of rows to be uploaded at once) and starts the timer

#put a variable for the teradata password

tic = time.perf_counter()
batchsize = 1000

#Creates a string for your enumber to replace in the file paths

userstr = os.environ['USERNAME']
onedrive = 'C:/Users/' + str(userstr) + '/Documents/'

#Connects to teradata

print('Connecting to Teradata...')

udaExec = teradata.UdaExec (appName="Teradata", version="1.0", logConsole=False)
session = udaExec.connect(method='odbc',DSN='---', username='',
                            password='');

#Creates a string with the datestamp for the text backup

dt = datetime.datetime.now().strftime('%d-%m-%Y')

#Queries the PTR table and stores the information in a dataframe (table inside python memory)

backup = pd.read_sql_query('SELECT * FROM Database.Table', con=session)

#Builds the little graphic interface with the buttons to receive the input to whether update or refresh the table

def select(opt):

    if opt == True:
        print('Refreshing table')
        onedrive = 'C:/Users/' + str(userstr) + '/' + str(txtbox.get()) + '/'
        root.destroy()
        backup.to_csv(str(onedrive) + 'Path ' + str(dt) + '.txt', header=None, index=None, sep=',', mode='a')
        backuplist = backup.values.tolist()
        session.execute('DROP TABLE Database.Table')
        session.execute('CREATE SET TABLE Database.Table ,FALLBACK , NO BEFORE JOURNAL, NO AFTER JOURNAL, CHECKSUM = DEFAULT, DEFAULT MERGEBLOCKRATIO, MAP = TD_MAP1 ( Country CHAR(2) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL...;')
        session.execute('GRANT SELECT ON Database.Table TO User')

        for row in range(0,len(backuplist),batchsize):
            session.executemany("INSERT INTO Database.Table (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", backuplist[row:row+batchsize],batch=True)
        print('Table refreshed')
        session.close()
        exit('Exiting the script...')
    
    else:
        print('Updating table')
        onedrive = 'C:/Users/' + str(userstr) + '/' + str(txtbox.get()) + '/'
        root.destroy()
        backup.to_csv(str(onedrive) + 'Path' + str(dt) + '.txt', header=None, index=None, sep=',', mode='a')
        print('Backup created')

        #Reads the first excel file and add to main dataframe
        
        df = pd.read_excel(str(onedrive) + 'FilePath', header=0, sheet_name='Export', usecols="A:R", nrows=169)
        
        print('Inserting PT in the dataframe')
        
        #List of two letter codes that will be replaced in the file name to read all files
        
        countries = ['AE','AL','AM','AT','BA','BE','BG','BR','C1','C2','CH','CY','CZ','DK','EE','EG','FI','GE','GR','HR','HU','IL','IS','IT','JO','KW','LT','LU','LV','ME','MK','MT','NL','NO','OM','PL','QA','RO','RS','SA','SE','SI','SK','TR','XK']
        
        #Loops through all files and adds the data to the main dataframe
        
        for cntry in countries:
            print('Appending ' + str(cntry) + ' to dataframe' )
            cntry = pd.read_excel(str(onedrive) + 'Path' + str(cntry) + '.xlsm', header=0, sheet_name='FileName', usecols="A:R", nrows=169)
            df = pd.concat([df, cntry], ignore_index=True)
        
        
        print('Dataframe ready')
        
        #Adjusts formatting 
        df['Update_Week'] = pd.to_datetime(df['Update_Week']).dt.date
        df.fillna('', inplace=True)
        df.drop_duplicates(subset=['Country', 'Location', 'Year', 'Month', 'Update_Week', 'Dataset'], keep='first', inplace=True)
        dfclean = df.loc[df['Year'].isin([2022,2023])] 
        print(dfclean.info())
        
        #Converts from dataframe to list
        
        dflist = dfclean.values.tolist()
        
        #Creates a volatile (temporary) table and uploads all the PTR data
        
        session.execute('CREATE MULTISET VOLATILE TABLE Databse.TEMP ')
        
        for row in range(0,len(dflist),batchsize):
            try:
                session.executemany("INSERT INTO E798RC.PTR_TEMP (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", dflist[row:row+batchsize],batch=True)
            except:
                print(dflist[row])
            
        
        print('Volatile table ready. Merging...')
        
        #Merges the PTR table with the temporary one to either update or insert new rows to the PTR table, then drops the temporary table
        
        session.execute('MERGE INTO Database.Table tgt USING Database.TEMP;')
        session.execute('DROP TABLE Database.TEMP')
        
        toc = time.perf_counter()
        finaltime = toc - tic
        
        #Finishes the timer and closes connection
        
        print('Update completed in ' + str(finaltime) + ' seconds')
        
        session.close()

def on_closing():
    root.destroy()
    exit('You exited the script when the window was closed')

root = tk.Tk()
root.geometry("300x500")
labeltxt = 'Would you like to refresh \n the 30 days period or just \n update the table?'
labeltxt2 = 'Make sure the name of your \n shared directory below \n is correct:'
label = tk.Label(root,text=labeltxt)
label.place(x=75,y=30)
label2 = tk.Label(root,text=labeltxt2)
label2.place(x=75,y=300)

root.title('Update')
root.attributes('-topmost', True)
txtbox = tk.Entry(root)
txtbox.insert(0,'PathToFolder')
txtbox.place(x=87,y=400)

button1 = tk.Button(root, text= "Refresh", height=3,width=20,command=lambda: select(True))
button1.place(x=75,y=110)
button2 = tk.Button(root, text= "Update", height=3,width=20,command=lambda: select(False))
button2.place(x=75,y=185)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
