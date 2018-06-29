import json
import pickle

from classes.transaction import Transaction
from classes.vote import Vote
from classes.voted import Voted
from classes.blocks import Block
from classes.key import Key
from util.hashing import hash_block
from util.verification import Verification
from util.analytics import get_balance,get_userlist,check_offer
from util.build_chain import b_trans,v_trans,k_trans,vd_trans
from util.inputs import Input
from mining.mining import wait_for_apprvl

MINING_REWARD = 1.0

class Blockchain:
    def __init__(self,host,kind):
        self.user = host
        #Transactions
        genesis_block = Block(0,'',[],100,0)
        self.chain = [genesis_block]
        self.kind = []
        self.file = kind
        #kind variable makes the same functions availible for different kind of chains
        self.load_data()

    # @property
    # def chain(self):
    #     return self.chain[:]

    # @chain.setter
    # def chain(self,val):
    #     self.chain = val
    
    def get_to_chain(self):
        return self.kind[:]

    def return_text(self):
        return json.dumps([tx.__dict__ for tx in self.kind])
    
    def print_everything(self):
        print('-'*30)
        print(self.chain)
        print('-'*30)
        print(self.kind)
        print('-'*30)

    def load_data(self,backup=False):
        backup = '_backup' if backup else ''
        try:
            with open(self.file + backup + '.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # __open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                kind = json.loads(file_content[1])
                if self.file == 'transaction':
                    updated_blockchain, updated_transactions = b_trans(blockchain,kind)
                elif self.file == 'vote':
                    updated_blockchain, updated_transactions = v_trans(blockchain,kind)
                elif self.file == 'key':
                    updated_blockchain, updated_transactions = k_trans(blockchain,kind)
                elif self.file == 'voted':
                    updated_blockchain, updated_transactions = vd_trans(blockchain,kind)
                # print(updated_blockchain)
                # print('\n')
                # print(updated_transactions)
                # print('\n')
                # print(type(updated_blockchain))
                # print('\n')
                # print(type(updated_transactions))
                self.chain = updated_blockchain
                self.kind = updated_transactions
        except IOError:
            pass

    def save_data(self,backup=False):
        backup = '_backup' if backup else ''
        try:
            with open(self.file + backup + '.txt', mode='w') as f:
                savable_chain = [block.__dict__ for block in [Block(block_el.index,block_el.phash,[tx.__dict__ for tx in block_el.content],block_el.proof,block_el.timestamp) for block_el in self.chain]]
                f.write(json.dumps(savable_chain))
                f.write('\n')
                savable_tx = [tx.__dict__ for tx in self.kind]
                f.write(json.dumps(savable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': __open_transactions 
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')
    
    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.kind, last_hash,proof):
            proof += 1
        return proof 

    def userlist(self):
        return get_userlist(self.chain)

    def offerlist(self):
        return check_offer(self.chain)

    def balance(self, check, value=0):
        balance = get_balance(self.chain,self.kind, value)
        return balance if check == True else balance[self.user]
    
    def add_transaction(self,recipient,sender,kind,amount=1.0,check=True):
        if sender == 'MINING' or sender == 'TRADE':
            check = False
        transaction = Transaction(sender,recipient,amount,kind)
        if check == True:
            if Verification.verify_transaction(transaction,self.balance(False)):
                self.kind.append(transaction)
                self.save_data()
                return True
        else:
            self.kind.append(transaction)
            self.save_data()
            return True
        return False

    def create_user(self,offerlist,choice):
        offer = offerlist[int(choice)]
        for i in self.chain:
            for j in i.content:
                if j.kind == offer:
                    print('\n\nOffer found. Ready to proceed.')
                    sender = j.sender
                    amount = j.recipient
                    tokens = j.amount
        recipient = Input.new_user()
        self.user = sender
        if self.add_transaction(recipient,sender,'opening transaction',amount=tokens):
            self.user = sender
            if self.add_transaction('Realized',sender,offer,amount=amount,check=False):
                print('All set!')
                return 
            else:
                print('Transaction failed!')
            self.mine_block()
        else:
            print('Procedure failed...')

    def add_vote(self,user,data):
        ano,top,des,opt = data
        vote = Vote(ano,top,des,opt)
        self.kind.append(vote)
        self.save_data()

    def add_key(self, index,user,key):
        key = Key(index,user,key)
        self.kind.append(key)
        self.save_data()

    def add_voted(self,index,user,vote):
        voted = Voted(index,user,vote) 
        self.kind.append(voted)
        self.save_data()

    def mine_block(self):
        savable = json.dumps([tx.__dict__ for tx in self.kind])
        # if savable == "[]":
        #     print('-----------------')
        #     print('No inout to mine.')
        #     print('-----------------')
        #     return True
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #     'sender':'MINING',
        #     'recipient':owner,
        #     'amount':MINING_REWARD
        # }
        copied_transactions = self.kind[:]
        if self.file == 'transaction':
            reward_transaction = Transaction('MINING',self.user,MINING_REWARD,'token transaction')
            copied_transactions.append(reward_transaction)
        block = Block(len(self.chain),hashed_block, copied_transactions,proof)
        if wait_for_apprvl(savable):
            self.chain.append(block)
            self.kind = []
            self.save_data()
            x = len('{} block successfully chained.'.format(self.file))
            print('-'*x)
            print('{} block successfully chained.'.format(self.file))
            print('-'*x)
        return True