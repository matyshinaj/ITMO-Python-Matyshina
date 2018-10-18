L = ('A','B', 'C', 'D', 'E', 'F', 'G','H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
l = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
def encrypt_vigenere(plaintext:str, keyword:str) -> str:
    ciphertext = ''
    keyword *= (len(plaintext)//len(keyword)) + 1
    for index, element in enumerate(plaintext):
        if element in (L):
            ciphertext += chr((ord(element)+ord(keyword[index])) % 26 + ord('A'))
        elif element in (l):
            ciphertext += chr((ord(element) + ord(keyword[index])) % 26 + ord('a'))
        else:
            ciphertext += element
    return ciphertext


def decrypt_vigenere(ciphertext:str, keyword:str) -> str:
    plaintext = ''
    keyword *= (len(ciphertext) // len(keyword)) + 1
    for index, element in enumerate(ciphertext):
        if element in (L):
            plaintext += chr((ord(element) - ord(keyword[index])) % 26 + ord('A'))
        elif element in (l):
            plaintext += chr((ord(element) - ord(keyword[index])) % 26 + ord('a'))
        else:
            plaintext += element
    return plaintext
