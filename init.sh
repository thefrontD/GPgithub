#set ethereum data directory
fullDataDir="~/ether/data"

#remove chaindata if you want to start etheruem from genesis block
rm -vrf ${fullDataDir}

#rebuild geth
cd ../..
make geth
cd build/bin

#init
./geth --datadir ${fullDataDir} init genesis.json

#run geth
./geth --datadir ${fullDataDir} --keystore "./keystore" --gcmode archive --networkid 76927692 --http --http.port "8081" --http.corsdomain "*" --port 30303 --nodiscover --http.api="admin,eth,debug,miner,net,txpool,personal,web3" --allow-insecure-unlock
