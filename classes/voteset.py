from time import time,strftime,localtime
def raise_funds():
    try:
        amount = float(input('How much equity do you want to raise? '))
        tokens = float(input('How many shares (Tokens) are you ready to issue? '))
        topic = 'Raise Funds by {}€'.format(amount)
        return [True,(True,topic,[amount,tokens],['Yes','No'])]
    except:
        return[False]

def aquire_bldg(data):
    portfolio = data[0]
    balance = data[1]
    ended = data[2]
    chain = data[3]
    print(ended)
    pending = set()
    for block in chain:
        if block.index != 0:
            if not block.index in ended and 'aquisition' in block.content[0].topic:
                pending.add(block.content[0].description[1])
    print(pending)
    while 1:
        print('Please check the following list to choose a building to aquire.')
        bldglist = {}
        c = 1
        for bldg in portfolio:
            if bldg.own == False and not bldg.id in pending:
                bldglist.update({c:bldg.id})
                print('{0:4}: {1:} at the currrent price of {2:} €'.format(c,bldg.id,bldg.current))
                c+=1
        print(bldglist)
        choice= input('\nPlease make your choice or enter "q" to quit: ')
        try:
            choice = int(choice)
            if choice in bldglist.keys():
                print('in keys')
                for bldg in portfolio:
                    if bldg.id == bldglist[choice]:
                        if bldg.current > balance['BANK']:
                            print('-----------------------')
                            print('Building not affortable')
                            print('-----------------------')
                        else:
                            topic = 'Building aquisition of {} on {}'.format(str(bldg.id),strftime('%Y-%m-%d %H:%M:%S', localtime(time())))
                            return [True,(True,topic,[bldg.current,bldg.id],['Yes','No'])]
        except:
            print('pass')
            pass
        if choice == 'q':
            return [False]

def dispose_bldg(data):
    portfolio = data[0]
    ended = data[2]
    chain = data[3]
    print(ended)
    pending = set()
    for block in chain:
        if block.index != 0:
            if not block.index in ended and 'disposal' in block.content[0].topic:
                pending.add(block.content[0].description[1])
    print(pending)
    while 1:
        print('Please check the following list to choose a building to dispose.\n')
        bldglist = {}
        c = 1
        for bldg in portfolio:
            if bldg.own == True and not bldg.id in pending:
                bldglist.update({c:bldg.id})
                print('{0:4}: {1:} at the currrent price of {2:} €'.format(c,bldg.id,bldg.current))
                c+=1
        if bldglist == {}:
            print('\n-----------------------------------------------')
            print('There are no Objects in your Portfolio to sell.')
            print('-----------------------------------------------')
            return [False]
        choice= input('\nPlease make your choice or enter "q" to quit: ')
        try:
            choice = int(choice)
            if choice in bldglist.keys():
                for bldg in portfolio:
                    if bldg.id == bldglist[choice]:
                        topic = 'Building disposal of {} on {}'.format(str(bldg.id),strftime('%Y-%m-%d %H:%M:%S', localtime(time())))
                        return [True,(True,topic,[bldg.current,bldg.id],['Yes','No'])]
        except:
            pass
        if choice == 'q':
            return [False]