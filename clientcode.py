import socket

SECRET_KEY = b'farhana10022025p'

def initialize_sbox(key):
    sbox = list(range(256))
    j = 0
    for i in range(256):
        j = (j + sbox[i] + key[i % len(key)]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
    return sbox

def generate_keystream(sbox, data_length):
    i = j = 0
    keystream = []
    for _ in range(data_length):
        i = (i + 1) % 256
        j = (j + sbox[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
        keystream.append(sbox[(sbox[i] + sbox[j]) % 256])
    return keystream

def rc4_cipher(data, key):
    key = list(key)  # Convert byte key into a list of integers
    sbox = initialize_sbox(key)
    keystream = generate_keystream(sbox, len(data))
    return bytes([data[i] ^ keystream[i] for i in range(len(data))])

def send_file_encrypted(filepath, server_ip='127.0.0.1', server_port=12345):
    with open(filepath, 'rb') as file:
        plaintext = file.read()

    encrypted_content = rc4_cipher(plaintext, SECRET_KEY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((server_ip, server_port))
        client_sock.sendall(encrypted_content)
        print("File encrypted and sent successfully.")

send_file_encrypted('plain_text.txt')
