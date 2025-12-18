# Socket Programming Assignment – Error Detection Methods

This project demonstrates data transmission with error detection techniques using
Python socket programming.

## 📌 Project Description

The system consists of three components:

1. **Client 1 – Data Sender**
   - Takes text input from the user
   - Generates control information using:
     - Parity Bit
     - 2D Parity
     - CRC-16
     - Hamming Code
     - Internet Checksum
   - Sends packet in the format:
     ```
     DATA|METHOD|CONTROL_INFORMATION
     ```

2. **Server – Intermediate Node + Data Corruptor**
   - Receives packet from Client 1
   - Injects random transmission errors
   - Forwards corrupted packet to Client 2

3. **Client 2 – Receiver + Error Checker**
   - Recomputes control information
   - Compares received and computed values
   - Detects data corruption

---

## ⚙️ Requirements

- Python 3.8+
- Required library:
```bash
pip install crcmod
# socket-error-detection
