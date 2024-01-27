from tkinter import *
from tkinter import ttk
import csv

def insertBarcodeBox(indx, barcode):
    barcodeListBox.configure(state=NORMAL)
    barcodeListBox.insert(END, "#" + str(indx) + " - " + barcode + '\n')
    barcodeListBox.configure(state=DISABLED)

def clear_barcode_box():
    barcodeListBox.configure(state=NORMAL)
    barcodeListBox.delete("1.0",END)
    barcodeListBox.configure(state=DISABLED)

def clear_all_input():
    clear_barcode_box()
    barcodeList.clear()

def create_result(*args):
    barcode = scannedBarcode.get()
    if barcode and barcode[-3:] == 'BXE':
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
    # save to csv button
    saveButton = Button(master=popWindow, text="Save", command=save_to_csv(result))
    saveButton.grid()


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
        

# app name
window = Tk()
window.title("Women's Health ___ Snowflake")

# global variables
barcodeList = []
scannedBarcode = StringVar()
scannedBarcode.trace_add("write", create_result)

buttonFrame = Frame()
buttonFrame.pack()

# clear list button
clearListButton = Button(master=buttonFrame, text="Clear", command=clear_all_input, takefocus=0)
clearListButton.grid(column=0, row=0, padx=10, pady=(10,0))

# query button
queryButton = Button(master=buttonFrame, text="Query", command=query_snowflake, takefocus=0)
queryButton.grid(column=1, row=0, padx=10, pady=(10,0))

# generate list button
generateListButton = Button(master=buttonFrame, text="Get List", command=generate_list_string, takefocus=0)
generateListButton.grid(column=2,row=0,padx=10,pady=(10,0))

# remove code enter box
codeRemoveEntry = Entry(master=buttonFrame, width=8, takefocus=0)
codeRemoveEntry.grid(column=3,row=0,padx=20, pady=(10,0))
# remove code button
codeRmoveButton = Button(master=buttonFrame, text="Remove", command=remove_index_barcode, takefocus=0)
codeRmoveButton.grid(column=3,row=1,pady=(0,10))

# input/scan box title
inputBoxTitle = Label(text="# Scan Barcode into Below #")
inputBoxTitle.pack()
# input/scan box
barcodeEntry = Entry(textvariable=scannedBarcode, width=50)
barcodeEntry.pack(pady=10)

barcodeListBox = Text(state=DISABLED)
barcodeListBox.pack()

window.mainloop()
