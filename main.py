from tkinter import *
from tkinter import font
import mysql.connector
import datetime as d
import random

#toplevel windows
SETTINGS_WINDOW = False
ERROR_WINDOW = False
SUCCESS_WINDOW = False
ADD_USER_WINDOW = False
DELETE_USER_WINDOW = False
ROOMS_WINDOW = False
CHECK_IN_WINDOW = False
BOOK_WINDOW = False
GET_ROOM_WINDOW = False
CANCELLATION_WINDOW = False
CHECK_OUT_WINDOW = False
GUESTS_WINDOW = False
B = False
B2 = False

current_user = []
#database..
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='system_user'
)

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
    global ERROR_WINDOW
    ERROR_WINDOW = False
    mycursor = mydb.cursor()
    sql = "UPDATE log SET islogged = 'false'"
    mycursor.execute(sql)
    mydb.commit()
#is limit reached?
def numOfUsers():
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT username FROM user")
    res = mycursor.fetchall()
    count_users = []
    for x in res:
        count_users.append(x)
    return len(count_users)
#create error pop-up window
def error(title, message):
    global ERROR_WINDOW
    #error window closing function
    def close_error_window():
        global ERROR_WINDOW
        ERROR_WINDOW = False
        error_window.destroy()
    #is created?
    if ERROR_WINDOW is not True:
        ERROR_WINDOW = True
        error_window = Toplevel()
        error_window.protocol('WM_DELETE_WINDOW', close_error_window)
        error_window.title(title)
        error_window.resizable(False, False)
        width = 320
        height = 90
        #get screen dimension
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        center_x = int(screen_width/2 - width/2)
        center_y = int(screen_height/2 - height/2)
        error_window.iconbitmap('./assets/hotel_icon.ico')
        error_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
        error_icon = PhotoImage(file='./assets/alert-icon-red.png')
        Label(error_window, image=error_icon, text=message, font=('sans-serif', 15), compound=LEFT).pack(fill='x', pady=17)
        error_window.mainloop()
#create success pop-up window
def success(title, message):
    global SUCCESS_WINDOW
    #error window closing function
    def close_success_window():
        global SUCCESS_WINDOW
        SUCCESS_WINDOW = False
        success_window.destroy()
    #is created?
    if SUCCESS_WINDOW is not True:
        SUCCESS_WINDOW = True
        success_window = Toplevel()
        success_window.protocol('WM_DELETE_WINDOW', close_success_window)
        success_window.title(title)
        success_window.resizable(False, False)
        width = 320
        height = 90
        #get screen dimension
        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()
        center_x = int(screen_width/2 - width/2)
        center_y = int(screen_height/2 - height/2)
        success_window.iconbitmap('./assets/hotel_icon.ico')
        success_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
        success_icon = PhotoImage(file='./assets/success-icon.png')
        Label(success_window, image=success_icon, text=message, font=('sans-serif', 15), compound=LEFT).pack(fill='x', pady=21)
        success_window.mainloop()
#is admin?
def isAdmin():
    if current_user[3] == 'true':
        global SETTINGS_WINDOW
        #close function
        def close_window():
            global SETTINGS_WINDOW
            SETTINGS_WINDOW = False
            settings_window.destroy()
        #is created?
        if SETTINGS_WINDOW is not True:
            SETTINGS_WINDOW = True
            settings_window = Toplevel()
            settings_window.title('Manage Users')
            settings_window.resizable(False, False)
            settings_window.iconbitmap('./assets/hotel_icon.ico')
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
            main_frame.pack(fill='y', side='left')
            res = fetch_users()
            list = ['Name', 'Username', 'Password', 'Admin']
            for x in range(4):
                Label(main_frame, text=list[x], background='gray', fg='#fff', font=('sans-serif', 13)).grid(column=x, row=0, ipadx=45, ipady=5, pady=(0, 15))
            r = 1
            for x in res:
                for n in range(4):
                    Label(main_frame, text=x[n], font=('sans-serif', 11), fg='#242526').grid(column=n, row=r, pady=(0, 5))
                r += 1
            Label(main_frame, text=(f'{r-1} of 5'), font=('sans-serif', 12), fg='gray').grid(column=0, row=r, pady=(8, 0))
            #delete user icon function
            def delete_user():
                global DELETE_USER_WINDOW
                if DELETE_USER_WINDOW is not True:
                    DELETE_USER_WINDOW = True
                    entered_username = StringVar()
                    delete_user_window = Toplevel()
                    delete_user_window.title('Delete User')
                    delete_user_window.resizable(False, False)
                    #close self window
                    def close_delete_user_window():
                        global DELETE_USER_WINDOW
                        DELETE_USER_WINDOW = False
                        delete_user_window.destroy()
                    delete_user_window.iconbitmap('./assets/hotel_icon.ico')
                    delete_user_window.protocol('WM_DELETE_WINDOW', close_delete_user_window)
                    #window dimension
                    width = 300
                    height = 120
                    #get screen dimension
                    screen_width = delete_user_window.winfo_screenwidth()
                    screen_height = delete_user_window.winfo_screenheight()
                    center_x = int(screen_width/2 - width/2)
                    center_y = int(screen_height/2 - height/2)
                    delete_user_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
                    delete_user_window.columnconfigure(0, weight=2)
                    delete_user_window.columnconfigure(1, weight=3)
                    #delete user
                    def deleteUser():
                        global DELETE_USER_WINDOW, SETTINGS_WINDOW
                        username = entered_username.get()
                        mycursor = mydb.cursor()
                        mycursor.execute(f"DELETE FROM user WHERE username = '{username}'")
                        mydb.commit()
                        #is deleted?
                        if mycursor.rowcount: #if success..
                            SETTINGS_WINDOW = False
                            DELETE_USER_WINDOW = False
                            settings_window.destroy()
                            delete_user_window.destroy()
                            title = 'Success'
                            message = ' User Deleted'
                            success(title, message)

                        else: #otherwise..
                            DELETE_USER_WINDOW = False
                            delete_user_window.destroy()
                            title = 'An Error Occurred'
                            message = ' Username does not exist'
                            error(title, message)
                    #delete user window widgets
                    Label(delete_user_window, text='Username:', font=('sans-serif', 11)).grid(column=1, row=0, sticky=W, pady=(15, 0), padx=5)
                    Entry(delete_user_window, width=30, font=('sans-serif', 9), textvariable=entered_username, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=1, sticky=W, padx=5, ipady=1)
                    Button(delete_user_window, text='Delete', fg='#fff', background='#242526', font=('sans-serif', 8), borderwidth=0, command=deleteUser).grid(padx=5, sticky=W, column=1, row=2, ipadx=10, ipady=3, pady=(10, 5))
                    delete_user_window.mainloop()
            #add user icon function
            def add_user():
                users = numOfUsers()
                if (users < 5):
                    global ADD_USER_WINDOW
                    #entries variable
                    name = StringVar()
                    username = StringVar()
                    password = StringVar()
                    admin = StringVar()
                    #is created?
                    if ADD_USER_WINDOW is not True:
                        ADD_USER_WINDOW = True
                        add_user_window = Toplevel()
                        add_user_window.title('Add User')
                        add_user_window.resizable(False, False)
                        #close self window
                        def close_add_user_window():
                            global ADD_USER_WINDOW
                            ADD_USER_WINDOW = False
                            add_user_window.destroy()
                        add_user_window.iconbitmap('./assets/hotel_icon.ico')
                        add_user_window.protocol('WM_DELETE_WINDOW', close_add_user_window)
                        #add user in database
                        def addUser():
                            if len(name.get()) is not 0 and len(username.get()) is not 0 and len(password.get()) is not 0:
                                global ADD_USER_WINDOW, SETTINGS_WINDOW
                                if admin.get() == '':
                                    admin.set('true')
                                mycursor = mydb.cursor()
                                mycursor.execute(f"INSERT INTO user (name, username, password, isadmin) VALUES ('{name.get()}', '{username.get()}', '{password.get()}', '{admin.get()}')")
                                mydb.commit()
                                if mycursor.rowcount:#if success
                                    ADD_USER_WINDOW = False
                                    SETTINGS_WINDOW = False
                                    add_user_window.destroy()
                                    settings_window.destroy()
                                    title = 'Success'
                                    message =' User Added'
                                    success(title, message)
                        #window dimension
                        width = 400
                        height = 270
                        #get screen dimension
                        screen_width = add_user_window.winfo_screenwidth()
                        screen_height = add_user_window.winfo_screenheight()
                        center_x = int(screen_width/2 - width/2)
                        center_y = int(screen_height/2 - height/2)
                        add_user_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
                        add_user_window.rowconfigure(0, weight=3)
                        add_user_window.rowconfigure(1, weight=1)
                        #entries frame
                        entries_frame = Frame(add_user_window)
                        entries_frame.grid(column=0, row=0, sticky=S)
                        #entries labels
                        labels = ['Name:', 'Username:', 'Password:']
                        r = 0
                        for x in labels:
                            Label(entries_frame, text=x, font=('sans-serif', 11)).grid(column=0, row=r, pady=2, sticky=E, columnspan=2, padx=(30, 5))
                            r += 1
                        #entries
                        Entry(entries_frame, textvariable=name, width=30, font=('sans-serif', 9), highlightthickness=1, highlightbackground='#e0dada').grid(column=3, row=0, padx=(0, 30), pady=2, sticky=E)
                        Entry(entries_frame, textvariable=username, width=30, font=('sans-serif', 9), highlightthickness=1, highlightbackground='#e0dada').grid(column=3, row=1, padx=(0, 30), pady=2, sticky=E)
                        Entry(entries_frame, textvariable=password, width=30, font=('sans-serif', 9), highlightthickness=1, highlightbackground='#e0dada').grid(column=3, row=2, padx=(0, 30), pady=2, sticky=E)
                        isadmin_checkbutton = Checkbutton(entries_frame, text='Admin', variable=admin, onvalue='true', offvalue='false', font=('sans-serif', 10))
                        isadmin_checkbutton.grid(column=3, row=3, sticky=W, pady=3)
                        isadmin_checkbutton.deselect()
                        #bottom widgets frame
                        bottom_frame = Frame(add_user_window)
                        bottom_frame.grid(column=0, row=1, sticky=NE)

                        Button(bottom_frame, text='Add user', borderwidth=0, background='#242526', foreground='#fff', font=('sans-serif', 11), command=addUser).pack(ipadx=120, ipady=5, pady=10)
                        add_user_window.mainloop()
                else: 
                    title = 'An Error Occurred'
                    message = ' User limit exceeded'
                    error(title, message)

            delete_icon = PhotoImage(file='./assets/delete_user_icon.png')
            add_icon = PhotoImage(file='./assets/add_user_icon.png')
            Frame(main_frame, height=100, width=600, background='#fff').place(x=0, y=200)
            delete = Button(main_frame, image=delete_icon, compound=LEFT, text='Delete', borderwidth=0, font=('sans-serif', 11), background='#fff', command=delete_user)
            delete.place(x=350, y=230)
            add = Button(main_frame, image=add_icon, compound=LEFT, text=' Add user', borderwidth=0, font=('sans-serif', 11), background='#fff', command=add_user)
            add.place(x=200, y=230)
            settings_window.mainloop()
    else:
        #call error function
        title = 'An Error Occurred'
        message = ' Access Denied'
        error(title , message)
