import logging
import sys
from PyQt5 import QtWidgets
from monitoring import monitoring
import threading
from peerproperty import nodeproperty
from peerproperty import set_peer
from storage import file_controller
from communication.p2p import receiver
from service.blockmanager import genesisblock
from communication.msg_dispatch import dispatch_queue_list
from communication.msg_dispatch import t_type_queue_thread
from communication.msg_dispatch import b_type_queue_thread
from communication.msg_dispatch import v_type_queue_thread
from communication.peermgr import peermgr


# Logchain launcher function for TrustPeer
# TrustPeer acts as a peer like ordinary nodes
# TrustPeer performs the role of PeerMgr in parallel.
def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.debug('Start Logchain launcher for TrustPeer...')

    initialize()

    logging.info('Run threads for PeerMgr.')
    if not peermgr.start_peermgr():
        logging.info('Aborted because PeerMgr execution failed.')
        return

    set_peer.set_my_peer_num()
    logging.info("My peer num: " + str(nodeproperty.My_peer_num))

    'Genesis Block Create'
    genesisblock.genesisblock_generate()

    logging.info("Start a thread to receive messages from other peers.")
    recv_thread = receiver.ReceiverThread(
        1, "RECEIVER", nodeproperty.My_IP_address, nodeproperty.My_receiver_port)
    recv_thread.start()
    logging.info("The thread for receiving messages from other peers has started.")


    t_type_qt = t_type_queue_thread.TransactionTypeQueueThread(
        1, "TransactionTypeQueueThread",
        dispatch_queue_list.T_type_q,
        dispatch_queue_list.Connected_socket_q
    )
    t_type_qt.start()

    v_type_qt = v_type_queue_thread.VotingTypeQueueThread(
        1, "VotingTypeQueueThread",
        dispatch_queue_list.V_type_q,
        dispatch_queue_list.Connected_socket_q
    )
    v_type_qt.start()

    b_type_qt = b_type_queue_thread.BlockTypeQueueThread(
        1, "BlockTypeQueueThread",
        dispatch_queue_list.B_type_q,
        dispatch_queue_list.Connected_socket_q
    )
    b_type_qt.start()




def initialize():
    logging.info('Start the blockchain initialization process...')
    file_controller.remove_all_transactions()
    file_controller.remove_all_blocks()
    file_controller.remove_all_voting()
    logging.info('Complete the blockchain initialization process...')
    set_peer.init_myIP()


def monitoring_ui():
    app = QtWidgets.QApplication(sys.argv)

    main_form = monitoring.Form()

    main_form.change_status_text("Server Status : NOMAL            13:22:09")

    main_form.add_queue_data('block.Block1{add}')
    main_form.add_queue_data('block.Block2{add}')
    main_form.add_queue_data('block.Block3{add}')

    main_form.add_queue_data('transaction.tx1{node1->node2}')
    main_form.add_queue_data('transaction.tx2{node1->node2}')
    main_form.add_queue_data('transaction.tx3{node1->node2}')

    main_form.add_queue_data('log.start voting')
    main_form.add_queue_data('log.end voting')
    sys.exit(app.exec())


if __name__ == '__main__':
    t1 = threading.Thread(target=monitoring_ui)
    t1.start()
    main()