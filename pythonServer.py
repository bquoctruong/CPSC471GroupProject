#Name: Brian Truong
#Date: 11/12/2017
#File Name: pythonServer.py
#File Description: Creates an FTP like server to run in conjunction with pythonClient.py
#NOTE: Done in Python 3.6
import os
from socket import *
import socket
import threading
import ftplib

# Function:RetrFile
# Date of code(Last updated): 11/25/17
# Programmer: Brian Truong
# Input: name, sock
# Output: N/A
# Description: Receives a response from the client and performs one of three actions:
#   1) Sends a file from the server machine to the client
#   2) Receives a file from the client machine
#   3) Sends a list of items in the current directory of the server
def RetrFile(name, sock):
    #Receives response from client; determines actions
    userResponse = sock.recv(1024)

    #If user responds with GET, server proceeds to send file to user
    if(str(userResponse)[2:5] == 'GET'):
        #Obtains file name
        filename = sock.recv(1024)
        #Confirms file existence
        if os.path.isfile(filename):
            fileInt = os.path.getsize(filename) #Gets file size
            fileStr = 'EXISTS' + str(fileInt)   #Appends 'EXISTS' to string to send back to client for confirmation
            byteName = str.encode(fileStr)  #Encodes string for socket transmission
            sock.send(byteName) #Wants to send a str, not bytes
            userResponse = sock.recv(1024)
            if str(userResponse)[2:4] == 'OK':    #Check first two bytes to see if it's okay
                print("OK received")
                f= open(filename, 'rb') #Opens file for reading purposes
                l = f.read(1024)    #Reads 1024 bytes from file
                while(l):
                    sock.send(l)    #Sends bytes to client
                    l = f.read(1024)    #Reads next 1024 bytes
        #testResponse = sock.recv(1024)
        #if(str(testResponse)[2:] == 'CLOSE'):
        #    systemMessage = 'OK'
        #    systemMessage = str.encode(systemMessage)
        #    sock.send(systemMessage)
        sock.close()    #Closes socket after transmission
    #If server receives PUT command, prepares to write data to server's directory
    if(str(userResponse)[2:5] == 'PUT'):
        filename = sock.recv(1024)  #Receives filename from client
        f = open(filename, 'wb')    #Opens file to write to
        data = sock.recv(1024)      #Receives data for file
        totalRecv = len(data)       #Tallies amount of data received
        while(data):
            f.write(data)      #Writes data to file
            data = sock.recv(1024)  #Retrieves more data from file
        print("Download Complete")
        sock.close()
    #If server receives LS command, prepares to send list of files in the server directory
    if(str(userResponse)[2:4] == 'LS'):
        #Uses os.listdir() to check files in current dircetory
        for line in os.listdir():
            data = line #Assigns file name to data
            print(data) #Prints files in directory; also prevents concatentation of filenames
            data = str.encode(data)
            sock.send(data) #Sends file name to client
        sock.close()

# Function: Main()
# Date of code (Last updated): 11/25/17 
# Prorgrammer: Brian Truong
# Description: Initialize socket and thread for FTP server
# Input: N/A
# Output: N/A
def Main():
    host = gethostbyname(socket.gethostname())  #Retrieves host IP; credit: https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    print(host)
    port = int(input("Enter your port number: "))
    #host = 'localhost'
    #port = 5000

    #Creates socket for server
    s = socket.socket()
    s.bind((host,port)) #Bind socket to host and port

    s.listen(5)

    print("Server Started")
    #While server is active
    while True:
        c, addr = s.accept()
        print("Client connected to IP :< " + str(addr) + ">")   #Confirms that connection is established
        t = threading.Thread(target = RetrFile, args=("retrThread", c)) #Uses thread to run main function
        t.start()   #Starts thread
    s.close()

if __name__ == '__main__':
    Main()


#Resources: https://www.youtube.com/watch?v=LJTaPaFGmM4

