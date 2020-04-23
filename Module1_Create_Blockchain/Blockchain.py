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
        self.genesis = self.create_block(proof = 1, prev_hash = '0')
        self.genesis_hash = self.hash(self.genesis)
    
    def create_block(self, proof, prev_hash):
        block = {'index':      len(self.chain) + 1,
                 'time_stamp': str(datetime.datetime.now()), 
                 'proof':      proof,
                 'prev_hash':  prev_hash}
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return(self.chain[-1])

    #Proof of Work: challenging to find hard to verify
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #Equation inside hashlib must be asymmetric, the more complicated the better
            hash_val = self.hash_operation(prev_proof, new_proof)
            if hash_val[:6] == '000000':
               check_proof = True
            else:
               new_proof += 1
        return new_proof

    def hash_operation(self, prev_proof, proof):
        y = 2
        y = y^3
        return hashlib.sha256(str((4^13*y-proof**2) - prev_proof**2*22/y).encode()).hexdigest()

    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_num = 0
        while block_num < len(chain):
            if block_num == 0 and self.hash(previous_block) == self.genesis_hash:
               block_num += 1
               continue
            block = chain[block_num]
            if block['prev_hash'] != self.hash(previous_block):
               return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_val = self.hash_operation(previous_proof, proof)
            if hash_val[:4] != '0000':
               return False
            previous_block = block
            block_num += 1
        return True
        
#Part 2 - Mining our Blockchain

#Creating a Web App
app = Flask(__name__)
blockchain = Blockchain()
print(blockchain.chain)

#Mining New Block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_proof = blockchain.get_prev_block()['proof']
    new_proof = blockchain.proof_of_work(prev_proof)
    previous_hash = blockchain.hash(blockchain.get_prev_block())
    block = blockchain.create_block(new_proof, previous_hash)
    response = {'message': 'Congratulations you just mined a block!',
                'index': block['index'],
                'timestamp': block['time_stamp'],
                'proof': block['proof'],
                'previous_hash': block['prev_hash']}
    print(response)
    #200 is an http status code for success
    return jsonify(response), 200

#Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain':  blockchain.chain, 
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#Validating the blockchain
@app.route('/chain_is_valid', methods = ['GET'])
def is_valid():
    if blockchain.is_chain_valid(blockchain.chain) == True:
       response =  'Yes! The chain is valid!'
    else:
       response = 'No the chain has been comprimised'
    return jsonify(response), 200

#Running the App
#From flask's quickstart guide, we can use 0.0.0.0 to make the app public, port 5000 also from the quickstart guide
app.run(host = '0.0.0.0', port = 5000)
