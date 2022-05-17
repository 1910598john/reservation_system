from tkinter import *
from tkinter import font
import mysql.connector


#create rooms window
root = Tk()
root.geometry('950x500')
headers = ['Guest Name', 'Contact #', 'Room ID', 'isBooked', 'Check-in Date',  'Duration', 'isChecked-out', 'Selected Payment', 'Amount Paid']
c = 0
for x in headers:
    Label(root, text=x, background='gray', fg='#fff', font=('sans-serif', 9, font.BOLD)).grid(column=c, row=0, ipadx=16, ipady=5)
    c += 1

c2 = 0
test = ['JM Catamora', '09468837618', '102', 'Booked', '15/16/22', '1 day', 'Yes', 'Down payment', '475']
for x in test:
    Label(root, text=x).grid(column=c2, row=1)
    c2 += 1
root.mainloop()


