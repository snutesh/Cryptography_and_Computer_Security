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
    file1 = open(file_name,'w')
    file1.write(text)
    file1.close()
    return

def block_size(n):
    r = 0
    while mp.mpz(char_space)**r < mp.mpz(n):
        r = r + 1
    return r

def get_msgblock(text, l):
    message_blocks = []
    temporary_blocks = ""
    
    for char in text:
        temporary_blocks = temporary_blocks + char
        if(len(temporary_blocks) == l):
            message_blocks.append(temporary_blocks)
            temporary_blocks = ""
    message_blocks.append(temporary_blocks) 
    return message_blocks

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

def unsign_CA(key):
    pub_key = file_reader("pub_ca.txt").split()
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

def decrypt1_RSA(text):
    pvt_key = file_reader("pvt_b.txt").split()
    if verify_sign(pvt_key):
        print("\nCA SIGNATURE Verified. Hence Key is Valid")
    print("\nDecrypting by Receiver's Secret Key.")    
    d = unsign_CA(mp.mpz(pvt_key[0]))
    n = unsign_CA(mp.mpz(pvt_key[1]))
    block_length = block_size(n)
    message_blocks = get_msgblock(text, block_length)
    plain_text = []
    for block in message_blocks:
        msg = 0
        if len(block) != 0:
            for i in range(block_length):
                a = char_to_int[block[i]]
                b = mp.mpz(char_space)**(block_length -1 -i)
                msg = msg + mp.mul(a, b)
            plain_text.append(msg)
    decrypt_messageBlocks = []  
    for block in plain_text:
        remain = mp.mpz(mp.powmod(block, d, n))
        decrypt_messageBlocks.append(remain)
    plain_text = ""
    for msg in decrypt_messageBlocks:
        remainder = msg
        m = []
        for i in range(block_length):
            temp = mp.mpz(char_space)**(block_length -1 -i)
            qt, remainder = mp.t_divmod(remainder, temp)
            m.append(int_to_char[mp.t_mod(qt, char_space)])
        plain_text = plain_text + ''.join(m)
    return plain_text

def decrypt2_RSA(text):
    '''RSA Decryption'''    
    pub_key = file_reader("pub_a.txt").split()
    if verify_sign(pub_key):
        print("\nCA SIGNATURE Verified. Hence Key is Valid")
    else:
        print("\nCA SIGNATURE Verification Failed. Hence Key is invalid")
        return
    print("\nDecrypting by Sender's Public Key.")
    e = unsign_CA(mp.mpz(pub_key[0]))
    n = unsign_CA(mp.mpz(pub_key[1]))
    block_length = block_size(n)
    message_blocks = get_msgblock(text, block_length)
    plain_text = []
    for block in message_blocks:
        msg = 0
        if len(block) != 0:
            for i in range(block_length):
            	a = char_to_int[block[i]]
            	b = mp.mpz(char_space)**(block_length -1 -i)
            	msg = msg + mp.mul(a, b)
            plain_text.append(msg)
    decrypt_messageBlocks = []  
    for block in plain_text:
        remain = mp.powmod(mp.t_mod(block, n), e, n)
        decrypt_messageBlocks.append(remain)
    plain_text = ""
    for msg in decrypt_messageBlocks:
        remainder = msg
        m = []
        for i in range(block_length):
            temp = mp.mpz(char_space)**(block_length -1 -i)
            qt, remainder = mp.t_divmod(remainder, temp)
            m.append(int_to_char[mp.t_mod(qt, char_space)])
        plain_text = plain_text + ''.join(m)
    return plain_text

def rec_vigenere(text):
    vig_len = char_to_int[text[0]]
    vig_key = ""
    for i in range(vig_len):
        vig_key = vig_key + text[i+1]
    pl_text = text[vig_len+1:]
    return vig_key, pl_text

def decrypt_vignere(text, key):
    message_blocks = get_msgblock(text, len(key))
    decrypt_message = ""
    for block in message_blocks:
        for i in range(len(block)):
        	x = char_to_int[block[i]]
        	y = char_to_int[key[i]]
        	decrypt_message = decrypt_message + int_to_char[(x-y)%char_space]
    return decrypt_message

def receive():
    print("\n********RECEIVING & DECRYPTING SECURE MESSAGE********\n")
    '''Read Secure Message'''
    msgReceived = file_reader("sent_message.txt")
    
    '''Decrpyt the message with SECRET KEY of RECEIVER'''
    MsgDe_ReceiverPvtKey = decrypt1_RSA(msgReceived)
    
    '''Decrpyt the message with PUBLIC KEY of SENDER'''
    MsgDe_SenderPubKey = decrypt2_RSA(MsgDe_ReceiverPvtKey)
    
    vigkey, MsgEn_Vig = rec_vigenere(MsgDe_SenderPubKey)
    
    MsgDe_Vig = decrypt_vignere(MsgEn_Vig, vigkey)
    
    file_writer("received_message.txt", MsgDe_Vig)
    
    print("\nRecovered Message:\n", MsgDe_Vig)
    
    return

if __name__ == '__main__':
	char_to_int = chartoint_dictionary() #Generate Characters to Number Dictionary
	int_to_char = inttochar_dictionary() #Generate Numbers to Characters Dictionary
	receive()
