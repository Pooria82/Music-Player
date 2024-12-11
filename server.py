import socket
import os
import threading
from hashlib import sha256

HOST = '127.0.0.1'
PORT = 8080
UPLOAD_FOLDER = "uploaded_music"
USERS_FILE = "users.txt"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ذخیره کاربران در یک فایل متنی
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        pass


def hash_password(password):
    """هش کردن رمز عبور برای امنیت بیشتر."""
    return sha256(password.encode()).hexdigest()


def register_user(username, password):
    """ثبت‌نام کاربر جدید."""
    with open(USERS_FILE, "r") as f:
        users = f.readlines()

    for user in users:
        if username == user.split(":")[0]:
            return "ERROR: Username already exists."

    hashed_password = hash_password(password)
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}:{hashed_password}\n")
    return "User registered successfully."


def authenticate_user(username, password):
    """ورود کاربر با تایید شناسه و رمز عبور."""
    hashed_password = hash_password(password)
    with open(USERS_FILE, "r") as f:
        users = f.readlines()

    for user in users:
        stored_username, stored_password = user.strip().split(":")
        if username == stored_username and hashed_password == stored_password:
            return "Login successful."
    return "ERROR: Invalid username or password."


def handle_client(conn, addr):
    """مدیریت کلاینت."""
    print(f"New connection from {addr}")
    try:
        while True:
            # دریافت دستور اولیه
            initial_data = conn.recv(1024).decode('utf-8').strip()
            print(f"Command received: {initial_data}")

            parts = initial_data.split(" ")
            command = parts[0]

            if command == "register":
                username, password = parts[1], parts[2]
                response = register_user(username, password)
                conn.sendall(response.encode('utf-8'))

            elif command == "login":
                username, password = parts[1], parts[2]
                response = authenticate_user(username, password)
                conn.sendall(response.encode('utf-8'))

            elif command == "upload":
                filename, file_size = parts[1], int(parts[2])
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                print(f"Preparing to receive file: {filename} (size: {file_size} bytes)")
                conn.sendall("READY".encode('utf-8'))

                with open(filepath, "wb") as f:
                    total_received = 0
                    while total_received < file_size:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        f.write(chunk)
                        total_received += len(chunk)
                        print(f"Received {len(chunk)} bytes. Total: {total_received}/{file_size}")

                if total_received == file_size:
                    conn.sendall(f"File {filename} uploaded successfully.".encode('utf-8'))
                    print(f"File {filename} uploaded successfully.")
                else:
                    conn.sendall(f"ERROR: Incomplete file upload. Received {total_received} bytes.".encode('utf-8'))

            elif command == "play":
                response = "Playing song..."
                print(response)
                conn.sendall(response.encode('utf-8'))

            elif command == "stop":
                response = "Playback stopped."
                print(response)
                conn.sendall(response.encode('utf-8'))

            elif command == "next":
                response = "Skipping to next song..."
                print(response)
                conn.sendall(response.encode('utf-8'))

            elif command == "prev":
                response = "Going back to previous song..."
                print(response)
                conn.sendall(response.encode('utf-8'))

            elif command == "exit":
                conn.sendall("Connection closed.".encode('utf-8'))
                print("Client disconnected.")
                break

            else:
                conn.sendall("ERROR: Invalid command.".encode('utf-8'))
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection closed: {addr}")


def main():
    """اجرای سرور."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server running on {HOST}:{PORT}")
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
