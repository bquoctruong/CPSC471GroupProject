import os
from socket import *
import socket
import threading
import ftplib
# Function:
# Date of code (Last upInedt: 
# Output: r: 
# Description: 
# Input: 
# Output: 
#Obtains file from remote server
def downloadFileFTP():
    filename = 'fileName.txt'
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 4096)
    ftp.quit()
    localfile.close()

#Places a file
def uploadFileFTP():
    filename = 'fileName.txt'
    ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
    ftp.quit()

def runServerSocket():
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
        print("Connected to client")

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

def RetrFile(name, sock):
    filename = socket.recv(1024)
    if os.path.isfile(filename):
        sock.send("Exists " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':    #Check first two bytes to see if it's okay
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)  #Read 1024 bytes from the file
                sock.send(bytesToSend)
                while bytesToSend != "":    #If file exceeds 1024 bytes, grab another 1024 bytes
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:   #If file doesn't exist
        sock.send("ERR")
    sock.close()

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host,port)) #Bind socket to host and port

    s.listen(5)

    print("Server Started")
    while True:
        c, addr = s.accept()
        print("Client connected to IP :< " + str(addr) + ">")
        t = threading.Thread(target = RetrFile, args=("retrThread", c))
        t.start()
    s.close()

if __name__ == '__main__':
    Main()


#Resources: https://www.youtube.com/watch?v=LJTaPaFGmM4

