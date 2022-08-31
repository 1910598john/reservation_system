from tkinter import *
from tkinter import font
import datetime as d
import random
import db.connection as conn

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

class HotelReservation(Tk):
    def __init__(self):
        super().__init__()
        self.current_user = []
        self.available = StringVar()
        self.occupied = StringVar()
        self.capacity = StringVar()
        self.reserved = StringVar()
        self.hotels_available_rooms = StringVar()
        self.hotels_occupied_rooms = IntVar()
        self.hotels_capacity = IntVar()
        self.hotels_reserved_rooms = IntVar()
        self.hotels_remaining_rooms = IntVar()
        self.available_icon = PhotoImage(file='./assets/available.png')
        self.action = None
        self.hotels_remaining_rooms.set(self.get_numberOf_available_rooms())
        self.hotels_occupied_rooms.set(self.get_numberOf_occupied_rooms())
        self.hotels_reserved_rooms.set(self.get_numberOf_reserved_rooms())
        self.protocol('WM_DELETE_WINDOW', self.close_main_window)
        self.title('King\'s Inn Hotel')
        self.resizable(False, False)
        self.geometry(self.windows_geometry(800, 550))
        self.iconbitmap('./assets/hotel_icon.ico')
        self.header = Frame(self, highlightthickness=1, highlightbackground='gray')
        self.header.pack(fill='x', side='top')
        self.header.columnconfigure(0, weight=1)
        self.settings_icon = PhotoImage(file='./assets/settings.png')
        self.logo = PhotoImage(file='./assets/hotel_logo.png')
        Label(self.header, image=self.logo).grid(column=0, row=0, sticky=W, padx=25, pady=15)
        Button(self.header, image=self.settings_icon, compound=LEFT, text='Settings', borderwidth=0, font=('sans-serif', 15), fg='#242526', command=self.settings).grid(column=1, row=0, sticky=E, padx=20, pady=10)
        self.leftSect = Frame(self, highlightbackground='gray', highlightthickness=1)
        self.leftSect.pack(fill='y', side='left')
        self.leftSect.rowconfigure(1, weight=3)
        self.user_icon = PhotoImage(file='./assets/user.png')
        self.rank_icon = PhotoImage(file='./assets/rank.png')
        self.user_info_frame = Frame(self.leftSect)
        self.user_info_frame.grid(column=0, row=0, padx=10, pady=30, sticky=S)
        self.user_info_frame.columnconfigure(0, weight=1)
        self.user_info_inner_frame = Frame(self.user_info_frame)
        self.user_info_inner_frame.grid(column=0, row=0, padx=10)
        self.user_info_inner_frame.columnconfigure(0, weight=1)
        self.user_name = StringVar()
        self.user_name.set('User: unsigned')
        self.isadmin = StringVar()
        self.isadmin.set(' : (Receptionist)')
        Label(self.user_info_inner_frame, image=self.user_icon, textvariable=self.user_name, compound=LEFT, font=('sans-serif', 11)).grid(column=0, row=0, sticky=W)
        Label(self.user_info_inner_frame, image=self.rank_icon, textvariable=self.isadmin, compound=LEFT, font=('sans-serif', 11)).grid(column=0, row=1, sticky=W)
        self.capacity_icon = PhotoImage(file='./assets/capacity.png')
        self.occupied_icon = PhotoImage(file='./assets/occupied.png')
        self.reserved_icon = PhotoImage(file='./assets/reserved.png')
        self.availability_frame = Frame(self.leftSect, highlightbackground='gray', highlightthickness=1)
        self.availability_frame.grid(column=0, row=1, padx=10, pady=10, sticky=N)
        self.availability_frame.columnconfigure(0, weight=1)
        self.availability_inner_frame = Frame(self.availability_frame)
        self.availability_inner_frame.grid(column=0, row=0, pady=20, padx=30)
        self.availability_inner_frame.columnconfigure(0, weight=1)
        Label(self.availability_inner_frame, image=self.available_icon, compound=LEFT, textvariable=self.available, font=('sans-serif', 11)).grid(column=0, row=0, sticky=W)
        Label(self.availability_inner_frame, image=self.capacity_icon, compound=LEFT, textvariable=self.capacity, font=('sans-serif', 11)).grid(column=0, row=1, sticky=W)
        Label(self.availability_inner_frame, image=self.occupied_icon, compound=LEFT, textvariable=self.occupied, font=('sans-serif', 11)).grid(column=0, row=2, sticky=W)
        Label(self.availability_inner_frame, image=self.reserved_icon, compound=LEFT, textvariable=self.reserved, font=('sans-serif', 11)).grid(column=0, row=3, sticky=W)
        self.sign_out_frame = Frame(self.leftSect)
        self.sign_out_icon = PhotoImage(file='./assets/sign-out.png')
        self.sign_out_frame.grid(column=0, row=2, pady=70)
        Button(self.sign_out_frame, image=self.sign_out_icon, compound=LEFT, text=' Sign-out', font=('sans-serif', 11), borderwidth=0, command=self.sign_out).pack()
        self.main_section_frame = Frame(self)
        self.main_section_frame.pack(pady=70)
        self.check_in_icon = PhotoImage(file='./assets/check_in.png')
        self.check_out_icon = PhotoImage(file='./assets/check_out.png')
        self.book_icon = PhotoImage(file='./assets/book.png')
        self._rooms = PhotoImage(file='./assets/rooms.png')
        self.cancel_booking = PhotoImage(file='./assets/cancel_booking.png')
        self.guests = PhotoImage(file='./assets/guests.png')
        Button(self.main_section_frame, text='Check In', image=self.check_in_icon, compound=LEFT, borderwidth=0, font=('sans-serif', 15), fg='#242526', command=self.open_check_in_window).grid(column=0, row=1)
        Button(self.main_section_frame, text=' Check Out', image=self.check_out_icon, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=self.open_check_out_window).grid(column=1, row=1, sticky=E)
        Button(self.main_section_frame, text=' Guests', image=self.guests, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=self.open_guests_data_window).grid(column=2, row=1, sticky=W)
        Button(self.main_section_frame, text=' Rooms', image=self._rooms, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=self.open_rooms_data_window).grid(column=0, row=0)
        Button(self.main_section_frame, text='Book', image=self.book_icon, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=self.open_book_window).grid(column=1, row=0, sticky=W)
        Button(self.main_section_frame, text='Cancel', image=self.cancel_booking, compound=LEFT,  borderwidth=0, font=('sans-serif', 15), fg='#242526', command=self.open_cancellation_window).grid(column=2, row=0)
        for widget in self.main_section_frame.winfo_children():
            widget.grid(ipady=30, padx=10, pady=10)
        #system hotel's data visualization
        if self.hotels_remaining_rooms.get() == 60:
            self.available.set(" Available: 100%")
            self.capacity.set(" Capacity: 60")
            self.occupied.set(" Occupied: 0")
            self.reserved.set(" Reserved: 0/60")
        else:
            #get availability
            _available = (60 - (60 - self.hotels_remaining_rooms.get())) / 60
            _convert_to_string = str(_available)
            _get_percentage = _convert_to_string[2:4]
            if len(_get_percentage) == 1:
                self.available.set(f" Available: {_get_percentage}0%")
            else:
                self.available.set(f" Available: {_get_percentage}%")
            #hotel's capacity
            self.capacity.set(" Capacity: 60")
            self.occupied.set(f" Occupied: {self.hotels_occupied_rooms.get()}")
            self.reserved.set(f" Reserved: {self.hotels_reserved_rooms.get()}/{self.hotels_remaining_rooms.get() + self.hotels_reserved_rooms.get()}")

    def windows_geometry(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - width/2)
        center_y = int(screen_height/2 - height/2)
        return f'{width}x{height}+{center_x}+{center_y}'
        
    def authentication(self, action):
        self.action = action
        self.withdraw()
        login = Login(self)
        login.grab_set()
    
    def sign_out(self):
        self.signOut()
        self.authentication("")
        
    def close_main_window(self):
        self.signOut()
        self.destroy()

    def settings(self):
        is_signed = self.isSigned()
        if is_signed == 0:
            self.authentication("settings")
        else:
            self.isAdmin()

    def get_numberOf_available_rooms(self):
        mycursor = conn.mydb.cursor()
        mycursor.execute("SELECT room_id FROM rooms WHERE availability = 'Available'")
        res = mycursor.fetchall()
        return len(res)

    def get_numberOf_occupied_rooms(self):
        mycursor = conn.mydb.cursor()
        mycursor.execute("SELECT room_id FROM rooms WHERE availability = 'Checked In'")
        res = mycursor.fetchall()
        return len(res)

    def get_numberOf_reserved_rooms(self):
        mycursor = conn.mydb.cursor()
        mycursor.execute("SELECT room_id FROM rooms WHERE availability = 'Booked'")
        res = mycursor.fetchall()
        return len(res)
    
    def open_check_in_window(self):
        global CHECK_IN_WINDOW
        is_signed = self.isSigned()
        if is_signed == 0:
            self.authentication("check_in")
        else:
            if CHECK_IN_WINDOW is not True:
                CHECK_IN_WINDOW = True
                check_in = CheckIn(self)
                check_in.grab_set()
    
    def open_check_out_window(self):
        global CHECK_OUT_WINDOW
        is_signed = self.isSigned()
        if is_signed == 0:
            self.authentication("check_out")
        else:
            if CHECK_OUT_WINDOW is not True:
                CHECK_OUT_WINDOW = True
                check_out = CheckOut(self)
                check_out.grab_set()
    
    def open_cancellation_window(self):
        global CANCELLATION_WINDOW
        is_signed = self.isSigned()
        if is_signed == 0:

            self.authentication("cancel")
        else:
            if CANCELLATION_WINDOW is not True:
                CANCELLATION_WINDOW = True
                cancellation_window = BookCancellation(self)
                cancellation_window.grab_set()

    def open_guests_data_window(self):
        global GUESTS_WINDOW
        is_signed = self.isSigned()
        if is_signed == 0: 
            self.authentication("guests")
        else:
            if GUESTS_WINDOW is not True:
                GUESTS_WINDOW = True
                guest_data_window = GuestsData(self)
                guest_data_window.grab_set()

    def open_book_window(self):
        global BOOK_WINDOW
        is_signed = self.isSigned()
        if is_signed == 0: 
            self.authentication("book")
        else: 
            if BOOK_WINDOW is not True:
                BOOK_WINDOW = True
                book_window = Book(self)
                book_window.grab_set()

    def open_rooms_data_window(self):
        global ROOMS_WINDOW
        is_signed = self.isSigned()
        if is_signed == 0:
            self.authentication("rooms")
        else: 
            if ROOMS_WINDOW is not True:
                ROOMS_WINDOW = True
                show_rooms = ShowRooms(self)
                show_rooms.grab_set()

    def add_guest(self, name, contact, roomId, isbooked, checkInDate, _duration, ischeckedOut, payment_selected, paid_amount, checkoutdate):
        mycursor = conn.mydb.cursor()
        mycursor.execute(f"INSERT INTO guests (guest_name, contact_num, room_id, isbooked, check_in_date, duration, ischecked_out, selected_payment, amount_paid) VALUES ('{name}', '{contact}', '{roomId}', '{isbooked}', '{checkInDate}', '{_duration}', '{ischeckedOut}', '{payment_selected}', '{paid_amount}')")
        conn.mydb.commit()
        if isbooked == 'Booked':
            availability = 'Booked'
            _reserved =  self.hotels_reserved_rooms.get() + 1
            self.hotels_reserved_rooms.set(_reserved)
            _remaining_rooms = self.hotels_remaining_rooms.get() - 1
            self.hotels_remaining_rooms.set(_remaining_rooms)
            _available = self.hotels_remaining_rooms.get() / 60
            _convert_to_string = str(_available)
            _get_percentage = _convert_to_string[2:4]
            if len(_get_percentage) == 1:
                self.available.set(f" Available: {_get_percentage}0%")
            else:
                self.available.set(f" Available: {_get_percentage}%")
            self.reserved.set(f" Reserved: {self.hotels_reserved_rooms.get()}/{self.hotels_remaining_rooms.get() + self.hotels_reserved_rooms.get()}")
        elif isbooked == 'Checked In':
            availability = 'Checked In'
            _occupied =  self.hotels_occupied_rooms.get() + 1
            self.hotels_occupied_rooms.set(_occupied)
            _remaining_rooms = self.hotels_remaining_rooms.get() - 1
            self.hotels_remaining_rooms.set(_remaining_rooms)
            if self.hotels_remaining_rooms.get() == 60:
                self.available.set(" Available: 98%")
            else:
                _available = self.hotels_remaining_rooms.get() / 60
                _convert_to_string = str(_available)
                _get_percentage = _convert_to_string[2:4]
   
                if len(_get_percentage) == 1:
                    self.available.set(f" Available: {_get_percentage}0%")
                else:
                    self.available.set(f" Available: {_get_percentage}%")
            self.occupied.set(f" Occupied: {self.hotels_occupied_rooms.get()}")
            self.reserved.set(f" Reserved: {self.hotels_reserved_rooms.get()}/{self.hotels_remaining_rooms.get() + self.hotels_reserved_rooms.get()}")
        self.update_room_availability(roomId, checkInDate, checkoutdate, availability)
    
    def error(self, title, message):
        global ERROR_WINDOW
        if ERROR_WINDOW is not True:
            ERROR_WINDOW = True
            error_window = ErrorWindow(self, title, message)
            error_window.grab_set()

    def success(self, title, message):
        global SUCCESS_WINDOW
        if SUCCESS_WINDOW is not True:
            SUCCESS_WINDOW = True
            success_window = SuccessWindow(self, title, message)
            success_window.grab_set()

    def isAdmin(self):
        if self.current_user[3] == 'true':
            global SETTINGS_WINDOW
            if SETTINGS_WINDOW is not True:
                SETTINGS_WINDOW = True
                settings_window = SettingsWindow(self)
                settings_window.grab_set()
        else:
            title = 'An Error Occurred'
            message = ' Access Denied'
            self.error(title , message)

    def fetch_users(self):
        mycursor = conn.mydb.cursor()
        mycursor.execute('SELECT name, username, password, isadmin FROM user')
        res = mycursor.fetchall()
        return res

    def signed(self):
        mycursor = conn.mydb.cursor()
        sql = "UPDATE log SET islogged = 'true'"
        mycursor.execute(sql)
        conn.mydb.commit()

    def isSigned(self):
        mycursor = conn.mydb.cursor()
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

    def signOut(self):
        global ERROR_WINDOW
        ERROR_WINDOW = False
        mycursor = conn.mydb.cursor()
        sql = "UPDATE log SET islogged = 'false'"
        mycursor.execute(sql)
        conn.mydb.commit()

    def numOfUsers(self):
        mycursor = conn.mydb.cursor()
        mycursor.execute(f"SELECT username FROM user")
        res = mycursor.fetchall()
        count_users = []
        for x in res:
            count_users.append(x)
        return len(count_users)

    def update_room_availability(self, roomId, check_in_date, check_out_date, availability):
        mycursor = conn.mydb.cursor()
        mycursor.execute(f"UPDATE rooms SET check_in_date = '{check_in_date}', check_out_date = '{check_out_date}', availability = '{availability}' WHERE room_id = '{roomId}'")
        conn.mydb.commit()
        title = 'Success'
        message = ' {}'.format(availability)
        self.success(title, message)

    def update_guests(self, roomId, action):
        mycursor = conn.mydb.cursor()
        if action == 'checked-out':
            mycursor.execute(f"UPDATE guests SET ischecked_out = 'Yes' WHERE room_id = '{roomId}'")
            conn.mydb.commit()
            if mycursor.rowcount: #success
                title = 'Success'
                message = ' Check Out Success'
                self.success(title, message)

        elif action == 'cancelled':
            mycursor.execute(f"UPDATE guests SET ischecked_out = 'Cancelled', isbooked = 'Cancelled' WHERE room_id = '{roomId}'")
            conn.mydb.commit()

            if mycursor.rowcount: #success
                title = 'Success'
                message = ' Cancellation Success'
                self.success(title, message)

    def fetch_guests(self):
        mycursor = conn.mydb.cursor()
        mycursor.execute("SELECT * FROM guests ORDER BY check_in_date")
        res = mycursor.fetchall()
        return res

