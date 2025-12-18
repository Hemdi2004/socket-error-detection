import socket
import crcmod

HOST = "127.0.0.1"
PORT = 6000

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def parity_bit(text):
    return "0" if text_to_bits(text).count("1") % 2 == 0 else "1"

def parity_2d(text):
    bits = text_to_bits(text)
    rows = [bits[i:i+8] for i in range(0,len(bits),8)]
    row_p = ''.join(str(r.count("1") % 2) for r in rows)
    col_p = ''.join(str(sum(int(r[i]) for r in rows if len(r)==8)%2) for i in range(8))
    return row_p + "|" + col_p

crc16_func = crcmod.predefined.mkCrcFun("crc-ccitt-false")

def crc16(text):
    return hex(crc16_func(text.encode()))[2:].upper()

def internet_checksum(text):
    data = text.encode()
    if len(data)%2: data += b'\x00'
    checksum = 0
    for i in range(0,len(data),2):
        checksum += (data[i]<<8)+data[i+1]
        checksum = (checksum & 0xFFFF)+(checksum>>16)
    return hex(~checksum & 0xFFFF)[2:].upper()

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)
print("Client 2 listening...")

conn,_ = server.accept()
packet = conn.recv(4096).decode()
conn.close()

data, method, incoming = packet.split("|")

if method == "PARITY":
    computed = parity_bit(data)
elif method == "2D_PARITY":
    computed = parity_2d(data)
elif method == "CRC16":
    computed = crc16(data)
elif method == "CHECKSUM":
    computed = internet_checksum(data)
else:
    computed = "N/A"

print("Received Data :", data)
print("Method :", method)
print("Sent Check Bits :", incoming)
print("Computed Check Bits :", computed)

if incoming == computed:
    print("Status : DATA CORRECT")
else:
    print("Status : DATA CORRUPTED")
