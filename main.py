from cProfile import label
from re import I
from tkinter import *
import mysql.connector


SETTINGS_WINDOW = False
#database..
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='system_user'
)

#verify user input..
def verification():
    mycursor = mydb.cursor()
    mycursor.execute('SELECT name, username, password, isadmin FROM user')
    res = mycursor.fetchall()
    return res

#fetch all users..
def fetch_users():
    mycursor = mydb.cursor()
    mycursor.execute('SELECT name, username, password, isadmin FROM user')
    res = mycursor.fetchall()
    return res

#user signed in
def signed():
    mycursor = mydb.cursor()
    sql = "UPDATE log SET islogged = 'true'"
    mycursor.execute(sql)
    mydb.commit()

#already signed?
def isSigned():
    mycursor = mydb.cursor()
    mycursor.execute('SELECT islogged FROM log')
    res = mycursor.fetchall()
    is_signed = 0


    for x in res:
        for y in x:
            if y != 'false':
                is_signed = 1
            else:
                is_signed = 0
    
    return is_signed

#sign out
def signOut():
    mycursor = mydb.cursor()
    sql = "UPDATE log SET islogged = 'false'"
    mycursor.execute(sql)
    mydb.commit()

def authentication():
    main_window.withdraw()
    def sign_in():
        #get values
        username = username_value.get()
        password = password_value.get()
        res = verification()
        #verification..
        for x in res:
            if x[1] == username and x[2] == password:
                user_name.set('User: {}'.format(x[0]))
                isADMIN = 'Receptionist'
                if x[3] == 'true':
                    isADMIN = 'Admin'
                    isadmin.set('({})'.format(isADMIN))
                    signed()

                else:
                    isadmin.set('({})'.format(isADMIN))

                login_form.destroy()
                main_window.deiconify()
                print('Log in success.')
            elif x[1] == username and x[2] != password:
                print('Incorrect password.')

    #create login form
    login_form = Toplevel()
    login_form.title('Sign-in')
    login_form.resizable(False, False)
    
    #close form window
    def close_windows():
        login_form.destroy()
        main_window.destroy()

    login_form.protocol("WM_DELETE_WINDOW", close_windows)

    #window dimension
    width = 450
    height = 230
    #get screen dimension
    screen_width = login_form.winfo_screenwidth()
    screen_height = login_form.winfo_screenheight()
    center_x = int(screen_width/2 - width/2)
    center_y = int(screen_height/2 - height/2)
    login_form.geometry(f'{width}x{height}+{center_x}+{center_y}')

    login_form.columnconfigure(0, weight=1)
    login_form.columnconfigure(1, weight=2)
    #hotel logo
    logo = PhotoImage(file='./assets/hotel_logo.png')
    Label(login_form, image=logo).grid(column=0, row=0, columnspan=2, pady=10)
    #username
    Label(login_form, text='Username:').grid(column=0, row=1, sticky=E, pady=3)
    username_value = StringVar()
    username_entry = Entry(login_form, width=40, highlightthickness=1, highlightbackground='#242526', textvariable=username_value)
    username_entry.grid(column=1, row=1, sticky=W, padx=5, pady=3)
    username_entry.focus()
    #password
    Label(login_form, text='Password:').grid(column=0, row=2, sticky=E, pady=3)
    
    password_value = StringVar()
    Entry(login_form, width=40, highlightthickness=1, highlightbackground='#242526', show='*', textvariable=password_value).grid(column=1, row=2, sticky=W, padx=5, pady=3)

    #button
    Button(login_form, text='Sign-in', fg='#242526', borderwidth=0, background='#242526', foreground='#fff', command=sign_in).grid(column=1, row=3, ipadx=10, ipady=5, sticky=W, pady=10, padx=5)

    login_form.mainloop()

#settings function
def settings():
    is_signed = isSigned()
    if is_signed is 0:
        authentication()
    else:
        global SETTINGS_WINDOW
        #is created?
        if SETTINGS_WINDOW is not True:
            SETTINGS_WINDOW = True
            settings_window = Toplevel()
            settings_window.title('Manage Users')
            settings_window.resizable(False, False)
            #close function
            def close_window():
                global SETTINGS_WINDOW
                SETTINGS_WINDOW = False
                settings_window.destroy()

            settings_window.protocol('WM_DELETE_WINDOW', close_window)
            #window dimension
            width = 600
            height = 400
            #get screen dimension
            screen_width = settings_window.winfo_screenwidth()
            screen_height = settings_window.winfo_screenheight()
            center_x = int(screen_width/2 - width/2)
            center_y = int(screen_height/2 - height/2)
            settings_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
            #header
            header_frame = Frame(settings_window, highlightthickness=1, highlightbackground='gray')
            header_frame.pack(fill='x', side='top')
            banner = PhotoImage(file='./assets/settings_header_banner.png')
            Label(header_frame, image=banner).pack()
            
            main_frame = Frame(settings_window)
            main_frame.pack(side='left', fill='y')

            res = fetch_users()
            list = ['Name', 'Username', 'Password', 'Admin', 'Action']
            for x in range(5):
                Label(main_frame, text=list[x], background='gray', fg='#fff', font=('sans-serif', 13)).grid(column=x, row=0, ipadx=30, ipady=5, pady=(0, 15))

            r = 1
            for x in res:
                for n in range(4):
                    Label(main_frame, text=x[n], font=('sans-serif', 11), fg='#242526').grid(column=n, row=r, pady=(0, 5))
                Button(main_frame, text='Delete', background='#db300d', fg='#fff', borderwidth=0).grid(column=n+1, row=r, ipadx=17, ipady=1, pady=(0, 5))
                r += 1
            Button(main_frame, text='Add user', borderwidth=0, background='#0bb04d', fg='#fff').grid(column=4, row=r, ipadx=10, ipady=3)
            settings_window.mainloop()