#authentication..
def authentication(action):
    main_window.withdraw()
    #verify user input..
    def sign_in():
        #get values
        entered_username = username_value.get()
        entered_password = password_value.get()
        global current_user
        res = fetch_users()
        for x in res:
            #verify
            if x[1] == entered_username and x[2] == entered_password:
                #get current user
                if len(current_user) != 0:
                    current_user.clear()
                for c in range(4):
                    current_user.append(x[c])
                user_name.set('User: {}'.format(x[0]))
                isADMIN = 'Receptionist'
                if x[3] == 'true':
                    isADMIN = 'Admin'
                    isadmin.set(' : ({})'.format(isADMIN))
                else:
                    isadmin.set(' : ({})'.format(isADMIN))
                signed()
                login_form.destroy()
                main_window.deiconify()
                print('Logged in as {}'.format(isADMIN))
                #clicked before logged
                if action == 'settings':
                    settings()
                elif action =='book':
                    book()
                elif action == 'check_in':
                    check_in()
                elif action == 'check_out':
                    check_out()
                elif action == 'rooms':
                    show_rooms()
                elif action == 'guests':
                    show_guests()
                elif action == 'cancel':
                    cancel_book()
    #create login form
    login_form = Toplevel()
    login_form.title('Sign-in')
    login_form.resizable(False, False)
    #close form window
    def close_windows():
        global ERROR_WINDOW
        ERROR_WINDOW = True
        login_form.destroy()
        main_window.destroy()
    login_form.iconbitmap('./assets/hotel_icon.ico')
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
    Label(login_form, text='Username:', font=('sans-serif', 10)).grid(column=0, row=1, sticky=E, pady=3)
    username_value = StringVar()
    username_entry = Entry(login_form, width=35, font=('sans-serif', 9), textvariable=username_value, highlightthickness=1, highlightbackground='#e0dada')
    username_entry.grid(column=1, row=1, sticky=W, padx=5, pady=3)
    username_entry.focus()
    #password
    Label(login_form, text='Password:', font=('sans-serif', 10)).grid(column=0, row=2, sticky=E, pady=3)
    password_value = StringVar()
    Entry(login_form, width=35, font=('sans-serif', 9), show='*', textvariable=password_value, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=2, sticky=W, padx=5, pady=3)
    #button
    Button(login_form, text='Sign-in', fg='#242526', borderwidth=0, background='#242526', foreground='#fff', command=sign_in).grid(column=1, row=3, ipadx=10, ipady=5, sticky=W, pady=10, padx=5)
    login_form.mainloop()
#settings function
def settings():
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0:
        authentication("settings")
    else:
        isAdmin()
#sign out function
def sign_out():
    #sign out current user
    signOut()
    #re-authenticate
    authentication("")
#main window closing function
def close_main_window():
    signOut()
    main_window.destroy()
#update rooms data
def update_room_availability(roomId, check_in_date, check_out_date, availability):
    mycursor = mydb.cursor()
    mycursor.execute(f"UPDATE rooms SET check_in_date = '{check_in_date}', check_out_date = '{check_out_date}', availability = '{availability}' WHERE room_id = '{roomId}'")
    mydb.commit()
    title = 'Success'
    message = ' Transaction Success'
    success(title, message)
#add guest
def add_guest(name, contact, roomId, isbooked, checkInDate, _duration, ischeckedOut, payment_selected, paid_amount, checkoutdate):
    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO guests (guest_name, contact_num, room_id, isbooked, check_in_date, duration, ischecked_out, selected_payment, amount_paid) VALUES ('{name}', '{contact}', '{roomId}', '{isbooked}', '{checkInDate}', '{_duration}', '{ischeckedOut}', '{payment_selected}', '{paid_amount}')")
    mydb.commit()
    if isbooked == 'Booked':
        availability = 'Booked'
        _reserved =  hotels_reserved_rooms.get() + 1
        hotels_reserved_rooms.set(_reserved)
        _remaining_rooms = hotels_remaining_rooms.get() - 1
        hotels_remaining_rooms.set(_remaining_rooms)
        #get availability
        _available = hotels_remaining_rooms.get() / 60
        _convert_to_string = str(_available)
        _get_percentage = _convert_to_string[2:4]
        #update
        if len(_get_percentage) == 1:
            available.set(f" Available: {_get_percentage}0%")
        else:
            available.set(f" Available: {_get_percentage}%")
        #available.set(f" Available: {_get_percentage}%")
        reserved.set(f" Reserved: {hotels_reserved_rooms.get()}/{hotels_remaining_rooms.get() + hotels_reserved_rooms.get()}")
    elif isbooked == 'Checked In':
        availability = 'Checked In'
        #update system's visualization
        _occupied =  hotels_occupied_rooms.get() + 1
        hotels_occupied_rooms.set(_occupied)
        _remaining_rooms = hotels_remaining_rooms.get() - 1
        hotels_remaining_rooms.set(_remaining_rooms)

        #get availability
        if hotels_remaining_rooms.get() is 60:
            available.set(" Available: 98%")
        else:
            _available = hotels_remaining_rooms.get() / 60
            _convert_to_string = str(_available)
            _get_percentage = _convert_to_string[2:4]
            #update
            if len(_get_percentage) == 1:
                available.set(f" Available: {_get_percentage}0%")
            else:
                available.set(f" Available: {_get_percentage}%")
        occupied.set(f" Occupied: {hotels_occupied_rooms.get()}")
        reserved.set(f" Reserved: {hotels_reserved_rooms.get()}/{hotels_remaining_rooms.get() + hotels_reserved_rooms.get()}")
    #update room availability
    update_room_availability(roomId, checkInDate, checkoutdate, availability)

