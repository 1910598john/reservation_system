from tkinter import *

root = Tk()
testvar = StringVar()
testvar.set('Yawa ka lds')
def test(event):
    x = event.x_root - f.winfo_rootx()
    y = event.y_root - f.winfo_rooty()
 
    # Here grid_location() method is used to
    # retrieve the relative position on the
    # parent widget
    z = f.grid_info(x, y)
    
    print(z)
        
    
f = Frame(root)
f.pack()
f.columnconfigure(0, weight=1)
button = Button(f, text='Click me')

Label(f, textvariable=testvar).grid(column=0, row=0)
button.grid(column=3, row=0)
button.bind('<Button-1>', test)

root.mainloop()