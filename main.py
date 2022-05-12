from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_doc():
    if len(website_entry.get()) <= 0 or len(password_entry.get()) <= 0:
        messagebox.showerror("Incomplete Field", "Please don't leave any field empty")
    else:
        information1 = website_entry.get().title()
        information2 = username_entry.get()
        information3 = password_entry.get()
        new_data = {
            information1: {
                "username": information2,
                "password": information3,
            }
        }
        try:
            with open("password.json", "r") as file:
                data = json.load(file)
                data.update(new_data)

        except FileNotFoundError:
            with open("password.json", "w") as file:
                json.dump(new_data, file, indent=4)

        else:
            with open("password.json", "w") as file:
                json.dump(data, file, indent=4)

        finally:
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")


def search():
    try:
        with open("password.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Sorry no file has been created")
    else:
        website = website_entry.get().title()
        try:
            username = data[f"{website}"]["username"]
            password = data[f"{website}"]["password"]
        except KeyError:
            messagebox.showerror("Error", f"Sorry the website {website} hasn't been added")
        else:
            messagebox.showinfo(f"{website}", f"Username: {username}\nPassword: {password}\n"
                                              f"The password has been copied to your clipboard")
            pyperclip.copy(password)
    finally:
        website_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

photo = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=photo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky="EW")

username_entry = Entry(width=35)
username_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
username_entry.insert(0, "ope.akinseloyin@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

password_button = Button(text="Generate Password", command=password_generator)
password_button.grid(row=3, column=2, sticky="EW")

add_button = Button(text="Add", width=36, command=save_doc)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=2, sticky="EWSN")

window.mainloop()
