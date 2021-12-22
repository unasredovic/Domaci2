import tkinter as tk
from tkinter import messagebox
from db import Database


db = Database('store.db')

# Glavni dio 


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Spisak studenata na predmetu programiranje 2')
        # Width height
        master.geometry("500x350")
        master['bg'] = "#add8e6"
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()

    def create_widgets(self):
        # ime
        self.ime_text = tk.StringVar()
        self.ime_label = tk.Label(
            self.master, text='Ime', font=('bold', 17),  pady=20, fg="yellow", background="#add8e6"
                )
        self.ime_label.grid(row=0, column=0, sticky=tk.W)
        self.ime_entry = tk.Entry(self.master, textvariable=self.ime_text)
        self.ime_entry.grid(row=0, column=1)
        # prezime
        self.prezime_text = tk.StringVar()
        self.prezime_label = tk.Label(
            self.master, text='Prezime', font=('bold', 20), fg="yellow", background="#add8e6")
        self.prezime_label.grid(row=0, column=2, sticky=tk.W)
        self.prezime_entry = tk.Entry(
            self.master, textvariable=self.prezime_text)
        self.prezime_entry.grid(row=0, column=3)
        # godina
        self.godina_text = tk.StringVar()
        self.godina_label = tk.Label(
            self.master, text='Godina', font=('bold', 20), fg="yellow", background="#add8e6")
        self.godina_label.grid(row=1, column=0, sticky=tk.W)
        self.godina_entry = tk.Entry(
            self.master, textvariable=self.godina_text)
        self.godina_entry.grid(row=1, column=1)
        # ocjena
        self.ocjena_text = tk.StringVar()
        self.ocjena_label = tk.Label(
            self.master, text='Ocjena', font=('bold', 20) , fg="yellow", background="#add8e6")
        self.ocjena_label.grid(row=1, column=2,  sticky=tk.W)
        self.ocjena_entry = tk.Entry(self.master, textvariable=self.ocjena_text)
        self.ocjena_entry.grid(row=1, column=3)

        # imena list (listbox)
        self.imena_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.imena_list.grid(row=3, column=0, columnspan=3,
                             rowspan=6, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=3)
        # Set scrollbar to imena
        self.imena_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.imena_list.yview)

        # Bind select
        self.imena_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        self.add_btn = tk.Button(
            self.master, text="Dodaj studenta", width=12,bg= "yellow", 
                activebackground="blue", command=self.add_item)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = tk.Button(
            self.master, text="Izbrisi studenta", width=12,bg= "yellow", 
                activebackground="blue", command=self.remove_item)
        self.remove_btn.grid(row=2, column=1)

        self.update_btn = tk.Button(
            self.master, text="Promjena", width=12,bg= "yellow", 
                activebackground="blue", command=self.update_item)
        self.update_btn.grid(row=2, column=2)

        self.exit_btn = tk.Button(
            self.master, text="Obrisati unos", width=12,bg= "yellow", 
                activebackground="blue", command=self.clear_text)
        self.exit_btn.grid(row=2, column=3)

    def populate_list(self):
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.imena_list.delete(0, tk.END)
        # Loop through records
        for row in db.fetch():
            # Insert into list
            self.imena_list.insert(tk.END, row)

    # Add new item
    def add_item(self):
        if self.ime_text.get() == '' or self.prezime_text.get() == '' or self.godina_text.get() == '' or self.ocjena_text.get() == '':
            messagebox.showerror(
                "Obavezna polja", "Unesite sva polja")
            return
        print(self.ime_text.get())
        # Insert into DB
        db.insert(self.ime_text.get(), self.prezime_text.get(),
                  self.godina_text.get(), self.ocjena_text.get())
        # Clear list
        self.imena_list.delete(0, tk.END)
        # Insert into list
        self.imena_list.insert(tk.END, (self.ime_text.get(),  self.prezime_text.get(
        ), self.godina_text.get(), self.ocjena_text.get()))
        self.clear_text()
        self.populate_list()

    # Runs when item is selected
    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.imena_list.curselection()[0]
            # Get selected item
            self.selected_item = self.imena_list.get(index)
            # print(selected_item) # Print tuple

            # Add text to entries
            self.ime_entry.delete(0, tk.END)
            self.ime_entry.insert(tk.END, self.selected_item[1])
            self.prezime_entry.delete(0, tk.END)
            self.prezime_entry.insert(tk.END, self.selected_item[2])
            self.godina_entry.delete(0, tk.END)
            self.godina_entry.insert(tk.END, self.selected_item[3])
            self.ocjena_entry.delete(0, tk.END)
            self.ocjena_entry.insert(tk.END, self.selected_item[4])
        except IndexError:
            pass

    # Remove item
    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    # Update item
    def update_item(self):
        db.update(self.selected_item[0], self.ime_text.get(
        ), self.prezime_text.get(), self.godina_text.get(), self.ocjena_text.get())
        self.populate_list()

    # Clear all text fields
    def clear_text(self):
        self.ime_entry.delete(0, tk.END)
        self.prezime_entry.delete(0, tk.END)
        self.godina_entry.delete(0, tk.END)
        self.ocjena_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()