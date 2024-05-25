import tkinter as tk
from typing import Any
from tkinter import messagebox, simpledialog
from result import Result, Ok, Err
from logic import (
    connect_to_fpt_server,
    delete_file,
    get_file_list,
    retrieve_file,
    store_file,
    update_file,
)

root = tk.Tk()
root.geometry("500x500")
root.title("FTP Client")

server = tk.StringVar(value="127.0.0.1")
server_label = tk.Label(root, text="Server:")
server_entry = tk.Entry(root, textvariable=server)

port = tk.StringVar(value="21")
port_label = tk.Label(root, text="Port:")
port_entry = tk.Entry(root, textvariable=port)

username = tk.StringVar(value="TestUser")
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root, textvariable=username)

password = tk.StringVar(value="12345")
password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*", textvariable=password)


def log(msg: str):
    log_text.insert(tk.END, msg)


def parse_connection(connection_result):
    global ftp
    match connection_result:
        case Err(err):
            messagebox.showerror("Error", err)
        case Ok(conn):
            ftp = conn


connect_button = tk.Button(
    root,
    text="Connect",
    command=lambda: parse_connection(
        connect_to_fpt_server(
            server_entry.get(),
            int(port_entry.get()),
            username.get(),
            password.get(),
            log,
        )
    ),
)
list_button = tk.Button(
    root,
    text="Print Files List",
    command=lambda: get_file_list(ftp, log),
)

filename_label = tk.Label(root, text="Filename:")
filename_entry = tk.Entry(root)


def show_error_if_occurs(result: Result[Any, str]):
    result.map_err(lambda err: messagebox.showerror("Error", err))


retrieve_button = tk.Button(
    root,
    text="Retrieve File",
    command=lambda: show_error_if_occurs(
        retrieve_file(ftp, filename_entry.get(), log)
    ),
)


def ask_file_content() -> str:
    content = simpledialog.askstring(
        "Enter File Content", "Enter the content of the file:"
    )
    return "" if content is None else content


create_button = tk.Button(
    root,
    text="Create File",
    command=lambda: show_error_if_occurs(
        store_file(ftp, filename_entry.get(), ask_file_content(), log)
    ),
)
delete_button = tk.Button(
    root,
    text="Delete File",
    command=lambda: show_error_if_occurs(
        delete_file(ftp, filename_entry.get(), log)
    ),
)


def update_content_gui(content: str) -> str:
    new_content = simpledialog.askstring(
        "File Content",
        "Update content of the file:",
        initialvalue=content,
    )
    return "" if new_content is None else new_content


update_button = tk.Button(
    root,
    text="Update File",
    command=lambda: update_file(
        ftp, filename_entry.get(), update_content_gui, log
    ),
)

server_label.place(x=50, y=0)
server_entry.place(x=150, y=0)
username_label.place(x=350, y=0)
username_entry.place(x=450, y=0)
port_label.place(x=50, y=30)
port_entry.place(x=150, y=30)
password_label.place(x=350, y=30)
password_entry.place(x=450, y=30)
connect_button.place(x=250, y=70)
list_button.place(x=350, y=70)
filename_label.place(x=200, y=110)
filename_entry.place(x=300, y=110)
retrieve_button.place(x=150, y=150)
create_button.place(x=250, y=150)
delete_button.place(x=350, y=150)
update_button.place(x=450, y=150)

log_text = tk.Text(root, height=30, width=40)
log_text.place(x=150, y=200)

root.mainloop()
