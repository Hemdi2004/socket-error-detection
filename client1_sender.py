import socket
import crcmod
import struct

# ------------------ CONFIG ------------------
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

# ------------------ UTILITIES ------------------
def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

# ---------- PARITY ----------
def parity_bit(text, mode="even"):
    bits = text_to_bits(text)
    ones = bits.count("1")
    if mode == "even":
        return "0" if ones % 2 == 0 else "1"
    else:
        return "1" if ones % 2 == 0 else "0"

# ---------- 2D PARITY ----------
def parity_2d(text):
    bits = text_to_bits(text)
    matrix = [bits[i:i+8] for i in range(0, len(bits), 8)]

    row_parity = ''.join(str(row.count("1") % 2) for row in matrix)

    col_parity = ""
    for col in range(8):
        col_bits = [row[col] for row in matrix if len(row) == 8]
        col_parity += str(col_bits.count("1") % 2)

    return row_parity + "|" + col_parity

# ---------- CRC16 ----------
crc16_func = crcmod.predefined.mkCrcFun("crc-ccitt-false")

def crc16(text):
    return hex(crc16_func(text.encode()))[2:].upper()

# ---------- HAMMING (7,4) ----------
def hamming74(bits4):
    d1, d2, d3, d4 = map(int, bits4)
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    return f"{p1}{p2}{d1}{p3}{d2}{d3}{d4}"

def hamming_encode(text):
    bits = text_to_bits(text)
    blocks = [bits[i:i+4] for i in range(0, len(bits), 4)]
    return ''.join(hamming74(b) for b in blocks if len(b) == 4)

# ---------- INTERNET CHECKSUM ----------
def internet_checksum(text):
    data = text.encode()
    if len(data) % 2 != 0:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        word = data[i] << 8 | data[i+1]
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return hex(~checksum & 0xFFFF)[2:].upper()

# ------------------ MAIN ------------------
print("Choose method:")
print("1. PARITY")
print("2. 2D_PARITY")
print("3. CRC16")
print("4. HAMMING")
print("5. CHECKSUM")

choice = input("Choice: ")
text = input("Enter text: ")

if choice == "1":
    method = "PARITY"
    control = parity_bit(text)
elif choice == "2":
    method = "2D_PARITY"
    control = parity_2d(text)
elif choice == "3":
    method = "CRC16"
    control = crc16(text)
elif choice == "4":
    method = "HAMMING"
    control = hamming_encode(text)
elif choice == "5":
    method = "CHECKSUM"
    control = internet_checksum(text)
else:
    raise ValueError("Invalid choice")

packet = f"{text}|{method}|{control}"

sock = socket.socket()
sock.connect((SERVER_HOST, SERVER_PORT))
sock.send(packet.encode())
sock.close()

print("Packet sent:", packet)