#sign out function
def sign_out():
    #sign out current user
    signOut()
    #re-authenticate
    authentication()


main_window = Tk()
main_window.title('King Inn Hotel')
main_window.resizable(False, False)

#window dimension
width = 800
height = 550
#get screen dimension
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
center_x = int(screen_width/2 - width/2)
center_y = int(screen_height/2 - height/2)
main_window.geometry(f'{width}x{height}+{center_x}+{center_y}')

#header..
header = Frame(main_window, highlightthickness=1, highlightbackground='gray')
header.pack(fill='x', side='top')
header.columnconfigure(0, weight=1)
settings_icon = PhotoImage(file='./assets/settings.png')
logo = PhotoImage(file='./assets/hotel_logo.png')

#header widgets..

#hotel logo
Label(header, image=logo).grid(column=0, row=0, sticky=W, padx=20, pady=10)

#user settings
Button(header, image=settings_icon, compound=LEFT, text='Settings', borderwidth=0, font=('sans-serif', 15), fg='#242526', command=settings).grid(column=1, row=0, sticky=E, padx=20, pady=10)


#left section frame..
leftSect = Frame(main_window, highlightbackground='gray', highlightthickness=1)
leftSect.pack(fill='y', side='left')
leftSect.rowconfigure(1, weight=3)

#system user info frame..
user_icon = PhotoImage(file='./assets/user.png')
rank_icon = PhotoImage(file='./assets/rank.png')
user_info_frame = Frame(leftSect)
user_info_frame.grid(column=0, row=0, padx=10, pady=30, sticky=S)
user_info_frame.columnconfigure(0, weight=1)

#inner frame
user_info_inner_frame = Frame(user_info_frame)
user_info_inner_frame.grid(column=0, row=0, padx=10)
user_info_inner_frame.columnconfigure(0, weight=1)
user_name = StringVar()
user_name.set('User: unsigned')
isadmin = StringVar()
isadmin.set('(Receptionist)')
Label(user_info_inner_frame, image=user_icon, textvariable=user_name, compound=LEFT, font=('sans-serif', 11)).grid(column=0, row=0, sticky=W)
Label(user_info_inner_frame, image=rank_icon, textvariable=isadmin, compound=LEFT, font=('sans-serif', 11)).grid(column=0, row=1, sticky=W)

#availability visualization
available_icon = PhotoImage(file='./assets/available.png')
capacity_icon = PhotoImage(file='./assets/capacity.png')
occupied_icon = PhotoImage(file='./assets/occupied.png')
reserved_icon = PhotoImage(file='./assets/reserved.png')
availability_frame = Frame(leftSect, highlightbackground='gray', highlightthickness=1)
availability_frame.grid(column=0, row=1, padx=10, pady=10, sticky=N)
availability_frame.columnconfigure(0, weight=1)
#inner frame
availability_inner_frame = Frame(availability_frame)
availability_inner_frame.grid(column=0, row=0, pady=20, padx=30)
availability_inner_frame.columnconfigure(0, weight=1)
Label(availability_inner_frame, image=available_icon, compound=LEFT, text=' Available: 95%', font=('sans-serif', 11)).grid(column=0, row=0, sticky=W)
Label(availability_inner_frame, image=capacity_icon, compound=LEFT,text=' Capacity: 200', font=('sans-serif', 11)).grid(column=0, row=1, sticky=W)
Label(availability_inner_frame, image=occupied_icon, compound=LEFT,text=' Occupied: 10', font=('sans-serif', 11)).grid(column=0, row=2, sticky=W)
Label(availability_inner_frame, image=reserved_icon, compound=LEFT,text=' Reserved: 1/190', font=('sans-serif', 11)).grid(column=0, row=3, sticky=W)

#sign out frame
sign_out_frame = Frame(leftSect)
sign_out_icon = PhotoImage(file='./assets/sign-out.png')
sign_out_frame.grid(column=0, row=2, pady=70)


    
Button(sign_out_frame, image=sign_out_icon, compound=LEFT, text=' Sign-out', font=('sans-serif', 11), borderwidth=0, command=sign_out).pack()

#main section
main_section_frame = Frame(main_window)
main_section_frame.pack(pady=70)

check_in = PhotoImage(file='./assets/check_in.png')
check_out = PhotoImage(file='./assets/check_out.png')
book = PhotoImage(file='./assets/book.png')
rooms = PhotoImage(file='./assets/rooms.png')
cancel_booking = PhotoImage(file='./assets/cancel_booking.png')
guests = PhotoImage(file='./assets/guests.png')
Button(main_section_frame, text='Check In', image=check_in, compound=LEFT, borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=0, row=1)
Button(main_section_frame, text=' Check Out', image=check_out, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=1, row=1, sticky=E)
Button(main_section_frame, text=' Guests', image=guests, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=2, row=1, sticky=W)
Button(main_section_frame, text=' Rooms', image=rooms, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=0, row=0)
Button(main_section_frame, text='Book', image=book, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=1, row=0, sticky=W)
Button(main_section_frame, text='Cancel Booking', image=cancel_booking, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=2, row=0)


for widget in main_section_frame.winfo_children():
    widget.grid(ipady=30, padx=10, pady=10)

main_window.mainloop()



