from socket import *
import Property
import threading
import json


class ReceiverThread(threading.Thread):
    def __init__(self, p_thrd_id, p_thrd_name, p_ip, p_port):
        """

        :param p_thrd_id:
        :param p_thrd_name:
        :param p_ip:
        :param p_port:
        """
        threading.Thread.__init__(self)
        self.thrd_name = p_thrd_name
        self.thrd_id = p_thrd_id
        self.thrd_ip = p_ip
        self.thrd_port = p_port

    def run(self):
        print ("Start Receiver Thread")
        receive_data(self.thrd_name, self.thrd_ip, self.thrd_port)


def receive_data(p_thrd_name, p_ip, p_port):
    """

    :param p_thrd_name:
    :param p_ip:
    :param p_port:
    :return:
    """

    addr = (p_ip, p_port)
    buf_size = 10000
    #to check my node info
    #print(p_thrd_name, p_ip, p_port)
    #
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    num_tx =0
    num_block =0
    while True:
        print ("waiting")
        request_sock, request_ip = tcp_socket.accept()

        while True:
            recv_data = request_sock.recv(buf_size).decode('utf-8')

            try:
                if recv_data == "":
                    break
                #print("from ip : " + str(request_ip[0]))
                #node mapping table 관리를 넣는다.
                if recv_data == "new node":
                    if str(request_ip[0]) in Property.my_node.linked_node:
                        print("already connected")
                        break
                    else:
                        print("new node connection received")
                        Property.my_node.table_add(str(request_ip[0]),'stable')
                        #Property.my_node.print_table()
                        Property.my_node.write_table()
                        break

                if str(request_ip[0]) not in Property.my_node.linked_node : # 연결이 안되있는 노드로 부터 오는 메세지는 무시.
                    break



                Property.my_node.table_update(str(request_ip[0]), 'true')
                #Property.my_node.print_table()
                Property.my_node.write_table()
                #node mapping table 관리
                data_jobj = json.loads(recv_data)
                #print(data_jobj['type'])
                if data_jobj['type'] is 'T':
                    print ("Transaction received")


                    num_tx = num_tx + 1
                    #print(num_tx)
                    f = open("transaction_new" + str(num_tx) + ".txt", 'w')
                    f.write(recv_data)
                    f.close()


                elif data_jobj['type'] is 'B':
                    print ("Block received")

                    # block verification thread

                    num_block = num_block +1
                    #print(num_block)
                    f = open("block" + str(num_block) + ".txt", 'w')
                    f.write(recv_data)
                    f.close()
                    # remove all txs call


            except Exception as e:
                print ("SOCKET ERROR", e)
                break

    tcp_socket.close()