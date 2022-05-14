
from tkinter import *
from tkinter.ttk import Labelframe
import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='system_user'
)

mycursor = mydb.cursor()
mycursor.execute('SELECT name, username, password FROM user')
res = mycursor.fetchall()

root = Tk()
root.geometry('300x200')
wrapper2 = LabelFrame(root).grid(column=0, row=1)

canvas = Canvas(wrapper2)
canvas.grid(column=0, row=0, padx=5, pady=5)
scrollbar = Scrollbar(wrapper2, orient=VERTICAL, command=canvas.yview)
scrollbar.place(x=280, y=0, height=200)
frame = Frame(canvas)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e : canvas.configure(scrollregion=canvas.bbox('all')))
canvas.create_window((0,0), window=frame, anchor=NW)



r = 1
for x in res:
    Label(frame, text=x[0]).grid(column=0, row=r)
    Label(frame, text=x[1]).grid(column=1, row=r)
    Label(frame, text=x[1]).grid(column=2, row=r)
    r += 1

for x in res:
    Label(frame, text=x[0]).grid(column=0, row=r)
    Label(frame, text=x[1]).grid(column=1, row=r)
    Label(frame, text=x[1]).grid(column=2, row=r)
    r += 1

for x in res:
    Label(frame, text=x[0]).grid(column=0, row=r)
    Label(frame, text=x[1]).grid(column=1, row=r)
    Label(frame, text=x[1]).grid(column=2, row=r)
    r += 1
for x in res:
    Label(frame, text=x[0]).grid(column=0, row=r)
    Label(frame, text=x[1]).grid(column=1, row=r)
    Label(frame, text=x[1]).grid(column=2, row=r)
    r += 1
for x in res:
    Label(frame, text=x[0]).grid(column=0, row=r)
    Label(frame, text=x[1]).grid(column=1, row=r)
    Label(frame, text=x[1]).grid(column=2, row=r)
    r += 1
for x in res:
    Label(frame, text=x[0]).grid(column=0, row=r)
    Label(frame, text=x[1]).grid(column=1, row=r)
    Label(frame, text=x[1]).grid(column=2, row=r)
    r += 1


headers = ['Name', 'Username', 'Password']

Label(root, text=headers[0], background='green', fg='#fff', width=15, height=2).place(x=0, y=0)
Label(root, text=headers[1], background='green', fg='#fff', width=15, height=2).place(x=100, y=0)
Label(root, text=headers[2], background='green', fg='#fff', width=15, height=2).place(x=200, y=0)
root.mainloop()