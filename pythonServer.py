import os
from socket import *
# Function:
# Date of code (Last upInedt: 
# Output: r: 
# Description: 
# Input: 
# Output: 
#Obtains file from remote server
def downloadFile():
    filename = 'fileName.txt'
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 4096)
    ftp.quit()
    localfile.close()

#Places a file
def uploadFile():
    filename = 'fileName.txt'
    ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
    ftp.quit()

def runServer():
    print("Running server")

    #Initiate port
    inputPortNumber = int(input("Enter the port number: "))
    inputHostName = ''
    bindedHostNum = (inputHostName, inputPortNumber)
    
    #create TCP socket
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Bind socket to port
    serverSocket.bind(bindedHostNum)

    #Listens for incoming connection
    serverSocket.listen(1)

    print("Server listening....")

    #Waits for connection
    while(1):
        #Accept conncetion
        connectionSocket, addr = serverSocket.accept()

        #Recieve whatever the newly connected client has to send
        temporaryBuffer = ""
        data = ""

        length = connectionSocket.recv(1024)

        while len(data) != 40:
            #Receive whatever connected client sends
            temporaryBuffer = connectionSocket.recv(40)

            #OTher side unexpectedly closes
            if not temporaryBuffer:
                break
            #Save data
            data += temporaryBuffer

    print(data)

    #Close socket
    connectionSocket.close()

runServer()
