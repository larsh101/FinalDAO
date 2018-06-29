from classes.blocks import Block
from classes.transaction import Transaction
from classes.vote import Vote
from classes.voted import Voted
from classes.key import Key

def b_trans(blockchain,__kind):
    updated_blockchain = []
    for block in blockchain:
        converted_tx = [Transaction(tx['sender'],tx['recipient'],tx['amount'],tx['kind']) for tx in block['content']]
        updated_block = Block(block['index'], block['phash'],converted_tx, block['proof'], block['timestamp'])
        updated_blockchain.append(updated_block)
    updated_transactions = []
    for tx in __kind:
        updated_transaction = Transaction(tx['sender'],tx['recipient'],tx['amount'],tx['kind'])
        updated_transactions.append(updated_transaction)
    return updated_blockchain,updated_transactions

def v_trans(blockchain,__kind):
    updated_blockchain = []
    for block in blockchain:
        converted_tx = [Vote(tx['anonymous'],tx['topic'],tx['description'],tx['options']) for tx in block['content']]
        updated_block = Block(block['index'], block['phash'],converted_tx, block['proof'], block['timestamp'])
        updated_blockchain.append(updated_block)
    updated_transactions = []
    for tx in __kind:
        updated_transaction = Vote(tx['anonymous'],tx['topic'],tx['description'],tx['options'])
        updated_transactions.append(updated_transaction)
    return updated_blockchain,updated_transactions

def k_trans(blockchain,__kind):
    updated_blockchain = []
    for block in blockchain:
        converted_tx = [Key(tx['index'],tx['user'],tx['key']) for tx in block['content']]
        updated_block = Block(block['index'], block['phash'],converted_tx, block['proof'], block['timestamp'])
        updated_blockchain.append(updated_block)
    updated_transactions = []
    for tx in __kind:
        updated_transaction = Key(tx['index'],tx['user'],tx['key'])
        updated_transactions.append(updated_transaction)
    return updated_blockchain,updated_transactions

def vd_trans(blockchain,__kind):
    updated_blockchain = []
    for block in blockchain:
        converted_tx = [Voted(tx['index'],tx['user'],tx['vote']) for tx in block['content']]
        updated_block = Block(block['index'], block['phash'],converted_tx, block['proof'], block['timestamp'])
        updated_blockchain.append(updated_block)
    updated_transactions = []
    for tx in __kind:
        updated_transaction = Voted(tx['index'],tx['user'],tx['vote'])
        updated_transactions.append(updated_transaction)
    return updated_blockchain,updated_transactions