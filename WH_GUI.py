from tkinter import *
from tkinter import ttk
import csv

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
        writer.writerow(('bar-code', 'case number', 'parent kit-code', 'gender', 'age'))
        writer.writerows(result)

# fake query now
def query_snowflake():
    popWindow = Toplevel()

    columns = ('bar-code', 'case number', 'parent kit-code', 'gender', 'age')
    sheet = ttk.Treeview(popWindow, columns=columns, show='headings', height=20)
    for col in columns:
        sheet.heading(col, text=col)

    caseNumber = "123456789"
    parent = "0000000-SB"
    gender = 'F'
    age = '2'

    result = [["#"+str(indx+1)+" - "+barcode,caseNumber,parent,gender,age] for indx, barcode in enumerate(barcodeList)]

    for case in result:
        sheet.insert('', END, values=case)

    sheet.grid(row=0, column=0)

    saveButtonFrame = Frame(master=popWindow)
    saveButtonFrame.grid(row=1)
    # save to csv button
    saveButton = Button(master=saveButtonFrame, text="Save", command=save_to_csv(result))
    saveButton.grid(row=0, column=0)

    sheetButton = Button(master=saveButtonFrame, text="Bechworksheet", command=generate_benchworksheet(result))
    sheetButton.grid(row=0, column=1)


def generate_list_string():
    popWindow = Toplevel()

    delim = "','"
    listString = delim.join(barcodeList)
    listString = "'" + listString + "'"
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
        <th>bar-code</th>
        <th>case number</th>
        <th>parent kit-code</th>
        <th>gender</th>
        <th>age</th>
    </tr>
    """

    singleCase = "<tr><td>barcode</td><td>caseNumber</td><td>parentKitCode</td><td>gender</td><td>age</td></tr>"

    ending = """
    </table>
    <p>To understand the example better, we have added borders to the table.</p>
    </body>
    </html>
    """
    
    file = open('./benchworksheet.html', 'w')
    file.write(header)

    for caseNum in result:
        file.write(singleCase.format(caseNum[0], caseNum[1], caseNum[2], caseNum[3], caseNum[4]))

    file.write(ending)

    file.close()
        

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

buttonFrame = Frame()
buttonFrame.pack()

# suffix list option
suffixOption = OptionMenu(buttonFrame, suffix, *suffixList)
suffixOption.grid(column=0, row=0, padx=10, pady=(10,0))

# clear list button
clearListButton = Button(master=buttonFrame, text="Clear", command=clear_all_input, takefocus=0)
clearListButton.grid(column=1, row=0, padx=10, pady=(10,0))

# query button
queryButton = Button(master=buttonFrame, text="Query", command=query_snowflake, takefocus=0)
queryButton.grid(column=2, row=0, padx=10, pady=(10,0))

# generate list button
generateListButton = Button(master=buttonFrame, text="Get List", command=generate_list_string, takefocus=0)
generateListButton.grid(column=3,row=0,padx=10,pady=(10,0))

# remove code enter box
codeRemoveEntry = Entry(master=buttonFrame, width=8, takefocus=0)
codeRemoveEntry.grid(column=4,row=0,padx=20, pady=(10,0))
# remove code button
codeRmoveButton = Button(master=buttonFrame, text="Remove", command=remove_index_barcode, takefocus=0)
codeRmoveButton.grid(column=4,row=1,pady=(0,10))

# input/scan box title
inputBoxTitle = Label(text="# Scan Barcode into Below #")
inputBoxTitle.pack()
# input/scan box
barcodeEntry = Entry(textvariable=scannedBarcode, width=50)
barcodeEntry.pack(pady=10)

barcodeListBox = Text(state=DISABLED)
barcodeListBox.pack()

window.mainloop()
