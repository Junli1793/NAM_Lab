import paramiko
import os
import pexpect
import re



def lab_ping(linux_ip, username, passwd, ip):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(linux_ip,22,username,passwd,timeout=5)
        stdin,stdout,stderr = ssh.exec_command('ping -c 3 %s' % ip)
        out = stdout.readlines()[6]
        print(out)
        #ping_succeed_output = "3 packets transmitted, 3 received, 0% packet loss"
        #ping_failed_output = "3 packets transmitted, 0 received, +3 errors, 100% packet loss"

        if bool(re.search(r'errors', out)):
            labping_index = 1
        else:
            labping_index = 0

        print(labping_index)

    except:
        print('ssh fail')


if __name__ == '__main__':
    linux_ip = "10.79.46.155"
    username = "root"
    passwd = "poPPee$41"
    ip = "10.79.46.199"
    lab_ping(linux_ip,username,passwd,ip)
