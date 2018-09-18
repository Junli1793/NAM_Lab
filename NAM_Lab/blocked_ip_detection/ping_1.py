import pexpect
import paramiko
import re
import multiprocessing
from multiprocessing import Pool
import time
from time import ctime
from functools import partial

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

    global result_A
    global result_B
    global result_U

    linux_ip = "10.79.46.155"
    username = "root"
    passwd = "poPPee$41"
    lab_index = lab_ping(linux_ip,username,passwd,ip)
    local_index = local_ping(ip)
    lock.acquire()
    if lab_index == 0 & local_index == 0:
        result_U.write(ip + '   ' + ctime() + "\n")
        print(ip + " is working fine!")

    elif lab_index == 0 & (local_index == 1 or local_index == 2):
        result_B.write(ip + '   ' + ctime() + "\n")
        print(ip + " is blocked! Please open case to IT")
    else:
        print(ip + " is available(better to check manually")
        result_A.write(ip + '   ' + ctime() + "\n")
    lock.release()


# def ip_detection():

def init(l):
    global lock
    lock = l

if __name__ == '__main__':

    lock = multiprocessing.Lock()

    global result_A
    global result_B
    global result_U

    result_U = open('IP_In_Using.txt', 'w')
    result_B = open('IP_been_Blocked.txt', 'w')
    result_A = open('IP_Available.txt', 'w')

    result_U.truncate()
    result_U.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.75.169.x        *" + "\n" + "* Below ip addresses are in using *" + "\n" + "*" * 35 + "\n\n")

    result_B.truncate()
    result_B.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.75.169.x        *" + "\n" + "* Below ip addresses are bloked *" + "\n" + "*" * 35 + "\n\n")

    result_A.truncate()
    result_A.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.75.169.x        *" + "\n" + "* Below ip addresses are available *" + "\n" + "*" * 35 + "\n\n")

    # result_U.close()
    # result_B.close()
    # result_A.close()
    print("Ping Detection Begin......" + "\n."*3)
    s_time = time.time()


    p = Pool(multiprocessing.cpu_count(), initializer=init, initargs=(lock,))
    for i in range(2,10):
        ip = "10.75.169."+ str(i)
        p.apply_async(aligenment, args=(ip,))

    p.close()
    p.join()

    result_U.close()
    result_B.close()
    result_A.close()

    # result_U.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.79.46.x        *" + "\n" + "* Below ip addresses are in using *" + "\n" + "*" * 35 + "\n\n")
    #
    # result_B.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.79.46.x        *" + "\n" + "* Below ip addresses are bloked *" + "\n" + "*" * 35 + "\n\n")
    #
    # result_A.write("\n" + "*" * 35 + "\n" + "*        Subnet 10.79.46.x        *" + "\n" + "* Below ip addresses are available *" + "\n" + "*" * 35 + "\n\n")

    # p = Pool(multiprocessing.cpu_count())
    # for i in range(2,254):
    #     ip = "10.79.46."+ str(i)
    #     p.apply_async(aligenment, args=(ip,))
    # p.close()
    # p.join()


    f_time = time.time()
    print("\n" + "Detection Time elapsed %0.2f seconds" %(f_time-s_time))


    # ip = "10.79.46.199"
    # lab_index = lab_ping(linux_ip,username,passwd,ip)
    # print("lab index is: " + str(lab_index))
    # local_index = local_ping(ip)
    # print("local index is: " + str(local_index))
    #
    # if lab_index == 0 & local_index == 0:
    #     print(ip + " is working fine!")
    # elif lab_index == 0 & (local_index == 1 or local_index == 2):
    #     print(ip + " is blocked! Please open case to IT")
    # else:
    #     print(ip + " status is unsure, maybe not in use...")














