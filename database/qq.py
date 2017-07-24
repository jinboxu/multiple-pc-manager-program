# import paramiko
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname='192.168.0.200', port=22, username='root', password='123456')
# sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
# sftp.put('users_data.json', 'test.json')

import json
with open('users_data.json', 'w', encoding='utf-8') as f:
    json.dump({'192.168.0.200':['test1', '22', 'root', '123456']}, f)