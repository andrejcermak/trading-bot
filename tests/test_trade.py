from scripts.bot import swap
from brownie import config, network
from web3 import Web3
from scripts.helpful_scripts import get_account

def test_single_trade():
    network.gas_limit(300_480)
    network.gas_price(Web3.toWei(300, "gwei"))
    print(get_account().balance())
    balance = 0.01
    pair = [config["networks"][network.show_active()]["ftm"], config["networks"][network.show_active()]["spook"]]
    print(swap(balance=balance, pair=pair))
