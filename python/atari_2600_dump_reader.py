#-------------------------------------------------------------------------------
# Name:        atari_2600_dump_reader
# Purpose:
#
# Author:      github.com/aporto
#
# Created:     25/05/2021
# Copyright:   (c) alex 2021
# Licence:     Apache
#-------------------------------------------------------------------------------

import serial

SERIAL_PORT = "COM3"
FILE_NAME = "atari_2600_rom_dump"

def dumpDataFromPort(port):
    curAddress = 0
    rawData = bytearray()
    while True:
        line = port.readline().decode("ascii").strip()
        print(line)
        
        if "***" in line:
            continue
            
        if "+++" in line:
            break
                
        if len(line) == "":
            continue

        address, data = line.split(":")
        address = int(address, 16)

        if address != curAddress:
            print ("ERROR! Missing data chunk during reception. Please check you cables!")
            return None

        # Break data into a list of 16 elements of hex values (still string)
        data = [data[i:i+2] for i in range(0, len(data), 2)]
        # Convert all string elements in data to integer
        data = [int(d, 16) for d in data]

        for b in data:
            rawData.append(b)
            curAddress += 1

    with open(FILE_NAME + ".bin" , "wb") as f:
        f.write(rawData)
    print ("File '%s.bin' created!" % (FILE_NAME ))


def convertHexFileToRaw():
    print ("Converting hex file to binary raw rom file...")

    with open(FILE_NAME + ".hex", "r") as f:
        lines = f.readlines()

    curAddress = 0
    rawData = bytearray()
    for line in lines:
        line = line.strip()
        if "+++" in line:
            break
        if "***" in line:
            continue
        if len(line) == "":
            continue

        address, data = line.split(":")
        address = int(address, 16)

        if address != curAddress:
            print ("ERROR! Missing data chunk during reception. Please check you cables!")
            return None

        # Break data into a list of 16 elements of hex values (still string)
        data = [data[i:i+2] for i in range(0, len(data), 2)]
        # Convert all string elements in data to integer
        data = [int(d, 16) for d in data]

        for b in data:
            rawData.append(b)
            curAddress += 1

    with open(FILE_NAME + ".bin", "wb") as f:
        f.write(rawData)
    print ("File '%s.bin' created!" % (FILE_NAME ))

def downloadHexDump(port):
    out = open(FILE_NAME + ".hex", "w")
    while True:
        line = port.readline().decode("ascii").strip()
        print(line)
        out.write("%s\n" % (line))
        if "+++" in line:
            break
        if "***" in line:
            continue
        if len(line) == "":
            continue

    print ("Downloaded hex data to '%s.hex'" % (FILE_NAME ))

if __name__ == '__main__':
    try:
        port = serial.Serial(SERIAL_PORT, 115200)
    except:
        port = None
        print ("ERROR! Could not open serial port '%s'" % SERIAL_PORT)

    if port:
        #dumpDataFromPort(port)
        downloadHexDump(port)
        convertHexFileToRaw()
        port.close()

    print ("Finished!")







