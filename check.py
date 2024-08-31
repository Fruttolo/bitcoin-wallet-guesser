import requests
from bitcoin import *
import sqlite3

class Checker():

    def __init__(self, storage_db):
        self.x_value=0
        self.storage_db = storage_db

    def run(self):
        # Connect to the database (or create it if it doesn't exist)
        conn = sqlite3.connect(self.storage_db)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Create a table
        cursor.execute('''CREATE TABLE IF NOT EXISTS wallets (
                                id INTEGER PRIMARY KEY,
                                address TEXT,
                                private_key TEXT,
                                balance INTEGER)''')
        
        while True:

            self.count = 1
            cursor.execute("SELECT COUNT(*) FROM wallets")
            n_elements = cursor.fetchone()[0]
                
            while self.count <= n_elements:
                
                cursor.execute("SELECT address FROM wallets WHERE id="+str(self.count))
                address = cursor.fetchone()[0]
                    
                url = 'https://blockchain.info/balance?active=' + address
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    self.x_value = data[address]['final_balance']
                    print(self.count,":", address, ": ", self.x_value)
                else:
                    print('Errore nella richiesta:', response.status_code)
                    raise Exception('Errore nella richiesta:', response.status_code)
                    
                if self.x_value > 0:
                    with open('tesori_scovati.txt', 'a') as file:
                        # Scrivo il testo nel file
                        file.write("TROVATO!!! \n")
                        file.write("Address:  "+address+"\n")
                        file.write("Value:  "+str(self.x_value)+"\n")

                    print('TROVATO!!!')
                    print('Address:', address)
                    print('Value:', self.x_value)

                    raise Exception('TROVATO!!!', address, self.x_value)
                
                self.count = self.count + 1