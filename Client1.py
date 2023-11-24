
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from unidecode import unidecode

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # Xác định loại ký tự (in hoa hoặc thường)
            is_upper = char.isupper()

            # Chuyển về chữ cái in hoa để mã hóa
            char = char.upper()

            # Mã hóa ký tự chữ cái
            result += chr((ord(char) + shift - ord('A')) % 26 + ord('A'))

            # Chuyển về chữ cái thường nếu ban đầu là chữ cái thường
            if not is_upper:
                result = result.lower()
        else:
            result += char
    return result


# Hàm giải mã caesar
def caesar_decrypt(ciphertext, shift):
    result = ""
    for char in ciphertext:
        if char.isalpha():
            # Giải mã ký tự chữ cái, bao gồm cả chữ cái thường và in hoa
            is_upper = char.isupper()
            char = char.upper()  # Chuyển chữ cái về in hoa để giải mã
            result += chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            if not is_upper:
                result = result.lower()  # Chuyển về chữ cái thường nếu ban đầu là chữ cái thường
        else:
            result += char
    return result
#Hàm nhận tin nhắn từ server thông qua kết nối socket và hiển thị lại trên giao diện tkinter
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

# Hàm gởi tin nhẵn từ client lên server
def send(event=None):
    msg = my_msg.get()
    #Đánh dấu tin nhắn đã được mã hóa
    marked_mgs = f"[Encrypt] {msg}"
    encrypted_mgs = caesar_encrypt(marked_mgs, shift= 3)
    my_msg.set("")
    client_socket.send(bytes(encrypted_mgs, "utf8")) # mã hóa tin nhắn khi gởi lên server
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

