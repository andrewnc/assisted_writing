from Tkinter import *
import tkFileDialog
import tkMessageBox
from tkColorChooser import askcolor
import datetime
import webbrowser
from tkFileDialog import askopenfilename, asksaveasfilename
from textgenrnn import textgenrnn

"""I should definitely make this into a class...."""


class Writrz-Blk(object):
    def __init__(self):
        self.root = root = Tk()
        root.title("Writrz-Blk")

        build_menu()

        self.text = Text(self.root, height=30, width=60, font = ("Arial", 10))
        self.text_suggestion = Text(self.root, height=30, width=30, font = ("Arial", 10))

        self.generate_text = Button(self.root, text="Generate Text", command=self.gen)
        self.generate_text.grid(row=0, column=0)

        self.w = Label(self.root, text="Suggested Text", anchor=E, justify=LEFT)
        self.w.grid(row=0, column=1)

        self.text_suggestion.grid(row=1,column=1)

        self.text.focus_set()
        self.text.grid(row=1,column=0)
        self.text.bind('<Command-KeyRelease-a>', self.select_all)

        self.root.resizable(0,0)
        self.root.mainloop()

    def build_menu():
        menu = Menu(self.root)
        filemenu = Menu(self.root)
        root.config(menu = menu)
        menu.add_cascade(label="File", menu=filemenu)

        # Add command to file menu
        filemenu.add_command(label="Open", command=self.opn)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.kill)

        modmenu = Menu(self.root)
        menu.add_cascade(label="Edit",menu = modmenu)

        #Add commands to Edit menu
        modmenu.add_command(label="Copy", command = self.copy)
        modmenu.add_command(label="Paste", command=self.paste)
        modmenu.add_separator()
        modmenu.add_command(label = "Clear Selection", command = self.clear)
        modmenu.add_command(label = "Clear All", command = self.clearall)

        insmenu = Menu(self.root)

        menu.add_cascade(label="Insert",menu= insmenu)
        insmenu.add_command(label="Date",command=self.date)
        insmenu.add_command(label="Line",command=line)
        insmenu.add_command(label = "Generate Text", command = gen)

        formatmenu = Menu(self.menu)

        menu.add_cascade(label="Format",menu = formatmenu)
        formatmenu.add_cascade(label="Font Color", command = font)
        formatmenu.add_separator()
        formatmenu.add_radiobutton(label='Normal',command=normal)
        formatmenu.add_radiobutton(label='Bold',command=bold)
        formatmenu.add_radiobutton(label='Underline',command=underline)
        formatmenu.add_radiobutton(label='Italic',command=italic)

    def line():
        lin = "_" * 60
        text.insert(INSERT,lin)

    def gen():
        textgen = textgenrnn()
        a = textgen.generate(return_as_list=True)
        text.insert(INSERT,"".join(a))

    def date():
        data = datetime.date.today()
        text.insert(INSERT,data)

    def normal():
        text.config(font = ("Arial", 10))

    def bold():
        text.config(font = ("Arial", 10, "bold"))

    def underline():
        text.config(font = ("Arial", 10, "underline"))

    def italic():
        text.config(font = ("Arial",10,"italic"))

    def font():
        (triple,color) = askcolor()
        if color:
           text.config(foreground=color)

    def kill():
        root.destroy()

    def select_all(event):
        text.tag_add(SEL, "1.0", END)
        text.mark_set(INSERT, END)


    def opn():
        text.delete(1.0 , END)
        file = open(askopenfilename() , 'r')
        if file != '':
            txt = file.read()
            text.insert(INSERT,txt)
        else:
            pass    

    def save():
        filename = asksaveasfilename()
        if filename:
            alltext = text.get(1.0, END)                      
            open(filename, 'w').write(alltext) 

    def copy():
        text.clipboard_clear()
        text.clipboard_append(text.selection_get()) 


    def paste():
        try:
            teext = text.selection_get(selection='CLIPBOARD')
            text.insert(INSERT, teext)
        except:
            tkMessageBox.showerror("Error","Could not paste")

    def clear():
        sel = text.get(SEL_FIRST, SEL_LAST)
        text.delete(SEL_FIRST, SEL_LAST)

    def clearall():
        text.delete(1.0 , END)

    def background():
        (triple,color) = askcolor()
        if color:
           text.config(background=color)

