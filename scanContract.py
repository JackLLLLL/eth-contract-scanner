from web3 import Web3
import subprocess, os, sys, json


def scanContractInPeriod(web3, startBlockNumber, endBlockNumber):
    for i in range(startBlockNumber, endBlockNumber):
        print('Scaning block ', i, ' ...')
        block = web3.eth.getBlock(i)
        transactions = block.transactions
        for transaction in transactions:
            receipt = web3.eth.getTransactionReceipt(transaction)
            # check if contract deployed successfully
            # if receipt.contractAddress and web3.toHex(web3.eth.getCode(receipt.contractAddress)) == '0x':
            if receipt.contractAddress:
                contract = receipt.contractAddress + '\n'
                with open('ContractList.txt', 'a') as f:
                    f.write(contract)
    with open('ContractList.txt', 'a') as f:
        end = '... till block ' + str(i) + ' \n'
        f.write(end)

def auditContractByAddress(address):
    location = 'reports/'+address+'.md'
    if not os.path.isfile(location):
        with open(location, 'w') as f:
            subprocess.call(["myth", "-xia", address, "-o", "markdown", "--max-depth", "12", "-l"], stdout=f, stderr=f)
    else:
        print('audit exists ...')

def auditAllContractFound():
    with open('ContractList.txt', 'r') as f:
        for line in f:
            print('Auditing ' + line.rstrip('\n') + ' contract \n...')
            auditContractByAddress(line.rstrip('\n'))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Use argument -a to audit all contracts found, and -s to scan all contract till lastest block!")
    elif sys.argv[1] == '-a':
        auditAllContractFound()
    elif sys.argv[1] == '-s':
        web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/f8fd67ea548840fcacb384f39e6f579d"))
        startBlockNumber = 1
        endBlockNumber = web3.eth.blockNumber
        scanContractInPeriod(web3, startBlockNumber, endBlockNumber)
    else:
        print("Use argument -a to audit all contracts found, and -s to scan all contract till lastest block!")
