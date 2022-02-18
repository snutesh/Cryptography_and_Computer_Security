import gmpy2 as mp
import numpy as np
import math

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

def file_writer (file_name, text):
    print('Writing to the file in the directory')   
    file1 = open(file_name, 'w')
    file1.write(text)
    file1.close()
    return

def gen_strong_prime (bits):
    print( "Using Gordon's algorithm to generate strong primes")
    b = round(bits/2)
    s = mp.next_prime(2**b)
    b = b + 1 
    t = mp.next_prime(2**b)
    r = mp.next_prime(t)
    u = mp.powmod(mp.mpz(s), r-2, r)
    p0 = 2*mp.mul(u, s) -1
    prp= mp.next_prime(p0 + 2*mp.mul(r,s))
    print('Verifying if the generated prime number is strong prime')
    strong_prime = False
    prp = mp.next_prime(2**bits)
    while not strong_prime:
        if mp.is_strong_prp(prp, 2):
            strong_prime = True
        elif not mp.is_strong_prp(prp, 2):
            prp = mp.next_prime(prp)
        return prp

def RSA_key (bits):
    print('Generating public and private key')
    b = round(bits/2)
    p = gen_strong_prime(b) 
    b = b + 1
    q = gen_strong_prime(b) 
    n = mp.mul(p, q)
    phi = mp.mul(p-1, q-1)
    e = 3
    while e < phi:
        if mp.gcd (e, phi) == 1:
            break
        else:
            e = e + 1
    d = mp.invert(e, phi)
    return e, n, d


def CA_dig_sign (key):
    print('Signing the document digitally by CA by his private key')
    pvt_key = file_reader("pvt_ca.txt").split()
    d = mp.mpz(pvt_key[0])
    n = mp.mpz(pvt_key[1])
    return mp.powmod(key, d, n)

def publish_key ():
    print('Publishing the CA signed public keys in the public directory and sending keys to respective users')
    # Generate Keys for CA, Sender and Receiver
    e_CA, n_CA, d_CA = RSA_key(1028)
    bits = 1024
    e_A, n_A, d_A = RSA_key(bits)
    e_B, n_B, d_B = RSA_key(bits)
    
    pvt_ca = str(d_CA) + " " + str(n_CA)
    file_writer("pvt_ca.txt", pvt_ca)

    pub_ca = str(e_CA) + " " + str(n_CA)
    file_writer("pub_ca.txt", pub_ca)
    
    # Digitally Sign all the keys
    e_A_ds = CA_dig_sign(e_A)
    e_B_ds = CA_dig_sign(e_B)
    d_A_ds = CA_dig_sign(d_A)
    d_B_ds = CA_dig_sign(d_B)
    n_A_ds = CA_dig_sign(n_A)
    n_B_ds = CA_dig_sign(n_B)

    # Write Keys to Files
    
    pub_a = str(e_A_ds) + " " + str(n_A_ds) + " " + str(e_A) + " " + str(n_A)    
    file_writer("pub_a.txt", pub_a)
    pub_b = str(e_B_ds) + " " + str(n_B_ds) + " " + str(e_B) + " " + str(n_B)
    file_writer("pub_b.txt", pub_b)
    
    pvt_a = str(d_A_ds) + " " + str(n_A_ds)+ " " + str(d_A) + " " + str(n_A)
    file_writer("pvt_a.txt", pvt_a)
    pvt_b = str (d_B_ds) + " " + str(n_B_ds) + " " + str(d_B) + " " + str(n_B)
    file_writer("pvt_b.txt", pvt_b) 
    return

if __name__ == '__main__':
    publish_key()