#update guests data
def update_guests(roomId, action):
    mycursor = mydb.cursor()
    if action == 'checked-out':
        mycursor.execute(f"UPDATE guests SET ischecked_out = 'Yes' WHERE room_id = '{roomId}'")
        mydb.commit()
        if mycursor.rowcount: #success
            title = 'Success'
            message = ' Check Out Success'
            success(title, message)

    elif action == 'cancelled':
        mycursor.execute(f"UPDATE guests SET ischecked_out = 'Cancelled', isbooked = 'Cancelled' WHERE room_id = '{roomId}'")
        mydb.commit()

        if mycursor.rowcount: #success
            title = 'Success'
            message = ' Cancellation Success'
            success(title, message)
#fetch guests data
def fetch_guests():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM guests ORDER BY check_in_date")
    res = mycursor.fetchall()

    return res
#show rooms
def show_rooms():
    global ROOMS_WINDOW
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0: #if not..
        #authenticate
        authentication("rooms")
    else: #otherwise create rooms window
        if ROOMS_WINDOW is not True:
            ROOMS_WINDOW = True
            #fetch from database
            mycursor = mydb.cursor()
            mycursor.execute('SELECT room_id, type, capacity, check_in_date, check_out_date, availability FROM rooms')
            res = mycursor.fetchall()
            #rooms window closing function..
            def close_rooms_window():
                global ROOMS_WINDOW
                ROOMS_WINDOW = False
                rooms_window.destroy()
            #create rooms window
            rooms_window = Toplevel()

            rooms_window.protocol('WM_DELETE_WINDOW', close_rooms_window)
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
            rooms_window.iconbitmap('./assets/hotel_icon.ico')
            wrapper = LabelFrame(rooms_window)
            canvas = Canvas(wrapper, width=750, height=450)
            frame = Frame(canvas)
            scrollbar = Scrollbar(wrapper, orient=VERTICAL, command=canvas.yview)
            scrollbar.place(x=730, y=37, height=463)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind('<Configure>', lambda e : canvas.configure(scrollregion=canvas.bbox('all')))
            canvas.create_window((0,0), window=frame, anchor=NW)
            #row variable
            r = 0
            #fetch rooms data
            for x in res:
                Label(frame, text=x[0]).grid(column=0, row=r, ipadx=30, ipady=10)
                Label(frame, text=x[1]).grid(column=1, row=r, ipadx=20, ipady=10)
                Label(frame, text=x[2]).grid(column=2, row=r, ipadx=40, ipady=10)
                Label(frame, text=x[3]).grid(column=3, row=r, ipadx=35, ipady=10)
                Label(frame, text=x[4]).grid(column=4, row=r, ipadx=40, ipady=10)
                if x[5] == 'Checked In':
                    Label(frame, text="Occupied").grid(column=5, row=r, ipadx=30, ipady=10)
                else:
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
            Label(rooms_window, text=headers[4], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=460, y=0)
            Label(rooms_window, text=headers[5], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=590, y=0)
            canvas.grid(column=0, row=0, pady=(40, 5))
            wrapper.pack()
            rooms_window.mainloop()
