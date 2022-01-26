import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = socket.socket()
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(msg)

        data = input(">>> ") # reads input from user and stores it in data(string)
        data = data.split(" ")#value in data is splited on basis of " " now returned data is a list
        cmd = data[0]

        if cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        elif cmd == "UPLOAD":
            filename = data[1].strip()
            with open(filename, "r") as f: #opens the file in the path using read permission.
                text = f.read() #fetches the content of the file
            client.send(f"{cmd}@{filename}@{text}".encode(FORMAT))#sends the data to server
        else :
            client.send(cmd.encode(FORMAT)) # sends cmd to the server

    client.close()

if __name__ == "__main__":
    main()