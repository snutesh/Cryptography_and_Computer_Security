import gmpy2 as mp
import numpy as np
import math

block_length = 0
char_to_int = {}
int_to_char = {}
char_space = 29

def file_reader (file_name):
    print('Reading the file from the directory')
    text = ""
    file1 = open(file_name, 'r')
    text = file1.read()
    text = text.replace('\n', '')
    text = text.replace("'", "")
    text = text.replace('?', "") 
    file1.close()
    return text.lower()

def file_writer(file_name, text):
    '''Write to File from the directory'''
    file1 = open(file_name,'w')
    file1.write(text)
    file1.close()
    return

def chartoint_dictionary():  
    '''Creates a dictionary of characters from a-z and maps each of them to numbers from 0-25'''
    chartoint_dictionary = {"a":0}
    ch = 'a'
    chartoint_dictionary['.'] = 26
    chartoint_dictionary[' '] = 27
    chartoint_dictionary[','] = 28
    for i in range(0,26):
        chartoint_dictionary[ch] = i
        ch = chr(ord(ch) + 1)
    return chartoint_dictionary

def inttochar_dictionary():  
    '''Creates a dictionary of numbers from 0-25 and maps each of them to characters from a-z'''
    inttochar_dictionary = {0:'a'}
    ch = 'a'
    inttochar_dictionary[26] = '.'
    inttochar_dictionary[27] = ' '
    inttochar_dictionary[28] = ','    
    for i in range(0,26):
        inttochar_dictionary[i] = ch
        ch = chr(ord(ch) + 1)
    return inttochar_dictionary

def block_size(n):
    r = 0
    while mp.mpz(char_space)**r < mp.mpz(n):
        r = r + 1
    return r

def get_msgblock(text, l):
    '''Returns list of message blocks of length l'''
    message_blocks = []
    temporary_blocks = ""
    
    for char in text:
        temporary_blocks = temporary_blocks + char
        if(len(temporary_blocks) == l):
            message_blocks.append(temporary_blocks)
            temporary_blocks = ""
    message_blocks.append(temporary_blocks) 
    return message_blocks

def unsign_CA(key):
    pub_key = file_reader("pub_" + "ca" + ".txt").split()
    e = mp.mpz(pub_key[0])
    n = mp.mpz(pub_key[1])
    
    return mp.powmod(key, e, n)    

def verify_sign(dSig):
    temp1 = unsign_CA(mp.mpz(dSig[0]))
    temp2 = unsign_CA(mp.mpz(dSig[1]))
    temp3 = mp.mpz(dSig[2])
    temp4 = mp.mpz(dSig[3])
    if temp1 == temp3 and temp2 == temp4:
        return True
    else:
        return False

def encrypt_vigenere(text, key):
    '''Encrypt the given message from vigenere cipher.'''
    
    message_blocks = get_msgblock(text, len(key))
    encrypt_message = ""
    for block in message_blocks:
        for i in range(len(block)):
            encrypt_message = encrypt_message + int_to_char[(char_to_int[block[i]] + char_to_int[key[i]])%char_space]
    
    return encrypt_message

def encrypt1_RSA(text):
    
    pvt_key = file_reader("pvt_a.txt").split()
    if verify_sign(pvt_key):
        print("CA SIGNATURE Verified. Hence Key is Valid\n")
    d = unsign_CA(mp.mpz(pvt_key[0]))
    n = unsign_CA(mp.mpz(pvt_key[1]))
    block_length = block_size(n)
    message_blocks = get_msgblock(text, block_length)
    if(len(message_blocks[-1]) != block_length):
        for i in range(block_length - len(message_blocks[-1])):
            message_blocks[-1] = message_blocks[-1] + int_to_char[np.random.randint(0, 2)]
            
    cipher_text = []
    for block in message_blocks:
        msg = 0
        for i in range(block_length):
            a = char_to_int[block[i]]
            b = mp.mpz(char_space)**(block_length -1 -i)
            msg = msg + mp.mul(a, b)
        eMsg = mp.mpz(mp.powmod(msg, d, n))
        cipher_text.append(eMsg)
      
    encrypt_message = ""
    for msg in cipher_text:
        remainder = mp.mpz(msg)
        m = []
        for i in range(block_length):
            temp = mp.mpz(char_space)**(block_length -1 -i)
            qt, remainder = mp.t_divmod(remainder, temp)
            m.append(int_to_char[qt])
        encrypt_message = encrypt_message + ''.join(m)
    return encrypt_message

def encrypt2_RSA(text):
    '''RSA Encryption'''

    pub_key = file_reader("pub_b.txt").split()
    if verify_sign(pub_key):
        print("\nCA SIGNATURE Verified. Hence Key is Valid")
    e = unsign_CA(mp.mpz(pub_key[0]))
    n = unsign_CA(mp.mpz(pub_key[1]))
    N = n
    block_length = block_size(N)
    message_blocks = get_msgblock(text, block_length)
    if(len(message_blocks[-1]) != block_length):
        for i in range(block_length - len(message_blocks[-1])):
            message_blocks[-1] = message_blocks[-1] + int_to_char[np.random.randint(0, 2)]
            
    cipher_text = []
    for block in message_blocks:
        msg = 0
        for i in range(block_length):
            a = char_to_int[block[i]]
            b = mp.mpz(char_space)**(block_length -1 -i)
            msg = msg + mp.mul(a, b)   
        eMsg = mp.powmod(mp.t_mod(msg, N), e, N)
        cipher_text.append(eMsg)
      
    encrypt_message = ""
    for msg in cipher_text:
        remainder = mp.mpz(msg)
        m = []
        for i in range(block_length):
            temp = mp.mpz(char_space)**(block_length -1 -i)
            qt, remainder = mp.t_divmod(remainder, temp)
            m.append(int_to_char[qt])
        encrypt_message = encrypt_message + ''.join(m)
    return encrypt_message
    
def send_message(msg):
    print("Encrypting Message using Vigenere Cipher\n")
    MsgEn_Vig = encrypt_vigenere(msg, vigenere_key)
    
    MsgForRSA = int_to_char[vigenere_key_length] + vigenere_key + MsgEn_Vig
    
    print("Encrypting Message using Sender's Secret Key \n")
    MsgEn_SenderPvtKey = encrypt1_RSA(MsgForRSA) 
    
    print("Encrypting Message using Receiver's Public Key \n")
    MsgEn_ReceiverPubKey = encrypt2_RSA(MsgEn_SenderPvtKey) 
    print("Sending Message.....")
    print("\nSent Message:\n", MsgEn_ReceiverPubKey)
    file_writer("sent_message.txt", MsgEn_ReceiverPubKey)
    return

if __name__ == '__main__':
    
    char_to_int = chartoint_dictionary() #Generate Characters to Number Dictionary
    int_to_char = inttochar_dictionary()

    print("Reading message and key from file")
    vigenere_key = file_reader("vigenere_key.txt") #read vigenere cipher key 
    vigenere_key_length = len(vigenere_key)
    Message = file_reader("message.txt") #Read Msg from message text file
    '''Send Secure Message'''
    send_message(Message) #Send Message With High Security