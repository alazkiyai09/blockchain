import numpy as np
import hashlib
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import random
import os

def sha3(data):
    return hashlib.sha3_256(data.encode('utf-8')).hexdigest()

def hashValue(index, data, timestamp, prevHash, randomPadding):
    allData = str(index) + str(data) + str(timestamp) + str(prevHash) + str(randomPadding)
    allData = sha3(allData)
    return allData

def pcg32(param1, param2, param3) -> np.uint32:
    np.seterr(all='ignore') # remove overflow messages.

    engine = np.array([param1, param2], dtype='uint64')
    multiplier = param3
    big_1 = np.uint32(1)
    big_18 = np.uint32(18)
    big_27 = np.uint32(27)
    big_59 = np.uint32(59)
    big_31 = np.uint32(31)

    while True:
        old_state = engine[0]
        inc = engine[1]
        engine[0] = old_state * multiplier + (inc | big_1)
        xorshifted = np.uint32(((old_state >> big_18) ^ old_state) >> big_27)
        rot = np.uint32(old_state >> big_59)
        yield np.uint32((xorshifted >> rot) | (xorshifted << ((-rot) & big_31)))


def read_file(filename):
    data = pd.read_csv(filename)
    return data

def create_blockchain():
    filename = "Blockchain.csv"
    newData = pd.DataFrame(columns=['Index','Data','Time','Previous Hash','Random Padding','Hash'], index=None)
    newData = newData.append({'Index':str(0), 'Data': 'Genesis', 'Time': str(datetime.now()), 'Previous Hash': "0", 'Random Padding': "0", 'Hash': "0"}, ignore_index=True)

    newData.to_csv(filename, index=None)

def addBlockchain(newData):
    filename = "Blockchain.csv"
    param1 = np.uint64(random.random()*(2**64))
    param2 = np.uint64(random.random()*(2**64))
    param3 = np.uint64(random.random()*(2**64))
    data = read_file(filename)
    index = len(data)
    timestamp = str(datetime.now())
    prevHash = data['Hash'][index - 1]
    randomGen = pcg32(param1, param2, param3)
    randomPadding = next(randomGen)
    Hash = hashValue(index, newData, timestamp, prevHash, randomPadding)
    data = data.append({"Index": str(index), "Data": newData, "Time": timestamp, "Previous Hash": prevHash, "Random Padding": str(randomPadding), "Hash": Hash}, ignore_index=True)
    data.to_csv(filename, index=None)

def viewBlock():
    filename = "Blockchain.csv"
    data = pd.read_csv(filename, delimiter=',',names=['Index','Data','Time','Previous Hash','Random Padding','Hash'])
    for i in range(1, len(data)):
        print("Index: ", data["Index"][i])
        print("Data: ", data["Data"][i])
        print("Time: ", data["Time"][i])
        print("Previous Hash: ", data["Previous Hash"][i])
        print("Hash: ", data["Hash"][i])
        print("Random Padding: ", data["Random Padding"][i])
        print("\n")

def validateBlock():
    filename = "Blockchain.csv"
    data = pd.read_csv(filename, delimiter=',',names=['Index','Data','Time','Previous Hash','Random Padding','Hash'])
    status = False
    for i in range(2, len(data)-1):
        prevHash = data["Previous Hash"][i+1]
        currentHash = hashValue(data['Index'][i], data['Data'][i], data['Time'][i], data['Previous Hash'][i], data['Random Padding'][i])
        if (currentHash == prevHash):
            status = True
        else:
            status = False

    if status==True:
        status = "Safe"
    else:
        status = "Danger"
    print("Blockchain Status: ", status)

def changeBlcok(newData, index):
    filename = "Blockchain.csv"
    data = pd.read_csv(filename)
    print(newData)
    data["Data"][index] = newData
    data.to_csv(filename, index=None)



def main():
    exit = False
    while (exit==False):
        print("\nBlcokchain\n")
        print("1. Create New Blockchain (Previous File Will be Deleted)")
        print("2. Add New Block or Data")
        print("3. View Block")
        print("4. Validate Block")
        print("5. Exit")
        x = int(input("Write Number of Action: "))
        if x == 1:
            os.system('cls')
            create_blockchain()
            print("Blockchain Successfully Created")
        elif x == 2:
            os.system('cls')
            newData = input("Input New Data: ")
            addBlockchain(newData)
            print("New Data Successfully Added")
        elif x == 3:
            os.system('cls')
            viewBlock()
        elif x == 4:
            os.system('cls')
            validateBlock()
        elif x == 5:
            exit = True
            os.system('cls')


if __name__ == '__main__':
    main()
