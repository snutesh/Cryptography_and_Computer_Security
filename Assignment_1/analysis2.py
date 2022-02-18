import numpy
import math

def multiplicativemodinverse(base):
    
    for x in range(1, 26):
        if (((base%26) * (x%26)) % 26 == 1):
            return x
    return -1

def getmatrix(stringarray, cipherarray, keysize) :
    ciphertextmatrix = numpy.reshape(cipherarray,(-1, keysize))
    plaintextmatrix = numpy.reshape(stringarray, (-1, keysize))
    return (plaintextmatrix, ciphertextmatrix)        

def matrixinverse(matrix, determinant, detinverse) :
#Find the Cofactor of Key Matrix
    adjointmatrix = numpy.linalg.inv(matrix) * determinant
#Multiply Cofactor Matrix with Determinant Inverse
    invmatrix = adjointmatrix * detinverse
    invmatrix = numpy.mod(invmatrix, 26)
    return invmatrix.round()

def decryption (ciphertextmatrix, inversekeymatrix):
    cipherarray = []
    ptmatrix = []
    for i in ciphertextmatrix:
        temprow = numpy.dot(inversekeymatrix, i)
        ptmatrix.append(temprow)
    ptmatrix = numpy.mod(ptmatrix,26)
    return(ptmatrix)

#Reading inputs from file
ptfilename = input("Enter name of plain text input file: ")
plaintextfile = open(ptfilename, "r")
plaintext = plaintextfile.read();
plaintext = plaintext.replace(" ","")
plaintext = plaintext.replace(".","")
plaintext = plaintext.upper()
stringarray = []
for i in plaintext:
    stringarray.append(int(ord(i)) - 65)
ctfilename = input("Enter name of cipher text input file: ")
ciphertextfile = open(ctfilename, "r")
ciphertext = ciphertextfile.read();
ciphertext = ciphertext.replace(" ","")
ciphertext = ciphertext.replace(".","")
ciphertext = ciphertext.upper()
cipherarray = []
for i in ciphertext:
    cipherarray.append(int(ord(i)) - 65)
#print(stringarray)
#print(cipherarray)
flag = True
for keysize in range(2, 11) :
    if flag == False :
        break
    j = 0
    while(j <= (len(plaintext)-(keysize*keysize))) :
        plaintextmatrix, ciphertextmatrix = getmatrix(stringarray, cipherarray, keysize)
        tempptmat = plaintextmatrix[j:j+keysize, :]
        tempctmat = ciphertextmatrix[j:j+keysize, :]
    #    print(tempptmat)
    #    print(tempctmat)
        ptdeterminant = numpy.linalg.det(tempptmat)
        ptdetinverse = multiplicativemodinverse(ptdeterminant)
    #    print(determinant)
    #    print(detinverse)

        if ptdeterminant != 0 and ptdetinverse != -1 :
            invptmat = matrixinverse(tempptmat, ptdeterminant, ptdetinverse)
            keymatrix = tempctmat@invptmat
            keymatrix = numpy.round(keymatrix)
            keymatrix = keymatrix.astype(int)
            keymatrix = numpy.mod(keymatrix, 26)
            keydeterminant = numpy.linalg.det(keymatrix)
            keydetinverse = multiplicativemodinverse(keydeterminant)
    #        print("keydeterminant = ")
    #        print(keydeterminant)
    #        print("keydetinverse = ")
    #        print(keydetinverse)
            if keydeterminant !=0 and keydetinverse != -1 :
                invkeymat = matrixinverse(keymatrix, keydeterminant, keydetinverse)
                print(invkeymat)
                newptmatrix = decryption(ciphertextmatrix, invkeymat)
                newptmatrix = newptmatrix.astype(int)
                newstringarray = newptmatrix.ravel()
                #print(stringarray)
                newplaintext = ""
                for i in newstringarray:
                    j = round(i + 65)
                #    print(j)
                    newplaintext = newplaintext + chr(j)
                print("New plain text :")
                print(newplaintext)
                frequency = 0
                for k in set(newplaintext) :
                    frequency = frequency + (newplaintext.count(k) * (newplaintext.count(k)-1))
                IC = (1/(len(newplaintext)*(len(newplaintext)-1)))*frequency
                print(IC)
                if IC >= 0.067 :
                    print("Assumed Key Size is correct")
                    
                    print(keysize)
                    flag = False
                    break
                else :
                    keysize = keysize + 1
                    continue
            else :
                j = j + keysize
                continue 
        else :
            j = j + keysize
            continue
    
    