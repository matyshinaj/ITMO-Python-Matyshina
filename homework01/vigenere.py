def encrypt_vigenere(plaintext:str, keyword:str) -> str:
    ciphertext = ''
    keyword *= (len(plaintext)//len(keyword)) + 1
    for index, element in enumerate(plaintext):
        if element.isupper():
            ciphertext += chr((ord(element)+ord(keyword[index])) % 26 + ord('A'))
        elif element.islower():
            ciphertext += chr((ord(element) + ord(keyword[index])) % 26 + ord('a'))
        else:
            ciphertext += element
    return ciphertext


def decrypt_vigenere(ciphertext:str, keyword:str) -> str:
    plaintext = ''
    keyword *= (len(ciphertext) // len(keyword)) + 1
    for index, element in enumerate(ciphertext):
        if element.isupper():
            plaintext += chr((ord(element) - ord(keyword[index])) % 26 + ord('A'))
        elif element.islower():
            plaintext += chr((ord(element) - ord(keyword[index])) % 26 + ord('a'))
        else:
            plaintext += element
    return plaintext
