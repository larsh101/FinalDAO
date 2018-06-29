import os
from os import listdir
from os.path import isfile, join
from time import time

def approve(user, kind):
    path = os.path.dirname(os.path.realpath(__file__)) + '/'
    f=open(path + 'to_approve.txt', 'r')
    contents = f.read()
    f.close()
    if contents == kind:
        os.remove(path + user+'.txt')
        open(path + user+'-ok.txt','w')
        while 1:
            files = [f for f in listdir(path) if isfile(join(path, f))]
            if 'to_approve.txt' in files:
                pass
            else:
                os.remove(path + user+'-ok.txt')
                return True
    else:
        os.remove(path + user+'.txt')
        return False

def check_if_apprv():
    path = os.path.dirname(os.path.realpath(__file__)) + '/'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return True if 'to_approve.txt' in files else False

def wait_for_apprvl(kind):
    path = os.path.dirname(os.path.realpath(__file__)) + '/'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    participans = len(files)
    if participans == 1:
            print('instant approval')
            return True
    print('no instant')
    f = open(path + 'to_approve.txt', 'w')
    f.write(kind)
    f.close()
    timestamp = time()
    while 1:
        if time() - timestamp > 5:
            remove_file()
            print('It does not seem like you are getting any approval.')
            print('---------------------------------------------------')
            return False
        files = [f for f in listdir(path) if isfile(join(path, f))]
        ok = 0
        for item in files:
            if 'ok' in item:
                ok+=1
        if ok > (participans-2)*0.5:
            remove_file()
            print('done')
            return True

def open_user(user):
    path = os.path.dirname(os.path.realpath(__file__)) + '/'
    open(path + user+'.txt','w')

def remove_file():
    path = os.path.dirname(os.path.realpath(__file__)) + '/'
    while 1:
        try:
            os.remove(path + 'to_approve.txt')
            return
        except:
            print('remove error')