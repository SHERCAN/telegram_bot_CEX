from tronpy import Tron
from tronpy.keys import PrivateKey


class Wallet_tech:

    def __init__(self, **kwargs) -> None:
        self.__client = Tron()
        try:
            self.__private_key = kwargs['priv_key']
            self.address = kwargs['address']
        except:
            self.__private_key = ''
            self.address = ''

    def create_wallet(self) -> dict():
        # creación de la wallet en la red de tron
        wallet = self.__client.generate_address()
        return {'private_key': wallet['private_key'],
                'address': wallet['base58check_address']}

    def check_balance(self, address: str) -> float:
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
