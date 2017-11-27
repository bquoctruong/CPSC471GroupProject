#Name: Brian Truong
#Date: 11/12/17
#File Name: pythonClient.py
#File Description:  Runs an FTP client to interact with pythonServer.py
#NOTE: Done in Python 3.6
from socket import *
import socket
import os
import ftplib
from ftplib import *
from time import sleep

# Function: Main
# Date of code (Last updated): 11/25/17
# Programmer: Brian Truong
# Description: Runs the entirety of the ftp client
# Input: N/A
# Output: N/A

def Main():

    #Prompts user to enter host and port number to connect to
    host = input("Enter host name: ")
    port = int(input("Enter port number: "))

    #Establishes connection with given host and port number
    s = socket.socket()
    s.connect((host,port))

    #After connection is established, gives user a list of prompts
    print("Commands:")
    print("get <filename>")
    print("put <filename>")
    print("ls")
    print("quit")

    #User is prompted to enter a command
    answer = input("ftp> ")

    #If user enters get <filename>, client sends filename to server and command to "get" file
    if(answer[:3] == "get"):
        systemMessage = 'GET'   #Sends system message to prompt server to use correct function
        systemMessage = str.encode(systemMessage)   #Encodes message for socket transmission
        s.send(systemMessage)   #Sends message to server
        filename = answer[4:]   #Obtains file name from user-inputted string
        byteName = str.encode(filename)
        if filename != 'q':
            s.send(byteName)
            #Wait to see if the file exists or not
            data = s.recv(1024)     #Receive 1024 bytes
            if (str(data)[2:8] == 'EXISTS'):    #If the first 6 bytes are EXISTS, continues on with retrieving file; first 2 bytes are encoders
                filesize = str(data)[8:]    #Obtains file size
                filesize = filesize[:-1]    #Cuts off "'" at the end; Credit: https://stackoverflow.com/questions/1798465/python-remove-last-3-characters-of-a-string
                filesize = int(filesize)    #Converts filesize to int
                message = str(input("File Exists, " + str(filesize) + " Bytes, download? (Y/N) >"))
                if message == 'Y':
                    okMessage = 'OK'    #Sends system message saying it is okay to send file
                    okMessage = str.encode(okMessage)
                    s.send(okMessage)
                    f = open('new_'+filename, 'wb') #Opens local file in client's directory
                    data = s.recv(1024) #Receives first 1024 bytes
                    totalRecv = len(data)   #Tracks amount of data received
                    while(data):
                        f.write(data)   #Writes data received to file
                        data = s.recv(1024) #Obtains more bytes from server
                        totalRecv += len(data)  #Increments total bytes received
                        print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done") #Keeps progress of download to user
                    print("Download Complete")
                    s.close()
            else:
                    print("File does not exist")
                    s.close()
        else:
            s.close()
    #If put is selected, transfers a file from the client's directory to the server
    if(answer[:3] == "put"):
        systemMessage = 'PUT'   #Creates a system message to send to server
        systemMessage = str.encode(systemMessage)
        s.send(systemMessage)   #Sends message to server
        filename = answer[4:]   #Obtains file name from user-inputted list
        if os.path.isfile(filename):
            print("Found file")
            byteName = str.encode(filename)
            s.send(byteName)
            f = open(filename, 'rb')    #Opens file for reading
            l = f.read(1024)    #Reads first 1024 bytes of file
            filesize = os.path.getsize(filename)    #Obtains filesize of file
            totalRecv = len(l)  #Keeps track of how much data is being sent
            while(l):
                s.send(l)
                l = f.read(1024)
                totalRecv += len(l)
                print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done") #Keeps progress of download to user
        else:
            print("File does not exist")
        s.close()
    #If ls is inputted, sends message to server to list all files in the directory
    if(answer == "ls"):
        systemMessage = 'LS'    #Creates message for server
        systemMessage = str.encode(systemMessage)
        s.send(systemMessage)   #Sends message to server
        l = s.recv(1024)    #Obtains part of list from server
        l = str(l)[2:-1]    #Trims beginning and end
        while(l):
            print(l)    #Prints whatever is on the server
            l = s.recv(1024)    #Obtains more bytes
            l = str(l)[2:-1]    #Trims beginning and end
        s.close()
#Initialize client
if __name__=="__main__":
    Main()

#Resources: https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
#https://www.youtube.com/watch?v=LJTaPaFGmM4