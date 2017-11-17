from Tkinter import *
import tkFileDialog
import tkMessageBox
from tkColorChooser import askcolor
import datetime
import webbrowser
from tkFileDialog import askopenfilename, asksaveasfilename
from textgenrnn import textgenrnn

"""I should definitely make this into a class...."""


class Writrz_Blk(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Writrz-Blk")

        

        self.text = Text(self.root, height=30, width=60, font = ("Arial", 10))
        self.text_suggestion = Text(self.root, height=30, width=30, font = ("Arial", 10))

        self.generate_text = Button(self.root, text="Generate Text", command=self.gen)
        self.generate_text.grid(row=0, column=0)

        self.w = Label(self.root, text="Suggested Text", anchor=E, justify=LEFT)
        self.w.grid(row=0, column=1)

        self.text_suggestion.grid(row=1,column=1)

        self.text.focus_set()
        self.text.grid(row=1,column=0)
        

        self.build_menu()
        self.root.resizable(0,0)
        self.root.mainloop()

    def build_menu(self):
        menu = Menu(self.root)
        filemenu = Menu(self.root)
        self.root.config(menu = menu)
        menu.add_cascade(label="File", menu=filemenu)
        self.text.bind('<Command-KeyRelease-a>', self.select_all)

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
        insmenu.add_command(label="Line",command=self.line)
        insmenu.add_command(label = "Generate Text", command = self.gen)

        formatmenu = Menu(menu)

        menu.add_cascade(label="Format",menu = formatmenu)
        formatmenu.add_cascade(label="Font Color", command = self.font)
        formatmenu.add_separator()
        formatmenu.add_radiobutton(label='Normal',command=self.normal)
        formatmenu.add_radiobutton(label='Bold',command=self.bold)
        formatmenu.add_radiobutton(label='Underline',command=self.underline)
        formatmenu.add_radiobutton(label='Italic',command=self.italic)

    def line(self):
        lin = "_" * 60
        self.text.insert(INSERT,lin)

    def gen(self):
        textgen = textgenrnn()
        a = textgen.generate(return_as_list=True)
        self.text.insert(INSERT,"".join(a))

    def date(self):
        data = datetime.date.today()
        self.text.insert(INSERT,data)

    def normal(self):
        self.text.config(font = ("Arial", 10))

    def bold(self):
        self.text.config(font = ("Arial", 10, "bold"))

    def underline(self):
        self.text.config(font = ("Arial", 10, "underline"))

    def italic(self):
        self.text.config(font = ("Arial",10,"italic"))

    def font(self):
        (triple,color) = askcolor()
        if color:
           self.text.config(foreground=color)

    def kill(self):
        self.root.destroy()

    def select_all(self,event):
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(INSERT, END)


    def opn(self):
        self.text.delete(1.0 , END)
        file = open(askopenfilename() , 'r')
        if file != '':
            txt = file.read()
            self.text.insert(INSERT,txt)
        else:
            pass    

    def save(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.text.get(1.0, END)                      
            open(filename, 'w').write(alltext) 

    def copy(self):
        self.text.clipboard_clear()
        self.text.clipboard_append(text.selection_get()) 


    def paste(self):
        try:
            teext = self.text.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, teext)
        except:
            tkMessageBox.showerror("Error","Could not paste")

    def clear(self):
        sel = self.text.get(SEL_FIRST, SEL_LAST)
        self.text.delete(SEL_FIRST, SEL_LAST)

    def clearall(self):
        self.text.delete(1.0 , END)

    def background():
        (triple,color) = askcolor()
        if color:
           self.text.config(background=color)

if __name__ == "__main__":
    w = Writrz_Blk()