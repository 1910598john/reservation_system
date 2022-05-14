from tkinter import *
import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='system_user'
)
 #fetch from database

mycursor = mydb.cursor()
mycursor.execute('SELECT room_id, type, capacity, check_in_date, check_out_date, availability FROM rooms')
res = mycursor.fetchall()

#create rooms window
rooms_window = Tk()
#rooms_window.protocol('WM_DELETE_WINDOW', test)
rooms_window.title('Rooms')
rooms_window.resizable(False, False)
width = 750
height = 500
#get screen dimension
screen_width = rooms_window.winfo_screenwidth()
screen_height = rooms_window.winfo_screenheight()
center_x = int(screen_width/2 - width/2)
center_y = int(screen_height/2 - height/2)
rooms_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
wrapper2 = LabelFrame(rooms_window).grid(column=0, row=1)
canvas = Canvas(wrapper2, width=750, height=450)
canvas.grid(column=0, row=0, pady=(40, 5))
scrollbar = Scrollbar(wrapper2, orient=VERTICAL, command=canvas.yview)
scrollbar.place(x=735, y=0, height=500)
frame = Frame(canvas)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e : canvas.configure(scrollregion=canvas.bbox('all')))
canvas.create_window((0,0), window=frame, anchor=NW)
#row variable
r = 0
#fetch rooms data
for x in res:
    Label(frame, text=x[0]).grid(column=0, row=r, ipadx=30, ipady=10)
    Label(frame, text=x[1]).grid(column=1, row=r, ipadx=20, ipady=10)
    Label(frame, text=x[2]).grid(column=2, row=r, ipadx=30, ipady=10)
    Label(frame, text=x[3]).grid(column=3, row=r, ipadx=50, ipady=10)
    Label(frame, text=x[4]).grid(column=4, row=r, ipadx=50, ipady=10)
    Label(frame, text=x[5]).grid(column=5, row=r, ipadx=30, ipady=10)
    #increment row by 1
    r += 1
#headers name list
headers = ['ID', 'Type', 'Capacity', 'Check-in Date', 'Check-out Date', 'Availability']
#headers widgets
Label(rooms_window, text=headers[0], background='gray', fg='#fff', width=13, height=2, font=('sans-serif', 10)).place(x=0, y=0)
Label(rooms_window, text=headers[1], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=60, y=0)
Label(rooms_window, text=headers[2], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=180, y=0)
Label(rooms_window, text=headers[3], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=310, y=0)
Label(rooms_window, text=headers[4], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=450, y=0)
Label(rooms_window, text=headers[5], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=570, y=0)
rooms_window.mainloop()


