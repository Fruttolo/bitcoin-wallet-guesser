import requests
from bitcoin import *
import sqlite3
import time

class Guesser():

    @staticmethod
    def generate_key():
        key_pair = random_key()
        private_key = encode_privkey(key_pair, 'wif')
        address = privkey_to_address(key_pair)
        return private_key, address

    def __init__(self, storage_db):
        self.count=0
        self.x_value=0
        self.storage_db = storage_db

    def run(self):
        # Connect to the database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(self.storage_db)

        # Create a cursor object to execute SQL queries
        cursor = self.conn.cursor()

        # Create a table
        cursor.execute('''CREATE TABLE IF NOT EXISTS wallets (
                                id INTEGER PRIMARY KEY,
                                address TEXT,
                                private_key TEXT,
                                balance INTEGER)''')
        
        if cursor.execute("SELECT COUNT(*) FROM wallets").fetchone()[0]:
            self.count = cursor.execute("SELECT MAX(id) FROM wallets").fetchone()[0] + 1

        while True:

            private_key, address = Guesser.generate_key()

            url = 'https://blockchain.info/balance?active=' + address
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                self.x_value = data[address]['final_balance']
                print(self.count,":", address, private_key)
            else:
                print('Errore nella richiesta:', response.status_code)
                raise Exception('Errore nella richiesta:', response.status_code)
            
            # Insert some data into the table
            cursor.execute("INSERT INTO wallets (address, private_key, balance) VALUES (?, ?, ?)", (address, private_key, self.x_value))
            self.conn.commit()
            
            if self.x_value>0:
                with open('tesori_scovati.txt', 'a') as file:
                    # Scrivo il testo nel file
                    file.write("TROVATO!!! \n")
                    file.write("Private: "+private_key+"\n")
                    file.write("Address:  "+address+"\n")
                    file.write("Value:  "+str(self.x_value)+"\n")

                print('TROVATO!!!')
                print('Private:', private_key)
                print('Address:', address)
                print('Value:', self.x_value)

                raise Exception('TROVATO!!!', private_key, address, self.x_value)
                
            self.count=self.count+1