class DeleteUser(Toplevel):
    def __init__(self, parent, grandParent):
        super().__init__(parent)
        self.title('Delete User')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry(grandParent.windows_geometry(300, 120))
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.entered_username = StringVar()
        Label(self, text='Username:', font=('sans-serif', 11)).grid(column=1, row=0, sticky=W, pady=(15, 0), padx=5)
        Entry(self, width=30, font=('sans-serif', 9), textvariable=self.entered_username, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=1, sticky=W, padx=5, ipady=1)
        Button(self, text='Delete', fg='#fff', background='#242526', font=('sans-serif', 8), borderwidth=0, command=lambda:self.deleteUser(parent, grandParent)).grid(padx=5, sticky=W, column=1, row=2, ipadx=10, ipady=3, pady=(10, 5))

    def close_window(self):
        global DELETE_USER_WINDOW
        DELETE_USER_WINDOW = False
        self.destroy()

    def deleteUser(self, parent, grandParent):
        global DELETE_USER_WINDOW, SETTINGS_WINDOW
        username = self.entered_username.get()
        mycursor = conn.mydb.cursor()
        mycursor.execute(f"DELETE FROM user WHERE username = '{username}'")
        conn.mydb.commit()
        if mycursor.rowcount: 
            SETTINGS_WINDOW = False
            DELETE_USER_WINDOW = False
            parent.destroy()
            self.destroy()
            title = 'Success'
            message = ' User Deleted'
            grandParent.success(title, message)

        else: 
            DELETE_USER_WINDOW = False
            self.destroy()
            title = 'An Error Occurred'
            message = ' Username does not exist'
            grandParent.error(title, message)

