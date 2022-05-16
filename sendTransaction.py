from web3 import Web3
import sys
#import socket
#import random
#import json
#import rlp
#import time
#import numpy as np
import os, binascii
import time
from datetime import datetime
from multiprocessing import Pool




# Settings
FULL_PORT = "8085"
PASSWORD = "1234"

# Account number
ACCOUNT_NUM = int(sys.argv[1])

# multiprocessing
THREAD_COUNT = 8

# providers
fullnode = Web3(Web3.HTTPProvider("http://localhost:" + FULL_PORT))

# functions
def main():
    print("Insert ", ACCOUNT_NUM, " accounts")

    # unlock coinbase
    fullnode.geth.personal.unlockAccount(fullnode.eth.coinbase, PASSWORD, 0)

    # get current block
    currentBlock = fullnode.eth.blockNumber

    # main loop for send txs
    print("start sending transactions")

    # send transactions
    # sendPool.map(sendTransactions, ACCOUNT_NUM)
    sendTransactions(ACCOUNT_NUM)

    # mining
    fullnode.geth.miner.start(1)  # start mining
    while (fullnode.eth.blockNumber == currentBlock):
        pass # just wait for mining
    fullnode.geth.miner.stop()  # stop mining
    currentBlock = fullnode.eth.blockNumber


def sendTransaction(to):
    #print("start try to send tx to full node")
    #print("to: ", to, "/ from: ", fullnode.eth.coinbase)
    while True:
        try:
            fullnode.eth.sendTransaction(
                {'to': to, 'from': fullnode.eth.coinbase, 'value': '1', 'gas': '21000', 'data': ""})
            break
        except:
            continue



def sendTransactions(num):
    checkpoint = num/20
    for i in range(int(num)):
        if i%100 == 0:
            print("current time: ",time.process_time() , "transaction:",i)
        to = makeRandHex()
        while True:
            try:
                fullnode.eth.sendTransaction(
                    {'to': to, 'from': fullnode.eth.coinbase, 'value': '1', 'gas': '21000', 'data': ""})
                break
            except:
                continue



def makeRandHex():
	randHex = binascii.b2a_hex(os.urandom(20))
	return Web3.toChecksumAddress("0x" + randHex.decode('utf-8'))



if __name__ == "__main__":

    totalStartTime = datetime.now()
    sendPool = Pool(THREAD_COUNT) # -> important: this should be in this "__main__" function
    main()
    totalEndTime = datetime.now() - totalStartTime
    print("total elapsed:", totalEndTime.seconds, "seconds")
    print("DONE")
