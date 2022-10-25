from tkinter import *
import socket
from threading import Thread
from datetime import datetime

window = Tk()
window.title('Naytwork communication')
window.geometry("600x660")

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 
separator_token = "<SEP>"
name = ""

def Getinput():
    global name
    global nbr
    to_send = entry.get()
    if to_send.startswith("/login"):
        if name == "":
            name = to_send.lstrip("/login ")
            to_send = f"[+] {name} Connected."
            s.send(to_send.encode())
    
    elif to_send.startswith("/leave"):
        to_send=f"[-] {name} leave the chatroom."
        s.send(to_send.encode())
        window.destroy()

    elif to_send.startswith("/"):
        s.send(to_send.encode())
    else :
        if name == "":
            pass
        else:
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            to_send = f"[{date_now}] {name}{separator_token}{to_send}"
            s.send(to_send.encode())
    entry.delete(0, END)
    entry.insert(0,"")

def Tk_message(message):
    global nbr
    if nbr <=580 :
        nbr += 20
    else:
        nbr = 5
        canva_message.delete("all")
    canva_message.create_text(5,nbr,anchor="nw",fill='white',text=message)

def listen_for_messages():
    global name
    global message
    while True:
        if name == "":
            message = s.recv(1024).decode()
            message = ""
        else:
            message = s.recv(1024).decode()
            Tk_message(message)


canva_message = Canvas(window, width=600, height=600, background='#414e54')
entry = Entry(window, textvariable='string', width=300)
check = Button(window,padx=610,pady=650, text="Send", command=Getinput)
nbr = 5

s = socket.socket()
canva_message.create_text(5,nbr,anchor="nw",fill='lime',text=f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
nbr += 20
canva_message.create_text(5,nbr,anchor="nw",fill='lime',text="[+] Connected.")
nbr += 20
canva_message.create_text(5,nbr,anchor="nw",fill='lime',text="[!] Do '/login <Username>' to join the discution.")

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

canva_message.pack()
entry.pack()
check.pack()

window.mainloop()
