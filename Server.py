#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # Mã hóa ký tự chữ cái
            result += chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
        else:
            result += char
    return result

def caesar_decrypt(ciphertext, shift):
    result = ""
    for char in ciphertext:
        if char.isalpha():
            # Giải mã ký tự chữ cái
            result += chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
        else:
            result += char
    return result
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Nhập tên của bạn rồi bắt đầu chat!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Xin chào %s! Nếu bạn muốn thoát gõ, {quit} để thoát.' % name

    # Đánh dấu tin nhắn đã được mã hóa
    marked_welcome = f"[Đã mã hóa] {welcome}"

    client.send(bytes(caesar_encrypt(marked_welcome, shift=3), "utf8"))
    msg = "%s đã tham gia phòng chat!" % name

    # Đánh dấu tin nhắn đã được mã hóa
    marked_msg = f"[Đã mã hóa] {msg}"

    broadcast(bytes(caesar_encrypt(marked_msg, shift=3), "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)

        # Kiểm tra xem tin nhắn có đánh dấu là đã mã hóa hay không
        if f"[Đã mã hóa]" in msg:
            decrypted_msg = caesar_decrypt(msg.decode("utf8"), shift=3)
            # Xử lý tin nhắn đã được giải mã
            # ...
        else:
            # Tin nhắn chưa mã hóa, xử lý như bình thường
            decrypted_msg = msg.decode("utf8")

        if decrypted_msg != "{quit}":
            broadcast(bytes(decrypted_msg, "utf8"), name + ": ")
        else:
            client.send(bytes(caesar_encrypt("{quit}", shift=3), "utf8"))
            client.close()
            del clients[client]

            # Đánh dấu tin nhắn đã được mã hóa
            marked_exit_msg = f"[Đã mã hóa] {name} đã thoát phòng chat."
            broadcast(bytes(caesar_encrypt(marked_exit_msg, shift=3), "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Chờ kết nối từ các client...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()