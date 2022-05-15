from tkinter import *
from tkinter import font
import mysql.connector

#toplevel windows
SETTINGS_WINDOW = False
ERROR_WINDOW = False
SUCCESS_WINDOW = False
ADD_USER_WINDOW = False
DELETE_USER_WINDOW = False
ROOMS_WINDOW = False
CHECK_IN_WINDOW = False
BOOK_WINDOW = False
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
        width = 300
        height = 100
        #get screen dimension
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        center_x = int(screen_width/2 - width/2)
        center_y = int(screen_height/2 - height/2)
        error_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
        error_icon = PhotoImage(file='./assets/alert-icon-red.png')
        Label(error_window, image=error_icon, text=message, font=('sans-serif', 15), compound=LEFT).pack(fill='x', pady=30)
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
        width = 300
        height = 100
        #get screen dimension
        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()
        center_x = int(screen_width/2 - width/2)
        center_y = int(screen_height/2 - height/2)
        success_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
        success_icon = PhotoImage(file='./assets/success-icon.png')
        Label(success_window, image=success_icon, text=message, font=('sans-serif', 15), compound=LEFT).pack(fill='x', pady=30)
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
            #create column names
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
                            message = ' User deleted'
                            success(title, message)

                        else: #otherwise..
                            DELETE_USER_WINDOW = False
                            delete_user_window.destroy()
                            title = 'An error occured'
                            message = ' Username doesn\'t exist'
                            error(title, message)
                    #delete user window widgets
                    Label(delete_user_window, text='Username:', font=('sans-serif', 11)).grid(column=1, row=0, sticky=W, pady=(15, 0), padx=5)
                    Entry(delete_user_window, width=30, font=('sans-serif', 9), textvariable=entered_username).grid(column=1, row=1, sticky=W, padx=5, ipady=1)
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
                                    message =' User added'
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
                        Entry(entries_frame, textvariable=name, width=30, font=('sans-serif', 9)).grid(column=3, row=0, padx=(0, 30), pady=2, sticky=E)
                        Entry(entries_frame, textvariable=username, width=30, font=('sans-serif', 9)).grid(column=3, row=1, padx=(0, 30), pady=2, sticky=E)
                        Entry(entries_frame, textvariable=password, width=30, font=('sans-serif', 9)).grid(column=3, row=2, padx=(0, 30), pady=2, sticky=E)
                        Checkbutton(entries_frame, text='Admin', variable=admin, onvalue='true', offvalue='false', font=('sans-serif', 10)).grid(column=3, row=3, sticky=W, pady=3)
                        #bottom widgets frame
                        bottom_frame = Frame(add_user_window)
                        bottom_frame.grid(column=0, row=1, sticky=NE)

                        Button(bottom_frame, text='Add user', borderwidth=0, background='#242526', foreground='#fff', font=('sans-serif', 11), command=addUser).pack(ipadx=120, ipady=5, pady=10)
                        add_user_window.mainloop()
                else: 
                    title = 'An error occured'
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
        title = 'An error occured'
        message = ' Access denied'
        error(title , message)
#authentication..
def authentication():
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
                    isadmin.set('({})'.format(isADMIN))
                else:
                    isadmin.set('({})'.format(isADMIN))
                signed()
                login_form.destroy()
                main_window.deiconify()
                print('Logged in as {}'.format(isADMIN))
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
        authentication()
    else:
        isAdmin()

#sign out function
def sign_out():
    #sign out current user
    signOut()
    #re-authenticate
    authentication()

#main window closing function
def close_main_window():
    signOut()
    main_window.destroy()