class AddUser(Toplevel):
    def __init__(self, parent, grandParent):
        super().__init__(parent)
        self.name = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.admin = StringVar()
        self.title('Add User')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry(grandParent.windows_geometry(400, 270))
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.entries_frame = Frame(self)
        self.entries_frame.grid(column=0, row=0, sticky=S)

        self.labels = ['Name:', 'Username:', 'Password:']
        self.r = 0
        for x in self.labels:
            Label(self.entries_frame, text=x, font=('sans-serif', 11)).grid(column=0, row=self.r, pady=2, sticky=E, columnspan=2, padx=(30, 5))
            self.r += 1

        Entry(self.entries_frame, textvariable=self.name, width=30, font=('sans-serif', 9), highlightthickness=1, highlightbackground='#e0dada').grid(column=3, row=0, padx=(0, 30), pady=2, sticky=E)
        Entry(self.entries_frame, textvariable=self.username, width=30, font=('sans-serif', 9), highlightthickness=1, highlightbackground='#e0dada').grid(column=3, row=1, padx=(0, 30), pady=2, sticky=E)
        Entry(self.entries_frame, textvariable=self.password, width=30, font=('sans-serif', 9), highlightthickness=1, highlightbackground='#e0dada').grid(column=3, row=2, padx=(0, 30), pady=2, sticky=E)
        self.isadmin_checkbutton = Checkbutton(self.entries_frame, text='Admin', variable=self.admin, onvalue='true', offvalue='false', font=('sans-serif', 10))
        self.isadmin_checkbutton.grid(column=3, row=3, sticky=W, pady=3)
        self.isadmin_checkbutton.deselect()

        self.bottom_frame = Frame(self)
        self.bottom_frame.grid(column=0, row=1, sticky=NE)

        Button(self.bottom_frame, text='Add user', borderwidth=0, background='#242526', foreground='#fff', font=('sans-serif', 11), command=lambda:self.addUser(parent, grandParent)).pack(ipadx=120, ipady=5, pady=10)


    def addUser(self, parent, grandParent):
        if len(self.name.get()) != 0 and len(self.username.get()) != 0 and len(self.password.get()) != 0:
            global ADD_USER_WINDOW, SETTINGS_WINDOW
            if self.admin.get() == '':
                self.admin.set('true')
            mycursor = conn.mydb.cursor()
            mycursor.execute(f"INSERT INTO user (name, username, password, isadmin) VALUES ('{self.name.get()}', '{self.username.get()}', '{self.password.get()}', '{self.admin.get()}')")
            conn.mydb.commit()
            if mycursor.rowcount:
                ADD_USER_WINDOW = False
                SETTINGS_WINDOW = False
                self.destroy()
                parent.destroy()
                title = 'Success'
                message =' User Added'
                grandParent.success(title, message)


    def close_window(self):
        global ADD_USER_WINDOW
        ADD_USER_WINDOW = False
        self.destroy()

class SettingsWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.entered_username = StringVar()
        self.title('Manage Users')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry(parent.windows_geometry(600, 400))

        self.header_frame = Frame(self, highlightthickness=1, highlightbackground='gray')
        self.header_frame.pack(fill='x', side='top')
        banner = PhotoImage(file='./assets/settings_header_banner.png')
        Label(self.header_frame, image=banner).pack()
        self.main_frame = Frame(self)
        self.main_frame.pack(fill='y', side='left')
        self.res = parent.fetch_users()
        self.list = ['Name', 'Username', 'Password', 'Admin']
        for x in range(4):
            Label(self.main_frame, text=self.list[x], background='gray', fg='#fff', font=('sans-serif', 13)).grid(column=x, row=0, ipadx=45, ipady=5, pady=(0, 15))
        self.r = 1
        for x in self.res:
            for n in range(4):
                Label(self.main_frame, text=x[n], font=('sans-serif', 11), fg='#242526').grid(column=n, row=self.r, pady=(0, 5))
            self.r += 1
        Label(self.main_frame, text=(f'{self.r - 1} of 5'), font=('sans-serif', 12), fg='gray').grid(column=0, row=self.r, pady=(8, 0))

        self.delete_icon = PhotoImage(file='./assets/delete_user_icon.png')
        self.add_icon = PhotoImage(file='./assets/add_user_icon.png')
        Frame(self.main_frame, height=100, width=600, background='#fff').place(x=0, y=200)
        self.delete = Button(self.main_frame, image=self.delete_icon, compound=LEFT, text='Delete', borderwidth=0, font=('sans-serif', 11), background='#fff', command=lambda:self.delete_user(parent))
        self.delete.place(x=350, y=230)
        self.add = Button(self.main_frame, image=self.add_icon, compound=LEFT, text=' Add user', borderwidth=0, font=('sans-serif', 11), background='#fff', command=lambda:self.add_user(parent))
        self.add.place(x=200, y=230)

    def delete_user(self, parent):
        global DELETE_USER_WINDOW
        if DELETE_USER_WINDOW is not True:
            DELETE_USER_WINDOW = True
            delete_user_window = DeleteUser(self, parent)
            delete_user_window.grab_set()
                

    def add_user(self, parent):
        users = parent.numOfUsers()
        if (users < 5):
            global ADD_USER_WINDOW
            if ADD_USER_WINDOW is not True:
                ADD_USER_WINDOW = True
                add_user_window = AddUser(self, parent)
                add_user_window.grab_set()
            else: 
                title = 'An Error Occurred'
                message = ' User limit exceeded'
                parent.error(title, message)
 
    def close_window(self):
        global SETTINGS_WINDOW
        SETTINGS_WINDOW = False
        self.destroy()

