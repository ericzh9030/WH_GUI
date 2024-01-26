from tkinter import *
from tkinter import ttk
import csv

def insertBarcodeBox(barcode):
    barcodeListBox.configure(state=NORMAL)
    barcodeListBox.insert(END, "#" + str(len(barcodeList)) + " - " + barcode + '\n')
    barcodeListBox.configure(state=DISABLED)

def clear_barcode_box():
    barcodeListBox.configure(state=NORMAL)
    barcodeListBox.delete("1.0",END)
    barcodeListBox.configure(state=DISABLED)
    barcodeList.clear()

def create_result(*args):
    #barcodeListBox.pack_forget()
    barcode = scannedBarcode.get()
    if barcode and barcode[-3:] == 'BXE':
        barcodeList.append(barcode)
        insertBarcodeBox(barcode)
        barcodeEntry.select_range(0,END)

# save generated sheet to csv file
def save_to_csv(result):
    with open('./sheet.csv', 'w') as file:
        writer = csv.writer(file)
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
    # save to csv button
    saveButton = Button(master=popWindow, text="Save", command=save_to_csv(result))
    saveButton.grid()



# app name
window = Tk()
window.title("Women's Health ___ Snowflake")

# global variables
barcodeList = []
scannedBarcode = StringVar()
scannedBarcode.trace_add("write", create_result)
resultFrame = Frame()

# clear list button
clearListButton = Button(text="Clear", command=clear_barcode_box)
clearListButton.pack()

# query button
queryButton = Button(text="Query", command=query_snowflake)
queryButton.pack()

# input/scan box title
inputBoxTitle = Label(text="# Scan Barcode into Below #")
inputBoxTitle.pack()
# input/scan box
barcodeEntry = Entry(textvariable=scannedBarcode, width=50)
barcodeEntry.pack(pady=10)

barcodeListBox = Text(state=DISABLED)
barcodeListBox.pack()

window.mainloop()
