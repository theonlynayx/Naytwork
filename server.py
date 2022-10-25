import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"

client_addresses = set()
client_sockets = set()
client_name = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):

    while True:
        try:
            msg = cs.recv(1024).decode()

        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)

        else:
            if msg.startswith("/") :

                if msg.lstrip("/") == "list" :
                    mesg = f"{client_name}"
                    cs.send(mesg.encode())
                print("\n" + msg + "\n" + mesg)
            elif msg.startswith("[+]") :
                client_name.add(msg.lstrip("[+] ").rstrip(" Connected."))
                nnnn=msg.lstrip("[+] ").rstrip(" Connected.")
                print(f"\n{nnnn} added to the list")
                for client_socket in client_sockets:
                    try:
                        client_socket.send(msg.encode())
                    except Exception as e:
                        print(f"[!] Error: {e}")
                        client_sockets.remove(cs)
                        cs.close()
            elif msg.startswith("[-]") :
                client_name.remove(msg.lstrip("[-] ").rstrip(" leave the chatroom."))
                cs.close()
                nnnn=msg.lstrip("[-] ").rstrip(" leave the chatroom.")
                print(f"\n{nnnn} added to the list")
                for client_socket in client_sockets:
                    try:
                        client_socket.send(msg.encode())
                    except Exception as e:
                        print(f"[!] Error: {e}")
                        client_sockets.remove(cs)
                        cs.close()
            else:
                mesg = msg.replace(separator_token, ": ")
                for client_socket in client_sockets:
                    try:
                        client_socket.send(mesg.encode())
                    except Exception as e:
                        print(f"[!] Error: {e}")
                        client_sockets.remove(cs)
                        cs.close()
                print("\n" + mesg)


while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_addresses.add(client_address)
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

for cs in client_sockets:
    cs.close()

s.close()