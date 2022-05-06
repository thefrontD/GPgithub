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
import logging
from datetime import datetime
from multiprocessing import Pool

#logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(u'%(asctime)s [%(levelname)8s] %(message)s')

file_handler = logging.FileHandler('./pythonOutput.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.debug("debug logging")



# Settings
FULL_PORT = "8085"
TEST_PORT = "8084"
PASSWORD = "1234"

# Account number
ACCOUNT_NUM = int(sys.argv[1])

# multiprocessing
THREAD_COUNT = 8

# providers
fullnode = Web3(Web3.HTTPProvider("http://localhost:" + FULL_PORT))
testnode = Web3(Web3.HTTPProvider("http://localhost:" + TEST_PORT))

# functions
def main():
    logger.debug("Insert ", ACCOUNT_NUM, " accounts")

    # unlock coinbase
    fullnode.geth.personal.unlockAccount(fullnode.eth.coinbase, PASSWORD, 0)

    # get current block
    currentBlock = fullnode.eth.blockNumber

    # main loop for send txs
    logger.debug("start sending transactions")

    # send transactions
    # sendPool.map(sendTransactions, ACCOUNT_NUM)
    sendTransactions(ACCOUNT_NUM)

    # mining
    fullnode.geth.miner.start(1)  # start mining
    while (fullnode.eth.blockNumber == currentBlock):
        pass # just wait for mining
    fullnode.geth.miner.stop()  # stop mining
    currentBlock = fullnode.eth.blockNumber

    #sync
    fullpeer = fullnode.geth.admin.node_info()
    logger.debug("adding peer")
    syncStartTime = time.process_time()
    testnode.geth.admin.add_peer(fullpeer.enode)
    while(testnode.eth.blockNumber < currentBlock):
        pass
    syncEndTime = time.process_time()
    logger.debug("sync time:", syncEndTime- syncStartTime, "seconds")



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
            logger.debug("current time: ",time.process_time() , "transaction:",i)
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
    logger.debug("total elapsed:", totalEndTime.seconds, "seconds")
    logger.debug("DONE")
