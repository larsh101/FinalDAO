from time import time,strftime,localtime
from classes.voteset import *
from util.hashing import hash_string_256

class Input():
    def __init__(self):
        pass
    
    @staticmethod
    def transaction_input(Ulist):
        while 1:
            recipient = input('Enter the recipient or "q" to exit: ')
            if recipient in Ulist:
                amount = float(input('Enter the amount: '))
                return (recipient,amount)
            elif recipient == 'q':
                return recipient
            else:
                print('{} is no valid user of the chain'.format(recipient))
        

    @classmethod
    def vote_input(cls,data):
        print('\n\nWhat do you want to vote on?\n')
        print('1: Raise funds')
        print('2: Acquire Building')
        print('3: Dispose Building')
        print('q: Quit')
        choice = input('Choose: ')
        if choice == '1':
            return raise_funds()
        elif choice == '2':
            return aquire_bldg(data)
        elif choice == '3':
            return dispose_bldg(data)
        elif choice == 'q':
            return [False]
        #return (ano,top,des,opt)

    @staticmethod
    def select_vote_input(indexlist):
        while 1:
            num = input("Please select the number for the topic you want to vote on or 'q' to end: ")
            if num == 'q':
                return num
            try:
                num = int(num)
                if num in indexlist:
                    return num
                else:
                    print("\n\nInvalid input!")
            except ValueError:
                print("\n\nInvalid input, please enter a number!")
            
    @staticmethod
    def make_vote(block):
        a = block.content[0]
        print(a.topic + ' - ' + str(a.description))
        print('Please select on of the following\n')
        x = 0
        for i in a.options:
            x += 1
            print(str(x)+': '+i)
        while 1:
            choice = input('Your choice: ')
            try:
                choice = int(choice)
                if choice <= len(a.options) and choice > 0:
                    return a.options[choice-1]
                else:
                    print("\n\nInvalid input!")
            except ValueError:
                print("\n\nInvalid input, please enter a number!")

    @staticmethod
    def sell_token_input():
        print('\nPlease enter the conditions to sell tokens\n\n')
        while 1:
            tokens = input('How many tokens do you want to sell?\n')
            price = input('Enter a price for the tokens: ')
            try:
                tokens = float(tokens)
                price = float(price)
                break
            except:
                print('Invalid input')
        timestamp = 'Offer at {}'.format(strftime('%Y-%m-%d %H:%M:%S', localtime(time())))
        return [tokens,price,timestamp]
    
    @staticmethod
    def choose_offer(offerlist):
        print('Enter the offernumber to take the offer.')
        print('Type "q" if you do not want to take an offer and leave.')
        while 1:
            choice = input('Choose: ')
            try:
                choice = int(choice)
                return choice
            except:
                if choice == 'q':
                    return choice
                else:
                    print('Invalid input.')

    @staticmethod
    def new_user():
        print('----------------------------------------------------------------------')
        print('We are looking forward to welcome you as a new member of this network.\n')
        print('Please enter the required information. Once you hit ENTER you will not')
        print('be able to change your input afterwards. Be careful about your input!\n')
        while 1:
            name = input('Your log in name   :')
            pw = input('Choose a password  :')
            if name == "" or pw == "":
                print('Invalid input!')
            else:
                break
        print('\n######################################################################')
        print('As soon as your transaction was mined you will have access.\n')
        print('Please note that once you forgot your login name or password, you will')
        print('lose access to this network.')
        print('######################################################################\n\n')
        tohash = name+pw
        return hash_string_256(tohash.encode())