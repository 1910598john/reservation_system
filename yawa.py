import tkinter
  
# Create the default window
root = tkinter.Tk()
root.title("Welcome to GeeksForGeeks")
root.geometry('700x500')
  
# Create the list of options
options_list = ["Standard", "Economy", "VIP"]
  
# Variable to keep track of the option
# selected in OptionMenu
value_inside = tkinter.StringVar(root)
  
# Set the default value of the variable
value_inside.set("Standard")
  
# Create the optionmenu widget and passing 
# the options_list and value_inside to it.
question_menu = tkinter.OptionMenu(root, value_inside, *options_list)
question_menu.pack()
  
# Function to print the submitted option-- testing purpose
  
  
def print_answers():
    print("Selected Option: {}".format(value_inside.get()))
    return None
  
  
# Submit button
# Whenever we click the submit button, our submitted
# option is printed ---Testing purpose
submit_button = tkinter.Button(root, text='Submit', command=print_answers)
submit_button.pack()
  
root.mainloop()