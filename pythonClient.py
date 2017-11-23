from socket import *
import socket
import os
import ftplib
from ftplib import *

#To-do: - Append size of file to the first 10 bytes of data (See example code)
 

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

def runClientSocket():
    print("Running client")

    #Get hostname and port
    inputHost = str(input("Enter the host name: "))
    inputPortNumber = int(input("Enter the port number: "))
    bindHostNumber = (inputHost, inputPortNumber)

    #Create socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    #Connect to server
    clientSocket.connect(bindHostNumber)
    print("Connected to server")

    #Data sent
    file = open('text.txt', 'rb')
    length = file.read(1024)

    #Bytes
    bytesSent = 0

    #Send string
    while bytesSent != len(file):
        #Send data
        bytesSent += clientSocket.send(data[bytesSent:])

    #Close socket
    print("Closing socket")
    clientSocket.close()

def runClientFTP():
    ftp = FTP.connect(host='', port = 1234)
    ftp.login()
    while ftp:
        print("Connected to server")

def Main():
    host = 'localhost'
    port = 5000

    s = socket.socket()
    s.connect((host,port))

    filename = input("Enter the file's name: ")
    byteName = str.encode(filename)
    if filename != 'q':
        s.send(byteName)
        #Wait to see if the file exists or not
        data = s.recv(1024)     #Receive 1024 bytes
        #if data[:6] == 'EXISTS':    #If the first 6 bytes are EXISTS
        filesize = int(data[6:])
        message = str(input("File Exists, " + str(filesize) + "Bytes, download? (Y/N) >"))
        if message == 'Y':
            okMessage = 'OK'
            okMessage = str.encode(okMessage)
            s.send(okMessage)
            f = open('new_'+filename, 'wb')
            data = s.recv(1024)
            totalRecv = len(data)
            f.write(data)
            #if there is more than 1024 bytes, receive more
            while totalRecv < filesize:
                data = s.recv(1024)
                totalRecv += len(data)
                f.write(data)
                print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
            print("Download Complete")
    else:
            print("File does not exist")
    s.close()
if __name__=="__main__":
    Main()




#Resources: https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
#https://www.youtube.com/watch?v=LJTaPaFGmM4
