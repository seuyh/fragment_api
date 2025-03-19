import asyncio
from Functions.LogInit import log_init
import json
from wallet.Transactions import Transactions
from FragmentApi.PaymentGet import PaymentGet
from FragmentApi.BuyStars import buy_stars
from wallet.WalletUtils import WalletUtils



if __name__ == '__main__':
    log_init()

    with open("seed.json", "r") as f:
        mnemonics = json.load(f)
    recipient = input("Recipient: ")
    amount = input("Amount: ")

    # print(WalletUtils.wallet_from_mnemonics(mnemonics))
    # print(WalletUtils.create_wallet(save_to_file=True))
    # WalletUtils.init_wallet(mnemonics=mnemonics, testnet=False)
    # Transactions.send_ton(mnemonics, "UQBQ60OSZCvZJBrW2gqR50S64Gu_ya5sdd9X58HLKLSw24H6", 0.01, "test", nano_amount=False, send_mode=1)
    buy_stars(recipient, int(amount), mnemonics, send_mode=1)

