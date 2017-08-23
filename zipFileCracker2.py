# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 23:55:23 2017

@author: Christian
"""

import zipfile


# Function to attempt to extract the zip file taking in the zipfile name and password
def extractFile(zFile, password):
    
    # Attempt to extract the zip file
    try:
        zFile.extractall(pwd=password)
        return password
        
    # If an exception occurs ignore it and continue on running the application
    except:
        print("Tried: " + password + "\n")
        pass
    
def main():
    
    zFile = zipfile.ZipFile('testzip.zip')
    
    passFile = open('dictionary.txt')
    for line in passFile.readlines():
        password = line.strip()
        guess = extractFile(zFile, password)
        if guess:
            print("Found Password: " + password + "\n")
            exit(0)
            
if __name__ == '__main__':
    main()