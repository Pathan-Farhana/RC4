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
    key = list(key)  
    sbox = initialize_sbox(key)
    keystream = generate_keystream(sbox, len(data))
    return bytes([data[i] ^ keystream[i] for i in range(len(data))])

def start_server(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((host, port))
        server_sock.listen()
        print(f"Server listening on {host}:{port}...")

        conn, addr = server_sock.accept()
        with conn:
            print(f"Connected by {addr}")

            encrypted_data = conn.recv(4096)  
            print("Encrypted data received.")

            
            with open("received_encrypted_file.txt", "wb") as enc_file:
                enc_file.write(encrypted_data)
            print("Encrypted file saved as 'received_encrypted_file.txt'.")

            
            decrypted_data = rc4_cipher(encrypted_data, SECRET_KEY)


            with open("decrypted_file.txt", "wb") as dec_file:
                dec_file.write(decrypted_data)
            print("Decrypted file saved as 'decrypted_file.txt'.")


start_server()