#show rooms
def show_rooms():
    global ROOMS_WINDOW
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0: #if not..
        #authenticate
        authentication()
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
            rooms_window = Tk()
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
        authentication()
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
            #icons
            guest_info_image = PhotoImage(file='./assets/guest_info.png')
            contact_details_image = PhotoImage(file='./assets/contact_details.png')
            #left section widgets
            Label(left_frame, image=guest_info_image).grid(column=0, row=0, columnspan=4, ipady=10)
            Label(left_frame, text='First name:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
            Entry(left_frame, width=15, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=1, sticky=W)
            Label(left_frame, text='Last name:', font=('sans-serif', 11)).grid(column=2, row=1, sticky=E)
            Entry(left_frame, width=20, highlightthickness=1, highlightbackground='#e0dada').grid(column=3, row=1, sticky=W)
            Label(left_frame, text='Address:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=2, columnspan=3, sticky=W)
            Label(left_frame, image=contact_details_image).grid(column=0, row=3, columnspan=4, ipady=5)
            Label(left_frame, text='Email Add:', font=('sans-serif', 11)).grid(column=0, row=4, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=4, columnspan=3, sticky=W)
            Label(left_frame, text='Contact #:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=5, columnspan=3, sticky=W)
            for widget in left_frame.winfo_children():
                widget.grid(padx=5, pady=5)

            left_frame.pack(fill=X, side=LEFT, ipady=50, ipadx=5, padx=(10, 0))
            Button(left_frame, text='CLEAR', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD)).grid(ipadx=100, ipady=5, column=0, row=6, columnspan=4, pady=50)
            #right section widgets
            right_frame.columnconfigure(0, weight=1)
            right_frame.columnconfigure(1, weight=2)
            room_data_image = PhotoImage(file='./assets/room_data.png')
            Label(right_frame, image=room_data_image).grid(column=0, row=0, columnspan=3, sticky=N, pady=(70, 10))
            Label(right_frame, text='Room type:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
            room_type_list = ['Standard', 'Economy', 'VIP']
            selected_type = StringVar()
            selected_bed_capacity = StringVar()
            price = StringVar()
            price.set('3000')
            selected_type.set('Standard')
            dropdown_menu = OptionMenu(right_frame, selected_type, *room_type_list)
            dropdown_menu.grid(column=1, row=1, sticky=W, ipadx=10, pady=10)
            def single():
                selected_bed_capacity.set('SINGLE')
                print(selected_bed_capacity.get())
            def double():
                selected_bed_capacity.set('DOUBLE')
                print(selected_bed_capacity.get())
            Label(right_frame, text='Capacity:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
            single_radiobutton = Radiobutton(right_frame, text='SINGLE', command=single, value='Single')
            single_radiobutton.grid(column=1, row=3, sticky=W)
            single_radiobutton.deselect()
            double_radiobutton = Radiobutton(right_frame, text='DOUBLE', command=double, value='Double')
            double_radiobutton.grid(column=1, row=4, sticky=W)
            double_radiobutton.select()
            Label(right_frame, text='Price:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E, pady=10)
            Label(right_frame, textvariable=price, font=('sans-serif', 11)).grid(column=1, row=5, sticky=W, pady=10)
            Label(right_frame, text='Check out date:', font=('sans-serif', 11)).grid(column=0, row=6, sticky=E, pady=10)
            Entry(right_frame, width=20, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=6, sticky=W, pady=10, padx=5)
            right_frame.pack(fill=BOTH, side=RIGHT, expand=YES)
            Button(right_frame, text='CHECK IN', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD)).grid(ipadx=100, ipady=5, column=0, row=7, columnspan=2, pady=30)
            check_in_window.mainloop()
#book
def book():
    global BOOK_WINDOW
    #is signed in?
    is_signed = isSigned()
    if is_signed is 0: #if not..
        #authenticate
        authentication()
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
            book_window.protocol('WM_DELETE_WINDOW', close_book_window)
            width = 850
            height = 500
            #get screen dimension
            screen_width = book_window.winfo_screenwidth()
            screen_height = book_window.winfo_screenheight()
            center_x = int(screen_width/2 - width/2)
            center_y = int(screen_height/2 - height/2)
            book_window.geometry(f'{width}x{height}+{center_x}+{center_y}')
            left_frame = LabelFrame(book_window, borderwidth=0)
            right_frame = LabelFrame(book_window)
            #icons
            guest_info_image = PhotoImage(file='./assets/guest_info.png')
            contact_details_image = PhotoImage(file='./assets/contact_details.png')
            #left section widgets
            Label(left_frame, image=guest_info_image).grid(column=0, row=0, columnspan=4, ipady=(30))
            Label(left_frame, text='First name:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
            Entry(left_frame, width=15, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=1, sticky=W)
            Label(left_frame, text='Last name:', font=('sans-serif', 11)).grid(column=2, row=1, sticky=E)
            Entry(left_frame, width=20, highlightthickness=1, highlightbackground='#e0dada').grid(column=3, row=1, sticky=W)
            Label(left_frame, text='Address:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=2, columnspan=3, sticky=W)
            Label(left_frame, image=contact_details_image).grid(column=0, row=3, columnspan=4, ipady=(30))
            Label(left_frame, text='Email Add:', font=('sans-serif', 11)).grid(column=0, row=4, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=4, columnspan=3, sticky=W)
            Label(left_frame, text='Contact #:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E)
            Entry(left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=5, columnspan=3, sticky=W)
            for widget in left_frame.winfo_children():
                widget.grid(padx=5, pady=5)

            left_frame.pack(fill=X, side=LEFT, ipady=50, ipadx=5, padx=(10, 0))
            Button(left_frame, text='CLEAR', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD)).grid(ipadx=100, ipady=5, column=0, row=6, columnspan=4, pady=50)
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
            price = StringVar()
            selected_payment = StringVar()
            var1 = StringVar()
            var2 = StringVar()
            #set variables
            price.set('3000')
            selected_type.set('Standard')
            dropdown_menu = OptionMenu(right_frame, selected_type, *room_type_list)
            dropdown_menu.grid(column=1, row=1, sticky=W, ipadx=10, pady=0)
            def single():
                selected_bed_capacity.set('SINGLE')
                print(selected_bed_capacity.get())
            def double():
                selected_bed_capacity.set('DOUBLE')
                print(selected_bed_capacity.get())
            Label(right_frame, text='Capacity:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
            single_radiobutton = Radiobutton(right_frame, text='SINGLE', variable=var1, command=single, value='Single')
            single_radiobutton.grid(column=1, row=3, sticky=W)
            single_radiobutton.select()
            double_radiobutton = Radiobutton(right_frame, text='DOUBLE', variable=var1, command=double, value='Double')
            double_radiobutton.grid(column=1, row=4, sticky=W)
            double_radiobutton.deselect()
            Label(right_frame, image=payment_image).grid(column=0,row=5, columnspan=3, sticky=N, pady=(30, 0))
            Label(right_frame, text='Price:', font=('sans-serif', 11)).grid(column=0, row=6, sticky=E, pady=5)
            Label(right_frame, textvariable=price, font=('sans-serif', 11)).grid(column=1, row=6, sticky=W, pady=5)
            def down_payment():
                selected_payment.set('Down payment')
            def full_payment():
                selected_payment.set('Full payment')
            down_payment_radiobutton = Radiobutton(right_frame, text='Down payment', variable=var2, command=down_payment, value='down')
            down_payment_radiobutton.grid(column=1, row=7, sticky=W)
            down_payment_radiobutton.select()
            full_payment_radiobutton = Radiobutton(right_frame, text='Full payment', variable=var2, command=full_payment, value='full')
            full_payment_radiobutton.grid(column=1, row=8, sticky=W)
            full_payment_radiobutton.deselect()

            #get check in date and check out date
            expected_date_image = PhotoImage(file='./assets/expected_date.png')
            Label(right_frame, image=expected_date_image).grid(column=0, row=9, columnspan=3, sticky=N, pady=(10, 10))
            Label(right_frame, text='Check in:', font=('sans-serif', 11)).grid(column=0, row=10, sticky=E, pady=3)
            Entry(right_frame, width=20, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=10, sticky=W, padx=5, pady=3)
            Label(right_frame, text='Check out:', font=('sans-serif', 11)).grid(column=0, row=11, sticky=E, pady=3)
            Entry(right_frame, width=20, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=11, sticky=W, padx=5, pady=3)
            Button(right_frame, text='BOOK', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD)).grid(ipadx=100, ipady=5, column=0, row=12, columnspan=2, pady=20)
            right_frame.pack(fill=BOTH, side=RIGHT, expand=YES)
            book_window.mainloop()

#main window
main_window = Tk()
#if main window is closed
main_window.protocol('WM_DELETE_WINDOW', close_main_window)
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

check_in_icon = PhotoImage(file='./assets/check_in.png')
check_out_icon = PhotoImage(file='./assets/check_out.png')
book_icon = PhotoImage(file='./assets/book.png')
_rooms = PhotoImage(file='./assets/rooms.png')
cancel_booking = PhotoImage(file='./assets/cancel_booking.png')
guests = PhotoImage(file='./assets/guests.png')
Button(main_section_frame, text='Check In', image=check_in_icon, compound=LEFT, borderwidth=0, font=('sans-serif', 15), fg='#242526', command=check_in).grid(column=0, row=1)
Button(main_section_frame, text=' Check Out', image=check_out_icon, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=1, row=1, sticky=E)
Button(main_section_frame, text=' Guests', image=guests, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=2, row=1, sticky=W)
Button(main_section_frame, text=' Rooms', image=_rooms, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=show_rooms).grid(column=0, row=0)
Button(main_section_frame, text='Book', image=book_icon, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=book).grid(column=1, row=0, sticky=W)
Button(main_section_frame, text='Cancel', image=cancel_booking, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526').grid(column=2, row=0)
for widget in main_section_frame.winfo_children():
    widget.grid(ipady=30, padx=10, pady=10)
main_window.mainloop()



