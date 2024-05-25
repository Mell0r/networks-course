from typing import Callable
from ftplib import FTP
from result import Result, Ok, Err


def connect_to_fpt_server(
    server: str,
    port: int,
    username: str,
    password: str,
    log: Callable[[str], None],
) -> Result[FTP, str]:
    try:
        ftp = FTP()
        ftp.connect(server, port)
        ftp.login(username, password)
        log("Connected to FTP server\n")
        get_file_list(ftp, log)
        return Ok(ftp)
    except Exception as e:
        log(f"Error connecting to FTP server: {str(e)}\n")
        return Err(str(e))


def get_file_list(ftp: FTP, log: Callable[[str], None]) -> list[str]:
    log("\nFile list:\n")
    files = ftp.nlst()
    for file in files:
        log(f"{file}\n")
    log("\nFile list end.\n")
    return files


def retrieve_file(
    ftp: FTP, filename: str, log: Callable[[str], None]
) -> Result[str, str]:
    log("\nRertieving file...\n")

    try:
        lines = []
        ftp.retrlines(
            "RETR " + filename,
            lines.append,
        )
        content = "\n".join(lines)
        log(content)
        with open(filename, "w") as file:
            file.write("" if content is None else content)
        log("\n\nFile retrieved.\n")
        return Ok(content)
    except Exception as e:
        log(f"Error retrieving file: {str(e)}\n")
        return Err(str(e))


def store_file(
    ftp: FTP, filename: str, content: str, log: Callable[[str], None]
) -> Result[None, str]:
    try:
        with open(filename, "w") as file:
            file.write("" if content is None else content)
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
        log(f"FILE {filename} CREATED.\n")
        return Ok(None)
    except Exception as e:
        log(f"Error creating file: {str(e)}\n")
        return Err(str(e))


def update_file(
    ftp: FTP,
    filename: str,
    content_updater: Callable[[str], str],
    log: Callable[[str], None],
) -> Result[None, str]:
    log("\nUpdating file...\n")
    return retrieve_file(ftp, filename, log).and_then(
        lambda content: store_file(ftp, filename, content_updater(content), log)
    )


def delete_file(
    ftp: FTP,
    filename: str,
    log: Callable[[str], None],
) -> Result[None, str]:
    try:
        ftp.delete(filename)
        log(f"File '{filename}' deleted.\n")
        return Ok(None)
    except Exception as e:
        log(f"Error deleting file: {str(e)}\n")
        return Err(str(e))
