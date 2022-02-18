import numpy

#Global Variables
plaintext = ""
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
    print (keymatrix)

#Function to Perform Encryption
def encryption ():
    stringarray = []
    ctmatrix = []
    for i in plaintext:
        stringarray.append(int(ord(i))-65)
    plaintextmatrix = numpy.reshape(stringarray,(-1, keysize))
    for i in plaintextmatrix:
        temprow = numpy.dot(keymatrix, i)
        ctmatrix.append(temprow)
    ctmatrix = numpy.mod(ctmatrix,26)
 #   print(plaintextmatrix)
    return(ctmatrix)
    
#Get Plain Text as User Input
plaintext = input ("Enter Plain Text : ")
plaintext = plaintext.replace(" ","")
plaintext = plaintext.upper()
#Get Size of Key Matrix
keysize = int (input ("Enter Size of Key Matrix (Order) : "))
#Check if Dummy Character is Needed to Append at last of Plain Text
appendsize = len(plaintext)%keysize
if appendsize != 0 :
    appendsize = appendsize - keysize
    for i in range(appendsize):
        plaintext = plaintext + "Z"
#Convert String to 2D Array
nor = len(plaintext)/keysize

#Call Function to Get Key Matrix
getkeymatrix()

#Check if Key Matrix is valid or not by calculating determinant
determinant = numpy.linalg.det (keymatrix)
if determinant == 0:
    print ("Key Matrix is invalid, please enter again")
    getkeymatrix()
else:
    print("Key Matrix is Valid")
    
print("Encrypting Plain Text")
ciphertextmatrix = encryption()
#print(ciphertextmatrix)
#cipherarray = ciphertextmatrix.reshape([1, -1])
cipherarray = ciphertextmatrix.ravel()
#print(cipherarray)
ciphertext = ""
for i in cipherarray:
    i = i + 65
    ciphertext = ciphertext + chr(i)

#Print the Output
print(ciphertext)

#====== END OF PROGRAM ==========