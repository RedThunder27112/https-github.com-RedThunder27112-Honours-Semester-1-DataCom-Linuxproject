import socket
import tqdm
import os
import threading
import time

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Function to list files in a directory
def list_files(directory):
    return os.listdir(directory)

def handle_client(client_socket, address):
    print(f"[+] {address} is connected.")
    while True:
        # receive the request from the client
        request = client_socket.recv(BUFFER_SIZE).decode()
        if not request:
            break
        if request == "LIST":
            # Client requests a list of files
            files = list_files("./")
            # Send the list of files to the client
            files_str = "\n".join(files)
            client_socket.send(files_str.encode())

        elif request == "BACKUP":

            # Create backup
            start_backup(client_socket)

        elif request == "MLIST":

            # Client requests a list of files
            files = list_files("./dir2")
            # Send the list of files to the client
            files_str = "\n".join(files)
            client_socket.send(files_str.encode())

        elif request == "RPASSWORD":

            # Client requests a list of passwords from a file
            passwords_filepath = "./passwords.txt"
            send_passwords_to_client(client_socket, passwords_filepath)

        elif request.startswith("SPASSWORD"):

            requestType, text = request.split(SEPARATOR)
            passwords_filepath = "./passwords.txt"
            new_password = text
            append_password_to_file(passwords_filepath, new_password,client_socket)

        elif request.startswith("MORSE"):

            requestType, text = request.split(SEPARATOR)
            # Send the requested file to the client
            play_Morse(text)

        elif request.startswith("PLAYMUSIC"):

            # Client requests to download a file
            requestType, filename = request.split(SEPARATOR)
            # Send the requested file to the client
            play_music(filename)

        elif request.startswith("DOWNLOAD"):
            # Client requests to download a file
            requestType, filename = request.split(SEPARATOR)
            # Send the requested file to the client
            send_file(filename, client_socket)
        elif request.startswith("UPLOAD"):
            # Client requests to upload a file
            requestType, filename, filesize = request.split(SEPARATOR)
            receive_file(client_socket,filename,filesize)
    # close the client socket
    client_socket.close()
    print(f"[-] {address} is disconnected.")


def read_passwords_from_file(filepath):
    with open(filepath, "r") as file:
        passwords = file.readlines()
    return passwords

def send_passwords_to_client(client_socket, filepath):
    passwords = read_passwords_from_file(filepath)
    passwords_str = "\n".join(passwords)
    client_socket.send(passwords_str.encode())

def append_password_to_file(filepath, new_password,client_socket):
    try:
        with open(filepath, "a") as file:
            file.write(new_password + "\n")
        client_socket.send(f"SUCC".encode())
    except Exception as e:
        client_socket.send(f"FAIL".encode())






import subprocess

# method for playing music
def play_music(filename):

    try:
        command = f"./mediaPlayer.sh dir2/{filename}"
        subprocess.Popen(command, shell=True)
    except Exception as e:
        print("music no play")

# Play morse code
def play_Morse(text):

    try:
        command = f"python3 morseCodeSound.py '{text}'"
        subprocess.Popen(command, shell=True)
    except Exception as e:
        print("music no play")




# Modify the server script to include a method for playing music
def start_backup(client_socket):
    try:
        command = f"./googleD.sh"
        subprocess.Popen(command, shell=True)
        client_socket.send(f"SUCC".encode())
    except Exception as e:
        client_socket.send(f"FAIL".encode())
        print("backup no play")


def receive_file(client_socket,filename,filesize):
    # receive the file infos
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))


def send_file(filename, client_socket):
    filesize = os.path.getsize(filename)
    # send the filename and filesize
    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # start sending the file
    time.sleep(1)
    progress = tqdm.tqdm(range(int(filesize)), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
            progress.update(len(bytes_read))
    client_socket.close()


def main():
    # create the TCP server socket
    server_socket = socket.socket()
    # bind the socket to our local address
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept 5 connections
    server_socket.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # accept connection if there is any
        client_socket, address = server_socket.accept()
        # create a thread to handle the new client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    main()
