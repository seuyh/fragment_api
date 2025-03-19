import asyncio
import logging

from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from json import dumps
from pathlib import Path
from TonTools import TonCenterClient

from tonsdk.utils import bytes_to_b64str



class WalletUtils:
    @staticmethod
    def _generate_wallet_data(mnemonics, pub_k, priv_k, wallet_address):
        return {
            "wallet_address": wallet_address.address.to_string(True, True, True),
            "mnemonics": mnemonics,
            "public_key": pub_k.hex(),
            "private_key": priv_k.hex(),
            "wallet_address_testnet": wallet_address.address.to_string(True, True, True, True)
        }

    @staticmethod
    def create_wallet(version="v4r2", save_to_file=False, save_dir="created_wallets/wallets_data.txt"):
        mnemonics, pub_k, priv_k, wallet_address = Wallets.create(version=getattr(WalletVersionEnum, version),
                                                                  workchain=0)

        wallet_data = WalletUtils._generate_wallet_data(mnemonics, pub_k, priv_k, wallet_address)

        if save_to_file:
            Path(save_dir).parent.mkdir(parents=True, exist_ok=True)
            with open(save_dir, "a+", encoding="utf-8") as f:
                f.write(dumps(wallet_data, indent=4, ensure_ascii=False) + "\n\n")

        return wallet_data, wallet_address

    @staticmethod
    def wallet_from_mnemonics(mnemonics: list, version="v4r2"):
        mnemonics, pub_k, priv_k, wallet_address = Wallets.from_mnemonics(mnemonics=mnemonics,
                                                                          version=getattr(WalletVersionEnum, version),
                                                                          workchain=0)

        wallet_data = WalletUtils._generate_wallet_data(mnemonics, pub_k, priv_k, wallet_address)

        return wallet_data, wallet_address

    @staticmethod
    def init_wallet(mnemonics, testnet=False):
        result = asyncio.run(WalletUtils._init_wallet_async(mnemonics, testnet))
        return result

    @staticmethod
    async def _init_wallet_async(mnemonics, testnet=False):
        wallet_data, wallet_address = WalletUtils.wallet_from_mnemonics(mnemonics=mnemonics)
        provider = TonCenterClient(testnet=testnet)
        query = wallet_address.create_init_external_message()
        deploy_message = bytes_to_b64str(query['message'].to_boc(False))

        if await provider.send_boc(deploy_message) != 200:
            logging.error('Init error or wallet already init')
        else:
            logging.info("Wallet inited!")
