import threading, paramiko
import json, os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir , 'database', 'users_data.json')


class MyThread(threading.Thread):
    '''核心处理类，该类得到用户的指令，通过paramiko管理主机'''
    def __init__(self, ip_addr, port, username, passwd):
        super(MyThread, self).__init__()
        self.ip_addr = ip_addr
        self.port = int(port)
        self.username = username
        self.passwd = passwd
        print(self.ip_addr,self.port,self.username,self.passwd)

    def run(self):
        if self.choose_pc() == False:
            del self
            exit()

        while True:
            event.wait()
            self.cmd = Input_fun.message
            self.cmd_list = self.cmd.split()
            if hasattr(self, self.cmd_list[0]):
                getattr(self, self.cmd_list[0])()
            else:
                self.other_command()
            event.clear()

    def choose_pc(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname= self.ip_addr, port= self.port, username= self.username, password=self.passwd)
            self.sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        except:
            print('%s is not online,please check if first' %self.ip_addr)
            return False


    def put(self):
        for file in self.cmd_list[1::]:
            try:
                self.sftp.put(file, file)
            except FileNotFoundError as e:
                print('file %s not found' %file)

    def get(self):
        for file in self.cmd_list[1::]:
            try:
                self.sftp.get(file, file)
            except FileNotFoundError as e:
                print('ip: %s,no such file %s' %(self.ip_addr, file))


    def other_command(self):
        stdin ,stdout, stderr = self.ssh.exec_command(self.cmd)
        res, err = stdout.read(), stderr
        # result = res if res else err
        if res:
            print('IP:%s\n'%self.ip_addr,res.decode())
        elif err:
            print('IP: %s, command error' %self.ip_addr)
        else:
            print('......')


class Pc_manager(object):
    '''读取用户信息文件，同时可以增删主机信息，最后让管理员选择被管理的主机'''
    def __init__(self):
        self.users_dic = {}
        with open(data_path, 'r', encoding='utf-8') as f:
            self.users_data = json.load(f)

        self.show_users()
        while True:
            add_remove = input('add pc , remove pc or next (add/remove/next), : ').strip()
            if add_remove == 'add':
                self.add_to_file()
            elif add_remove == 'remove':
                self.remove_from_file()
            elif add_remove == 'next':
                break
            else:
                print('error command')
                continue
        while True:
            self.show_users()
            ip_addr_list = input('input the ip address you will connnect,input "q" to next: ').strip().split(',')
            if ip_addr_list == ['q']:
                print(self.users_dic)
                break
            for ip_addr in ip_addr_list:
                if ip_addr in self.users_data:
                    self.users_dic[ip_addr] = self.users_data[ip_addr]
                else:
                    print('ip:%s not exists'  %ip_addr)

    def add_to_file(self):
        try:
            ip_addr, name, port, username, passwd = input('ip_addr , pc_describe, port, username, password :').strip().split(',')
            self.users_data[ip_addr] = [name, port, username, passwd]
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(self.users_data, f)
        except:
            print('输入不符合规范')

    def remove_from_file(self):
        choosed_ip = input('choose which ip to remove: ').strip()
        if choosed_ip in self.users_data:
            del self.users_data[choosed_ip]
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(self.users_data, f)
        else:
            print("there's no this ip")

    def show_users(self):
        for k in self.users_data:
            print('%s   %s' % (k, self.users_data[k]))


class Input_fun(threading.Thread):   #11111
    '''这个继承式调用类用来跟第一个类进行交互的：此线程类专为得到管理用户的输入命令。 使用了单独的线程得到用户的命令，并与主机交互'''
    message = ''
    def __init__(self):
        super(Input_fun, self).__init__()

    def run(self):
        while True:
            event.clear()
            info = input("input something:").strip()
            if not info:
                continue
            Input_fun.message = info
            event.set()

if __name__ == '__main__':
    pc_dic = Pc_manager().users_dic
    t_obj = []

    event = threading.Event()
    event.clear()
    for ip_addr in pc_dic:
        port = pc_dic[ip_addr][1]
        username = pc_dic[ip_addr][2]
        passwd = pc_dic[ip_addr][3]
        t = MyThread(ip_addr, port, username, passwd)
        t_obj.append(t)
        t.start()

    tt = Input_fun()
    tt.start()

    # event = threading.Event()
    # event.clear()


