import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os
import socket
import sys

# مقداردهی اولیه Pygame و Mixer
pygame.init()
pygame.mixer.init()

# تنظیمات GUI
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player GUI")
FONT = pygame.font.Font(None, 36)
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 150, 50)

HOST = '127.0.0.1'
PORT = 8080

logged_in = False  # وضعیت ورود کاربر
uploaded_file = None  # مسیر فایل آپلود‌شده


def check_server_connection():
    """بررسی اینکه سرور در حال اجرا است."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(2)
            client.connect((HOST, PORT))
        print("Connected to server successfully.")
    except (socket.timeout, ConnectionRefusedError):
        print("Error: Unable to connect to the server. Please ensure the server is running.")
        sys.exit(1)


def draw_progress_bar(progress):
    """نمایش پروگرس بار."""
    pygame.draw.rect(screen, (50, 50, 50), (100, 500, 600, 20))
    pygame.draw.rect(screen, (50, 150, 50), (100, 500, int(6 * progress), 20))
    pygame.display.flip()


def register_user():
    """ثبت‌نام کاربر جدید."""
    root = tk.Tk()
    root.withdraw()

    username = simpledialog.askstring("Register", "Enter username:")
    if not username:
        messagebox.showerror("Error", "Username cannot be empty!")
        return

    password = simpledialog.askstring("Register", "Enter password:", show="*")
    if not password:
        messagebox.showerror("Error", "Password cannot be empty!")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.sendall(f"register {username} {password}".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            messagebox.showinfo("Register", response)
    except Exception as e:
        messagebox.showerror("Error", f"Error during registration: {e}")


def login_user():
    """ورود کاربر."""
    global logged_in
    root = tk.Tk()
    root.withdraw()

    username = simpledialog.askstring("Login", "Enter username:")
    if not username:
        messagebox.showerror("Error", "Username cannot be empty!")
        return

    password = simpledialog.askstring("Login", "Enter password:", show="*")
    if not password:
        messagebox.showerror("Error", "Password cannot be empty!")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.sendall(f"login {username} {password}".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            if response == "Login successful.":
                logged_in = True
                messagebox.showinfo("Login", "Login successful!")
            else:
                messagebox.showerror("Login", response)
    except Exception as e:
        messagebox.showerror("Error", f"Error during login: {e}")


def upload_file():
    """آپلود فایل به سرور."""
    global uploaded_file
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a Music File",
        filetypes=[("Music Files", "*.mp3;*.wav;*.ogg"), ("All Files", "*.*")]
    )
    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.sendall(f"upload {file_name} {file_size}\n".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            if response != "READY":
                raise Exception(f"Server error: {response}")

            total_sent = 0
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    client.sendall(chunk)
                    total_sent += len(chunk)
                    progress = (total_sent / file_size) * 100
                    draw_progress_bar(progress)

            response = client.recv(1024).decode('utf-8')
            messagebox.showinfo("Upload", response)
            uploaded_file = file_path  # ذخیره مسیر فایل آپلود شده
    except Exception as e:
        messagebox.showerror("Error", f"Error during upload: {e}")


def play_music():
    """پخش فایل موسیقی."""
    if uploaded_file:
        pygame.mixer.music.load(uploaded_file)
        pygame.mixer.music.play()
        messagebox.showinfo("Playback", f"Playing: {os.path.basename(uploaded_file)}")
    else:
        messagebox.showerror("Error", "No file uploaded to play.")


def stop_music():
    """توقف پخش موسیقی."""
    pygame.mixer.music.stop()
    messagebox.showinfo("Playback", "Playback stopped.")


def show_auth_menu():
    """نمایش منوی ورود و ثبت‌نام."""
    buttons = [
        {"text": "Register", "callback": register_user, "x": 300, "y": 200},
        {"text": "Login", "callback": login_user, "x": 300, "y": 300},
    ]

    running = True
    while running:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if pygame.Rect(button["x"], button["y"], 200, 50).collidepoint(event.pos):
                        button["callback"]()
                        if logged_in:
                            running = False

        for button in buttons:
            pygame.draw.rect(screen, BUTTON_COLOR, (button["x"], button["y"], 200, 50))
            text = FONT.render(button["text"], True, TEXT_COLOR)
            screen.blit(text, (button["x"] + 50, button["y"] + 10))

        pygame.display.flip()


def show_main_menu():
    """نمایش منوی اصلی."""
    buttons = [
        {"text": "Upload File", "callback": upload_file, "x": 300, "y": 200},
        {"text": "Play", "callback": play_music, "x": 300, "y": 300},
        {"text": "Stop", "callback": stop_music, "x": 300, "y": 350},
    ]

    running = True
    while running:
        screen.fill(BG_COLOR)

        # نمایش نام فایل آپلود شده
        if uploaded_file:
            text = FONT.render(f"Uploaded: {os.path.basename(uploaded_file)}", True, TEXT_COLOR)
            screen.blit(text, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if pygame.Rect(button["x"], button["y"], 200, 50).collidepoint(event.pos):
                        button["callback"]()

        for button in buttons:
            pygame.draw.rect(screen, BUTTON_COLOR, (button["x"], button["y"], 200, 50))
            text = FONT.render(button["text"], True, TEXT_COLOR)
            screen.blit(text, (button["x"] + 50, button["y"] + 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    check_server_connection()
    show_auth_menu()
    show_main_menu()
