from cmath import exp
from webbrowser import get
from brownie import interface, IUniswapV2Router01, network, config
from web3 import Web3
from scripts.v1.bot import get_contract, get_account


def main():
    spooky_pairs_contract = get_contract("spooky_pairs", interface.IUniswapV2Factory)
    # print(spooky_pairs_contract.allPairs(0))
    spooky_contract = get_contract("spooky_swap", IUniswapV2Router01)
    for i in range (spooky_pairs_contract.allPairsLength()):
        output_pair(i, spooky_pairs_contract, spooky_contract) 
        print(f"pair #{i}")

def output_pair(index, spooky_pairs_contract, spooky_contract):
    try:
        print("--------------------------------------------------------------------")
        pair_contract = get_contract("", interface.IUniswapV2Pair, spooky_pairs_contract.allPairs(index))
        # print(pair_contract.token0(), pair_contract.token1())
        token0 = get_contract("", interface.IERC20, pair_contract.token0())
        token1 = get_contract("", interface.IERC20, pair_contract.token1())
        reserves = pair_contract.getReserves()
        reserve0 = reserves[0]
        reserve1 = reserves[1]
        print(token0.name(), token0.symbol(), "+", token1.name(), token1.symbol())
        print(token0, token1)
        print("pair: ", pair_contract, " reserves: ", pair_contract.getReserves())
        if reserve1:
            print(f"ratio: {reserve0/reserve1}")

    except Exception as e:
        print(e)
