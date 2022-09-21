from tronpy import Tron
from tronpy.keys import PrivateKey
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L


class Wallet_tech:

    def __init__(self) -> None:
        self.__client = Tron()

    def create_wallet(self, id) -> dict():
        # creación de la wallet en la red de tron
        wallet = self.__client.generate_address()
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(wallet['base58check_address'])
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qr-'+str(id)+'.png')
        return {'private_key': wallet['private_key'],
                'address': wallet['base58check_address']}

    def get_balance(self, address: str) -> float:
        # verificar el balance en la billetera
        balance = self.__client.get_account_balance(addr=address)
        return balance

    def withdraw(self, amount: int, wallet: str) -> dict():
        # Enviar saldo a una cuenta
        try:
            priv_key = PrivateKey(bytes.fromhex(self.__private_key))
            txn = (
                self.__client.trx.transfer(self.address, str(
                    wallet), int(int(amount)*1000000))
                .memo("Transaction Description")
                .build()
                .inspect()
                .sign(priv_key)
                .broadcast()
            )
            return txn.wait()
        except Exception as ex:
            return ex

    def delete_wallet(self) -> dict():
        # Eliminar las claves de la base de datos

        pass
