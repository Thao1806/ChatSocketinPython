#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from unidecode import unidecode


# Hàm mã hóa caesar
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


# Hàm chấp nhận kết nối từ client:
# Một vòng lặp vô hạn để chấp nhận kết nối từ client.
# Mỗi khi có kết nối mới, một luồng mới được tạo để xử lý client đó.
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Nhập tên của bạn rồi bắt đầu chat!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


# Hàm xử lí client: xử lí gửi nhận tin nhắn
def handle_client(client):  # Takes client socket as argument.
    encrypted_name = client.recv(BUFSIZ).decode("utf8") # Lấy tin nhắn tên của client gởi lên
    decrypted_name = caesar_decrypt(encrypted_name, shift=3)# Giải mã (Lúc này tên sau khi giải mã sẽ là: [Encrypt] + tên người dùng nhập)
    welcome = 'Xin chào %s! Nếu bạn muốn thoát gõ, {quit} để thoát.' % decrypted_name # Biến chứa câu chào người dùng
    client.send(bytes(welcome, "utf8")) #Gửi chuỗi văn bản welcome từ server đến client thông qua kết noiois socket
    msg = "%s đã tham gia phòng chat!" % decrypted_name # Biến chứa chuỗi thông báo đến các client
    broadcast(bytes(msg, "utf8"))# Gửi chuỗi mgs đến toàn bộ các client khác khi có 1 client tham gia phòng chat
    clients[client] = decrypted_name # Lưu thông tin của client vào dictionary clients, sử dụng client làm key và decrypted_name làm giá trị.
    #Lặp vô hạn
    while True:
        msg = client.recv(BUFSIZ) # Lấy chuỗi tin nhẵn client gởi lên server lưu vào biên msg
        if msg != bytes("{quit}", "utf8"):
            # Kiểm tra nếu tin nhắn được mã hóa chứa chuỗi [hqfubsw] (Đây là chuỗi encrypt được client gắn vào trước khi gởi lên cho server để đánh dấu tin nhắn đã được mã hóa thành công)
            if b"[hqfubsw]" in msg:
                decrypt_msg = caesar_decrypt(msg.decode("utf8"), shift=3)# Giải mã msg
                broadcast(bytes(decrypt_msg, "utf8"), decrypted_name + ": ")# Gởi lại cho tất cả client tham gia chat
            else:
                broadcast(msg, decrypted_name + ": ")# Nếu không chứa chuỗi trên thì thực hiện gởi thẳng tin nhẵn chưa được mã hóa cho các client khác
        else: #Nếu client thoát thì đóng chương trinh và thông báo cho tất cả client còn lại
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s đã thoát phòng chat." % decrypted_name, "utf8"))
            break


# Hàm gửi tin tin nhắn đến tất cả các client khác
def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}  # Lưu trữ các clients kết nối và tên của họ
addresses = {}  # Lưu trữ địa chỉ của các clients

HOST = '127.0.0.1'  # Địa chỉ IP kết nối
PORT = 33000  # Cổng kết nối
BUFSIZ = 1024  # Kích thước tối đa của các gói tin
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)  # Giới hạn số clients kết nối là 5
    print("Chờ kết nối từ các client...")
    # Tạo một luồng mới để chạy hàm accept_incoming_connections.
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    # Bắt đầu luồng để chấp nhận kết nối.
    ACCEPT_THREAD.start()
    # Đợi luồng này kết thúc trước khi tiếp tục thực thi mã chính.
    ACCEPT_THREAD.join()
    SERVER.close()