#check in
def check_in():
    global CHECK_IN_WINDOW
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0: #if not..
        #authenticate
        authentication("check_in")
    else:
        if CHECK_IN_WINDOW is not True:
            CHECK_IN_WINDOW = True
            check_in_window = Toplevel()
            check_in_window.title('Check in')
            check_in_window.resizable(False, False)
            #check in window closing function
            def close_check_in_window():
                global CHECK_IN_WINDOW
                CHECK_IN_WINDOW = False
                check_in_window.destroy()
            check_in_window.iconbitmap('./assets/hotel_icon.ico')
            check_in_window.protocol('WM_DELETE_WINDOW', close_check_in_window)
            width = 850
            height = 450
            #get screen dimension
            screen_width = check_in_window.winfo_screenwidth()
            screen_height = check_in_window.winfo_screenheight()
            center_x = int(screen_width/2 - width/2)
            center_y = int(screen_height/2 - height/2)
            check_in_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
            left_frame = LabelFrame(check_in_window, borderwidth=0)
            right_frame = LabelFrame(check_in_window)
            #variables
            firstname = StringVar()
            lastname = StringVar()
            address = StringVar()
            email_address = StringVar()
            contact_number = StringVar()
            #get full name
            full_name = StringVar()
            #icons
            guest_info_image = PhotoImage(file='./assets/guest_info.png')
            contact_details_image = PhotoImage(file='./assets/contact_details.png')
            #left section widgets
            Label(left_frame, image=guest_info_image).grid(column=0, row=0, columnspan=4, ipady=10)
            Label(left_frame, text='First name:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
            Entry(left_frame, width=15, highlightthickness=1, highlightbackground='#e0dada', textvariable=firstname).grid(column=1, row=1, sticky=W)
            Label(left_frame, text='Last name:', font=('sans-serif', 11)).grid(column=2, row=1, sticky=E)
            Entry(left_frame, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=lastname).grid(column=3, row=1, sticky=W)
            Label(left_frame, text='Address:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=address).grid(column=1, row=2, columnspan=3, sticky=W)
            Label(left_frame, image=contact_details_image).grid(column=0, row=3, columnspan=4, ipady=5)
            Label(left_frame, text='Email Add:', font=('sans-serif', 11)).grid(column=0, row=4, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=email_address).grid(column=1, row=4, columnspan=3, sticky=W)
            Label(left_frame, text='Contact #:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=contact_number).grid(column=1, row=5, columnspan=3, sticky=W)
            for widget in left_frame.winfo_children():
                widget.grid(padx=5, pady=5)

            left_frame.pack(fill=X, side=LEFT, ipady=50, ipadx=5, padx=(10, 0))
            #clear entries
            def clear_fields():
                firstname.set("")
                lastname.set("")
                address.set("")
                email_address.set("")
                contact_number.set("")

            Button(left_frame, text='CLEAR', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD), command=clear_fields).grid(ipadx=100, ipady=5, column=0, row=6, columnspan=4, pady=50)
            #right section widgets
            right_frame.columnconfigure(0, weight=1)
            right_frame.columnconfigure(1, weight=2)
            room_data_image = PhotoImage(file='./assets/room_data.png')
            Label(right_frame, image=room_data_image).grid(column=0, row=0, columnspan=3, sticky=N, pady=(70, 10))
            Label(right_frame, text='Room type:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
            room_type_list = ['Standard', 'Economy', 'VIP']
            selected_type = StringVar()
            selected_bed_capacity = StringVar()
            price = IntVar()
            selected_type = StringVar()
            selected_bed_capacity = StringVar()
            price = IntVar()
            #get current date
            date = d.datetime.now()
            date_format= StringVar()
            x = date.strftime("%m/%d/%y")
            date_format.set(f"Format: {x}")
            check_in_date = StringVar()
            check_in_date.set(date.strftime("%m/%d/%y"))
            check_out_date = StringVar()
            duration = IntVar()
            duration.set(1)
            price.set(475)
            selected_type.set('Standard')
            #get room type selected
            def type_selected():
                type = selected_type.get()
                return type
            #optionmenu function
            def typeselected(event):
                typeSelected = type_selected()
                if typeSelected == 'Standard':
                    if selected_bed_capacity.get() == 'SINGLE':
                        price.set(475)
                    elif selected_bed_capacity.get() == 'DOUBLE':
                        price.set(925)

                elif typeSelected == 'Economy':
                    if selected_bed_capacity.get() == 'SINGLE':
                        price.set(670)
                    elif selected_bed_capacity.get() == 'DOUBLE':
                        price.set(1180)

                elif typeSelected == 'VIP':
                    if selected_bed_capacity.get() == 'SINGLE':
                        price.set(3250)
                    elif selected_bed_capacity.get() == 'DOUBLE':
                        price.set(6000)
            dropdown_menu = OptionMenu(right_frame, selected_type, *room_type_list, command=typeselected)
            dropdown_menu.grid(column=1, row=1, sticky=W, ipadx=10, pady=10)
            def single():
                #call type selected function
                typeSelected = type_selected()
                #'Standard'
                if typeSelected == 'Standard':
                    price.set(475)
                #'Economy'
                elif typeSelected == 'Economy':
                    price.set(670)
                #'VIP'
                elif typeSelected == 'VIP':
                    price.set(3250)
            def double():
                #call type selected function
                typeSelected = type_selected()
                #STANDARD
                if typeSelected == 'Standard':
                    price.set(925)
                #ECONOMY
                elif typeSelected == 'Economy':
                    price.set(1180)
                #VIP
                elif typeSelected == 'VIP':
                    price.set(6000)

            def setPrice(event):
                global B2
                #get dates
                date1 = check_in_date.get()
                date2 = check_out_date.get()
                #start function if when string length is equal to 7
                if len(date2) == 7 and B2 is not True:
                    B2 = True
                    dropdown_menu.configure(state='disabled')
                    single_radiobutton.configure(state='disabled')
                    double_radiobutton.configure(state='disabled')
                    #slice and get chosen months
                    get_chosen_month1 = int(date1[0:2])
                    get_chosen_month2 = int(date2[0:2])
                    #slice and get chosen days
                    get_chosen_day1 = int(date1[3:5])
                    get_chosen_day2 = int(date2[3:5])
                    if get_chosen_day1 > 31 or get_chosen_day2 > 31:
                        title = 'An Error Occurred'
                        message = ' Invalid date'
                        error(title, message)
                    elif (get_chosen_month1 == get_chosen_month2) and (not get_chosen_day1 > 31 or not get_chosen_day2 > 31):
                        if get_chosen_day1 < get_chosen_day2:
                            #set duration
                            duration.set(get_chosen_day2 - get_chosen_day1)
                            current_price = price.get()
                            set_price = current_price * duration.get()
                            if duration.get() is not 0:
                                price.set(round(set_price))
                        else:
                            title = 'An Error Occurred'
                            message = ' Invalid date'
                            error(title, message)
                    elif (get_chosen_month2 > get_chosen_month1) and (not get_chosen_day1 > 31 or not get_chosen_day2 > 31):
                        difference = get_chosen_month2 - get_chosen_month1
                        #number of days based on number of months difference
                        _days = 31 #1 month
                        for x in range(1, 10):
                            if difference == x:
                                res = _days - get_chosen_day1
                                res = get_chosen_day1 + res + get_chosen_day2
                                _duration = res - get_chosen_day1
                                #set duration
                                duration.set(_duration)
                                current_price = price.get()
                                set_price = current_price * duration.get()
                                if duration.get() is not 0:
                                    price.set(round(set_price))
                            _days += 31
                        #hahahaha
                    print("Check in duration : {} days".format(duration.get()))
            def setPrice2(event):
                global B2
                _duration = duration.get()
                if B2 is not False:
                    B2 = False
                    if duration.get is not 0:
                        price.set(round(price.get() / _duration))
                    duration.set(1)
            def get_room():
                global GET_ROOM_WINDOW
                #get variables values
                fname = firstname.get()
                lname = lastname.get()
                full_name.set(f'{fname} {lname}')
                #values to insert
                name = full_name.get().upper()
                contact_num = contact_number.get()
                isbooked = 'Checked In'
                checkInDate = check_in_date.get()
                _duration = str(duration.get()) + " day(s)"
                isCheckedOut = 'No'
                selectedPayment = 'Full Payment'
                amountPaid = price.get()
                checkoutdate = check_out_date.get()
                if ((len(firstname.get()) and len(lastname.get()) and len(address.get()) and len(email_address.get()) and len(contact_number.get())) != 0) and (len(check_out_date.get()) == 8):
                    if GET_ROOM_WINDOW is not True:
                        GET_ROOM_WINDOW = True
                        type = selected_type.get().upper()
                        capacity = selected_bed_capacity.get().upper()
                        #fetch available rooms base on guest's chosen room type and capacity
                        mycursor = mydb.cursor()
                        mycursor.execute(f"SELECT room_id FROM rooms WHERE type = '{type}' AND capacity = '{capacity}' AND availability = 'available'")
                        res = mycursor.fetchall()
                        available_rooms = []
                        for x in res:
                            for y in x:
                                available_rooms.append(y)
                        get_room_window = Toplevel()
                        get_room_window.title('Selected Room ID')
                        get_room_window.resizable(False, False)
                        #book window closing function
                        def close_get_room_window():
                            global GET_ROOM_WINDOW
                            GET_ROOM_WINDOW = False
                            get_room_window.destroy()
                            if _text.get() == 'No available rooms':
                                show_rooms()

                        get_room_window.iconbitmap('./assets/hotel_icon.ico')
                        get_room_window.protocol('WM_DELETE_WINDOW', close_get_room_window)
                        width = 300
                        height = 100
                        #get screen dimension
                        screen_width = get_room_window.winfo_screenwidth()
                        screen_height = get_room_window.winfo_screenheight()
                        center_x = int(screen_width/2 - width/2)
                        center_y = int(screen_height/2 - height/2)
                        get_room_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
                        #add guest
                        _text = StringVar()
                        if not len(available_rooms) == 0:
                            _random = round(random.random() * len(available_rooms))
                            random_room = available_rooms[_random - 1]
                            _text.set(f'ROOM ID: {random_room}')
                            def addGuest():
                                global GET_ROOM_WINDOW, CHECK_IN_WINDOW
                                GET_ROOM_WINDOW = False
                                CHECK_IN_WINDOW = False
                                get_room_window.destroy()
                                check_in_window.destroy()
                                #call main add guest function
                                add_guest(name, contact_num, random_room, isbooked, checkInDate, _duration, isCheckedOut, selectedPayment, amountPaid, checkoutdate)
                            Label(get_room_window, textvariable=_text, font=('sans-serif', 11, font.BOLD), fg='#242526').pack(fill=BOTH, expand=YES, side=TOP)
                            Button(get_room_window, text='OK', font=('sans-serif', 11, font.BOLD), borderwidth=0 , fg='#fff', bg='#242526', command=addGuest).pack(side=BOTTOM, ipadx=30, ipady=2, pady=10)
                        else:
                            _text.set('No available rooms')
                            Label(get_room_window, textvariable=_text, font=('sans-serif', 11, font.BOLD), fg='#242526').pack(fill=BOTH, expand=YES, side=TOP)
                        get_room_window.mainloop()
            Label(right_frame, text='Capacity:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
            single_radiobutton = Radiobutton(right_frame, text='SINGLE', variable=selected_bed_capacity, command=single, value='SINGLE')
            single_radiobutton.grid(column=1, row=3, sticky=W)
            single_radiobutton.select()
            double_radiobutton = Radiobutton(right_frame, text='DOUBLE', variable=selected_bed_capacity, command=double, value='DOUBLE')
            double_radiobutton.grid(column=1, row=4, sticky=W)
            double_radiobutton.deselect()
            Label(right_frame, text='Price:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E, pady=10)
            Label(right_frame, textvariable=price, font=('sans-serif', 11)).grid(column=1, row=5, sticky=W, pady=10)
            Label(right_frame, textvariable=date_format, fg='gray').grid(column=1, row=6, sticky=W)
            Label(right_frame, text='Check out date:', font=('sans-serif', 11)).grid(column=0, row=7, sticky=E, pady=5)
            checkOutDate = Entry(right_frame, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=check_out_date)
            checkOutDate.grid(column=1, row=7, sticky=W, pady=5, padx=5)
            checkOutDate.bind('<KeyPress>', setPrice)
            checkOutDate.bind('<BackSpace>', setPrice2)
            right_frame.pack(fill=BOTH, side=RIGHT, expand=YES)
            Button(right_frame, text='CHECK IN', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD), command=get_room).grid(ipadx=100, ipady=5, column=0, row=8, columnspan=2, pady=20)
            check_in_window.mainloop()
#book
def book():
    global BOOK_WINDOW
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0: #if not..
        #authenticate
        authentication("book")
    else: #otherwise open book window
        if BOOK_WINDOW is not True:
            BOOK_WINDOW = True
            book_window = Toplevel()
            book_window.title('Book')
            book_window.resizable(False, False)
            #book window closing function
            def close_book_window():
                global BOOK_WINDOW
                BOOK_WINDOW = False
                book_window.destroy()
            book_window.iconbitmap('./assets/hotel_icon.ico')
            book_window.protocol('WM_DELETE_WINDOW', close_book_window)
            width = 850
            height = 520
            #get screen dimension
            screen_width = book_window.winfo_screenwidth()
            screen_height = book_window.winfo_screenheight()
            center_x = int(screen_width/2 - width/2)
            center_y = int(screen_height/2 - height/2)
            book_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
            left_frame = LabelFrame(book_window, borderwidth=0)
            right_frame = LabelFrame(book_window)
            #variables
            firstname = StringVar()
            lastname = StringVar()
            address = StringVar()
            email_address = StringVar()
            contact_number = StringVar()
            #get full name
            full_name = StringVar()
            #icons
            guest_info_image = PhotoImage(file='./assets/guest_info.png')
            contact_details_image = PhotoImage(file='./assets/contact_details.png')
            #left section widgets
            Label(left_frame, image=guest_info_image).grid(column=0, row=0, columnspan=4, ipady=(30))
            Label(left_frame, text='First name:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
            Entry(left_frame, width=15, highlightthickness=1, highlightbackground='#e0dada', textvariable=firstname).grid(column=1, row=1, sticky=W)
            Label(left_frame, text='Last name:', font=('sans-serif', 11)).grid(column=2, row=1, sticky=E)
            Entry(left_frame, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=lastname).grid(column=3, row=1, sticky=W)
            Label(left_frame, text='Address:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=address).grid(column=1, row=2, columnspan=3, sticky=W)
            Label(left_frame, image=contact_details_image).grid(column=0, row=3, columnspan=4, ipady=(30))
            Label(left_frame, text='Email Add:', font=('sans-serif', 11)).grid(column=0, row=4, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=email_address).grid(column=1, row=4, columnspan=3, sticky=W)
            Label(left_frame, text='Contact #:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=contact_number).grid(column=1, row=5, columnspan=3, sticky=W)
            for widget in left_frame.winfo_children():
                widget.grid(padx=5, pady=5)

            left_frame.pack(fill=X, side=LEFT, ipady=50, ipadx=5, padx=(10, 0))
            #clear entries
            def clear_fields():
                firstname.set("")
                lastname.set("")
                address.set("")
                email_address.set("")
                contact_number.set("")

            Button(left_frame, text='CLEAR', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD), command=clear_fields).grid(ipadx=100, ipady=5, column=0, row=6, columnspan=4, pady=50)
            #right section widgets
            right_frame.columnconfigure(0, weight=1)
            right_frame.columnconfigure(1, weight=2)
            room_data_image = PhotoImage(file='./assets/room_data.png')
            payment_image = PhotoImage(file='./assets/payment.png')
            Label(right_frame, image=room_data_image).grid(column=0, row=0, columnspan=3, sticky=N)
            Label(right_frame, text='Room type:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
            room_type_list = ['Standard', 'Economy', 'VIP']
            #variables
            selected_type = StringVar()
            selected_bed_capacity = StringVar()
            price = IntVar()
            selected_payment = StringVar()
            check_in_date = StringVar()
            check_out_date = StringVar()
            date_format= StringVar()
            duration = IntVar()
            #get date
            date = d.datetime.now()
            #initialized variables value
            price.set(475)
            selected_type.set('Standard')
            duration.set(1)
            #get current date
            x = date.strftime("%m/%d/%y")
            date_format.set(f"Format: {x}")
            #get room type selected
            def type_selected():
                type = selected_type.get()
                return type
            #optionmenu function
            def typeselected(event):
                typeSelected = type_selected()
                if typeSelected == 'Standard':
                    if selected_bed_capacity.get() == 'SINGLE' and selected_payment.get() == 'DOWN':
                        price.set(round(475 * 0.30))
                    elif selected_bed_capacity.get() == 'SINGLE' and selected_payment.get() == 'FULL':
                        price.set(475)
                    elif selected_bed_capacity.get() == 'DOUBLE' and selected_payment.get() == 'DOWN':
                        price.set(round(925 * 0.30))
                    elif selected_bed_capacity.get() == 'DOUBLE' and selected_payment.get() == 'FULL':
                        price.set(925)

                elif typeSelected == 'Economy':
                    if selected_bed_capacity.get() == 'SINGLE' and selected_payment.get() == 'DOWN':
                        price.set(round(670 * 0.30))
                    elif selected_bed_capacity.get() == 'SINGLE' and selected_payment.get() == 'FULL':
                        price.set(670)
                    elif selected_bed_capacity.get() == 'DOUBLE' and selected_payment.get() == 'DOWN':
                        price.set(round(1180 * 0.30))
                    elif selected_bed_capacity.get() == 'DOUBLE' and selected_payment.get() == 'FULL':
                        price.set(1180)

                elif typeSelected == 'VIP':
                    if selected_bed_capacity.get() == 'SINGLE' and selected_payment.get() == 'DOWN':
                        price.set(round(3250 * 0.30))
                    elif selected_bed_capacity.get() == 'SINGLE' and selected_payment.get() == 'FULL':
                        price.set(3250)
                    elif selected_bed_capacity.get() == 'DOUBLE' and selected_payment.get() == 'DOWN':
                        price.set(round(6000 * 0.30))
                    elif selected_bed_capacity.get() == 'DOUBLE' and selected_payment.get() == 'FULL':
                        price.set(6000)

            dropdown_menu = OptionMenu(right_frame, selected_type, *room_type_list, command=typeselected)
            dropdown_menu.grid(column=1, row=1, sticky=W, ipadx=10, pady=0)

            def single():
                #call type selected function
                typeSelected = type_selected()
                #'Standard'
                if typeSelected == 'Standard':
                    if selected_payment.get() == 'DOWN':
                        price.set(round(475 * 0.30))
                    else:
                        price.set(475)
                #'Economy'
                elif typeSelected == 'Economy':
                    if selected_payment.get() == 'DOWN':
                        price.set(round(670 * 0.30))
                    else:
                        price.set(670)
                #'VIP'
                elif typeSelected == 'VIP':
                    if selected_payment.get() == 'DOWN':
                        price.set(round(3250 * 0.30))
                    else:
                        price.set(3250)
            def double():
                #call type selected function
                typeSelected = type_selected()
                #STANDARD
                if typeSelected == 'Standard':
                    if selected_payment.get() == 'DOWN':
                        price.set(round(925 * 0.30))
                    else:
                        price.set(925)
                #ECONOMY
                elif typeSelected == 'Economy':
                    if selected_payment.get() == 'DOWN':
                        price.set(round(1180 * 0.30))
                    else:
                        price.set(1180)
                #VIP
                elif typeSelected == 'VIP':
                    if selected_payment.get() == 'DOWN':
                        price.set(round(6000 * 0.30))
                    else:
                        price.set(6000)
            Label(right_frame, text='Capacity:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
            single_radiobutton = Radiobutton(right_frame, text='SINGLE', variable=selected_bed_capacity,  command=single, value='SINGLE')
            single_radiobutton.grid(column=1, row=3, sticky=W)
            single_radiobutton.select()
            double_radiobutton = Radiobutton(right_frame, text='DOUBLE', variable=selected_bed_capacity,  command=double, value='DOUBLE')
            double_radiobutton.grid(column=1, row=4, sticky=W)
            double_radiobutton.deselect()
            Label(right_frame, image=payment_image).grid(column=0,row=5, columnspan=3, sticky=N, pady=(30, 0))
            Label(right_frame, text='Price:', font=('sans-serif', 11)).grid(column=0, row=6, sticky=E, pady=5)
            Label(right_frame, textvariable=price, font=('sans-serif', 11)).grid(column=1, row=6, sticky=W, pady=5)
            def down_payment():
                #call type selected function
                typeSelected = type_selected()
                #STANDARD
                if typeSelected == 'Standard':
                    if selected_bed_capacity.get() == 'SINGLE':
                        price.set(round(475 * 0.30))
                    else:
                        price.set(round(925 * 0.30))
                #ECONOMY
                elif typeSelected == 'Economy':
                    if selected_bed_capacity.get() == 'SINGLE':
                        price.set(round(670 * 0.30))
                    else:
                        price.set(round(1180 * 0.30))
                #VIP
                elif typeSelected == 'VIP':
                    if selected_bed_capacity.get() == 'SINGLE':
                        price.set(round(3250 * 0.30))
                    else:
                        price.set(round(6000 * 0.30))
            def full_payment():
                #call type selected function
                typeSelected = type_selected()
                #STANDARD
                if typeSelected == 'Standard':
                    if selected_bed_capacity.get() == 'DOUBLE':
                        price.set(925)
                    else:
                        price.set(475)
                #ECONOMY
                elif typeSelected == 'Economy':
                    if selected_bed_capacity.get() == 'DOUBLE':
                        price.set(1180)
                    else:
                        price.set(670)
                #VIP
                elif typeSelected == 'VIP':
                    if selected_bed_capacity.get() == 'DOUBLE':
                        price.set(6000)
                    else:
                        price.set(3250)
            down_payment_radiobutton = Radiobutton(right_frame, text='Down payment', variable=selected_payment,  command=down_payment, value='DOWN')
            down_payment_radiobutton.grid(column=1, row=7, sticky=W)
            down_payment_radiobutton.deselect()
            full_payment_radiobutton = Radiobutton(right_frame, text='Full payment', variable=selected_payment, command=full_payment, value='FULL')
            full_payment_radiobutton.grid(column=1, row=8, sticky=W)
            full_payment_radiobutton.select()
            def get_room():
                global GET_ROOM_WINDOW
                #get selected payment
                def _selectedPayment():
                    if selected_payment.get() == 'DOWN':
                        return 'Down payment'
                    elif selected_payment.get() == 'FULL':
                        return 'Full payment'
                #get variables values
                fname = firstname.get()
                lname = lastname.get()
                full_name.set(f'{fname} {lname}')
                #values to insert
                name = full_name.get().upper()
                contact_num = contact_number.get()
                isbooked = 'Booked'
                checkInDate = check_in_date.get()
                _duration = str(duration.get()) + " day(s)"
                isCheckedOut = 'No'
                selectedPayment = _selectedPayment()
                amountPaid = price.get()
                checkoutdate = check_out_date.get()
                if ((len(firstname.get()) and len(lastname.get()) and len(address.get()) and len(email_address.get()) and len(contact_number.get())) != 0) and (len(check_out_date.get()) == 8 and len(check_in_date.get()) == 8):
                    if GET_ROOM_WINDOW is not True:
                        GET_ROOM_WINDOW = True
                        type = selected_type.get().upper()
                        capacity = selected_bed_capacity.get().upper()
                        #fetch available rooms base on guest's chosen room type and capacity
                        mycursor = mydb.cursor()
                        mycursor.execute(f"SELECT room_id FROM rooms WHERE type = '{type}' AND capacity = '{capacity}' AND availability = 'Available'")
                        res = mycursor.fetchall()
                        available_rooms = []
                        for x in res:
                            for y in x:
                                available_rooms.append(y)
                        get_room_window = Toplevel()
                        get_room_window.title('Selected Room ID')
                        get_room_window.resizable(False, False)
                        #book window closing function
                        def close_get_room_window():
                            global GET_ROOM_WINDOW
                            GET_ROOM_WINDOW = False
                            get_room_window.destroy()
                            if _text.get() == 'No available rooms':
                                show_rooms()
                        get_room_window.iconbitmap('./assets/hotel_icon.ico')
                        get_room_window.protocol('WM_DELETE_WINDOW', close_get_room_window)
                        width = 300
                        height = 100
                        #get screen dimension
                        screen_width = get_room_window.winfo_screenwidth()
                        screen_height = get_room_window.winfo_screenheight()
                        center_x = int(screen_width/2 - width/2)
                        center_y = int(screen_height/2 - height/2)
                        get_room_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
                        #add guest
                        _random = round(random.random() * len(available_rooms))
                        _text = StringVar()
                        if len(available_rooms) == 0:
                            _text.set('No available rooms')
                            Label(get_room_window, textvariable=_text, font=('sans-serif', 11, font.BOLD), fg='#242526').pack(fill=BOTH, expand=YES, side=TOP)
                        else:
                            random_room = available_rooms[_random - 1]
                            _text.set(f'ROOM ID: {random_room}')
                            def addGuest():
                                global GET_ROOM_WINDOW, BOOK_WINDOW
                                GET_ROOM_WINDOW = False
                                BOOK_WINDOW = False
                                get_room_window.destroy()
                                book_window.destroy()
                                #call main add guest function
                                add_guest(name, contact_num, random_room, isbooked, checkInDate, _duration, isCheckedOut, selectedPayment, amountPaid, checkoutdate)
                            Label(get_room_window, textvariable=_text, font=('sans-serif', 11, font.BOLD), fg='#242526').pack(fill=BOTH, expand=YES, side=TOP)
                            Button(get_room_window, text='OK', font=('sans-serif', 11, font.BOLD), borderwidth=0 , fg='#fff', bg='#242526', command=addGuest).pack(side=BOTTOM, ipadx=30, ipady=2, pady=10)
                        get_room_window.mainloop()
            def setPrice(event):
                global B
                #get dates
                date1 = check_in_date.get()
                date2 = check_out_date.get()
                
                #start function if when string length is equal to 7
                if len(date2) == 7 and B is not True:
                    B = True
                    dropdown_menu.configure(state='disabled')
                    down_payment_radiobutton.configure(state='disabled')
                    full_payment_radiobutton.configure(state='disabled')
                    single_radiobutton.configure(state='disabled')
                    double_radiobutton.configure(state='disabled')
                    #slice and get chosen months
                    get_chosen_month1 = int(date1[0:2])
                    get_chosen_month2 = int(date2[0:2])
                    #slice and get chosen days
                    get_chosen_day1 = int(date1[3:5])
                    get_chosen_day2 = int(date2[3:5])
                    if get_chosen_day1 > 31 or get_chosen_day2 > 31:
                        title = 'An Error Occurred'
                        message = ' Invalid Date'
                        error(title, message)
                    elif (get_chosen_month1 == get_chosen_month2) and (not get_chosen_day1 > 31 or not get_chosen_day2 > 31):
                        if get_chosen_day1 < get_chosen_day2:
                            #set duration
                            duration.set(get_chosen_day2 - get_chosen_day1)
                            current_price = price.get()
                            set_price = current_price * duration.get()
                            if duration.get() is not 0:
                                price.set(round(set_price))
                        else:
                            title = 'An Error Occurred'
                            message = ' Invalid date'
                            error(title, message)
                    elif (get_chosen_month2 > get_chosen_month1) and (not get_chosen_day1 > 31 or not get_chosen_day2 > 31):
                        difference = get_chosen_month2 - get_chosen_month1
                        #number of days based on number of months difference
                        _days = 31 #1 month
                        for x in range(1, 10):
                            if difference == x:
                                res = _days - get_chosen_day1
                                res = get_chosen_day1 + res + get_chosen_day2
                                _duration = res - get_chosen_day1
                                #set duration
                                duration.set(_duration)
                                current_price = price.get()
                                set_price = current_price * duration.get()
                                if duration.get() is not 0:
                                    price.set(round(set_price))
                            _days += 31
                    #hahahaha
                    print("Booking duration : {} days".format(duration.get()))
            def setPrice2(event):
                global B
                _duration = duration.get()
                if B is not False:
                    B = False
                    if duration.get is not 0:
                        price.set(round(price.get() / _duration))
                    duration.set(1)

            #clear check out date entry on keypress
            def clear_date_entry2():
                if len(check_out_date.get()) > 6:
                     check_out_date.set()

            #get check in date and check out date
            expected_date_image = PhotoImage(file='./assets/expected_date.png')
            Label(right_frame, image=expected_date_image).grid(column=0, row=9, columnspan=3, sticky=N, pady=(10, 10))
            Label(right_frame, textvariable=date_format, fg='gray').grid(column=1, row=10, sticky=W, pady=2)
            Label(right_frame, text='Check-in date:', font=('sans-serif', 11)).grid(column=0, row=11, sticky=E, pady=3)
            Entry(right_frame, width=15, highlightthickness=1, highlightbackground='#e0dada', textvariable=check_in_date, font=('sans-serif', 10)).grid(column=1, row=11, sticky=W, padx=5, pady=3)
            checkInDate = Label(right_frame, text='Check-out date:', font=('sans-serif', 11))
            checkInDate.grid(column=0, row=12, sticky=E, pady=3)
            checkInDate.bind('<KeyPress>', clear_date_entry2)
            checkOutDate = Entry(right_frame, width=15, highlightthickness=1, highlightbackground='#e0dada', textvariable=check_out_date, font=('sans-serif', 10))
            checkOutDate.grid(column=1, row=12, sticky=W, padx=5, pady=3)
            checkOutDate.bind('<KeyPress>', setPrice)
            checkOutDate.bind('<BackSpace>', setPrice2)
            Button(right_frame, text='BOOK', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD), command=get_room).grid(ipadx=100, ipady=5, column=0, row=13, columnspan=2, pady=(10, 15))
            right_frame.pack(fill=BOTH, side=RIGHT, expand=YES)
            book_window.mainloop()
#guests data
def show_guests():
    global GUESTS_WINDOW
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0: #if not..
        #authenticate
        authentication("guests")
    else:
        if GUESTS_WINDOW is not True:
            GUESTS_WINDOW = True
            guests_window = Toplevel()
            guests_window.title('Guests')
            guests_window.resizable(False, False)
            #book window closing function
            def close_guests_window():
                global GUESTS_WINDOW
                GUESTS_WINDOW = False
                guests_window.destroy()
            guests_window.iconbitmap('./assets/hotel_icon.ico')
            guests_window.protocol('WM_DELETE_WINDOW', close_guests_window)
            width = 975
            height = 500
            #get screen dimension
            screen_width = guests_window.winfo_screenwidth()
            screen_height = guests_window.winfo_screenheight()
            center_x = int(screen_width/2 - width/2)
            center_y = int(screen_height/2 - height/2)
            guests_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
            #
            wrapper = LabelFrame(guests_window)
            canvas = Canvas(wrapper, width=975, height=450)
            frame = Frame(canvas)
            scrollbar = Scrollbar(wrapper, orient=VERTICAL, command=canvas.yview)
            scrollbar.place(x=948, y=36, height=460)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind('<Configure>', lambda e : canvas.configure(scrollregion=canvas.bbox('all')))
            canvas.create_window((0,0), window=frame, anchor=NW)
            #fetch guests date
            res = fetch_guests()
            r = 0
            for x in res:
                if len(x[1]) > 12:
                    name = str(x[1])
                    _sliced_name = name[0:11] + ".."
                    Label(frame, text=_sliced_name, font=('sans-serif', 9), width=15).grid(column=0, row=r, ipady=5)#, ipadx=5
                else:
                    Label(frame, text=x[1], font=('sans-serif', 9), width=15).grid(column=0, row=r, ipady=5)#, ipadx=5
                Label(frame, text=x[2], font=('sans-serif', 9), width=15).grid(column=1, row=r, ipady=5)#, ipadx=19
                Label(frame, text=x[3], font=('sans-serif', 9), width=12).grid(column=2, row=r, ipady=5)#, ipadx=20
                Label(frame, text=x[4], font=('sans-serif', 9), width=13).grid(column=3, row=r, ipady=5)#, ipadx=15
                Label(frame, text=x[5], font=('sans-serif', 9), width=15).grid(column=4, row=r, ipady=5)#, ipadx=25
                Label(frame, text=x[6], font=('sans-serif', 9), width=10).grid(column=5, row=r, ipady=5)#, ipadx=20
                Label(frame, text=x[7], font=('sans-serif', 9), width=15).grid(column=6, row=r, ipady=5)#, ipadx=10
                Label(frame, text=x[8], font=('sans-serif', 9), width=20).grid(column=7, row=r, ipady=5)#, ipadx=50
                Label(frame, text=x[9], font=('sans-serif', 9), width=15).grid(column=8, row=r, ipady=5)#, ipadx=20
                r += 1

            #headers name list
            headers = ['Guest Name', 'Contact #', 'Room ID', 'isBooked', 'Check-In Date', 'Duration', 'isChecked-Out', 'Selected Payment', 'Amount Paid']
            #headers widgets
            Label(guests_window, text=headers[0], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=0, y=0)
            Label(guests_window, text=headers[1], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=110, y=0)
            Label(guests_window, text=headers[2], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=210, y=0)
            Label(guests_window, text=headers[3], background='gray', fg='#fff', width=10, height=2, font=('sans-serif', 10)).place(x=320, y=0)
            Label(guests_window, text=headers[4], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=400, y=0)
            Label(guests_window, text=headers[5], background='gray', fg='#fff', width=10, height=2, font=('sans-serif', 10)).place(x=520, y=0)
            Label(guests_window, text=headers[6], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=590, y=0)
            Label(guests_window, text=headers[7], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=705, y=0)
            Label(guests_window, text=headers[8], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=850, y=0)
            canvas.grid(column=0, row=0, pady=(40, 5))
            wrapper.pack()
            guests_window.mainloop()
#cancel book
def cancel_book():
    global CANCELLATION_WINDOW
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0: #if not..
        #authenticate
        authentication("cancel")
    else:
        if CANCELLATION_WINDOW is not True:
            CANCELLATION_WINDOW = True
            cancellation_window = Toplevel()
            cancellation_window.title('Book Cancellation')
            cancellation_window.resizable(False, False)
            #variable
            entered_roomId = StringVar()
            #cancellation window closing function
            def close_cancellation_window():
                global CANCELLATION_WINDOW
                CANCELLATION_WINDOW = False
                cancellation_window.destroy()
            cancellation_window.iconbitmap('./assets/hotel_icon.ico')
            cancellation_window.protocol('WM_DELETE_WINDOW', close_cancellation_window)
            width = 300
            height = 150
            #get screen dimension
            screen_width = cancellation_window.winfo_screenwidth()
            screen_height = cancellation_window.winfo_screenheight()
            center_x = int(screen_width/2 - width/2)
            center_y = int(screen_height/2 - height/2)
            cancellation_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
            #cancellation function
            def cancellation():
                global CANCELLATION_WINDOW
                CANCELLATION_WINDOW = False
                cancellation_window.destroy()
                roomId = entered_roomId.get()
                mycursor = mydb.cursor()
                mycursor.execute(f"UPDATE rooms SET availability = 'Available' WHERE room_id = '{roomId}' AND availability = 'Booked'")
                mydb.commit()
                if mycursor.rowcount:
                    #set values
                    hotels_remaining_rooms.set(get_numberOf_available_rooms())
                    hotels_occupied_rooms.set(get_numberOf_occupied_rooms())
                    hotels_reserved_rooms.set(get_numberOf_reserved_rooms())
                    #system hotel's data visualization
                    if hotels_remaining_rooms.get() is 60:
                        available.set(" Available: 100%")
                        capacity.set(" Capacity: 60")
                        occupied.set(" Occupied: 0")
                        reserved.set(" Reserved: 0/60")
                    else:
                        #get availability
                        _available = (60 - (60 - hotels_remaining_rooms.get())) / 60
                        _convert_to_string = str(_available)
                        _get_percentage = _convert_to_string[2:4]
                        if len(_get_percentage) == 1:
                            available.set(f" Available: {_get_percentage}0%")
                        else:
                            available.set(f" Available: {_get_percentage}%")
                        #hotel's capacity
                        capacity.set(" Capacity: 60")
                        occupied.set(f" Occupied: {hotels_occupied_rooms.get()}")
                        reserved.set(f" Reserved: {hotels_reserved_rooms.get()}/{hotels_remaining_rooms.get() + hotels_reserved_rooms.get()}")
                    #update guests table
                    update_guests(roomId, 'cancelled')
                else:
                    title = 'An Error Occurred'
                    message = ' Room ID is not Booked'
                    error(title, message)
            Label(cancellation_window, text='Room ID:', font=('sans-serif', 11)).grid(column=0, row=0, pady=(60, 0), padx=(50, 0))
            Entry(cancellation_window, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=entered_roomId).grid(column=1, row=0, pady=(60, 0))
            Button(cancellation_window, text='Confirm', font=('sans-serif', 11, font.BOLD), background='#242526', fg='#fff', borderwidth=0, command=cancellation).grid(column=1, row=1, ipadx=10, ipady=1, sticky=W, pady=10)
            cancellation_window.mainloop()
#check out guest
def check_out():
    global CHECK_OUT_WINDOW
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0: #if not..
        #authenticate
        authentication("check_out")
    else:
        if CHECK_OUT_WINDOW is not True:
            CHECK_OUT_WINDOW = True
            check_out_window = Toplevel()
            check_out_window.title('Book Cancellation')
            check_out_window.resizable(False, False)
            #variable
            entered_roomId = StringVar()
            #cancellation window closing function
            def close_check_out_window():
                global CHECK_OUT_WINDOW
                CHECK_OUT_WINDOW = False
                check_out_window.destroy()
            check_out_window.iconbitmap('./assets/hotel_icon.ico')
            check_out_window.protocol('WM_DELETE_WINDOW', close_check_out_window)
            width = 300
            height = 150
            #get screen dimension
            screen_width = check_out_window.winfo_screenwidth()
            screen_height = check_out_window.winfo_screenheight()
            center_x = int(screen_width/2 - width/2)
            center_y = int(screen_height/2 - height/2)
            check_out_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
            #cancellation function
            def check_out_guest():
                global CHECK_OUT_WINDOW
                CHECK_OUT_WINDOW = False
                check_out_window.destroy()
                roomId = entered_roomId.get()
                mycursor = mydb.cursor()
                mycursor.execute(f"UPDATE rooms SET availability = 'Available' WHERE room_id = '{roomId}' AND availability = 'Checked In'")
                mydb.commit()
                if mycursor.rowcount:
                    #set values
                    hotels_remaining_rooms.set(get_numberOf_available_rooms())
                    hotels_occupied_rooms.set(get_numberOf_occupied_rooms())
                    hotels_reserved_rooms.set(get_numberOf_reserved_rooms())
                    #system hotel's data visualization
                    if hotels_remaining_rooms.get() is 60:
                        available.set(" Available: 100%")
                        capacity.set(" Capacity: 60")
                        occupied.set(" Occupied: 0")
                        reserved.set(" Reserved: 0/60")
                    else:
                        #get availability
                        _available = (60 - (60 - hotels_remaining_rooms.get())) / 60
                        _convert_to_string = str(_available)
                        _get_percentage = _convert_to_string[2:4]
                        if len(_get_percentage) == 1:
                            available.set(f" Available: {_get_percentage}0%")
                        else:
                            available.set(f" Available: {_get_percentage}%")
                        #hotel's capacity
                        capacity.set(" Capacity: 60")
                        occupied.set(f" Occupied: {hotels_occupied_rooms.get()}")
                        reserved.set(f" Reserved: {hotels_reserved_rooms.get()}/{hotels_remaining_rooms.get() + hotels_reserved_rooms.get()}")
                    update_guests(roomId, 'checked-out')

                else: #error
                    title = 'An Error Occurred'
                    message = ' Room ID is not Occupied'
                    error(title, message)

            Label(check_out_window, text='Room ID:', font=('sans-serif', 11)).grid(column=0, row=0, pady=(60, 0), padx=(50, 0))
            Entry(check_out_window, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=entered_roomId).grid(column=1, row=0, pady=(60, 0))
            Button(check_out_window, text='Confirm', font=('sans-serif', 11, font.BOLD), background='#242526', fg='#fff', borderwidth=0, command=check_out_guest).grid(column=1, row=1, ipadx=10, ipady=1, sticky=W, pady=10)
            check_out_window.mainloop()
#get number of occupied rooms
def get_numberOf_available_rooms():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT room_id FROM rooms WHERE availability = 'Available'")
    res = mycursor.fetchall()
    return len(res)
#get number of occupied rooms
def get_numberOf_occupied_rooms():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT room_id FROM rooms WHERE availability = 'Checked In'")
    res = mycursor.fetchall()
    return len(res)
#get number of reserved rooms
def get_numberOf_reserved_rooms():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT room_id FROM rooms WHERE availability = 'Booked'")
    res = mycursor.fetchall()
    return len(res)
#main window
main_window = Tk()
#if main window is closed
main_window.protocol('WM_DELETE_WINDOW', close_main_window)
main_window.title('King\'s Inn Hotel')
main_window.resizable(False, False)
#window dimension
width = 800
height = 550
#get screen dimension
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
center_x = int(screen_width/2 - width/2)
center_y = int(screen_height/2 - height/2)
main_window.iconbitmap('./assets/hotel_icon.ico')
main_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
#variables
available = StringVar()
occupied = StringVar()
capacity = StringVar()
reserved = StringVar()
hotels_available_rooms = StringVar()
hotels_occupied_rooms = IntVar()
hotels_capacity = IntVar()
hotels_reserved_rooms = IntVar()
hotels_remaining_rooms = IntVar()
#set values
hotels_remaining_rooms.set(get_numberOf_available_rooms())
hotels_occupied_rooms.set(get_numberOf_occupied_rooms())
hotels_reserved_rooms.set(get_numberOf_reserved_rooms())
#system hotel's data visualization
if hotels_remaining_rooms.get() is 60:
    available.set(" Available: 100%")
    capacity.set(" Capacity: 60")
    occupied.set(" Occupied: 0")
    reserved.set(" Reserved: 0/60")
else:
    #get availability
    _available = (60 - (60 - hotels_remaining_rooms.get())) / 60
    _convert_to_string = str(_available)
    _get_percentage = _convert_to_string[2:4]
    if len(_get_percentage) == 1:
        available.set(f" Available: {_get_percentage}0%")
    else:
        available.set(f" Available: {_get_percentage}%")
    #hotel's capacity
    capacity.set(" Capacity: 60")
    occupied.set(f" Occupied: {hotels_occupied_rooms.get()}")
    reserved.set(f" Reserved: {hotels_reserved_rooms.get()}/{hotels_remaining_rooms.get() + hotels_reserved_rooms.get()}")
#header..
header = Frame(main_window, highlightthickness=1, highlightbackground='gray')
header.pack(fill='x', side='top')
header.columnconfigure(0, weight=1)
settings_icon = PhotoImage(file='./assets/settings.png')
logo = PhotoImage(file='./assets/hotel_logo.png')
#header widgets..
#hotel logo
Label(header, image=logo).grid(column=0, row=0, sticky=W, padx=25, pady=15)
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
isadmin.set(' : (Receptionist)')
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

Label(availability_inner_frame, image=available_icon, compound=LEFT, textvariable=available, font=('sans-serif', 11)).grid(column=0, row=0, sticky=W)
Label(availability_inner_frame, image=capacity_icon, compound=LEFT, textvariable=capacity, font=('sans-serif', 11)).grid(column=0, row=1, sticky=W)
Label(availability_inner_frame, image=occupied_icon, compound=LEFT, textvariable=occupied, font=('sans-serif', 11)).grid(column=0, row=2, sticky=W)
Label(availability_inner_frame, image=reserved_icon, compound=LEFT, textvariable=reserved, font=('sans-serif', 11)).grid(column=0, row=3, sticky=W)
#sign out frame
sign_out_frame = Frame(leftSect)
sign_out_icon = PhotoImage(file='./assets/sign-out.png')
sign_out_frame.grid(column=0, row=2, pady=70)

Button(sign_out_frame, image=sign_out_icon, compound=LEFT, text=' Sign-out', font=('sans-serif', 11), borderwidth=0, command=sign_out).pack()
#main section
main_section_frame = Frame(main_window)
main_section_frame.pack(pady=70)

check_in_icon = PhotoImage(file='./assets/check_in.png')
check_out_icon = PhotoImage(file='./assets/check_out.png')
book_icon = PhotoImage(file='./assets/book.png')
_rooms = PhotoImage(file='./assets/rooms.png')
cancel_booking = PhotoImage(file='./assets/cancel_booking.png')
guests = PhotoImage(file='./assets/guests.png')
Button(main_section_frame, text='Check In', image=check_in_icon, compound=LEFT, borderwidth=0, font=('sans-serif', 15), fg='#242526', command=check_in).grid(column=0, row=1)
Button(main_section_frame, text=' Check Out', image=check_out_icon, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=check_out).grid(column=1, row=1, sticky=E)
Button(main_section_frame, text=' Guests', image=guests, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=show_guests).grid(column=2, row=1, sticky=W)
Button(main_section_frame, text=' Rooms', image=_rooms, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=show_rooms).grid(column=0, row=0)
Button(main_section_frame, text='Book', image=book_icon, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=book).grid(column=1, row=0, sticky=W)
Button(main_section_frame, text='Cancel', image=cancel_booking, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=cancel_book).grid(column=2, row=0)
for widget in main_section_frame.winfo_children():
    widget.grid(ipady=30, padx=10, pady=10)
main_window.mainloop()



