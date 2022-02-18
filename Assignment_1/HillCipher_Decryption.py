import numpy

#Global Variables
ciphertext = ""
keymatrix = []
plaintextmatrix = []
ciphertextmatrix = []

#Function to Get Key Matrix
def getkeymatrix ():
#Get Key Matrix as User Input
    print ("Enter the Key Matrix in Row Major Order : ")
    for i in range (keysize):
        temp = []
        for j in range (keysize):
            element = int(input())
            temp.append (element)
        keymatrix.append (temp)
#Print Key Matrix
#    print("keymatrix :")
#    print (keymatrix)

#Function to Calculate Modular Multiplicative Inverse of Key Matrix
def matrixinverse() :
#Find the Multiplicative Inverse Modulo m of Determinant
    detinverse = pow(determinant, -1, 26)
#    print("detinverse :")
#    print(detinverse)
#Find the Cofactor of Key Matrix
    adjointmatrix = numpy.linalg.inv(keymatrix) * determinant
#    cofactormatrix = cofactormatrix.astype(int)
#    print("adjoint matrix :")
#    print(adjointmatrix)
#    print(cofactormatrix)    
#Multiply Cofactor Matrix with Determinant Inverse
    invkeymatrix = adjointmatrix * detinverse
#    print(invkeymatrix)
    invkeymatrix = numpy.mod(invkeymatrix, 26)
    return(invkeymatrix)

#Function to Perform Decryption
def decryption ():
    cipherarray = []
    ptmatrix = []
    for i in ciphertext:
        cipherarray.append(int(ord(i))-65)
    ciphertextmatrix = numpy.reshape(cipherarray,(-1, keysize))
#    print("ciphertextmatrix :")
#    print(ciphertextmatrix)
    for i in ciphertextmatrix:
        temprow = numpy.dot(inversekeymatrix, i)
        ptmatrix.append(temprow)
#    print("ptmatrix without mod :")
#    print(ptmatrix)
    ptmatrix = numpy.mod(ptmatrix,26)
#    print("plaintextmatrix :")
#    print(ptmatrix)
    return(ptmatrix)
    
#Get Plain Text as User Input
ciphertext = input ("Enter Cipher Text : ")
#ciphertext = ciphertext.replace(" ","")
ciphertext = ciphertext.upper()
#Get Size of Key Matrix
keysize = int (input ("Enter Size of Key Matrix (Order) : "))
#Check if Dummy Character is Needed to Append at last of Plain Text
#appendsize = len(plaintext)%keysize
#if appendsize != 0 :
#    appendsize = appendsize - keysize
#    for i in range(appendsize):
#        plaintext = plaintext + "Z"

#Convert String to 2D Array
nor = len(ciphertext)/keysize
#print("number of rows :")
#print(nor)

#Call Function to Get Key Matrix
getkeymatrix()

#Check if Key Matrix is valid or not by calculating determinant
determinant = int(numpy.linalg.det (keymatrix))
#determinant = int(numpy.mod(determinant, 26))
#print("determinant :")
#print(determinant)
if determinant == 0:
    print ("Key Matrix is invalid, please enter again")
    getkeymatrix()
else:
    print("Key Matrix is Valid")
inversekeymatrix = matrixinverse()
#print("inversekeymatrix :")
#print(inversekeymatrix)
    
print("Decrypting Cipher Text")
plaintextmatrix = decryption()
stringarray = plaintextmatrix.ravel()
#print(stringarray)
plaintext = ""
for i in stringarray:
    j = round(i + 65)
#    print(j)
    plaintext = plaintext + chr(j)

#Print the Output
print("Plain Text is :")
print(plaintext)

#====== END OF PROGRAM ==========