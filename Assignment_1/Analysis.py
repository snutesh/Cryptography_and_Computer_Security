import numpy
import math

detinverseexist = 1
#Function to caculate multiplicative modulo inverse
def multiplicativemodinverse(base):
    
    for x in range(1, 26):
        if (((base%26) * (x%26)) % 26 == 1):
            return x
    return -1

#Function to Calculate Modular Multiplicative Inverse of Plain Text
def matrixinverse(determinant, matrix) :
#Find the Multiplicative Inverse Modulo m of Determinant
    detinverse = multiplicativemodinverse(determinant)
#    if (detinverse == -1) :
#        return 
    print("detinverse :")
    print(detinverse)
#Find the Adjoint of Key Matrix
    adjointmatrix = numpy.linalg.inv(matrix) * determinant
    print("adjoint matrix :")
    print(adjointmatrix)
#Multiply Cofactor Matrix with Determinant Inverse
    invmatrix = adjointmatrix * detinverse
    print(invmatrix)
    invmatrix = numpy.mod(invmatrix, 26)
    return(invmatrix)

#Function to Perform Decryption
def decryption (ciphertext, keysize, inversekeymatrix):
    cipherarray = []
    ptmatrix = []
    appendsize = len(ciphertext)%keysize
    if appendsize != 0 :
        appendsize = keysize - appendsize
        print(appendsize)
    for i in range(appendsize):
        ciphertext = ciphertext + "Z"
    for i in ciphertext:
        cipherarray.append(int(ord(i))-65)
    ciphertextmatrix = numpy.reshape(cipherarray,(-1, keysize))
    print("ciphertextmatrix :")
    print(ciphertextmatrix)
    for i in ciphertextmatrix:
        temprow = numpy.dot(inversekeymatrix, i)
        ptmatrix.append(temprow)
    ptmatrix = numpy.mod(ptmatrix,26)
    print("plaintextmatrix :")
    print(ptmatrix)
    return(ptmatrix)

#Function to convert string to square matrix
def getmatrix(plaintext, ciphertext, keysize, i) :
    stringarray = []
    cipherarray = []
    plaintextmatrix = []
    ciphertextmatrix = []
    print("value of i")
    print(i)
    for j in range(keysize*keysize) :
        stringarray.append(int(ord(plaintext[i]))-65)
        cipherarray.append(int(ord(ciphertext[i]))-65)
        i = i + 1
    plaintextmatrix = numpy.reshape(stringarray,(-1, keysize))
    ciphertextmatrix = numpy.reshape(cipherarray,(-1, keysize))
    print("plaintextmatrix :")
    print(plaintextmatrix)
    print("ciphertextmatrix :")
    print(ciphertextmatrix)

    return (plaintextmatrix, ciphertextmatrix)

#Analysis Function
def analysis(plaintext, ciphertext) :
    keysize = 2
    while (keysize <= 10) :
        i = 0

        while (i < len(plaintext)) :
            plaintextmatrix, ciphertextmatrix = getmatrix(plaintext, ciphertext, keysize,i )
            print("analysis function call.....")
            print("plaintextmatrix :")
            print(plaintextmatrix)
            print("ciphertextmatrix :")
            print(ciphertextmatrix)
            ptdeterminant = round(numpy.linalg.det(plaintextmatrix))
            print("ptdeterminant :")
            print(ptdeterminant)
            while (ptdeterminant == 0) :
                i = i + keysize*keysize
                if(i < (len(plaintext)-keysize*keysize)) :
                    plaintextmatrix, ciphertextmatrix = getmatrix(plaintext, ciphertext, keysize, i)
                    ptdeterminant = round(numpy.linalg.det(plaintextmatrix))
            invptmatrix = matrixinverse(ptdeterminant, plaintextmatrix)
            print("invptmatrix :")
            print(invptmatrix)
            keymatrix = numpy.dot(ciphertextmatrix, invptmatrix)
            print("keymatrix :")
            print(keymatrix)
            keymatrix = numpy.mod(keymatrix, 26)
            keydeterminant = round(numpy.linalg.det(keymatrix))
            print("keydeterminant :")
            print(keydeterminant)
            if(keydeterminant == 0) :
                i = i + keysize*keysize
                continue
            inversekeymatrix = matrixinverse(keydeterminant, keymatrix)
            print("inversekeymatrix :")
            print(inversekeymatrix)
    #        if (detinverseexist == 0) :
    #            i = i + 1
    #            continue
            newplaintextmatrix = decryption(ciphertext, keysize, inversekeymatrix)
            print("newplaintext :")
            print(newplaintextmatrix)
            stringarray = newplaintextmatrix.ravel()
            #print(stringarray)
            newplaintext = ""
            for j in stringarray:
                j = round(j + 65)
            #    print(j)
                newplaintext = newplaintext + chr(j)
            frequency = 0
            for k in set(newplaintext) :
                frequency = frequency + (newplaintext.count(k) * (newplaintext.count(k)-1))
            IC = (1/(len(newplaintext)*(len(newplaintext)-1)))*frequency
            if math.isclose(0.067, IC, abs_tol = 0.002) :
                print("Assumed Key Size" + keysize + "is correct")
                return
            print(IC)
        keysize = keysize + 1
#Reading inputs from file
ptfilename = input("Enter name of plain text input file: ")
plaintextfile = open(ptfilename, "r")
plaintext = plaintextfile.read();
plaintext = plaintext.replace(" ","")
plaintext = plaintext.replace(".","")
plaintext = plaintext.upper()
ctfilename = input("Enter name of cipher text input file: ")
ciphertextfile = open(ctfilename, "r")
ciphertext = ciphertextfile.read();
ciphertext = ciphertext.replace(" ","")
ciphertext = ciphertext.replace(".","")
ciphertext = ciphertext.upper()
analysis(plaintext, ciphertext)
