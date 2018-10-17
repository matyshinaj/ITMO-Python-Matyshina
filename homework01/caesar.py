def encrypt_caesar(plaintext:str) -> str:

    cliphertext = ''
    for i in range(len(plaintext)):
        if ord('a')<= ord(plaintext[i])<=ord('z'):
            s = ord(plaintext[i]) + 3
            if s > ord('z'):
                s -= 26
            cliphertext += chr(s)
        elif ord('A') <= ord(plaintext[i]) <= ord('Z'):
            p = ord(plaintext[i]) + 3
            if p > ord('z'):
                p -= 26
            cliphertext += chr(p)
        else:
            cliphertext += plaintext[i]
            
    return cliphertext

def decrypt_caesar(ciphertext:str) -> str:

    plaintext=''
    for i in range(len(ciphertext)):
        if ord('a')<= ord(ciphertext[i])<=ord('z'):
            s = ord(ciphertext[i]) - 3
            if s < ord('a'):
                s += 26
            plaintext += chr(s)
        elif ord('A') <= ord(ciphertext[i]) <= ord('Z'):
            p = ord(ciphertext[i]) - 3
            if p < ord('A'):
                p += 26
            plaintext += chr(p)
        else:
            plaintext += ciphertext[i]

    return plaintext
