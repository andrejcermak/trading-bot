from brownie import network, Contract, accounts, config, interface
from web3 import Web3
import time

def get_contract(contract_name, interface=None, address=None):
    contract_address = config["networks"][network.show_active()][contract_name] if address is None else address
    if interface is None:
        return Contract.from_explorer(contract_address)
    return Contract.from_abi(interface._name, contract_address, interface.abi)

def get_account():
    return accounts.add(config["wallets"][network.show_active()])

def buy_alt(amount, alt):
    pair = [config["networks"][network.show_active()]["ftm"], config["networks"][network.show_active()][alt]]
    return swap(balance=amount, expected = 0, pair=pair, state=0)
     
def sell_alt(amount, alt):
    pair = [config["networks"][network.show_active()][alt], config["networks"][network.show_active()]["ftm"]]
    return swap(balance=amount, expected = 0, pair=pair, state=1)

def approve_token(amount, alt, exchange="spooky_swap"):
    factory = Contract.from_abi(interface.IERC20._name,
                                config["networks"][network.show_active()][alt],
                                interface.IERC20.abi)
    return factory.approve(config["networks"][network.show_active()][exchange],
                    Web3.toWei(amount, "ether"),
                    {"from": get_account()})
    

def get_price(state: int) -> float:
    pair_contract = get_contract("tomb_pair")   
    return pair_contract.getReserves()[state]/pair_contract.getReserves()[1-state]

def swap(balance, expected, state, pair):
    contract = get_contract("spooky_swap")
    account = get_account()
    if state:  
        return contract.swapExactTokensForETH(
                Web3.toWei(balance, "ether"),
                Web3.toWei(expected, "ether"),
                pair,
                account,
                int(time.time())+200,
                {"from": account})
    return contract.swapExactETHForTokens(
            Web3.toWei(expected, "ether"),
            pair,
            account.address,
            int(time.time())+200,
            {"from": account, "value": Web3.toWei(balance, "ether"), "allow_revert": False}
        )