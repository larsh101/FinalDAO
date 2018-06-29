from util.hashing import hash_block, hash_string_256

class Verification:
    @staticmethod
    def valid_proof(block, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in block]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:4] == '0000'

    @classmethod
    def verify_chain(cls, blockchain, check=False):
        for (index,block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.phash != hash_block(blockchain[index - 1]):
                print('-----------------------------------------')
                print('Error at block {}!'.format(index))
                print('-----------------------------------------')
                return False
            if check == True:
                if not cls.valid_proof(block.content[:-1], block.phash, block.proof):
                    print('-----------------------------------------')
                    print('Error at block {}!'.format(index))
                    print('-----------------------------------------')
                    return False
            elif check == False:
                if not cls.valid_proof(block.content, block.phash, block.proof):
                    print('-----------------------------------------')
                    print('Error at block {}!'.format(index))
                    print('-----------------------------------------')
                    return False
        return True
    
    @staticmethod
    def verify_transaction(transaction,get_balance):
        sender_balance = get_balance
        return sender_balance >= transaction.amount

    @classmethod
    def verify_transactions(cls,open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])