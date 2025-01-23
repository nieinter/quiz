import ttkbootstrap as ttk
from random import randint
from tkinter import END
from tkinter import messagebox
import numpy as np
from tkinter.filedialog import askopenfilename
from ttkbootstrap import Style
from os import getcwd

from PIL import Image

Image.CUBIC = Image.BICUBIC


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.minsize(1500, 1000)
        self.title("Quiz")
        self.__lista_e = np.array([])
        self.__lista_p = np.array([])
        self.__random_pick = 0
        self.__progress = 0
        self.theme_reader()
        self.state('zoomed')

        style_b = Style()
        style_b.configure("Custom.TButton", font=(None, 12))

        button_choose = ttk.Button(self,
                                   text="➕",
                                   width=3,
                                   style="Custom.TButton",
                                   command=self.choose
                                   )

        button_swap = ttk.Button(self,
                                 text="⇆",
                                 width=3,
                                 style="Custom.TButton",
                                 command=self.swap
                                 )

        label_theme = ttk.Label(self,
                                text="Motyw:"
                                )

        self.__combobox_theme = ttk.Combobox(self,
                                             values=list(self.style.theme_names()),
                                             state="readonly"
                                             )
        self.__combobox_theme.current(self.cur_theme())

        self.__label_q = ttk.Label(self,
                                   text="Wybierz plik z rozszerzeniem\ntxt aby zacząć.",
                                   font=(None, 40),
                                   )

        self.__entry_e = ttk.Entry(self,
                                   width=16,
                                   font=(None, 30),
                                   state="disabled"
                                   )

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 12))

        self.__treeview = ttk.Treeview(self,
                                       columns=("W1", "D", "W2"),
                                       show="headings")
        self.__treeview.heading("W1", text="Zaliczone słówka:", anchor="w")
        self.__treeview.heading("D", text="", anchor="w")
        self.__treeview.heading("W2", text="", anchor="w")
        self.__treeview.column("W1", anchor="center", width=100)
        self.__treeview.column("D", anchor="center", width=10)
        self.__treeview.column("W2", anchor="center", width=100)

        self.__progress_bar = ttk.Meter(self,
                                        interactive=False,
                                        textright="/-",
                                        metertype="semi",
                                        meterthickness=50,
                                        arcoffset=90,
                                        arcrange=270,
                                        metersize=200
                                        )

        self.__entry_e.bind("<Return>", self.check)
        self.__entry_e.bind("<KeyPress>", self.grow)
        self.__combobox_theme.bind("<<ComboboxSelected>>", self.theme_selector)

        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        self.columnconfigure(2, weight=16, uniform="a")
        self.columnconfigure(3, weight=6, uniform="a")

        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=5, uniform="a")
        self.rowconfigure(2, weight=5, uniform="a")
        self.rowconfigure(3, weight=5, uniform="a")

        button_choose.grid(row=0, column=0, sticky="nw", padx=10, pady=10, ipadx=10, ipady=10)
        button_swap.grid(row=0, column=1, sticky="nw", padx=10, pady=10, ipadx=10, ipady=10)
        label_theme.grid(row=3, column=0, sticky="sw", pady=10)
        self.__combobox_theme.grid(row=4, column=0)
        self.__label_q.grid(row=1, column=2, sticky="s")
        self.__entry_e.grid(row=3, column=2, sticky="n")
        self.__treeview.grid(row=0, column=3, rowspan=3, sticky="news")
        self.__progress_bar.grid(row=3, column=3, sticky="news", pady=20)

    def cur_theme(self) -> int:
        theme_name = self.style.theme_use()
        return list(self.style.theme_names()).index(theme_name)

    def theme_reader(self) -> None:
        try:
            path = getcwd() + "\\theme.txt"
            with open(path, "r") as f:
                theme = str(f.readline()).strip()
                self.style.theme_use(theme)
        except FileNotFoundError:
            self.style.theme_use("superhero")

    def theme_selector(self, *args, **kwargs) -> None:
        theme_selected = str(self.__combobox_theme.get())
        self.style.theme_use(theme_selected)
        with open("theme.txt", "w") as f:
            f.write(theme_selected)

    def grow(self, *args, **kwargs) -> None:
        length = len(self.__entry_e.get())
        if length <= 15:
            self.__entry_e.configure(width=16)
        elif 30 > length > 16:
            self.__entry_e.configure(width=len(self.__entry_e.get()))

    def choose(self, *args, **kwargs) -> None:
        try:
            with open(self.open(), encoding="UTF-8") as f:
                lines = f.readlines()
            self.__lista_e = np.array([])
            self.__lista_p = np.array([])
            self.__random_pick = 0
            self.__progress = 0
            self.__progress_bar.configure(amountused=self.__progress)
            self.__label_q.configure(text="")
            try:
                for row in self.__treeview.get_children():
                    self.__treeview.delete(row)
            except:
                pass

            lines_s = np.array([])

            for i in lines:
                if i.strip():
                    lines_s = np.append(lines_s, i)

            for i, w in enumerate(lines_s):
                if i % 2 == 0:
                    self.__lista_e = np.append(self.__lista_e,
                                               w.strip().replace(" / ", "/").replace("/ ", "/").replace(" /", "/"))
                else:
                    self.__lista_p = np.append(self.__lista_p,
                                               w.strip().replace(" / ", "/").replace("/ ", "/").replace(" /", "/"))

            self.__progress_bar.configure(amounttotal=len(self.__lista_e), textright=f"/{len(self.__lista_e)}")
            self.__entry_e.configure(state="active")
            self.los()

        except TypeError:
            pass

    def swap(self, *args, **kwargs) -> None:
        if self.__lista_e.size != 0 and self.__lista_p.size != 0:
            self.__lista_p, self.__lista_e = self.__lista_e, self.__lista_p
            try:
                for row in self.__treeview.get_children():
                    self.__treeview.delete(row)
            except:
                pass
            self.__random_pick = 0
            self.__progress = 0
            self.__progress_bar.configure(amountused=self.__progress)
            self.los()

    @staticmethod
    def open() -> str:
        p = askopenfilename(filetypes=[("Text files", ".txt")])
        if p[-3:] == "txt":
            return p
        elif p[-3:] == "":
            pass
        else:
            messagebox.showerror("Nie obsługiwany rodzaj plików", "Wybierz plik z rozszerzeniem txt")

    def los(self) -> None:
        self.__random_pick = randint(0, len(self.__lista_p) - 1)
        self.__label_q.configure(text=str(self.__lista_p[self.__random_pick]))

    def check(self, *args, **kwargs):
        entry_s = str(self.__entry_e.get()).strip()

        if entry_s == self.__lista_e[self.__random_pick]:
            self.__treeview.insert("", END,
                                   values=(
                                     str(self.__lista_e[self.__random_pick]),
                                     "-",
                                     str(self.__lista_p[self.__random_pick])))
            self.__progress += 1
            self.__progress_bar.configure(amountused=self.__progress)
            self.__lista_p = np.delete(self.__lista_p, self.__random_pick)
            self.__lista_e = np.delete(self.__lista_e, self.__random_pick)
            if len(self.__lista_e) == 0:
                self.__label_q.configure(text="Wszystko zaliczone :)\n_𝚗𝚘𝚒𝚗𝚝")
                self.__entry_e.delete(0, END)
                self.__entry_e.configure(state="disable")
                for i in self.__treeview.get_children():
                    self.__treeview.delete(i)
                self.__progress_bar.configure(amountused=0, textright="/-")
                self.after(2000, lambda: self.__label_q.configure(text="Wybierz plik z rozszerzeniem\ntxt aby zacząć."))
            else:
                self.los()
        else:
            messagebox.showinfo("POPRAWNA ODP:", str(self.__lista_e[self.__random_pick]))
            self.los()
        self.__entry_e.delete(0, END)
        self.grow()


app = App()
app.mainloop()
