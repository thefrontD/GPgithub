#set ethereum data directory
fullDataDir="~/ether/data"
logData="./gethlog.log"

#remove chaindata if you want to start etheruem from genesis block
rm -vrf ${fullDataDir}

#rebuild geth
cd ../..
make geth
cd build/bin

#clear log
cat /dev/null > gethlog.log

#init
./geth --datadir ${fullDataDir} init genesis.json

#run geth
nohup ./geth --datadir ${fullDataDir} --keystore "./keystore" --gcmode archive --networkid 76927692 --http --http.port "8085" --http.corsdomain "*" --port 30307 --http.api="admin,eth,debug,miner,net,txpool,personal,web3" --nodiscover --allow-insecure-unlock --syncmode "full" --rpc 2>>${logData} &

##export PATH=$PATH:/usr/local/go/bin

##./geth --datadir "~/ether/data2" removedb

##./geth --datadir "~/ether/data2" init genesis.json

## nohup ./geth --datadir "~/ether/data2" --keystore "./keystore" --gcmode archive --networkid 76927692 --http --http.port "8086" --http.corsdomain "*" --port 30308 --http.api="admin,eth,debug,miner,net,txpool,personal,web3" --nodiscover --allow-insecure-unlock --syncmode "full" --rpc 2>>"./gethlog2.log" &

##python3 sendTransaction.py 1000

##tail -f -n 60 gethlog.log

##주영 5.26

##원본 5.15

##removedb를 하고 난 후에는 sync 시간이 길어진다
##





