import pexpect
import paramiko
import re
import multiprocessing
from multiprocessing import Pool
import time
from time import ctime

def local_ping(ip):
    locping = pexpect.spawn('ping -c 3 %s' % ip)
    locping_index = locping.expect(["3 packets transmitted, 3 packets received, 0.0% packet loss",
                                    "3 packets transmitted, 0 packets received, 100.0% packet loss",
                                    pexpect.TIMEOUT], timeout=3)
    return locping_index

def lab_ping(linux_ip,username,passwd,ip):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(linux_ip,22,username,passwd,timeout=10)
        stdin,stdout,stderr = ssh.exec_command('ping -c 3 %s' % ip)
        out = stdout.readlines()[6]
        if bool(re.search(r'errors', out)):
            labping_index = 1
        else:
            labping_index = 0
        return labping_index


    except:
        #print('ssh fail while trying to access ' + linux_ip + ' to ping ' + ip)
        pass

def aligenment(ip):


    linux_ip = "10.79.46.155"
    username = "root"
    passwd = "poPPee$41"
    lab_index = lab_ping(linux_ip,username,passwd,ip)
    local_index = local_ping(ip)
    print(ip + "  " + str(lab_index))
    print(ip + "  " + str(local_index))
    lock.acquire()
    if lab_index == 0 and local_index == 0:
        with open('IP_In_Using.txt', 'a') as result_U:
            result_U.write(ip + '   ' + ctime() + "\n")
        print(ip + " is working fine!")

    elif local_index == 2 and (lab_index == 0 or lab_index == 2):
        with open('IP_Been_Blocked.txt', 'a') as result_B:
                result_B.write(ip + '   ' + ctime() + "\n")
        print(ip + " is blocked! Please open case to IT")
    else:
        with open('IP_Available.txt', 'a') as result_A:
            result_A.write(ip + '   ' + ctime() + "\n")
        print(ip + " is available(better to check manually")
    lock.release()


def init(l):
    global lock
    lock = l

if __name__ == '__main__':

    lock = multiprocessing.Lock()


    with open ('IP_In_Using.txt', 'w') as result_u:
        result_u.truncate()
        result_u.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.75.169.x        *" + "\n" + "* Below ip addresses are in using *" + "\n" + "*" * 35 + "\n\n")
    with open ('IP_Been_Blocked.txt', 'w') as result_b:
        result_b.truncate()
        result_b.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.75.169.x        *" + "\n" + "* Below ip addresses are bloked *" + "\n" + "*" * 35 + "\n\n")
    with open ('IP_Available.txt', 'w') as result_a:
        result_a.truncate()
        result_a.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.75.169.x        *" + "\n" + "* Below ip addresses are available *" + "\n" + "*" * 35 + "\n\n")

    print("Ping Detection Begin......" + "\n."*3)
    s_time = time.time()

    p = Pool(multiprocessing.cpu_count(), initializer=init, initargs=(lock,))
    #p = Pool(multiprocessing.cpu_count())
    for i in range(1,126):
        ip = "10.75.169."+ str(i)
        p.apply_async(aligenment, args=(ip,))
    p.close()
    p.join()


    with open ('IP_In_Using.txt', 'a') as result_u:
        result_u.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.79.46.x        *" + "\n" + "* Below ip addresses are in using *" + "\n" + "*" * 35 + "\n\n")
    with open ('IP_Been_Blocked.txt', 'a') as result_b:
        result_b.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.79.46.x        *" + "\n" + "* Below ip addresses are bloked *" + "\n" + "*" * 35 + "\n\n")
    with open ('IP_Available.txt', 'a') as result_a:
        result_a.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.79.46.x        *" + "\n" + "* Below ip addresses are available *" + "\n" + "*" * 35 + "\n\n")

    p = Pool(multiprocessing.cpu_count(), initializer=init, initargs=(lock,))
    for i in range(2,255):
        ip = "10.79.46."+ str(i)
        p.apply_async(aligenment, args=(ip,))
    p.close()
    p.join()


    f_time = time.time()
    print("\n" + "Detection Time elapsed %0.2f seconds" %(f_time-s_time))












