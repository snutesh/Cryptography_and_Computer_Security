import numpy

#Global Variables
ciphertext = ""
keymatrix = []
plaintextmatrix = []
ciphertextmatrix = []

#Function to calculate multiplicative inverse
def multiplicativemodinverse(base):
    
    for x in range(1, 26):
        if (((base%26) * (x%26)) % 26 == 1):
            return x
    return -1

def getkeymatrix ():
    k = -1;
#Get Key Matrix as User Input
    for i in range (keysize):
        temp = []
        for j in range (keysize):
            k = k + 1
            element = int(keyfile[k])
            temp.append (element)
        keymatrix.append (temp)
    print("Keymatrix :")
    print (keymatrix)

#Function to Calculate Modular Multiplicative Inverse of Key Matrix
def matrixinverse() :
#Find the Multiplicative Inverse Modulo m of Determinant
    detinverse = multiplicativemodinverse(determinant)
#    print("detinverse :")
#    print(detinverse)
#Find the Cofactor of Key Matrix
    adjointmatrix = numpy.linalg.inv(keymatrix) * determinant
#    cofactormatrix = cofactormatrix.astype(int)
#    print("adjoint matrix :")
#    print(adjointmatrix)
#Multiply Cofactor Matrix with Determinant Inverse
    invkeymatrix = adjointmatrix * detinverse
#    print(invkeymatrix)
    invkeymatrix = numpy.mod(invkeymatrix, 26)
    return(invkeymatrix)

#Function to Perform Encryption
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
    
ctfilename = input("Enter name of cipher text input file: ")
inputFile = open(ctfilename, "r")
ciphertext = inputFile.read();
keysize = int (input ("Enter Size of Key Matrix (Order) : "))
#Function to Get Key Matrix
kmfile = input("Enter key matrix input file: ")
IF = open(kmfile,"r")
keyfile = IF.readlines();
#Get Plain Text as User Input
#ciphertext = input ("Enter Cipher Text : ")
ciphertext = ciphertext.replace(" ","")
ciphertext = ciphertext.upper()
#Get Size of Key Matrix
#keysize = int (input ("Enter Size of Key Matrix (Order) : "))
#Check if Dummy Character is Needed to Append at last of Plain Text
appendsize = len(ciphertext)%keysize
if appendsize != 0 :
    appendsize = keysize - appendsize
#    print(appendsize)
    for i in range(appendsize):
        ciphertext = ciphertext + "Z"

print("Ciphertext is :")
print(ciphertext)
#Call Function to Get Key Matrix
getkeymatrix()

#Check if Key Matrix is valid or not by calculating determinant
determinant = int(numpy.linalg.det (keymatrix))
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
    
print("Decrypting Cipher Text......")
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