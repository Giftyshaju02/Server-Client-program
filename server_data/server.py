

import os #remove file
import socket # tcp socket connection
import threading #enter each client spe-concurrent

pc_name = socket.gethostname() #pc_name recieves the name of your pc
IP = socket.gethostbyname(pc_name) #IP recieves the ipaddress of the pc whose name is specified in pc_name
PORT = 4456 #p
ADDR = (IP, PORT) #tuple with IP and port
SIZE = 1024
FORMAT = "utf-8" #encode and decode cl to server and back
SERVER_DATA_PATH = "server_data"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT) #command is recieved from the client eg list help
        data = data.split("@")
        cmd = data[0]

        if cmd == "LIST":
            files = os.listdir()#all the files inside the directory 'server_data' is send to files
            send_data = "OK@"

            if len(files) == 0:
                send_data = send_data + "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)#lists the names of all files

        elif cmd == "UPLOAD":
            name, text = data[1].strip(), data[2].strip()#uploads respectively
            with open(name, "w") as f: #create a file by name 'name'   in server_data directory and opens that file with write permission
                f.write(text) #contents are copied
            send_data = "OK@File uploaded successfully."

        elif cmd == "DELETE":
            files = os.listdir()
            send_data = "OK@"
            filename = data[1].strip()

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.remove(filename)#removes that particular file
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

        elif cmd == "HELP":
            send_data = "OK@"
            send_data += "LIST: List all the files from the server.\n"
            send_data += "UPLOAD <filename>: Upload a file to the server.\n"
            send_data += "DELETE <filename>: Delete a file from the server.\n"
            send_data += "LOGOUT: Disconnect from the server.\n"
            send_data += "HELP: List all the commands."

        elif cmd == "LOGOUT":
            print(f"[DISCONNECTED] {addr} disconnected")
            send_data = f"DISCONNECTED@{IP} disconnected"
            conn.send(send_data.encode(FORMAT))
            break

        else :
            send_data = "OK@INVALID COMMAND"

        conn.send(send_data.encode(FORMAT))

    conn.close()

def main():
    print("[STARTING] Server is starting")#where pgm us
    server = socket.socket()#create a server+tcp server
    server.bind(ADDR) # bind host name and IP
    server.listen() #server is listerning
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True: #explicitly closes pgm  within while client will connect server
        conn, addr = server.accept() #serevr is accepting connection client nte ip
        #thread = threading.Thread(target=handle_client, args=(conn, addr)) #
        #thread.start()
        handle_client(conn,addr)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()