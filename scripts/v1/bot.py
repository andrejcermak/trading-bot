import time

from brownie import Contract, accounts, config, network
from requests import get
from scripts.v1.helpful_scripts import get_contract, get_price, swap
from web3 import Web3

SAFE_GAS_PRICE = "SafeGasPrice"
PROPOSE_GAS_PRICE = "ProposeGasPrice"
FAST_GAS_PRICE = "FastGasPrice"

TRADING_FEE = 0.002
GAS_LIMIT = 200_000

    
def main():
    state=1
    pair = [config["networks"][network.show_active()]["tomb"], config["networks"][network.show_active()]["ftm"]]
    balance = 19
    contract = get_contract("spooky_swap")
    network.gas_limit(GAS_LIMIT)

    while(True):
        blockscan = get("https://gftm.blockscan.com/gasapi.ashx?apikey=key&method=gasoracle").json()["result"]
        gas = float(blockscan[SAFE_GAS_PRICE])
        res = contract.getAmountsOut(Web3.toWei(balance, "ether"),pair)
        price = res[state]/res[1-state]
        new_balance = price*(Web3.toWei(balance, "ether")*(1-TRADING_FEE) - Web3.toWei(gas*GAS_LIMIT, "gwei"))/Web3.toWei(1, "ether")
        print(gas, price, new_balance)
        if state:
            required_ratio = 1.02
        else:
            required_ratio = 1.03
        
        if get_price(state) >= required_ratio and new_balance > balance:
            print("we swap")
            network.gas_price(Web3.toWei(gas, "gwei"))
            tx = swap(balance, new_balance, pair, state)
            if tx.status == 1:
                pair.reverse()
                state = 1-state
                balance = new_balance
                time.sleep(1800)
        time.sleep(1)
