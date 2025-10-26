from Functions.LogInit import log_init
import json
from FragmentApi.BuyStars import buy_stars
import asyncio

if __name__ == '__main__':
    log_init()
    with open("created_wallets/wallets_data.txt", "r") as f:
        mnemonics = json.load(f)['mnemonics']

    recipient = input("Recipient: ")
    amount = input("Amount: ")

    asyncio.run(buy_stars(recipient, int(amount), mnemonics, send_mode=1, testnet=False))