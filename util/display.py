from time import strftime, localtime

def display_transactions(chain):
    print('\n\nP2P Transactions:\n')
    print(' {0:7}{1:23}{2:66}{3:66}{4:10}{5:20}\n'.format('Index','Time','Sender','Recipient','Amount','Type'))
    for i in chain:
        time = strftime('%Y-%m-%d %H:%M:%S', localtime(i.timestamp))
        for t in i.content:
            if t.sender != 'MINING' and t.kind == 'token transaction':
                print(' {0:7}{1:23}{2:66}{3:66}{4:10}{5:20}'.format(str(i.index),time,t.sender,t.recipient,str(t.amount),t.kind))
    print('\n\nMined Blocks:\n')
    print(' {0:7}{1:23}{2:70}{3:15}\n'.format('Index','Time','Miner','Received Reward'))
    for i in chain:
        time = strftime('%Y-%m-%d %H:%M:%S', localtime(i.timestamp))
        for t in i.content:
            if t.sender == 'MINING' and t.kind == 'token transaction':
                print(' {0:7}{1:23}{2:70}{3:15}'.format(str(i.index),time,t.recipient,str(t.amount)))
    print('\n\n')

def display_voting(chain,data,balance):
    voting_results = data[0]
    voting_ended = data[2]
    print('\n\nList of Votings:\n')
    print(' {0:7}{1:23}{2:50}{3:15}{4:10}\n'.format('Index','Time','Topic','Status','Visibility'))
    for i in chain:
        if i.index != 0:
            time = strftime('%Y-%m-%d %H:%M:%S', localtime(i.timestamp))
            status = 'Ended' if i.index in voting_ended else 'Open'         
            for c in i.content:
                anonymous = 'Anonoymous' if c.anonymous else 'Identified'
                print(' {0:7}{1:23}{2:50}{3:15}{4:10}'.format(str(i.index),time,c.topic,status,anonymous))
    print('\n\nVoting Results:')
    for i in chain:
        if i.index in voting_ended:
            for c in i.content:
                print('\nVoting results for vote no. {} ({}):\n'.format(i.index,c.topic))
                for x in voting_results[i.index].keys():
                    print(' {0:15}  {1:13.2f} Percent'.format(x,((voting_results[i.index][x])/balance['Total'])*100))
    print('\n\n')

def display_balance(balance):
    print('\n\n {0:68} {1:12}{2:12}{3:12}\n'.format('User Identification','Balance','Share','Absolut'))
    for k in balance.keys():
        if k == 'Total' or k == 'BANK' or k == 'Equity' or k == 'Value' or k == 'Revenue':
            continue
        print(' {0:68} {1:10.0f}{2:10.2f}{3:10.2f}'.format(k,balance[k],(balance[k]/balance['Total'])*100,(balance[k]/balance['Total'])*balance['Equity']))
    print('\n {0:58} {1:20.0f} Tokens'.format('Total',balance['Total']))
    print('-'*81)
    print(' {0:58} {1:20.2f} €'.format('Equity',balance['Equity']))
    print('-'*81)
    print(' {0:58} {1:20.2f} €'.format('Bank',balance['BANK']))
    print(' {0:58} {1:20.2f} €'.format('Portfolio Value',balance['Value']))
    print('-'*81)
    print(' {0:58} {1:20.2f} €'.format('Portfolio Revenue',balance['Revenue']))
    print('-'*81)
    print('\n {0:58} {1:20.4f} €/Token'.format('Nominal price per token',balance['Equity']/balance['Total']))
    print('\n\n')

def display_portfolio(portfolio):
    c = 1
    bldglist = {}
    for bldg in portfolio:
        print('{0:3}: {1:8} {2:}'.format(c,bldg.id,'Owned' if bldg.own else ''))
        bldglist.update({c:bldg.id})
        c+=1
    print('\nSelect an opject to review:\n')
    print('{0:3}: {1:}'.format('q','Quit'))
    while 1:
        choice = input('\nChoose: ')
        try:
            choice = int(choice)
            break
        except:
            if choice == 'q':
                break
            else:
                pass
    if type(choice) == int:
        for b in portfolio:
            if bldglist[choice] == b.id:
                print('\nGeneral information:')
                print('ID {}, {}, Year: {}'.format(b.id,b.location,b.year))
                print('\nPrices:\n')
                print('{0:.2f}   {1:.2f}   {2:.2f}   {3:.2f}   {4:.2f}   {5:.2f}   {6:.2f}   {7:.2f}'.format(b.current,b.t_1,b.t_2,b.t_3,b.t_4,b.t_5,b.t_6,b.t_7))
