import logging

from TonTools import TonCenterClient, Wallet
from tonsdk.utils import from_nano


class Transactions:
    async def send_ton(self, mnemonics, destination_address, amount, payload, nano_amount=True, version='v4r2', testnet=False, send_mode=0):
        provider = TonCenterClient(testnet=testnet)
        wallet = Wallet(mnemonics=mnemonics, version=version, provider=provider)
        if nano_amount:
            if isinstance(amount, str):
                amount = int(amount)
            amount = from_nano(amount, "ton")

        clean_payload = payload.replace("\n", " ")
        logging.warning(f'Sending {amount} TON to {destination_address} with payload: {clean_payload}')
        if await wallet.transfer_ton(destination_address=destination_address, amount=amount,
                                  message=payload, send_mode=send_mode) != 200:
            logging.error("Transaction failed!")
            return 0
        else:
            logging.info("Sending successful!")
            return 1