import aiohttp
from re import search
import logging
from wallet.WalletUtils import WalletUtils
from urllib.parse import urlencode
import json
import base64


class PaymentGet:
    def __init__(self):
        self.WalletUtils = WalletUtils()
        with open('cookies.json', 'r') as file:
            loaded_cookies = json.load(file)

        self.cookies = loaded_cookies
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://fragment.com/stars/buy",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0 (Edition Yx GX)"
        }

    async def _hash_get(self, session):
        async with session.get("https://fragment.com/stars/buy", cookies=self.cookies) as response:
            if response.status == 200:
                text = await response.text()
                return search(r'api\?hash=([a-zA-Z0-9]+)', text).group(1)

    async def _update_url(self, session):
        hash_val = await self._hash_get(session)
        return f"https://fragment.com/api?hash={hash_val}"

    def _payload_get(self, req_id, mnemonics):
        payload = {
            "account": json.dumps({
                "chain": "-239",
                "publicKey": self.WalletUtils.wallet_from_mnemonics(mnemonics)[0]["public_key"]
            }),
            "device": json.dumps({
                "platform": "web",
                "appName": "telegram-wallet",
                "appVersion": "1",
                "maxProtocolVersion": 2,
                "features": ["SendTransaction", {"name": "SendTransaction", "maxMessages": 4}]
            }),
            "transaction": 1,
            "id": req_id,
            "show_sender": 0,
            "method": "getBuyStarsLink"
        }
        return urlencode(payload)

    @staticmethod
    def _message_decode(encoded_payload):
        padding_needed = len(encoded_payload) % 4
        if padding_needed != 0:
            encoded_payload += '=' * (4 - padding_needed)
        decoded_payload = base64.b64decode(encoded_payload)
        text_part = decoded_payload.split(b"\x00")[-1].decode("utf-8")

        return text_part

    async def get_data_for_payment(self, recipient, quantity, mnemonics):
        logging.warning(f"Sending {quantity} stars to @{recipient}...")
        async with aiohttp.ClientSession(headers=self.headers, cookies=self.cookies) as session:
            url = await self._update_url(session)

            async with session.post(url, data=f"query={recipient}&quantity=&method=searchStarsRecipient") as response:
                recipient_id_dirt = await response.json()
                recipient_id = recipient_id_dirt.get("found", {}).get("recipient", "")

            async with session.post(url, data=f"recipient={recipient_id}&quantity={quantity}&method=initBuyStarsRequest") as response:
                req_id_dirt = await response.json()
                req_id = req_id_dirt.get("req_id", "")

            encoded_payload = self._payload_get(req_id, mnemonics)

            async with session.post(url, data=encoded_payload) as response:
                buy_payload_dirt = await response.json()
                buy_payload = buy_payload_dirt["transaction"]["messages"][0]

            address, amount, encoded_message = buy_payload["address"], buy_payload["amount"], buy_payload["payload"]
            payload = self._message_decode(encoded_message)
            logging.info("Payment data received!")
            logging.warning("Waiting to send transaction...")
            return address, amount, payload