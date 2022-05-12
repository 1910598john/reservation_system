from tkinter import *

root = Tk()

def test(event):
    x = event.x_root - f.winfo_rootx()
    y = event.y_root - f.winfo_rooty()
 
    # Here grid_location() method is used to
    # retrieve the relative position on the
    # parent widget
    z = f.grid_location(x, y)
 
    # printing position
    print(z)
    
f = Frame(root)
f.pack()
f.columnconfigure(0, weight=1)
button = Button(f, text='Click me')
button.grid(column=1, row=0)
button.bind('<Button-1>', test)

root.mainloop()