
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

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

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):
    msg = my_msg.get()
    # Đánh dấu tin nhắn đã được mã hóa
    marked_msg = f"[Đã mã hóa] {msg}"
    encrypted_msg = caesar_encrypt(marked_msg, shift=3)  # Thay đổi shift theo nhu cầu
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(encrypted_msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Nhập tên của bạn!.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Gửi", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#Ket noi toi server
HOST = '127.0.0.1'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.