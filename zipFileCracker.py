# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 23:05:28 2017

@author: Christian
"""

import zipfile
#import optparse
from threading import Thread

# Function to attempt to extract the zip file taking in the zipfile name and password
def extractFile(zFile, password):
    
    # Attempt to extract the zip file
    try:
        zFile.extractall(pwd=password)
        
        # Print the password used to extract the zip file
        print("Found Password: " + password + "\n")
        
    # If an exception occurs ignore it and continue on running the application
    except:
#        print("Tried: " + password + "\n")
        pass
    
def main():
    
#     Create the options for the cmd line parser
#    parser = optparse.OptionParser("usage%prog " + "-f <zipfile> -d <dictionary>")
#    parser.add_option('-f', dest='zname', type='string', help='specify zip file')
#    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
#    
#     Get the args and store
#    (options, args) = parser.parse_args()
#    
#     Check for both cmd line args : if not then exit and print out the usage
#    if(options.zname == None) | (options.dname == None):
#        print(parser.usage)
#        exit(0)
#        
#    else:
#        # Get the cmd line args and store into local variables
#        zname = options.zname
#        dname = options.dname

    zname = "testzip.zip"
    dname = "dictionary.txt"
    # Set the zip file object into zFile using the name of the file stored in zname
    zFile = zipfile.ZipFile(zname)
    
    # Pass the dictionary file into passFile
    passFile = open(dname)
    
    for line in passFile.readlines():
        password = line.read('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()
        
if __name__ == '__main__':
    main()