class SuccessWindow(Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.title(title)
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.geometry(parent.windows_geometry(320, 90))
        self.success_icon = PhotoImage(file='./assets/success-icon.png')
        Label(self, image=self.success_icon, text=message, font=('sans-serif', 15), compound=LEFT).pack(fill='x', pady=21)


    def close_window(self):
        global SUCCESS_WINDOW
        SUCCESS_WINDOW = False
        self.destroy()

class ErrorWindow(Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.title(title)
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.geometry(parent.windows_geometry(320, 90))
        self.error_icon = PhotoImage(file='./assets/alert-icon-red.png')
        Label(self, image=self.error_icon, text=message, font=('sans-serif', 15), compound=LEFT).pack(fill='x', pady=17)

    def close_window(self):
        global ERROR_WINDOW
        ERROR_WINDOW = False
        self.destroy()
        
class CheckOut(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.entered_roomId = StringVar()
        self.title('Check Out')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry(parent.windows_geometry(300, 150))
        Label(self, text='Room ID:', font=('sans-serif', 11)).grid(column=0, row=0, pady=(60, 0), padx=(50, 0))
        Entry(self, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.entered_roomId).grid(column=1, row=0, pady=(60, 0))
        Button(self, text='Confirm', font=('sans-serif', 11, font.BOLD), background='#242526', fg='#fff', borderwidth=0, command=lambda:self.check_out_guest(parent)).grid(column=1, row=1, ipadx=10, ipady=1, sticky=W, pady=10)

    def close_window(self):
        global CHECK_OUT_WINDOW
        CHECK_OUT_WINDOW = False
        self.destroy()

    def check_out_guest(self, parent):
        global CHECK_OUT_WINDOW
        CHECK_OUT_WINDOW = False
        self.destroy()
        roomId = self.entered_roomId.get()
        mycursor = conn.mydb.cursor()
        mycursor.execute(f"UPDATE rooms SET availability = 'Available' WHERE room_id = '{roomId}' AND availability = 'Checked In'")
        conn.mydb.commit()
        if mycursor.rowcount:
            parent.hotels_remaining_rooms.set(parent.get_numberOf_available_rooms())
            parent.hotels_occupied_rooms.set(parent.get_numberOf_occupied_rooms())
            parent.hotels_reserved_rooms.set(parent.get_numberOf_reserved_rooms())
   
            if parent.hotels_remaining_rooms.get() == 60:
                parent.available.set(" Available: 100%")
                parent.capacity.set(" Capacity: 60")
                parent.occupied.set(" Occupied: 0")
                parent.reserved.set(" Reserved: 0/60")
            else:
             
                _available = (60 - (60 - parent.hotels_remaining_rooms.get())) / 60
                _convert_to_string = str(_available)
                _get_percentage = _convert_to_string[2:4]
                if len(_get_percentage) == 1:
                    parent.available.set(f" Available: {_get_percentage}0%")
                else:
                    parent.available.set(f" Available: {_get_percentage}%")
               
                parent.capacity.set(" Capacity: 60")
                parent.occupied.set(f" Occupied: {parent.hotels_occupied_rooms.get()}")
                parent.reserved.set(f" Reserved: {parent.hotels_reserved_rooms.get()}/{parent.hotels_remaining_rooms.get() + parent.hotels_reserved_rooms.get()}")
            self.update_guests(roomId, 'checked-out')

        else: 
            title = 'An Error Occurred'
            message = ' Room ID is not Occupied'
            parent.error(title, message)


class Login(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.username_value = StringVar()
        self.password_value = StringVar()
        self.title('Sign-in')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol("WM_DELETE_WINDOW", lambda:self.close_window(parent))
        self.geometry(parent.windows_geometry(450, 230))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.logo = PhotoImage(file='./assets/hotel_logo.png')
        Label(self, image=self.logo).grid(column=0, row=0, columnspan=2, pady=10)
        Label(self, text='Username:', font=('sans-serif', 10)).grid(column=0, row=1, sticky=E, pady=3)
        self.username_entry = Entry(self, width=35, font=('sans-serif', 9), textvariable=self.username_value, highlightthickness=1, highlightbackground='#e0dada')
        self.username_entry.grid(column=1, row=1, sticky=W, padx=5, pady=3)
        self.username_entry.focus()
        Label(self, text='Password:', font=('sans-serif', 10)).grid(column=0, row=2, sticky=E, pady=3)
        Entry(self, width=35, font=('sans-serif', 9), show='*', textvariable=self.password_value, highlightthickness=1, highlightbackground='#e0dada').grid(column=1, row=2, sticky=W, padx=5, pady=3)
        Button(self, text='Sign-in', fg='#242526', borderwidth=0, background='#242526', foreground='#fff', command= lambda:self.sign_in(parent)).grid(column=1, row=3, ipadx=10, ipady=5, sticky=W, pady=10, padx=5)

    def close_window(self, parent):
        global ERROR_WINDOW
        ERROR_WINDOW = True
        self.destroy()
        parent.destroy()

    def sign_in(self, parent):
        entered_username = self.username_value.get()
        entered_password = self.password_value.get()
        res = parent.fetch_users()
        for x in res:
            if x[1] == entered_username and x[2] == entered_password:
                if len(parent.current_user) != 0:
                    parent.current_user.clear()
                for c in range(4):
                    parent.current_user.append(x[c])
                parent.user_name.set('User: {}'.format(x[0]))
                isADMIN = 'Receptionist'
                if x[3] == 'true':
                    isADMIN = 'Admin'
                    parent.isadmin.set(' : ({})'.format(isADMIN))
                else:
                    parent.isadmin.set(' : ({})'.format(isADMIN))
                parent.signed()
                self.destroy()
                parent.deiconify()
                print('Logged in as {}'.format(isADMIN))
             
                if parent.action == 'settings':
                    parent.settings()
                elif parent.action =='book':
                    parent.open_book_window()
                elif parent.action == 'check_in':
                    parent.open_check_in_window()
                elif parent.action == 'check_out':
                    parent.open_check_out_window()
                elif parent.action == 'rooms':
                    parent.open_rooms_data_window()
                elif parent.action == 'guests':
                    parent.open_guests_data_window()
                elif parent.action == 'cancel':
                    parent.open_cancellation_window()
        

class ShowRooms(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.title('Rooms')
        self.resizable(False, False)
        self.geometry(parent.windows_geometry(750, 500))
        self.iconbitmap('./assets/hotel_icon.ico')
        self.wrapper = LabelFrame(self)
        self.canvas = Canvas(self.wrapper, width=750, height=450)
        self.frame = Frame(self.canvas)
        scrollbar = Scrollbar(self.wrapper, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.place(x=730, y=37, height=463)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e : self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.frame, anchor=NW)
        self.r = 0
        for x in self.fetch_rooms_data():
            Label(self.frame, text=x[0]).grid(column=0, row=self.r, ipadx=30, ipady=10)
            Label(self.frame, text=x[1]).grid(column=1, row=self.r, ipadx=20, ipady=10)
            Label(self.frame, text=x[2]).grid(column=2, row=self.r, ipadx=40, ipady=10)
            Label(self.frame, text=x[3]).grid(column=3, row=self.r, ipadx=35, ipady=10)
            Label(self.frame, text=x[4]).grid(column=4, row=self.r, ipadx=40, ipady=10)
            if x[5] == 'Checked In':
                Label(self.frame, text="Occupied").grid(column=5, row=self.r, ipadx=30, ipady=10)
            else:
                Label(self.frame, text=x[5]).grid(column=5, row=self.r, ipadx=30, ipady=10)
            self.r += 1

        self.headers = ['ID', 'Type', 'Capacity', 'Check-in Date', 'Check-out Date', 'Availability']
        Label(self, text=self.headers[0], background='gray', fg='#fff', width=13, height=2, font=('sans-serif', 10)).place(x=0, y=0)
        Label(self, text=self.headers[1], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=60, y=0)
        Label(self, text=self.headers[2], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=180, y=0)
        Label(self, text=self.headers[3], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=310, y=0)
        Label(self, text=self.headers[4], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=460, y=0)
        Label(self, text=self.headers[5], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=590, y=0)
        self.canvas.grid(column=0, row=0, pady=(40, 5))
        self.wrapper.pack()

    def fetch_rooms_data(self):
        mycursor = conn.mydb.cursor()
        mycursor.execute('SELECT room_id, type, capacity, check_in_date, check_out_date, availability FROM rooms')
        res = mycursor.fetchall()
        return res

    def close_window(self):
        global ROOMS_WINDOW
        ROOMS_WINDOW = False
        self.destroy()

class CheckIn(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Check in')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close_check_in_window)
        self.geometry(parent.windows_geometry(850, 450))
        self.left_frame = LabelFrame(self, borderwidth=0)
        self.right_frame = LabelFrame(self)
        self.firstname = StringVar()
        self.lastname = StringVar()
        self.address = StringVar()
        self.email_address = StringVar()
        self.contact_number = StringVar()
        self.available_rooms = []
        self.full_name = StringVar()
        self.guest_info_image = PhotoImage(file='./assets/guest_info.png')
        self.contact_details_image = PhotoImage(file='./assets/contact_details.png')
        Label(self.left_frame, image=self.guest_info_image).grid(column=0, row=0, columnspan=4, ipady=10)
        Label(self.left_frame, text='First name:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
        Entry(self.left_frame, width=15, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.firstname).grid(column=1, row=1, sticky=W)
        Label(self.left_frame, text='Last name:', font=('sans-serif', 11)).grid(column=2, row=1, sticky=E)
        Entry(self.left_frame, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.lastname).grid(column=3, row=1, sticky=W)
        Label(self.left_frame, text='Address:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
        Entry(self.left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.address).grid(column=1, row=2, columnspan=3, sticky=W)
        Label(self.left_frame, image=self.contact_details_image).grid(column=0, row=3, columnspan=4, ipady=5)
        Label(self.left_frame, text='Email Add:', font=('sans-serif', 11)).grid(column=0, row=4, sticky=E)
        Entry(self.left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.email_address).grid(column=1, row=4, columnspan=3, sticky=W)
        Label(self.left_frame, text='Contact #:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E)
        Entry(self.left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.contact_number).grid(column=1, row=5, columnspan=3, sticky=W)
        for widget in self.left_frame.winfo_children():
            widget.grid(padx=5, pady=5)
        self.left_frame.pack(fill=X, side=LEFT, ipady=50, ipadx=5, padx=(10, 0))
        Button(self.left_frame, text='CLEAR', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD), command=self.clear_fields).grid(ipadx=100, ipady=5, column=0, row=6, columnspan=4, pady=50)
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=2)
        self.room_data_image = PhotoImage(file='./assets/room_data.png')
        Label(self.right_frame, image=self.room_data_image).grid(column=0, row=0, columnspan=3, sticky=N, pady=(70, 10))
        Label(self.right_frame, text='Room type:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
        self.room_type_list = ['Standard', 'Economy', 'VIP']
        self.selected_type = StringVar()
        self.selected_bed_capacity = StringVar()
        self.price = IntVar()
        self.selected_type = StringVar()
        self.selected_bed_capacity = StringVar()
        self.price = IntVar()
        self.date = d.datetime.now()
        self.date_format= StringVar()
        self.x = self.date.strftime("%m/%d/%y")
        self.date_format.set(f"Format: {self.x}")
        self.check_in_date = StringVar()
        self.check_in_date.set(self.date.strftime("%m/%d/%y"))
        self.check_out_date = StringVar()
        self.duration = IntVar()
        self.duration.set(1)
        self.price.set(475)
        self.selected_type.set('Standard')
        self.dropdown_menu = OptionMenu(self.right_frame, self.selected_type, *self.room_type_list, command=lambda event:self.typeselected())
        self.dropdown_menu.grid(column=1, row=1, sticky=W, ipadx=10, pady=10)
        Label(self.right_frame, text='Capacity:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
        self.single_radiobutton = Radiobutton(self.right_frame, text='SINGLE', variable=self.selected_bed_capacity, command=lambda: self.single(), value='SINGLE')
        self.single_radiobutton.grid(column=1, row=3, sticky=W)
        self.single_radiobutton.select()
        self.double_radiobutton = Radiobutton(self.right_frame, text='DOUBLE', variable=self.selected_bed_capacity, command=lambda: self.double(), value='DOUBLE')
        self.double_radiobutton.grid(column=1, row=4, sticky=W)
        self.double_radiobutton.deselect()
        Label(self.right_frame, text='Price:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E, pady=10)
        Label(self.right_frame, textvariable=self.price, font=('sans-serif', 11)).grid(column=1, row=5, sticky=W, pady=10)
        Label(self.right_frame, textvariable=self.date_format, fg='gray').grid(column=1, row=6, sticky=W)
        Label(self.right_frame, text='Check out date:', font=('sans-serif', 11)).grid(column=0, row=7, sticky=E, pady=5)
        self.checkOutDate = Entry(self.right_frame, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.check_out_date)
        self.checkOutDate.grid(column=1, row=7, sticky=W, pady=5, padx=5)
        self.checkOutDate.bind('<KeyPress>', self.setPrice)
        self.checkOutDate.bind('<BackSpace>', self.setPrice2)
        self.right_frame.pack(fill=BOTH, side=RIGHT, expand=YES)
        self.check_in_button = Button(self.right_frame, text='CHECK IN', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD), command=lambda:self.get_room(parent))
        self.check_in_button.grid(ipadx=100, ipady=5, column=0, row=8, columnspan=2, pady=20)
    def clear_fields(self):
        self.firstname.set("")
        self.lastname.set("")
        self.address.set("")
        self.email_address.set("")
        self.contact_number.set("")
    def close_check_in_window(self):
        global CHECK_IN_WINDOW
        CHECK_IN_WINDOW = False
        self.destroy()
    def type_selected(self):
        type = self.selected_type.get()
        return type
    def typeselected(self):
        typeSelected = self.type_selected()
        if typeSelected == 'Standard':
            if self.selected_bed_capacity.get() == 'SINGLE':
                self.price.set(475)
            elif self.selected_bed_capacity.get() == 'DOUBLE':
                self.price.set(925)
        elif typeSelected == 'Economy':
            if self.selected_bed_capacity.get() == 'SINGLE':
                self.price.set(670)
            elif self.selected_bed_capacity.get() == 'DOUBLE':
                self.price.set(1180)
        elif typeSelected == 'VIP':
            if self.selected_bed_capacity.get() == 'SINGLE':
                self.price.set(3250)
            elif self.selected_bed_capacity.get() == 'DOUBLE':
                self.price.set(6000)
    def single(self):
        typeSelected = self.type_selected()
        if typeSelected == 'Standard':
            self.price.set(475)
        elif typeSelected == 'Economy':
            self.price.set(670)
        elif typeSelected == 'VIP':
            self.price.set(3250)
    def double(self):
        typeSelected = self.type_selected()
        if typeSelected == 'Standard':
            self.price.set(925)
        elif typeSelected == 'Economy':
            self.price.set(1180)
        elif typeSelected == 'VIP':
            self.price.set(6000)
    def setPrice(self, parent):
        global B2
        date1 = self.check_in_date.get()
        date2 = self.check_out_date.get()
        if len(date2) == 7 and B2 is not True:
            B2 = True
            self.dropdown_menu.configure(state='disabled')
            self.single_radiobutton.configure(state='disabled')
            self.double_radiobutton.configure(state='disabled')
            get_chosen_month1 = int(date1[0:2])
            get_chosen_month2 = int(date2[0:2])
            get_chosen_day1 = int(date1[3:5])
            get_chosen_day2 = int(date2[3:5])
            if get_chosen_day1 > 31 or get_chosen_day2 > 31:
                title = 'An Error Occurred'
                message = ' Invalid date'
                parent.error(title, message)
            elif (get_chosen_month1 == get_chosen_month2) and (not get_chosen_day1 > 31 or not get_chosen_day2 > 31):
                if get_chosen_day1 < get_chosen_day2:
                    self.duration.set(get_chosen_day2 - get_chosen_day1)
                    current_price = self.price.get()
                    set_price = current_price * self.duration.get()
                    if self.duration.get() != 0:
                        self.price.set(round(set_price))
                else:
                    title = 'An Error Occurred'
                    message = ' Invalid date'
                    parent.error(title, message)
            elif (get_chosen_month2 > get_chosen_month1) and (not get_chosen_day1 > 31 or not get_chosen_day2 > 31):
                difference = get_chosen_month2 - get_chosen_month1
                _days = 31
                for x in range(1, 10):
                    if difference == x:
                        res = _days - get_chosen_day1
                        res = get_chosen_day1 + res + get_chosen_day2
                        _duration = res - get_chosen_day1
                        self.duration.set(_duration)
                        current_price = self.price.get()
                        set_price = current_price * self.duration.get()
                        if self.duration.get() != 0:
                            self.price.set(round(set_price))
                    _days += 31
            print("Check in duration : {} days".format(self.duration.get()))
    def setPrice2(self, event):
        global B2
        _duration = self.duration.get()
        if B2 is not False:
            B2 = False
            if self.duration.get != 0:
                self.price.set(round(self.price.get() / _duration))
            self.duration.set(1)
    def get_room(self, parent):
        global GET_ROOM_WINDOW
        fname = self.firstname.get()
        lname = self.lastname.get()
        self.full_name.set(f'{fname} {lname}')
        
        if ((len(self.firstname.get()) and len(self.lastname.get()) and len(self.address.get()) and len(self.email_address.get()) and len(self.contact_number.get())) != 0) and (len(self.check_out_date.get()) == 8):
            if GET_ROOM_WINDOW is not True:
                GET_ROOM_WINDOW = True
                type = self.selected_type.get().upper()
                capacity = self.selected_bed_capacity.get().upper()
                mycursor = conn.mydb.cursor()
                mycursor.execute(f"SELECT room_id FROM rooms WHERE type = '{type}' AND capacity = '{capacity}' AND availability = 'available'")
                res = mycursor.fetchall()
                for x in res:
                    for y in x:
                        self.available_rooms.append(y)
                getRoom = GetRoom(self, parent, "Checked In")
                getRoom.grab_set()
class GetRoom(Toplevel):
    def __init__(self, parent, grandParent, action):
        super().__init__(parent)
        self.name = parent.full_name.get().upper()
        self.contact_num = parent.contact_number.get()
        self.isbooked = action
        self.checkInDate = parent.check_in_date.get()
        self._duration = str(parent.duration.get()) + " day(s)"
        self.isCheckedOut = 'No'
        self.selectedPayment = 'Full Payment'
        self.amountPaid = parent.price.get()
        self.checkoutdate = parent.check_out_date.get()
        self.title('Selected Room ID')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', lambda:self.close_window(parent, grandParent))
        self.geometry(grandParent.windows_geometry(300, 100))
        self._text = StringVar()
        self.random_room = None
        if not len(parent.available_rooms) == 0:
            _random = round(random.random() * len(parent.available_rooms))
            self.random_room = parent.available_rooms[_random - 1]
            self._text.set(f'ROOM ID: {self.random_room}')
            Label(self, textvariable=self._text, font=('sans-serif', 11, font.BOLD), fg='#242526').pack(fill=BOTH, expand=YES, side=TOP)
            Button(self, text='OK', font=('sans-serif', 11, font.BOLD), borderwidth=0 , fg='#fff', bg='#242526', command=lambda:self.addGuest(parent, grandParent)).pack(side=BOTTOM, ipadx=30, ipady=2, pady=10)
        else:
            self._text.set('No available rooms')
            Label(self, textvariable=self._text, font=('sans-serif', 11, font.BOLD), fg='#242526').pack(fill=BOTH, expand=YES, side=TOP)
    def addGuest(self, parent, grandParent):
        global GET_ROOM_WINDOW, CHECK_IN_WINDOW
        GET_ROOM_WINDOW = False
        CHECK_IN_WINDOW = False
        self.destroy()
        parent.destroy()
        grandParent.add_guest(self.name, self.contact_num, self.random_room, self.isbooked, self.checkInDate, self._duration, self.isCheckedOut, self.selectedPayment, self.amountPaid, self.checkoutdate)
    def close_window(self, parent, grandParent):
        global GET_ROOM_WINDOW
        GET_ROOM_WINDOW = False
        self.destroy()
        if self._text.get() == 'No available rooms':
            grandParent.open_rooms_data_window()

class Book(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.left_frame = LabelFrame(self, borderwidth=0)
        self.right_frame = LabelFrame(self)
        #variables
        self.firstname = StringVar()
        self.lastname = StringVar()
        self.address = StringVar()
        self.email_address = StringVar()
        self.contact_number = StringVar()
        self.full_name = StringVar()
        self.name = None
        self.contact_num = None
        self.isbooked = 'Booked'
        self.checkInDate = None
        self._duration = None
        self.isCheckedOut = 'No'
        self.selectedPayment = None
        self.amountPaid = None
        self.checkoutdate = None
        self.guest_info_image = PhotoImage(file='./assets/guest_info.png')
        self.contact_details_image = PhotoImage(file='./assets/contact_details.png')
        self.expected_date_image = PhotoImage(file='./assets/expected_date.png')
        self.title('Book')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry(parent.windows_geometry(850, 520))
        Label(self.left_frame, image=self.guest_info_image).grid(column=0, row=0, columnspan=4, ipady=(30))
        Label(self.left_frame, text='First name:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
        Entry(self.left_frame, width=15, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.firstname).grid(column=1, row=1, sticky=W)
        Label(self.left_frame, text='Last name:', font=('sans-serif', 11)).grid(column=2, row=1, sticky=E)
        Entry(self.left_frame, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.lastname).grid(column=3, row=1, sticky=W)
        Label(self.left_frame, text='Address:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
        Entry(self.left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.address).grid(column=1, row=2, columnspan=3, sticky=W)
        Label(self.left_frame, image=self.contact_details_image).grid(column=0, row=3, columnspan=4, ipady=(30))
        Label(self.left_frame, text='Email Add:', font=('sans-serif', 11)).grid(column=0, row=4, sticky=E)
        Entry(self.left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.email_address).grid(column=1, row=4, columnspan=3, sticky=W)
        Label(self.left_frame, text='Contact #:', font=('sans-serif', 11)).grid(column=0, row=5, sticky=E)
        Entry(self.left_frame, width=40, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.contact_number).grid(column=1, row=5, columnspan=3, sticky=W)
        for widget in self.left_frame.winfo_children():
            widget.grid(padx=5, pady=5)
        self.left_frame.pack(fill=X, side=LEFT, ipady=50, ipadx=5, padx=(10, 0))
        Button(self.left_frame, text='CLEAR', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD), command=self.clear_fields).grid(ipadx=100, ipady=5, column=0, row=6, columnspan=4, pady=50)
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=2)
        self.room_data_image = PhotoImage(file='./assets/room_data.png')
        self.payment_image = PhotoImage(file='./assets/payment.png')
        Label(self.right_frame, image=self.room_data_image).grid(column=0, row=0, columnspan=3, sticky=N)
        Label(self.right_frame, text='Room type:', font=('sans-serif', 11)).grid(column=0, row=1, sticky=E)
        self.room_type_list = ['Standard', 'Economy', 'VIP']
        self.selected_type = StringVar()
        self.selected_bed_capacity = StringVar()
        self.price = IntVar()
        self.selected_payment = StringVar()
        self.check_in_date = StringVar()
        self.check_out_date = StringVar()
        self.date_format= StringVar()
        self.duration = IntVar()
        self.available_rooms = []
        self.date = d.datetime.now()
        self.price.set(475)
        self.selected_type.set('Standard')
        self.duration.set(1)
        self.x = self.date.strftime("%m/%d/%y")
        self.date_format.set(f"Format: {self.x}")
        self.dropdown_menu = OptionMenu(self.right_frame, self.selected_type, *self.room_type_list, command=lambda event:self.typeselected())
        self.dropdown_menu.grid(column=1, row=1, sticky=W, ipadx=10, pady=0)
        Label(self.right_frame, text='Capacity:', font=('sans-serif', 11)).grid(column=0, row=2, sticky=E)
        self.single_radiobutton = Radiobutton(self.right_frame, text='SINGLE', variable=self.selected_bed_capacity, value='SINGLE', command=lambda: self.single())
        self.single_radiobutton.grid(column=1, row=3, sticky=W)
        self.single_radiobutton.select()
        self.double_radiobutton = Radiobutton(self.right_frame, text='DOUBLE', variable=self.selected_bed_capacity, value='DOUBLE', command=lambda: self.double())
        self.double_radiobutton.grid(column=1, row=4, sticky=W)
        self.double_radiobutton.deselect()
        Label(self.right_frame, image=self.payment_image).grid(column=0,row=5, columnspan=3, sticky=N, pady=(30, 0))
        Label(self.right_frame, text='Price:', font=('sans-serif', 11)).grid(column=0, row=6, sticky=E, pady=5)
        Label(self.right_frame, textvariable=self.price, font=('sans-serif', 11)).grid(column=1, row=6, sticky=W, pady=5)
        self.down_payment_radiobutton = Radiobutton(self.right_frame, text='Down payment', variable=self.selected_payment,  command=lambda :self.down_payment(), value='DOWN')
        self.down_payment_radiobutton.grid(column=1, row=7, sticky=W)
        self.down_payment_radiobutton.deselect()
        self.full_payment_radiobutton = Radiobutton(self.right_frame, text='Full payment', variable=self.selected_payment, command=lambda : self.full_payment(), value='FULL')
        self.full_payment_radiobutton.grid(column=1, row=8, sticky=W)
        self.full_payment_radiobutton.select()
        Label(self.right_frame, image=self.expected_date_image).grid(column=0, row=9, columnspan=3, sticky=N, pady=(10, 10))
        Label(self.right_frame, textvariable=self.date_format, fg='gray').grid(column=1, row=10, sticky=W, pady=2)
        Label(self.right_frame, text='Check-in date:', font=('sans-serif', 11)).grid(column=0, row=11, sticky=E, pady=3)
        Entry(self.right_frame, width=15, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.check_in_date, font=('sans-serif', 10)).grid(column=1, row=11, sticky=W, padx=5, pady=3)
        self.checkInDate = Label(self.right_frame, text='Check-out date:', font=('sans-serif', 11))
        self.checkInDate.grid(column=0, row=12, sticky=E, pady=3)
        self.checkInDate.bind('<KeyPress>', lambda :self.clear_date_entry2())
        self.checkOutDate = Entry(self.right_frame, width=15, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.check_out_date, font=('sans-serif', 10))
        self.checkOutDate.grid(column=1, row=12, sticky=W, padx=5, pady=3)
        self.checkOutDate.bind('<KeyPress>', self.setPrice)
        self.checkOutDate.bind('<BackSpace>', self.setPrice2)
        Button(self.right_frame, text='BOOK', borderwidth=0, background='#242526', fg='#fff', font=('sans-serif', 10, font.BOLD), command=lambda:self.get_room(parent)).grid(ipadx=100, ipady=5, column=0, row=13, columnspan=2, pady=(10, 15))
        self.right_frame.pack(fill=BOTH, side=RIGHT, expand=YES)
    def type_selected(self):
        type = self.selected_type.get()
        return type
    def typeselected(self):
        typeSelected = self.type_selected()
        if typeSelected == 'Standard':
            if self.selected_bed_capacity.get() == 'SINGLE' and self.selected_payment.get() == 'DOWN':
                self.price.set(round(475 * 0.30))
            elif self.selected_bed_capacity.get() == 'SINGLE' and self.selected_payment.get() == 'FULL':
                self.price.set(475)
            elif self.selected_bed_capacity.get() == 'DOUBLE' and self.selected_payment.get() == 'DOWN':
                self.price.set(round(925 * 0.30))
            elif self.selected_bed_capacity.get() == 'DOUBLE' and self.selected_payment.get() == 'FULL':
                self.price.set(925)
        elif typeSelected == 'Economy':
            if self.selected_bed_capacity.get() == 'SINGLE' and self.selected_payment.get() == 'DOWN':
                self.price.set(round(670 * 0.30))
            elif self.selected_bed_capacity.get() == 'SINGLE' and self.selected_payment.get() == 'FULL':
                self.price.set(670)
            elif self.selected_bed_capacity.get() == 'DOUBLE' and self.selected_payment.get() == 'DOWN':
                self.price.set(round(1180 * 0.30))
            elif self.selected_bed_capacity.get() == 'DOUBLE' and self.selected_payment.get() == 'FULL':
                self.price.set(1180)
        elif typeSelected == 'VIP':
            if self.selected_bed_capacity.get() == 'SINGLE' and self.selected_payment.get() == 'DOWN':
                self.price.set(round(3250 * 0.30))
            elif self.selected_bed_capacity.get() == 'SINGLE' and self.selected_payment.get() == 'FULL':
                self.price.set(3250)
            elif self.selected_bed_capacity.get() == 'DOUBLE' and self.selected_payment.get() == 'DOWN':
                self.price.set(round(6000 * 0.30))
            elif self.selected_bed_capacity.get() == 'DOUBLE' and self.selected_payment.get() == 'FULL':
                self.price.set(6000)
    def clear_fields(self):
        self.firstname.set("")
        self.lastname.set("")
        self.address.set("")
        self.email_address.set("")
        self.contact_number.set("")
    def close_window(self):
        global BOOK_WINDOW
        BOOK_WINDOW = False
        self.destroy()
    def single(self):
        typeSelected = self.type_selected()
        if typeSelected == 'Standard':
            if self.selected_payment.get() == 'DOWN':
                self.price.set(round(475 * 0.30))
            else:
                self.price.set(475)
        elif typeSelected == 'Economy':
            if self.selected_payment.get() == 'DOWN':
                self.price.set(round(670 * 0.30))
            else:
                self.price.set(670)
        elif typeSelected == 'VIP':
            if self.selected_payment.get() == 'DOWN':
                self.price.set(round(3250 * 0.30))
            else:
                self.price.set(3250)
    def double(self):
        typeSelected = self.type_selected()
        if typeSelected == 'Standard':
            if self.selected_payment.get() == 'DOWN':
                self.price.set(round(925 * 0.30))
            else:
                self.price.set(925)
        elif typeSelected == 'Economy':
            if self.selected_payment.get() == 'DOWN':
                self.price.set(round(1180 * 0.30))
            else:
                self.price.set(1180)
        elif typeSelected == 'VIP':
            if self.selected_payment.get() == 'DOWN':
                self.price.set(round(6000 * 0.30))
            else:
                self.price.set(6000)
    def down_payment(self):
        typeSelected = self.type_selected()
        if typeSelected == 'Standard':
            if self.selected_bed_capacity.get() == 'SINGLE':
                self.price.set(round(475 * 0.30))
            else:
                self.price.set(round(925 * 0.30))
        elif typeSelected == 'Economy':
            if self.selected_bed_capacity.get() == 'SINGLE':
                self.price.set(round(670 * 0.30))
            else:
                self.price.set(round(1180 * 0.30))
        elif typeSelected == 'VIP':
            if self.selected_bed_capacity.get() == 'SINGLE':
                self.price.set(round(3250 * 0.30))
            else:
                self.price.set(round(6000 * 0.30))
    def full_payment(self):
        typeSelected = self.type_selected()
        if typeSelected == 'Standard':
            if self.selected_bed_capacity.get() == 'DOUBLE':
                self.price.set(925)
            else:
                self.price.set(475)
        elif typeSelected == 'Economy':
            if self.selected_bed_capacity.get() == 'DOUBLE':
                self.price.set(1180)
            else:
                self.price.set(670)
        elif typeSelected == 'VIP':
            if self.selected_bed_capacity.get() == 'DOUBLE':
                self.price.set(6000)
            else:
                self.price.set(3250)
    def get_room(self, parent):
        global GET_ROOM_WINDOW
        def _selectedPayment():
            if self.selected_payment.get() == 'DOWN':
                return 'Down payment'
            elif self.selected_payment.get() == 'FULL':
                return 'Full payment'
        fname = self.firstname.get()
        lname = self.lastname.get()
        self.full_name.set(f'{fname} {lname}')
        self.name = self.full_name.get().upper()
        self.contact_num = self.contact_number.get()
        self.checkInDate = self.check_in_date.get()
        self._duration = str(self.duration.get()) + " day(s)"
        self.selectedPayment = _selectedPayment()
        self.amountPaid = self.price.get()
        self.checkoutdate = self.check_out_date.get()
        
        if ((len(self.firstname.get()) and len(self.lastname.get()) and len(self.address.get()) and len(self.email_address.get()) and len(self.contact_number.get())) != 0) and (len(self.check_out_date.get()) == 8 and len(self.check_in_date.get()) == 8):
            if GET_ROOM_WINDOW is not True:
                GET_ROOM_WINDOW = True
                type = self.selected_type.get().upper()
                capacity = self.selected_bed_capacity.get().upper()
                mycursor = conn.mydb.cursor()
                mycursor.execute(f"SELECT room_id FROM rooms WHERE type = '{type}' AND capacity = '{capacity}' AND availability = 'Available'")
                res = mycursor.fetchall()
                for x in res:
                    for y in x:
                        self.available_rooms.append(y)
                getRoom = GetRoom(self, parent, "Booked")
                getRoom.grab_set()
    def setPrice(self, parent):
        global B
        date1 = self.check_in_date.get()
        date2 = self.check_out_date.get()
        if len(date2) == 7 and B is not True:
            B = True
            self.dropdown_menu.configure(state='disabled')
            self.down_payment_radiobutton.configure(state='disabled')
            self.full_payment_radiobutton.configure(state='disabled')
            self.single_radiobutton.configure(state='disabled')
            self.double_radiobutton.configure(state='disabled')
            get_chosen_month1 = int(date1[0:2])
            get_chosen_month2 = int(date2[0:2])
            get_chosen_day1 = int(date1[3:5])
            get_chosen_day2 = int(date2[3:5])
            if get_chosen_day1 > 31 or get_chosen_day2 > 31:
                title = 'An Error Occurred'
                message = ' Invalid Date'
                parent.error(title, message)
            elif (get_chosen_month1 == get_chosen_month2) and (not get_chosen_day1 > 31 or not get_chosen_day2 > 31):
                if get_chosen_day1 < get_chosen_day2:
                    self.duration.set(get_chosen_day2 - get_chosen_day1)
                    current_price = self.price.get()
                    set_price = current_price * self.duration.get()
                    if self.duration.get() != 0:
                        self.price.set(round(set_price))
                else:
                    title = 'An Error Occurred'
                    message = ' Invalid date'
                    parent.error(title, message)
            elif (get_chosen_month2 > get_chosen_month1) and (not get_chosen_day1 > 31 or not get_chosen_day2 > 31):
                difference = get_chosen_month2 - get_chosen_month1
                _days = 31 
                for x in range(1, 10):
                    if difference == x:
                        res = _days - get_chosen_day1
                        res = get_chosen_day1 + res + get_chosen_day2
                        _duration = res - get_chosen_day1
                        #set duration
                        self.duration.set(_duration)
                        current_price = self.price.get()
                        set_price = current_price * self.duration.get()
                        if self.duration.get() != 0:
                            self.price.set(round(set_price))
                    _days += 31
            print("Booking duration : {} days".format(self.duration.get()))
    def setPrice2(self, event):
        global B
        _duration = self.duration.get()
        if B is not False:
            B = False
            if self.duration.get != 0:
                self.price.set(round(self.price.get() / _duration))
            self.duration.set(1)
    def clear_date_entry2(self):
        if len(self.check_out_date.get()) > 6:
            self.check_out_date.set()
class GuestsData(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Guests')
        self.resizable(False, False)
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry(parent.windows_geometry(975, 500))
        self.wrapper = LabelFrame(self)
        self.canvas = Canvas(self.wrapper, width=975, height=450)
        self.frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.wrapper, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(x=948, y=36, height=460)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e : self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.frame, anchor=NW)
        self.res = parent.fetch_guests()
        self.r = 0
        for x in self.res:
            if len(x[1]) > 12:
                name = str(x[1])
                _sliced_name = name[0:11] + ".."
                Label(self.frame, text=_sliced_name, font=('sans-serif', 9), width=15).grid(column=0, row=self.r, ipady=5)
            else:
                Label(self.frame, text=x[1], font=('sans-serif', 9), width=15).grid(column=0, row=self.r, ipady=5)
            Label(self.frame, text=x[2], font=('sans-serif', 9), width=15).grid(column=1, row=self.r, ipady=5)
            Label(self.frame, text=x[3], font=('sans-serif', 9), width=12).grid(column=2, row=self.r, ipady=5)
            Label(self.frame, text=x[4], font=('sans-serif', 9), width=13).grid(column=3, row=self.r, ipady=5)
            Label(self.frame, text=x[5], font=('sans-serif', 9), width=15).grid(column=4, row=self.r, ipady=5)
            Label(self.frame, text=x[6], font=('sans-serif', 9), width=10).grid(column=5, row=self.r, ipady=5)
            Label(self.frame, text=x[7], font=('sans-serif', 9), width=15).grid(column=6, row=self.r, ipady=5)
            Label(self.frame, text=x[8], font=('sans-serif', 9), width=20).grid(column=7, row=self.r, ipady=5)
            Label(self.frame, text=x[9], font=('sans-serif', 9), width=15).grid(column=8, row=self.r, ipady=5)
            self.r += 1
        self.header = ['Guest Name', 'Contact #', 'Room ID', 'isBooked', 'Check-In Date', 'Duration', 'isChecked-Out', 'Selected Payment', 'Amount Paid']
        Label(self, text=self.header[0], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=0, y=0)
        Label(self, text=self.header[1], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=110, y=0)
        Label(self, text=self.header[2], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=210, y=0)
        Label(self, text=self.header[3], background='gray', fg='#fff', width=10, height=2, font=('sans-serif', 10)).place(x=320, y=0)
        Label(self, text=self.header[4], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=400, y=0)
        Label(self, text=self.header[5], background='gray', fg='#fff', width=10, height=2, font=('sans-serif', 10)).place(x=520, y=0)
        Label(self, text=self.header[6], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=590, y=0)
        Label(self, text=self.header[7], background='gray', fg='#fff', width=20, height=2, font=('sans-serif', 10)).place(x=705, y=0)
        Label(self, text=self.header[8], background='gray', fg='#fff', width=15, height=2, font=('sans-serif', 10)).place(x=850, y=0)
        self.canvas.grid(column=0, row=0, pady=(40, 5))
        self.wrapper.pack()
    def close_window(self):
        global GUESTS_WINDOW
        GUESTS_WINDOW = False
        self.destroy()
class BookCancellation(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Book Cancellation')
        self.resizable(False, False)
        self.entered_roomId = StringVar()
        self.iconbitmap('./assets/hotel_icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry(parent.windows_geometry(300, 150))
        Label(self, text='Room ID:', font=('sans-serif', 11)).grid(column=0, row=0, pady=(60, 0), padx=(50, 0))
        Entry(self, width=20, highlightthickness=1, highlightbackground='#e0dada', textvariable=self.entered_roomId).grid(column=1, row=0, pady=(60, 0))
        Button(self, text='Confirm', font=('sans-serif', 11, font.BOLD), background='#242526', fg='#fff', borderwidth=0, command=lambda:self.cancellation(parent)).grid(column=1, row=1, ipadx=10, ipady=1, sticky=W, pady=10)
    def close_window(self):
        global CANCELLATION_WINDOW
        CANCELLATION_WINDOW = False
        self.destroy()
    def cancellation(self, parent):
        global CANCELLATION_WINDOW
        CANCELLATION_WINDOW = False
        self.destroy()
        roomId = self.entered_roomId.get()
        mycursor = conn.mydb.cursor()
        mycursor.execute(f"UPDATE rooms SET availability = 'Available' WHERE room_id = '{roomId}' AND availability = 'Booked'")
        conn.mydb.commit()
        if mycursor.rowcount:
            parent.hotels_remaining_rooms.set(parent.get_numberOf_available_rooms())
            parent.hotels_occupied_rooms.set(parent.get_numberOf_occupied_rooms())
            parent.hotels_reserved_rooms.set(parent.get_numberOf_reserved_rooms())
            if parent.hotels_remaining_rooms.get() == 60:
                parent.available.set(" Available: 100%")
                parent.capacity.set(" Capacity: 60")
                parent.occupied.set(" Occupied: 0")
                parent.reserved.set(" Reserved: 0/60")
            else:
                _available = (60 - (60 - parent.hotels_remaining_rooms.get())) / 60
                _convert_to_string = str(_available)
                _get_percentage = _convert_to_string[2:4]
                if len(_get_percentage) == 1:
                    parent.available.set(f" Available: {_get_percentage}0%")
                else:
                    parent.available.set(f" Available: {_get_percentage}%")
                parent.capacity.set(" Capacity: 60")
                parent.occupied.set(f" Occupied: {parent.hotels_occupied_rooms.get()}")
                parent.reserved.set(f" Reserved: {parent.hotels_reserved_rooms.get()}/{parent.hotels_remaining_rooms.get() + parent.hotels_reserved_rooms.get()}")
            parent.update_guests(roomId, 'cancelled')
        else:
            title = 'An Error Occurred'
            message = ' Room ID is available'
            parent.error(title, message)

if __name__ == "__main__":
    app = HotelReservation()
    app.mainloop()

