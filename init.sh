#set ethereum data directory
fullDataDir="~/ether/data"
fullDataDir2="~/ether/data2"
logData="./gethlog.log"
logData2="./gethlog2.log"

#remove chaindata if you want to start etheruem from genesis block
rm -vrf ${fullDataDir}

#rebuild geth
cd ../..
make geth
cd build/bin

#init
./geth --datadir ${fullDataDir} init genesis.json

#run geth
nohup ./geth --datadir ${fullDataDir} --keystore "./keystore" --gcmode archive --networkid 76927692 --http --http.port "8081" --http.corsdomain "*" --port 30303 --http.api="admin,eth,debug,miner,net,txpool,personal,web3" --allow-insecure-unlock --rpc 2>>${logData} &

nohup ./geth --datadir "~/ether/data2" --keystore "./keystore" --gcmode archive --networkid 76927692 --http --http.port "8084" --http.corsdomain "*" --port 30306 --http.api="admin,eth,debug,miner,net,txpool,personal,web3" --allow-insecure-unlock --rpc 2>>"./gethlog2.log" &

