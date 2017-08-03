import os, sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core.main import MyThread
from core.main import Pc_manager
from core.main import Input_fun

if __name__ == '__main__':
    pc_dic = Pc_manager().users_dic
    t_obj = []

    # event = threading.Event()   必须在同一个进程下
    # event.clear()
    for ip_addr in pc_dic:
        port = pc_dic[ip_addr][1]
        username = pc_dic[ip_addr][2]
        passwd = pc_dic[ip_addr][3]
        t = MyThread(ip_addr, port, username, passwd)
        t_obj.append(t)
        t.start()

    tt = Input_fun()
    tt.start()

