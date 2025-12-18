import socket
import random

HOST = "127.0.0.1"
PORT = 5000
CLIENT2_PORT = 6000

def corrupt_data(data):
    methods = [
        "bit_flip",
        "char_substitution",
        "char_deletion",
        "char_insertion",
        "swap"
    ]
    choice = random.choice(methods)

    if len(data) == 0:
        return data

    if choice == "bit_flip":
        bits = list(''.join(format(ord(c),'08b') for c in data))
        i = random.randint(0, len(bits)-1)
        bits[i] = '1' if bits[i] == '0' else '0'
        chars = [chr(int(''.join(bits[i:i+8]),2)) for i in range(0,len(bits),8)]
        return ''.join(chars)

    if choice == "char_substitution":
        i = random.randint(0, len(data)-1)
        return data[:i] + chr(random.randint(65,90)) + data[i+1:]

    if choice == "char_deletion":
        i = random.randint(0, len(data)-1)
        return data[:i] + data[i+1:]

    if choice == "char_insertion":
        i = random.randint(0, len(data))
        return data[:i] + chr(random.randint(65,90)) + data[i:]

    if choice == "swap" and len(data) > 1:
        i = random.randint(0, len(data)-2)
        return data[:i] + data[i+1] + data[i] + data[i+2:]

    return data

# ---------------- SERVER ----------------
server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)
print("Server running...")

conn, _ = server.accept()
packet = conn.recv(4096).decode()
conn.close()

data, method, control = packet.split("|")
corrupted_data = corrupt_data(data)

new_packet = f"{corrupted_data}|{method}|{control}"

client2 = socket.socket()
client2.connect((HOST, CLIENT2_PORT))
client2.send(new_packet.encode())
client2.close()

print("Original:", data)
print("Corrupted:", corrupted_data)
