##블록 생성 시

from transaction_db import tx_db


aaaa=tx_db.Make_block_first(10)
print(aaaa)

tx_db.Make_block_last(aaaa)