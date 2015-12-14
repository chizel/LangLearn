#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *


# Create a button with a custommy_callback
def my_callback():
    print("The button was clicked!")  # Prints to console not the GUI


def add_words():
    print('In progress.')


def my_prog():
    root = Tk()
    # icon
    root.iconphoto(root, PhotoImage(file='./1.png')) 
    # title
    root.title('English quizes')

    # main menu
    #main_menu = Menu(root, tearoff=0)
    #main_menu.add_command(label="Quit", command=root.destroy)
    root.config(menu=main_menu)
    # create a menu
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=my_callback)
    filemenu.add_command(label="Add words from file", command=add_words)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.destroy)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=my_callback)

    # create a toolbar
    toolbar = Frame(root)

    b = Button(toolbar, text="new", width=6, command=my_callback)
    b.pack(side=LEFT, padx=2, pady=2)

    b = Button(toolbar, text="open", width=6, commandmy_callback)
    b.pack(side=LEFT, padx=2, pady=2)

    toolbar.pack(side=TOP, fill=X)
    mainloop()
#    def key(event):
        #print("pressed", repr(event.char))

    #def my_callback(event):
        #frame.focus_set()
        #print("clicked at", event.x, event.y)

    #frame = Frame(root, width=100, height=100)
    #frame.bind("<Key>", key)
    #frame.bind("<Button-1>",my_callback)
#    frame.pack()

    # Fullscreen
    #root.attributes('-fullscreen', True)

    #screen_width = root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()

    # Make window 300x150 and place at position (50,50)
    #root.geometry("500x350+400+300")


    #msg = Message(root, text='Hello, world!')

    # Font is a tuple of (font_family, size_in_points, style_modifier_string)
    #msg.config(font=('times', 48, 'italic bold underline'))
    #msg.pack()

    # Just text
    #my_text = Label(root, text='Hello, world!')
    #my_text.pack()

    # Create a button that will destroy the main window when clicked
    #exit_button = Button(root, text='Exit Program', command=root.destroy)
    #exit_button.pack()
    #print_button = Button(root, text='Click me!', command=my_callback)
    #print_button.pack()

    root.mainloop()
    return


def main():
    return


if __name__ == "__main__":
    main()
