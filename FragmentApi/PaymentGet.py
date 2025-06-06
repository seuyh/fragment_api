import requests
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

    def _hash_get(self):
        response = requests.get("https://fragment.com/stars/buy", cookies=self.cookies)
        if response.status_code == 200:
            return search(r'api\?hash=([a-zA-Z0-9]+)', response.text).group(1)

    def _update_url(self):
        return f"https://fragment.com/api?hash={self._hash_get()}"

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

    def get_data_for_payment(self, recipient, quantity, mnemonics):
        logging.warning(f"Sending {quantity} stars to @{recipient}...")

        url = self._update_url()

        recipient_id_dirt = requests.post(url, headers=self.headers, cookies=self.cookies,
                                          data=f"query={recipient}&quantity=&method=searchStarsRecipient")
        recipient_id = recipient_id_dirt.json().get("found", {}).get("recipient", "")


        req_id_dirt = requests.post(url, headers=self.headers, cookies=self.cookies,
                                    data=f"recipient={recipient_id}&quantity={quantity}&method=initBuyStarsRequest")
        req_id = req_id_dirt.json().get("req_id", "")

        encoded_payload = self._payload_get(req_id, mnemonics)

        buy_payload_dirt = requests.post(url, headers=self.headers, cookies=self.cookies, data=encoded_payload)
        buy_payload = buy_payload_dirt.json()["transaction"]["messages"][0]

        address, amount, encoded_message = buy_payload["address"], buy_payload["amount"], buy_payload["payload"]
        payload = self._message_decode(encoded_message)
        logging.info("Payment data received!")
        logging.warning("Waiting to send transaction...")
        return address, amount, payload
