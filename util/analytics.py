from functools import reduce
from time import time,strftime,localtime
from classes.buildings import Buildings

def get_userlist(chain):
    userlist = set()
    tabu = ('MINING','TRADE','Realized','money transaction','BANK','Valuation','Previous Owner','Future Owner','Market Revenue')
    for i in chain:
        for j in i.content:
            # if j.sender != "MINING" and j.recipient != "TRADE" and j.recipient != "Realized" and j.kind != "money transaction":
            if type(j.sender) == str:
                userlist.add(j.sender)
            if type(j.recipient) == str:
                userlist.add(j.recipient)
    for item in tabu:
        try:
            userlist.remove(item)
        except:
            continue
    return userlist

def get_balance(chain,kind,value):
    balance = {}
    total = 0
    bank = 0.0
    revenue = 0.0
    userlist = get_userlist(chain)
    for participant in userlist:
        tx_sender = [[tx.amount for tx in block.content if tx.sender == participant and (tx.kind == 'token transaction' or tx.kind == 'opening transaction')] for block in chain]
        open_tx_sender = [tx.amount for tx in kind if tx.sender == participant and (tx.kind == 'token transaction' or tx.kind == 'opening transaction')]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.content if tx.recipient == participant and (tx.kind == 'token transaction' or tx.kind == 'opening transaction')] for block in chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        a = {participant:amount_received-amount_sent}
        balance.update(a)
    for i in balance.keys():
        total = total + balance[i]

    for block in chain:
        for trans in block.content:
            if 'Raise' in trans.kind and trans.recipient == 'Realized':
                bank = bank + trans.amount
            elif trans.recipient == 'BANK':
                bank = bank + trans.amount
            elif trans.sender == 'BANK':
                bank = bank - trans.amount
            if trans.kind == 'Revenue':
                revenue = trans.amount
    
    balance.update({'Revenue':revenue})
    balance.update({'BANK':bank})
    balance.update({'Equity':bank + value})
    balance.update({'Total':total})
    balance.update({'Value':value})
    return balance

def get_voting_result(vote,voted,key,check=False,balance={}):
    indexlist = set()
    results = {}
    [indexlist.add(i.index) for i in vote]
    indexlist.remove(0)
    # Create empty result dict
    for i in vote:
        opt_res={}
        index = i.index
        if i.index != 0:
            for content in i.content:
                for option in content.options:   
                    res = {option:0}
                    opt_res.update(res)
            res = {index:opt_res}
            results.update(res)
    # Count all the votes
    for i in voted:
        if i.index != 0:
            for v in i.content:
                if v.user != 'FINAL':
                    results[v.index][v.vote] = results[v.index][v.vote] + balance[v.user]
    # Check if vote is done
    participants = []
    ended_votes = set()
    final_ended = set()
    to_end = set()
    for block in voted:
        for v in block.content:
            if v.vote == 'FINAL':
                final_ended.add(v.index)
    [participants.append(len(i.content)) for i in key]
    [ended_votes.add(index) for index in final_ended]
    for i in results.keys():
        count = 0
        for c in results[i]:
            count = results[i][c] + count
        # if participants[i] == count:
        #     ended_votes.add(i)
        if (time() - vote[i].timestamp) > 604800: #sec -> one week
            ended_votes.add(i)
        for x in results[i].keys():
            if 0.5 < ((results[i][x])/balance['Total']):
                ended_votes.add(i)
    if check == True:
        for i in results.keys():
            check = False if not i in ended_votes else True
        return check
    # check who has voted
    who = {}
    for index in indexlist:
        who.update({index:[]})
        for block in voted:
            for v in block.content:
                if index == v.index:
                    who[index].append(v.user)
    [to_end.add(index) for index in ended_votes]
    try:
        [to_end.remove(index) for index in final_ended]
    except:
        pass
    #return data
    return [results,participants,ended_votes,who,to_end]

def check_offer(chain):
    offerlist = {}
    offers = []
    c = 1
    print('\nSee the available offers below:\n\n')
    for i in chain:
        for j in i.content:
            if ('Offer' in j.kind or 'Raise' in j.kind) and j.recipient != 'Realized':
                #print(str(c) + ': {0:1}: {1:8} tokens for {2:10} Euro. ({3:1} €/Token)\n'.format(j.kind,j.amount,j.recipient,(j.recipient/j.amount)))
                offers.append(j.kind)
            elif j.recipient == 'Realized':
                offers.remove(j.kind)
    for i in offers:
        offer = {c:i}
        c+=1
        offerlist.update(offer)
    c=1
    for i in chain:
        for j in i.content:
            if j.kind in offers:
                print(str(c) + ': {0:1}: {1:8} tokens for {2:10} Euro. ({3:1} €/Token)\n'.format(j.kind,j.amount,j.recipient,(j.recipient/j.amount)))
                #print(str(c) + ': {0:1}: {1:8} tokens for {2:10} Euro. ( €/Token)\n'.format(j.kind,j.amount,j.recipient))
                c+=1
    if offerlist == {}:
        print('There seem to be no offers.\n')
    else:
        return offerlist

def check_raise(vote,ended,results):
    to_proceed = []
    for end in ended:
        if results[end]['Yes'] > results[end]['No']:
            for block in vote:
                if end == block.index:
                    if 'Raise Funds' in block.content[0].topic:
                        transaction = [block.content[0].description[1],block.content[0].description[0],'Raise through vote number {}'.format(end)]
                        to_proceed.append(transaction)
    return to_proceed

def check_aq(vote,ended,results):
    to_proceed = []
    for end in ended:
        if results[end]['Yes'] > results[end]['No']:
            for block in vote:
                if end == block.index:
                    if 'aquisition' in block.content[0].topic:
                        transaction = [block.content[0].description[0],'Previous Owner',['Aquisition no. {}'.format(end),block.content[0].description[1]]]
                        to_proceed.append(transaction)
    return to_proceed

def check_dis(vote,ended,results):
    to_proceed = []
    for end in ended:
        if results[end]['Yes'] > results[end]['No']:
            for block in vote:
                if end == block.index:
                    if 'disposal' in block.content[0].topic:
                        transaction = [block.content[0].description[0],'BANK',['Disposal no. {}'.format(end),block.content[0].description[1]]]
                        to_proceed.append(transaction)
    return to_proceed

def buildings(buildings,transactions,old_value):
    revenues = 0
    value = 0
    for building in buildings:
        if building.own == True:
            value = value + building.current
    if value != old_value:
        for building in buildings: 
            if building.own == True:
                revenues = revenues + building.rent
    return [value,revenues]
