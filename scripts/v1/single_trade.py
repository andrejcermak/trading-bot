from brownie import network
from web3 import Web3
from helpful_scripts import approve_token

def main():
    network.gas_limit( 305000 )
    network.gas_price(Web3.toWei(1000, "gwei"))
    approve_token(30, "tomb")