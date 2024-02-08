from tkinter import *
from tkinter import ttk
import csv

try:
    import snowflake.connector
except:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "snowflake-connector-python"])
    import snowflake.connector


def insertBarcodeBox(indx, barcode):
    barcodeListBox.configure(state=NORMAL)
    barcodeListBox.insert(END, "#" + str(indx) + " - " + barcode + '\n')
    barcodeListBox.configure(state=DISABLED)
    barcodeListBox.see(END)

def clear_barcode_box():
    barcodeListBox.configure(state=NORMAL)
    barcodeListBox.delete("1.0",END)
    barcodeListBox.configure(state=DISABLED)

def clear_all_input():
    clear_barcode_box()
    barcodeList.clear()

def create_result(*args):
    barcode = scannedBarcode.get()
    if barcode and barcode[-3:] == suffix.get():
        barcodeList.append(barcode)
        insertBarcodeBox(len(barcodeList), barcode)

# save generated sheet to csv file
def save_to_csv(result):
    with open('./sheet.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(('Casefile ID', 'Age'))
        writer.writerows(result)

# SnowFlake query
def query_snowflake():
    popWindow = Toplevel()

    columns = ('Casefile ID', 'Sample Age')
    sheet = ttk.Treeview(popWindow, columns=columns, show='headings', height=20)
    for col in columns:
        sheet.heading(col, text=col)

    listString = generate_barcode_list_string()

    sqlQuery = """select casefile_id as "Casefile ID", DATEDIFF(DAY, samp.collectiondate, CURRENT_DATE) AS "Sample Age" from "LIMSDB"."LIMSDB_PRODLIMS"."PARENTKIT" pk
    LEFT JOIN "LIMSDB"."LIMSDB_PRODLIMS"."PARENTKIT_SAMPLE" pks ON pk.id = pks.parentkit_id
    LEFT JOIN "LIMSDB"."LIMSDB_PRODLIMS"."SAMPLE" samp ON pks.sample_id = samp.id
    WHERE  samp.barcode IN (""" + listString + """);"""

    result = snowFlakeCursor.execute(sqlQuery)
    copyResult = []

    for res in result:
        copyResult.append(res)
        sheet.insert('', END, values=res)

    sheet.grid(row=0, column=0)

    saveButtonFrame = Frame(master=popWindow)
    saveButtonFrame.grid(row=1)
    # save to csv button
    saveButton = Button(master=saveButtonFrame, text="Save", command=save_to_csv(copyResult))
    saveButton.grid(row=0, column=0)

    # save to HTML benchworksheet
    sheetButton = Button(master=saveButtonFrame, text="Bechworksheet", command=generate_benchworksheet(copyResult))
    sheetButton.grid(row=0, column=1)

def generate_barcode_list_string():
    delim = "','"
    listString = delim.join(barcodeList)
    listString = "'" + listString + "'"
    return listString

# display barcode string list on pop up window
def get_barcode_list_string():
    popWindow = Toplevel()
    listString = generate_barcode_list_string()
    textBox = Text(master=popWindow)
    textBox.pack()
    textBox.insert(END, listString)
    textBox.configure(state=DISABLED)

def remove_index_barcode():
    try:
        indx = int(codeRemoveEntry.get())
        if indx > 0 and indx <= len(barcodeList):
            barcodeList.pop(int(indx)-1)
            clear_barcode_box()
            for indx, barcode in enumerate(barcodeList):
                insertBarcodeBox(indx+1, barcode)
        codeRemoveEntry.delete(0,END)
    except:
        codeRemoveEntry.delete(0,END)


def generate_benchworksheet(result):
    header = """
    <!DOCTYPE html>
    <html>
    <style>
    table, th, td {
    border:1px solid black;
    }
    </style>
    <body>
    <h2>A basic HTML table</h2>
    <table style="width:100%">
    <tr>
        <th>Casefile ID</th>
        <th>Sample Age</th>
    </tr>
    """

    singleCase = "<tr><td>{caseFileId}</td><td>{sampleAge}</td></tr>"

    ending = """
    </table>
    <p>To understand the example better, we have added borders to the table.</p>
    </body>
    </html>
    """

    with open('./benchworksheet.html', 'w') as file:
        file.write(header)
        for res in result:
            file.write(singleCase.format(caseFileId=res[0], sampleAge=res[1]))
        file.write(ending)


def log_in_SnowFlake():
    global snowFlakeCursor
    credentials = {'account': 'natera', 'user': userNameEntry.get(), 'authenticator': 'externalbrowser'}
    snowFlakeCursor = snowflake.connector.connect(**credentials).cursor()

# app name
window = Tk()
window.title("Women's Health ___ Snowflake")

# global variables
barcodeList = []
scannedBarcode = StringVar()
scannedBarcode.trace_add("write", create_result)
suffixList = ["BXE", "BXS"]
suffix = StringVar()
suffix.set("BXE")
snowFlakeCursor = None

buttonFrame = Frame()
buttonFrame.pack()

# log-in username input
userNameEntry = Entry(master=buttonFrame, width=10, takefocus=0)
logInButton = Button(master=buttonFrame, text="LogIn", command=log_in_SnowFlake, takefocus=0)
userNameEntry.grid(column=0,row=0, padx=20, pady=(10,0))
logInButton.grid(column=0, row=1, pady=(0,10)) 

# suffix list option
suffixOption = OptionMenu(buttonFrame, suffix, *suffixList)
suffixOption.grid(column=1, row=0, padx=10, pady=(10,0))

# clear list button
clearListButton = Button(master=buttonFrame, text="Clear", command=clear_all_input, takefocus=0)
clearListButton.grid(column=2, row=0, padx=10, pady=(10,0))

# query button
queryButton = Button(master=buttonFrame, text="Query", command=query_snowflake, takefocus=0)
queryButton.grid(column=3, row=0, padx=10, pady=(10,0))

# generate list button
generateListButton = Button(master=buttonFrame, text="Get List", command=get_barcode_list_string, takefocus=0)
generateListButton.grid(column=4,row=0,padx=10,pady=(10,0))

# remove code enter box
codeRemoveEntry = Entry(master=buttonFrame, width=8, takefocus=0)
codeRemoveEntry.grid(column=5,row=0,padx=20, pady=(10,0))
# remove code button
codeRmoveButton = Button(master=buttonFrame, text="Remove", command=remove_index_barcode, takefocus=0)
codeRmoveButton.grid(column=5,row=1,pady=(0,10))

# input/scan box title
inputBoxTitle = Label(text="# Scan Barcode into Below #")
inputBoxTitle.pack()
# input/scan box
barcodeEntry = Entry(textvariable=scannedBarcode, width=50)
barcodeEntry.pack(pady=10)

barcodeListBox = Text(state=DISABLED)
barcodeListBox.pack()

window.mainloop()
