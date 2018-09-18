import os
import shlex

import paramiko
import pexpect
import subprocess


def upload_md5sum_file():
    ping = pexpect.spawn("ping -c 3 10.79.46.131")
    ping_index = ping.expect(["3 packets transmitted, 3 packets received, 0.0% packet loss", pexpect.TIMEOUT],
                             timeout=3)
    if ping_index == 0:
        print("ping succeed, uploading md5sum local file...")

        su_junli = subprocess.Popen(['su', 'junli'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        su_junli_out, su_junli_error = su_junli.communicate('Jay1415123\n')

        scp_file = subprocess.Popen(shlex.split('scp /Users/junli/Documents/Python/git/NAM_Lab/md5sum_local.txt jun@10.79.46.131:/home/jun/Documents/python/'), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        scp_file.stdin.write("cisco123\n")
        scp_file_out, scp_file_error = scp_file.communicate()

        print(su_junli_out)
        print(su_junli_error)
        print(scp_file_out)
        print(scp_file_error)

    elif ping_index == 1:
        print("ping failed, check the connection to 10.79.46.131 first")
    else:
        print("ping failed, check the connection to 10.79.46.131 first")


if __name__ == '__main__':
    upload_md5sum_file()
