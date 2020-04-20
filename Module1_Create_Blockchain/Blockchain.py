import datetime
import hashlib
import json
from flask import Flask, jsonify

#Part 1 - Building a Blockchain

class Blockchain:
    def __init__(self):
        #to append the different blocks that are mined later
        self.chain = []
        #prev_has for genesis is arbritrary
        self.genesis = create_block(proof = 1, prev_hash = '0')
    
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'time_stamp': str(datetime.datetime.now()), 
                 'proof': proof,
                 'prev_hash': prev_hash}
        self.chain.append(block)
        return block

    def get_last_block(self):
        return(self.chain[-1])

    #Proof of Work: challenging to find hard to verify
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #Equation inside hashlib must be asymmetric, the more complicated the better
            hash_val = hash_operation(prev_proof, new_proof)
            if hash_val[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash_operation(self, prev_proof, proof):
        return hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()

    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_num = 0
        while block_num < len(chain):
            block = chain[block_num]
            if block['prev_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_val = hash_operation(previous_proof, proof)
            if hash_val[:4] != '0000':
                return False
            previous_block = block
            block_num += 1
        return True
             

            


#Part 2 - Mining our Blockchain