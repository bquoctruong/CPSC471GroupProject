from socket import *
import os

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

def runClient():
    print("Running client")

    #Get hostname and port
    inputHost = str(input("Enter the host name: "))
    inputPortNumber = int(input("Enter the port number: "))
    bindHostNumber = (inputHost, inputPortNumber)

    #Create socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    #Connect to server
    clientSocket.connect(bindHostNumber)

    #Data sent
    data = "Hello world! This is a very long string"

    #Bytes
    bytesSent = 0

    #Send string
    while bytesSent != len(data):
        #Send data
        bytesSent += clientSocket.send(data[bytesSent:])

    #Close socket
    clientSocket.close()

runClient()

#Resources: https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python