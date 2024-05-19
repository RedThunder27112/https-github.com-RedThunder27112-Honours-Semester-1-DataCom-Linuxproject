import socket
import tqdm
import os
import tkinter as tk
from tkinter import filedialog
import time

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
hostnamex = "10.0.1.15"

def select_file():
    root = tk.Tk()
    root.withdraw() # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path

def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    filesize = int(filesize)
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")


    # Inform the server that file sending is requested
    UPLOAD = "UPLOAD"
    s.send(f"{UPLOAD}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())
    time.sleep(1)
    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the socket
    s.close()

def close_connection():
    root = tk.Tk()
    root.destroy()
    exit()

def upload_file(host, port):
    filename = select_file()
    if filename:
        send_file(filename, host, port)

def list_files_from_server(host,port,file_listbox):
    s = socket.socket()
    s.connect((host, port))
    s.send("LIST".encode())
    files = s.recv(BUFFER_SIZE).decode().split("\n")

    s.close()

    # Clear the listbox
    file_listbox.delete(0, tk.END)

    # Update the listbox with the received files
    for file in files:
        file_listbox.insert(tk.END, file)

def download_file(filename, host, port):
    s = socket.socket()
    s.connect((host, port))
    DOWNLOAD = "DOWNLOAD"
    s.send(f"{DOWNLOAD}{SEPARATOR}{filename}".encode())
    # Receive and save the file similar to the existing send_file function
    request = s.recv(BUFFER_SIZE).decode()
    filename, filesize = request.split(SEPARATOR)

    progress = tqdm.tqdm(range(int(filesize)), f"Downloading {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    downloadDir = "./clientDownloads"
    with open(os.path.join(downloadDir,filename), "wb") as f:
        while True:
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    s.close()




def download_selected_file(file_listbox, host, port):
    selected_index = file_listbox.curselection()
    if selected_index:
        selected_file = file_listbox.get(selected_index)
        download_file(selected_file, host, port)

# function to request the list of music folders from the server
def list_music_folders(host, port, file_listbox):
    s = socket.socket()
    s.connect((host, port))
    s.send("MLIST".encode())
    files = s.recv(BUFFER_SIZE).decode().split("\n")

    s.close()

    # Clear the listbox
    file_listbox.delete(0, tk.END)

    # Update the listbox with the received files
    for file in files:
        file_listbox.insert(tk.END, file)

# function to send the selected music folder to the server for playback
def play_music_from_folder(host, port,file_listbox):
    selected_index = file_listbox.curselection()
    if selected_index:
        selected_file = file_listbox.get(selected_index)
        s = socket.socket()
        s.connect((host, port))
        s.send(f"PLAYMUSIC{SEPARATOR}{selected_file}".encode())
        s.close()

# function to create a backup
def create_backup(host, port,file_listbox):
    s = socket.socket()
    s.connect((host, port))
    s.send(f"BACKUP".encode())

    request = s.recv(BUFFER_SIZE).decode()

    # Clear the listbox
    file_listbox.delete(0, tk.END)

    if request == "SUCC":
        file_listbox.insert(tk.END, "Backing up")
    elif request == "FAIL":
        file_listbox.insert(tk.END, "Something went wrong")

    s.close()

    # function to send morse code
def send_morse_code(host, port, text):
    s = socket.socket()
    s.connect((host, port))
    s.send(f"MORSE{SEPARATOR}{text}".encode())

    s.close()


# function to send password to vault
def send_password(host, port,text,file_listbox):
    s = socket.socket()
    s.connect((host, port))
    s.send(f"SPASSWORD{SEPARATOR}{text}".encode())

    request = s.recv(BUFFER_SIZE).decode()

    # Clear the listbox
    file_listbox.delete(0, tk.END)

    if request == "SUCC":
        file_listbox.insert(tk.END, "Success")
    elif request == "FAIL":
        file_listbox.insert(tk.END, "Something went wrong")

    s.close()

# function to receive passwords from vault
def receive_password(host, port, file_listbox):
    s = socket.socket()
    s.connect((host, port))
    s.send("RPASSWORD".encode())  # Send a command to request the list of passwords
    passwords = s.recv(BUFFER_SIZE).decode().split("\n")  # Receive the list of passwords

    s.close()

    # Clear the listbox
    file_listbox.delete(0, tk.END)

    # Update the listbox with the received passwords
    for password in passwords:
        file_listbox.insert(tk.END, password)



def main():
    root = tk.Tk()
    root.title("Family File Server")

    # Entry widget for server IP

    label0 = tk.Label(root, text="Enter IP:", font=("Helvetica", 10))
    label0.pack(pady=5)

    input_entry1 = tk.Entry(root)
    input_entry1.pack(fill="x", padx=10, pady=5)



    # Create a listbox to display files
    file_listbox = tk.Listbox(root)
    file_listbox.pack(expand=True, fill="both", padx=10, pady=5)

    label1 = tk.Label(root, text=" ", font=("Helvetica", 10))
    label1.pack(pady=5)

    label2 = tk.Label(root, text="Morse Code and Passwords:", font=("Helvetica", 10))
    label2.pack(pady=5)

    # Entry widget for user input
    input_entry = tk.Entry(root)
    input_entry.pack(fill="x", padx=10, pady=5)

    # Row 1: Buttons for sending and retrieving passwords
    row1_frame = tk.Frame(root)
    row1_frame.pack(fill="x", padx=10, pady=5)

    send_password_button = tk.Button(row1_frame, text="Send New Password", command=lambda: send_password(input_entry1.get(), 5001, input_entry.get(), file_listbox))
    send_password_button.grid(row=0, column=0, sticky="nsew")

    receive_password_button = tk.Button(row1_frame, text="Retrieve Passwords", command=lambda: receive_password(input_entry1.get(), 5001, file_listbox))
    receive_password_button.grid(row=0, column=1, sticky="nsew")

    # Configure row1_frame weights for equal distribution of space
    row1_frame.grid_columnconfigure(0, weight=1)
    row1_frame.grid_columnconfigure(1, weight=1)


    # Row 2: Button to trigger morse code
    morse_button = tk.Button(root, text="Morse Code", command=lambda: send_morse_code(input_entry1.get(), 5001, input_entry.get()))
    morse_button.pack(fill="x", padx=10, pady=5)

    # Row 3: Buttons for listing and playing music files
    label3 = tk.Label(root, text=" ", font=("Helvetica", 10))
    label3.pack(pady=5)

    label4 = tk.Label(root, text="Music Playing:", font=("Helvetica", 10))
    label4.pack(pady=5)

    row3_frame = tk.Frame(root)
    row3_frame.pack(fill="x", padx=10, pady=5)
    list_music_button = tk.Button(row3_frame, text="List Music Files", command=lambda: list_music_folders(input_entry1.get(), 5001, file_listbox))
    list_music_button.grid(row=0, column=0, sticky="nsew")

    play_music_button = tk.Button(row3_frame, text="Play Music from Folder", command=lambda: play_music_from_folder(input_entry1.get(), 5001, file_listbox))
    play_music_button.grid(row=0, column=1, sticky="nsew")

    # Configure row weights for equal distribution of space
    row3_frame.grid_columnconfigure(0, weight=1)
    row3_frame.grid_columnconfigure(1, weight=1)

    # Row 4: Button to list files
    label5 = tk.Label(root, text=" ", font=("Helvetica", 10))
    label5.pack(pady=5)

    label6 = tk.Label(root, text="File Transfer:", font=("Helvetica", 10))
    label6.pack(pady=5)

    list_button = tk.Button(root, text="List Files", command=lambda: list_files_from_server(input_entry1.get(), 5001, file_listbox))
    list_button.pack(fill="x", padx=10, pady=5)

    # Row 5: Buttons for uploading and downloading files
    row5_frame = tk.Frame(root)
    row5_frame.pack(fill="x", padx=10, pady=5)
    upload_button = tk.Button(row5_frame, text="Upload File", command=lambda:
    upload_file(input_entry1.get(),5001))
    upload_button.grid(row=0, column=0, sticky="nsew")

    download_button = tk.Button(row5_frame, text="Download Selected File", command=lambda: download_selected_file(file_listbox, input_entry1.get(), 5001))
    download_button.grid(row=0, column=1, sticky="nsew")

    row5_frame.grid_columnconfigure(0, weight=1)
    row5_frame.grid_columnconfigure(1, weight=1)

    # Row 6: Button to create backup
    label7 = tk.Label(root, text=" ", font=("Helvetica", 10))
    label7.pack(pady=5)

    backup_button = tk.Button(root, text="Create Backup", command=lambda: create_backup(input_entry1.get(), 5001, file_listbox))
    backup_button.pack(fill="x", padx=10, pady=5)

    # Row 7: Button to close the connection
    close_button = tk.Button(root, text="Close Connection", command=close_connection)
    close_button.pack(fill="x", padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
