from blockchain import Blockchain
from classes.vote import Vote
from classes.buildings import Buildings
from util.inputs import Input
from util.verification import Verification
from util.analytics import * #get_voting_result
from util.display import * #display_transactions, display_voting, display_balance
from util.hashing import hash_string_256
from mining.mining import approve,check_if_apprv,open_user
from time import sleep
import random

class Run:
    def __init__(self,user):
        self.value = 0
        self.user = user
        self.vote = Blockchain(self.user,'vote')
        self.voted = Blockchain(self.user,'voted')
        self.blockchain = Blockchain(self.user,'transaction')
        self.key = Blockchain(self.user,'key')
        self.userlist = self.blockchain.userlist()
        self.portfolio = []
        self.get()
        if self.login(self.userlist):
            self.front_end()

    def get_choice(self):
        choice = input('Your choice: ')
        return choice

    def retrieve_balance(self):
        return self.blockchain.balance(True,self.value)

    def valuation(self):
        old_value = 0
        for block in self.blockchain.chain:
            for trans in block.content:
                if trans.kind == 'Valuation':
                    old_value = trans.amount
        for trans in self.blockchain.kind:
            if trans.kind == 'Valuation':
                old_value = trans.amount
        data = buildings(self.portfolio,self.blockchain.chain,old_value)
        self.value = data[0]
        revenue = data[1]
        if self.value != old_value:
            if self.blockchain.add_transaction('Valuation','Valuation','Valuation',amount=self.value,check=False):
                print('\n\n\n----------------------------------------')
                print('New value of the portfolio {0:.2f} €'.format(self.value))
                print('----------------------------------------')
            else:
                print('Valuation error!')
            if self.blockchain.add_transaction('BANK','Market Revenue','Revenue',amount=revenue,check=False):
                pass
            else:
                print('Revenue error')
        else:
            print('\n\n\n----------------------------------------')
            print('There are no changes in your portfolio.')
            print('Value remains at {0:.2f} €'.format(self.value))
            print('----------------------------------------')

    def loading(self,backup=False,only=False):
        self.vote.load_data(backup)
        self.voted.load_data(backup)
        self.blockchain.load_data(backup)
        self.key.load_data(backup)
        
        data = get_voting_result(self.vote.chain,self.voted.chain,self.key.chain,balance=self.retrieve_balance())
        voting_results = data[0]
        voting_participants = data[1]
        voting_ended = data[2]
        voting_who = data[3]
        to_end = data[4]
        self.publish(voting_ended, voting_results)
        self.trans_aquire(voting_ended, voting_results)
        self.trans_dispose(voting_ended, voting_results)
        self.check_own()
        self.valuation()

    def saving(self,backup=False):
        self.vote.save_data(backup)
        self.voted.save_data(backup)
        self.blockchain.save_data(backup)
        self.key.save_data(backup)

    def finalize_vote(self,to_end):
        for index in to_end:
            self.loading()######################################################
            self.voted.add_voted(index,'FINAL','FINAL')
            self.voted.mine_block()
            print('A vote has ended!')

    def proof_chain(self):
        print('                         Offers checked.\n')
        if Verification.verify_chain(self.blockchain.chain,check=True) and Verification.verify_chain(self.vote.chain) and Verification.verify_chain(self.voted.chain) and Verification.verify_chain(self.key.chain):
            print('                   Transactions proofed.')
            print('                        Votings proofed.')
            print('                          Votes proofed.')
            print('                           Keys proofed.')
            print('----------------------------------------')


    def trans_pass(self):
        ans = get_voting_result(self.vote.chain,self.voted.chain,self.key.chain,check=True,balance=self.retrieve_balance())
        if not ans:
            print('\n\n----------------------------------------------------------------')
            print('Your request has been denied, as there are one or more open votes')
            print('----------------------------------------------------------------\n\n')
        return ans

    def mine_appr(self):
        open_user(self.user)
        print('\n\n\n\n\n')
        print('-----------------------------------')
        print('You can lean back while the program')
        print('is doing the rest for you.')
        print('-----------------------------------')
        while 1:
            if check_if_apprv():
                self.loading(only=True)
                print('approving...')
                savable = self.blockchain.return_text()
                if approve(self.user,savable):
                    print('--------------------------')
                    print('Thank you for your help.')
                    print('Your reward is on his way!')
                    print('--------------------------')
                    sleep(5)
                    break
                else:
                    print('--------------------------')
                    print('You are not in consent.')
                    print('Thank you anyway.')
                    print('Your reward is on his way!')
                    print('--------------------------')
                    sleep(5)
                    break

    def login(self,userlist):
        while 1:
            if self.user == 'TRADE':
                self.publish
                offerlist = self.blockchain.offerlist()
                if offerlist == None:
                    return False
                else:
                    choice = Input.choose_offer(offerlist)
                    if choice == 'q':
                        return False
                    else:
                        if self.trans_pass():
                            self.blockchain.create_user(offerlist,choice)
                            return False

            else:
                if self.user in userlist:
                    return True
                else:
                    print('User not found or wrong password----------------------------')
                    return False
                        
    def front_end(self):
        self.proof_chain()
        waiting_for_input = True
        if self.user == 'exit':
            waiting_for_input = False
        while waiting_for_input:
            self.loading()
            print('\n\n\nWelcome to the RIECK-BLOCKCHAIN-DAO')
            print('This is your account number: {}\n'.format(self.user))
            print('Choose:')
            print('1: Manage token system')
            print('2: Manage votings')
            print('3: Status')
            print('4: Support the system by prooving')
            print('5: Simulate market')
            print('l: Log out')
            print('p: print raw chains')
            # print('q: Quit Program')
            choice = self.get_choice()
            if choice == '1':
                self.trans_front_end()
            elif choice == '2':
                self.vote_front_end()
            elif choice == '3':
                self.status_front_ent()
            elif choice == '4':
                self.mine_appr()
            elif choice == '5':
                self.new_prices()
                self.loading
            elif choice == 'l':
                # self.user = None
                # self.login()
                waiting_for_input = False
            elif choice == 'p':
                self.blockchain.print_everything()
                self.vote.print_everything()
                self.voted.print_everything()
                self.key.print_everything()

    def trans_front_end(self):
        waiting_for_input = True
        while waiting_for_input:
            print('\n\n\n\n')
            print('Choose:')
            print('1: Add token transaction')
            print('2: Mine a transaction block')
            print('3: Sell tokens')
            print('q: Quit')
            choice = self.get_choice()
            if choice == '1':
                if self.trans_pass():
                    data = Input.transaction_input(self.userlist)
                    if data != 'q':
                        recipient,amount = data
                        self.loading()######################################################
                        if self.blockchain.add_transaction(recipient,self.user,'token transaction',amount=amount):
                            print('Added transaction')
                        else:
                            print('Transaction failed!')
            elif choice == '2':
                self.loading()######################################################
                self.blockchain.mine_block()
            elif choice == '3':
                if self.trans_pass():
                    data = Input.sell_token_input()
                    self.loading()######################################################
                    if self.blockchain.add_transaction(data[1],self.user,data[2],amount=data[0]):
                        print('Offer published')
                    else:
                        print('Request denied!')
            elif choice == 'q':
                waiting_for_input = False
            elif choice == 'x':
                pass
            else:
                print('Input was invalid, please pick a value from the list!')
                print(self.user)
                print('Balance of {}: {:6.2f}'.format(self.user, self.blockchain.balance(False,self.value)))

    def vote_front_end(self):
        waiting_for_input = True
        while waiting_for_input:
            self.loading()
            data = get_voting_result(self.vote.chain,self.voted.chain,self.key.chain,balance=self.retrieve_balance())
            voting_results = data[0]
            voting_participants = data[1]
            voting_ended = data[2]
            voting_who = data[3]
            to_end = data[4]
            if to_end != set():    
                self.finalize_vote(to_end)
            print('\n\n\n\n')
            print('Choose:')
            print('1: Open new vote')
            print('2: Vote on existing topic')
            print('3: Mine a voting block')
            print('4: Analyze votes')
            print('q: Quit')
            choice = self.get_choice()
            if choice == '1':
                self.loading()######################################################
                data = Input.vote_input([self.portfolio,self.retrieve_balance(),voting_ended,self.vote.chain])
                if data[0]:
                    data = data[1]
                    self.loading()######################################################
                    self.vote.add_vote(self.user, data)
                    self.loading()######################################################
                    self.vote.mine_block()
                    index = self.vote.chain[-1].index
                    for user in self.userlist:
                        key = Vote.create_key(user)
                        self.key.add_key(index,user,key)
                    self.key.mine_block()
                else:
                    print('Vote canceled!')
            elif choice == '2':
                self.loading()######################################################
                indexlist = []
                for i in self.vote.chain:
                    if i.index != 0 and i.index not in voting_ended:
                        indexlist.append(i.index)
                if indexlist != []:
                    print('\n\nOpen votes:')
                    print('-----------\n')
                    for index in indexlist:
                        print(' {0:3}: {1:1}'.format(index,self.vote.chain[index].content[0].topic))
                    print('\n\n')
                    num = Input.select_vote_input(indexlist)
                    if num != 'q':
                        if voting_who != {}:
                            try:
                                if self.user in voting_who[num]:
                                    print('----------------------------------------')
                                    print('You have alredy taken part at this vote!')
                                    print('----------------------------------------')
                                else:
                                    block = [i for i in self.vote.chain if i.index == num][0]
                                    choice = Input.make_vote(block)
                                    self.loading()######################################################
                                    self.voted.add_voted(num,self.user,choice)
                                    self.voted.mine_block()
                            except:
                                block = [i for i in self.vote.chain if i.index == num][0]
                                choice = Input.make_vote(block)
                                self.loading()######################################################
                                self.voted.add_voted(num,self.user,choice)
                                self.voted.mine_block()
                        else:
                            block = [i for i in self.vote.chain if i.index == 1][0]
                            choice = Input.make_vote(block)
                            self.loading()######################################################
                            self.voted.add_voted(num,self.user,choice)
                            self.voted.mine_block()
                else:
                    print('\n\n---------------------------------------------')
                    print('There is no open vote. (Transactions allowed)')
                    print('---------------------------------------------\n\n')
            elif choice == '3':
                print('\n\n----------\nFunction removed\n----------\n')
            elif choice == '4':
                print('Please note that the analysis of the votes only takes votes into consideration that are already chained.')
                print('---------------------------------')
                print(voting_results)
                print('---------------------------------')
                print(voting_participants)
                print('---------------------------------')
                print(voting_ended)
                print('---------------------------------')
                print(voting_who)
                print('---------------------------------')
                print(to_end)
                print('---------------------------------')
            elif choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
    
    def status_front_ent(self):
        waiting_for_input = True
        while waiting_for_input:
            self.loading() 
            print('\n\n\n\n')
            print('Choose:')
            print('1: Show transactions')
            print('2: Show votings')
            print('3: Show balances')
            print('4: Show real estate market')
            print('q: Quit')
            choice = self.get_choice() 
            if choice == '1':
                self.loading()######################################################
                display_transactions(self.blockchain.chain)
            elif choice == '2':
                self.loading()######################################################
                data = get_voting_result(self.vote.chain,self.voted.chain,self.key.chain,balance=self.retrieve_balance())
                display_voting(self.vote.chain,data,self.retrieve_balance())
            elif choice == '3':
                self.loading()######################################################
                balance = self.retrieve_balance()
                display_balance(balance)
            elif choice == '4':
                display_portfolio(self.portfolio)
            elif choice == 'q':
                waiting_for_input = False

    def get(self): 
        import csv
        with open('i.csv') as i:
            reader = csv.reader(i, delimiter=';')
            portfolio = []
            for row in reader:
                data = Buildings(row[0],float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),int(row[9]),row[10],int(row[11]),float(row[12]),row[13],int(row[14]))
                portfolio.append(data)
        self.portfolio = portfolio

    def search_kind(self,content):
        for block in self.blockchain.chain:
            for inner in block.content:
                if inner.kind == content:
                    return True
        for inner in self.blockchain.kind:
            if inner.kind == content:
                    return True
        return False

    def check_own(self):
        bdlglist = {}
        for item in self.portfolio:
            bdlglist.update({item.id:False})
        for block in self.blockchain.chain:
            for trans in block.content:
                if 'Aquisition' in trans.kind[0]:
                    bdlglist[trans.kind[1]] = True
                elif 'Disposal' in trans.kind[0]:
                    bdlglist[trans.kind[1]] = False
        for bldg in self.portfolio:
            bldg.own = bdlglist[bldg.id]

    def new_prices(self):
        for bldg in self.portfolio:
            bldg.t_7 = bldg.t_6
            bldg.t_6 = bldg.t_5
            bldg.t_5 = bldg.t_4
            bldg.t_4 = bldg.t_3
            bldg.t_3 = bldg.t_2
            bldg.t_2 = bldg.t_1
            bldg.t_1 = bldg.current
            bldg.current = bldg.current * (random.randint(95,105)/100)
    
    def trans_aquire(self, voting_ended, voting_results):
        aqlist = check_aq(self.vote.chain,voting_ended,voting_results)
        for data in aqlist:
            if not self.search_kind(data[2]):
                if self.blockchain.add_transaction(data[1],'BANK',data[2],amount=data[0],check=False):
                    print('Aquisition in progress')
                else:
                    print('Request denied!')
        return True
        
    def trans_dispose(self, voting_ended, voting_results):
        aqlist = check_dis(self.vote.chain,voting_ended,voting_results)
        for data in aqlist:
            if not self.search_kind(data[2]):
                if self.blockchain.add_transaction(data[1],'Future Owner',data[2],amount=data[0],check=False):
                    print('Disposal in progress')
                else:
                    print('Request denied!')
        return True

    def publish(self, voting_ended, voting_results):
        raiselist = check_raise(self.vote.chain,voting_ended,voting_results)
        for data in raiselist:
            if not self.search_kind(data[2]):
                if self.trans_pass():
                    if self.blockchain.add_transaction(data[1],'MINING',data[2],amount=data[0],check=False):
                        print('Offer published')
                    else:
                        print('Request denied!')
        return True

while 1:
    print('\n\n\nWelcome, please log in or enter "TRADE" to check offers or "q" to end.')
    print('----------------------------------------------------------------------')
    name = input('Enter your name, please: ')
    if name == 'TRADE':
        run = Run(name)
    elif name == 'q':
        break
    else:
        pw = input('Enter your password, please: ')
        Hash = name + pw
        user = hash_string_256(Hash.encode())
        run = Run(user) 