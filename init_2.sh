fullDataDir="~/ether/data2"
logData="./gethlog2.log"

#remove chaindata if you want to start etheruem from genesis block
rm -vrf ${fullDataDir}

#init
./geth --datadir ${fullDataDir} init genesis.json

#clear log
cat /dev/null > gethlog2.log

#run geth
./geth --datadir ${fullDataDir} --keystore "./keystore" --gcmode archive --networkid 76927692 --http --http.port "8086" --http.corsdomain "*" --port 30308 --nodiscover --http.api="admin,eth,debug,miner,net,txpool,personal,web3" --allow-insecure-unlock --verbosity "6" --syncmode "full" --rpc 2>>${logData} &