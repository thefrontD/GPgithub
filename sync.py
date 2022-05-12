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

if __name__ == "__main__":

    totalStartTime = datetime.now()
    sendPool = Pool(THREAD_COUNT) # -> important: this should be in this "__main__" function
    main()
    totalEndTime = datetime.now() - totalStartTime
    logger.debug("total elapsed:", totalEndTime.seconds, "seconds")
    logger.debug("DONE")
