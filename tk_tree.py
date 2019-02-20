import tkinter
from tkinter import ttk


class TK_Tree():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.minsize(200, 200)

        frame = tkinter.Frame(self.root)
        frame.grid(row=0, column=0, sticky=tkinter.W+tkinter.E+tkinter.S+tkinter.N)

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)



        self.tree = ttk.Treeview(frame)
        self.tree.grid(row=0, column=0, sticky=tkinter.W+tkinter.E+tkinter.S+tkinter.N)

        self.tree["columns"] = ( "one", "two")
        self.tree.column("#0", minwidth=300)
        self.tree.column("one", width=10)
        self.tree.column("two", minwidth=10000, stretch=True)
        self.tree.heading("#0", text="Topic")
        self.tree.heading("one", text="QOS")
        self.tree.heading("two", text="Payload")

        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        ysb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscroll=ysb.set)
        xsb = ttk.Scrollbar(frame, orient=tkinter.HORIZONTAL, command=self.tree.xview)
        xsb.grid(row=1, column=0, sticky='we')
        self.tree.configure(xscroll=xsb.set)

        btn_frame = tkinter.Frame(self.root)
        btn_frame.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)
        self.button = tkinter.Button(btn_frame,
                                     text="QUIT", fg="red",
                                     command=frame.quit)
        self.button.pack(side=tkinter.LEFT)
        self.slogan = tkinter.Button(btn_frame,
                                     text="Hello",
                                     command=self.write_slogan)
        self.slogan.pack(side=tkinter.LEFT)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def tree_insert(self, parent, index, iid, text, values=None):
        if values:
            return self.tree.insert(parent, index, iid, text=text, values=values)
        else:
            return self.tree.insert(parent, index, iid, text=text)

    def item_update(self, iid, values):
        self.tree.item(iid, values=values)

    def write_slogan(self):
        print("Tkinter is easy to use!")

    def run(self):
        self.root.mainloop()
