from FragmentApi.PaymentGet import PaymentGet
from wallet.Transactions import Transactions


def buy_stars(recipient, amount, mnemonics, version="v4r2", testnet=False, send_mode=1):
    payment = PaymentGet()
    payment_address, payment_amount, payload = payment.get_data_for_payment(recipient=recipient, quantity=amount,
                                                                            mnemonics=mnemonics)

    Transactions.send_ton(mnemonics=mnemonics, destination_address=payment_address, amount=payment_amount,
                          nano_amount=True, payload=payload, version=version, testnet=testnet, send_mode=send_mode)
