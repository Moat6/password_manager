from tkinter import *
from tkinter import messagebox
import pyperclip,json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generator() :
    import random

    pass_list = []
    
    lower_alpha_list = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(",")
    upper_alpha_list = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z".split(',')
    num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    symbol_list = ['!', '@', '#', '%', '&', '*', '(', ')', '?']

    pass_len=int(pass_length.get())
    num_len=int(num_length.get())
    sym_len=int(symbol_length.get())
    upper_len=int(uppercase_length.get())

    length=pass_len -num_len -sym_len -upper_len

    for upper in range(upper_len):
        pass_list.append(random.choice(upper_alpha_list))
    for num in range(num_len):
        pass_list.append(str(random.choice(num_list)))
    for sym in range(sym_len):
        pass_list.append(random.choice(symbol_list))
    for sym in range(length):
        pass_list.append(random.choice(lower_alpha_list))


    random.shuffle(pass_list)
    pass_str = "".join(pass_list)
    
    pyperclip.copy(pass_str)
    
    pass_input.delete(0,END)
    pass_input.insert(0,pass_str)
    del pass_len,num_len,sym_len,upper_len

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_pass() :
    website = website_input.get().title()
    username= username_input.get().lower()
    password=pass_input.get()
    if len(website)==0 or len(username)==0 or len(password)==0 :
        messagebox.showerror(title="OOPS!!", message="You have left some fields empty. Please fill them up.")
        
    else :
        is_ok = messagebox.askyesno(title="Please Confirm", message=f"WEBSITE : {website}\n"
                                f"USERNAME : {username} \nPASSWORD : {password} \nDo you want to save?")
    if is_ok :
        pass_dict={
            website : {
                "email/username" : username,
                "password" : password
            }
        }
        try :
            with open("password_file.json","r") as file :
                data = json.load(file)
                data.update(pass_dict)
                print("data updated")
        except FileNotFoundError :
            with open("password_file.json","w") as file :
                json.dump(pass_dict, file, indent=4)
        else :
            with open("password_file.json","w") as file :
                json.dump(data, file, indent=4)
        finally :
            website_input.delete(0,END)
            num_length.delete(0,END)
            uppercase_length.delete(0,END)
            pass_length.delete(0,END)
            symbol_length.delete(0,END)
            pass_input.delete(0,END)

            pass_length.insert(0,10)
            num_length.insert(0,0)
            uppercase_length.insert(0,0)
            symbol_length.insert(0,0)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password() :
    website=website_input.get().title()

    try :
        with open("password_file.json","r") as file :
            data = json.load(file)
            
    except FileNotFoundError :
        messagebox.showerror(title="ERROR",message="NO File Found !!")
    else :
        if website in data :
            username=data[website]["email/username"]
            password=data[website]["password"]
            messagebox.showinfo(title="Search Result",message=f"WEBSITE : {website}\n"
                            f"USERNAME : {username} \nPASSWORD : {password}" )
            pyperclip.copy(password)
        else :
            messagebox.showerror(title="ERROR",message=f"{website} not found !!")

# ---------------------------- UI SETUP ------------------------------- #

window=Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas=Canvas(width=200, height=200)
logo_img=PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(row=0, column=0,columnspan=3)

# LABELS
website_label=Label(text="Website:")
website_label.grid(row=1,column=0,sticky=E)
username_label=Label(text="Email/Username:")
username_label.grid(row=2,column=0,sticky=E)
pass_label=Label(text="Password:")
pass_label.grid(row=5,column=0,sticky=E)
length_label=Label(text="Length of Password:")
length_label.grid(row=3,column=0,sticky=E)
num_label=Label(text="Numbers :")
num_label.grid(row=3,column=2,sticky=W)
uppercase_label=Label(text="UpperCases:")
uppercase_label.grid(row=4,column=0,sticky=E)
symbol_label=Label(text="Symbols :")
symbol_label.grid(row=4,column=2,sticky=W)

# ENTRY
website_input=Entry(width=25)
website_input.grid(row=1,column=1,columnspan=2,sticky=EW)
website_input.focus()
username_input=Entry(width=35)
username_input.grid(row=2,column=1,columnspan=2,sticky=EW)
username_input.insert(0,"username@email.com")
pass_input=Entry(width=25)
pass_input.grid(row=5,column=1,sticky=E)

# BUTTONS
search_button=Button(width=15,text="Search",highlightthickness=0,command=find_password)
search_button.grid(row=1,column=2)
pass_gen_button=Button(width=15,text="Generate Password",highlightthickness=0,command=generator)
pass_gen_button.grid(row=5,column=2)
add_button=Button(width=36,text="Add",highlightthickness=0,command=save_pass)
add_button.grid(row=6,column=1,columnspan=2,sticky=EW)

# SPINBOX
pass_length = Spinbox(from_=0, to=28, width=5)
pass_length.grid(row=3,column=1,sticky=W)
pass_length.insert(0,1)
num_length = Spinbox(from_=0, to=28, width=5)
num_length.grid(row=3,column=2,sticky=E)
uppercase_length = Spinbox(from_=0, to=28, width=5)
uppercase_length.grid(row=4,column=1,sticky=W)
symbol_length = Spinbox(from_=0, to=28, width=5)
symbol_length.grid(row=4,column=2,sticky=E)


window.mainloop()