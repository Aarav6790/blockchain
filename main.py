import hashlib
import time
from ecdsa import SigningKey, SECP256k1, VerifyingKey
import datetime


class Block:
    def __init__(self, sender, reciever, amount, prev_hash, index,nonce=0):
        self.next = None
        self.nonce = nonce
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
        self.prev_hash = prev_hash
        self.index = index
    def calculate_hash(self):
        data = str(self.sender)+str(self.reciever)+str(self.amount)+self.prev_hash+str(self.index)+str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()
    def show(self):
        print("----------------------")
        print("Index: ", self.index)
        print("Sender: ", self.sender)
        print("Reciever: ", self.reciever)
        print("Amount: ", self.amount)
        print("Previous Hash: ", self.prev_hash)
        print("Hash: ", self.calculate_hash())
        print("----------------------")

class Transaction:
    def __init__(self, sender, reciever, amount):
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
        self.timestamp = None
    def hash_transaction_data(self):
        data = str(self.sender)+str(self.reciever)+str(self.amount)
        self.hash = hashlib.sha256(data.encode()).hexdigest()
    def sign_transaction(self):
        self.signature = self.sender.private_key.sign(self.hash.encode()).hex()
    def verify_signature(self):
        return self.sender.public_key.verify(bytes.fromhex(self.signature), self.hash.encode())
    def verify_balance(self):
        return self.sender.balance >= self.amount
    def approve_transaction(self):
        if self.verify_balance():
            self.hash_transaction_data()
            self.sign_transaction()
            if self.verify_signature():
                return True
            else:
                print("Invalid signature")
                return False
        else:
            print("Insufficient balance")
            return False
        
class Wallet:
    def __init__(self, balance=0):
        self.blockcounter = 0
        self.blockchain = Blockchain()
        self.balance = balance
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.str_private_key = self.private_key.to_string().hex()
        self.str_public_key = self.public_key.to_string("compressed").hex()
        self.username = input("Enter username: ")
        self.password = hashlib.sha256(input("Enter Password: ").encode()).hexdigest()
        print("New wallet created")
        print("Public key: ", self.str_public_key)
        print("Private key: ", self.str_private_key)
    def send(self, reciever, amount):
        tx = Transaction(self, reciever, amount)
        if tx.approve_transaction():
            self.blockcounter += 1
            self.balance -= amount
            reciever.balance += amount
            tx.timestamp = datetime.datetime.now()
            block = Block(tx.sender.str_public_key, tx.reciever.str_public_key, tx.amount, self.blockchain.get_latest_block().calculate_hash(), self.blockcounter)
            self.blockchain.mine_block(block)
            self.blockchain.add_block(block)
            print("Transaction successful")
            print("Remaining balance: ", self.balance)
    

class Blockchain:
    def __init__(self):
        Genesis_block = self.head = self.tail = Block("Genesis", "Genesis", 0, "0"*64, 0)
        self.difficulty = 4
    
    def get_latest_block(self):
        return self.tail
    
    def add_block(self, block):
        self.tail.next = block
        self.tail = block
    
    def mine_block(self, block):
        target = '0' * self.difficulty
        while block.calculate_hash()[:self.difficulty] != target:
            block.nonce += 1
            if block.nonce%100000 == 0:
                print(block.nonce)
        print("----------------------")
        print("\n")
        print("Block mined:", block.calculate_hash(), "Nonce: ", block.nonce)
        print("\n")
    
    def is_chain_valid(self):
        current = self.head
        while current.next:
            if current.calculate_hash() != current.next.prev_hash:
                return False
            current = current.next
        return True
    
    def show_chain(self):
        current = self.head
        while current:
            current.show()
            current = current.next
            

class Standard_Blockchain:
    def __init__(self):
        self.blockchain = Blockchain()
    def update_blockchain(self, blockchain):
        self.blockchain = blockchain

def main():
    standard_blockchain = Standard_Blockchain()
    wallets = []
    
    w1 = Wallet(100)
    w2 = Wallet(50)
    wallets.append(w1)
    wallets.append(w2)
            
    
    w1.send(w2, 10)
    w1.send(w2, 10)
    for wallet in wallets:
        if wallet.blockchain.get_latest_block().index > standard_blockchain.blockchain.get_latest_block().index:
            standard_blockchain.update_blockchain(wallet.blockchain)
    
    print("Is blockchain valid?", standard_blockchain.blockchain.is_chain_valid())
    standard_blockchain.blockchain.show_chain()

main()
