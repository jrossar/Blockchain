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
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] is '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

#Part 2 - Mining our Blockchain