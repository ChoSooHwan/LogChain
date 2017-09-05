from service.blockmanager import block
import json
from storage import file_controller
import hashlib


def genesisblock_generate():
    transaction = "Base lab logchain project"
    prev_hash = "N/A"
    nonce = "N/A"
    merkle_root = hashlib.sha256(str(transaction).encode('utf-8')).hexdigest()
    vote_result = "N/A"
    timestamp = "20170904"
    block_header = block.BlockHeader(
        prev_hash, nonce, merkle_root, vote_result, timestamp)

    block_header.block_id = 'genesis_block'
    block_header.block_number = "1"
    block_header.block_info = block_header.prev_hash + block_header.merkle_root
    block_header.block_hash = hashlib.sha256(
        str(block_header.block_info).encode('utf-8')).hexdigest()
    block_header.miner = "Base Lab"
    block_header.num_tx = "1"

    genesisblock = block.Block(block_header, transaction)
    json_genesisblock = json.dumps(
        genesisblock, indent=4, default=lambda o: o.__dict__, sort_keys=True)
    file_controller.create_new_block(
        str(block_header.block_number), json_genesisblock)
    print('genesisblock_create')


'Test Code'
if __name__ == '__main__':
    genesisblock_generate()
