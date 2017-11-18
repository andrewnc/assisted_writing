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
        self.suggestion = Listbox(self.root, height=30, width=30)

        self.generate_text = Button(self.root, text="Generate Text", command=self.gen)
        self.generate_text.grid(row=0, column=0)

        # self.w = Label(self.root, text="Suggested Text", anchor=E, justify=LEFT)
        # self.w.grid(row=0, column=1)

        self.suggestion.grid(row=1,column=1, padx=10, pady=10)

        self.text.focus_set()
        self.text.grid(row=1,column=0, padx=10)

        self.selectButton = Button(self.root, text='Select', command=self.selection)
        self.selectButton.grid(row=0, column=1)


        self.suggestion.bind('<Double-1>', lambda x: self.selectButton.invoke())
        

        self.build_menu()
        self.root.resizable(0,0)
        self.root.mainloop()

    
    def line(self):
        lin = "_" * 60
        self.text.insert(INSERT,lin)

    def gen(self):
        textgen = textgenrnn()
        a = textgen.generate(return_as_list=True)[0].split()

        #get several different suggestions
        b = a[0]
        c = a[0:4]
        d = a[5:10]
        self.suggestion.insert(END,"".join(b).lower())
        self.suggestion.insert(END," ".join(c).lower())
        self.suggestion.insert(END," ".join(d).lower())

    def selection(self):
        current_text = self.text.get("1.0", END)

        #get the selected piece of text from the box
        to_insert = self.suggestion.selection_get()

        if len(current_text) < 2:
            self.text.insert(END, to_insert)
        # the last char is always a new line it seems
        elif current_text[-2] == ' ':
            self.text.insert(END,to_insert)
        else:
            self.text.insert(END, " "+to_insert)

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


if __name__ == "__main__":
    w = Writrz_Blk()