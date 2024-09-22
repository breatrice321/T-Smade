import os
import subprocess
import time
import event_1
import event_2
import event_3
import event_4
import event_5
import use_event_6
import attack
import threading

from itertools import combinations

def HPC():
    # cmd = "perf stat -a -e branches,branch-misses,r412e,r4f2e,HW_INTERRUPTS.RECEIVED -I 1000 -o ../raw_data/" + str(
    #     "spectre-v1")
    # cmd = "perf stat -a -e branches,branch-misses,r412e,r4f2e,HW_INTERRUPTS.RECEIVED -I 1000 -o ../raw_data/" + str(
    #     "evasive-spectre-nop")
    # cmd = "perf stat -a -e branches,branch-misses,r412e,r4f2e,HW_INTERRUPTS.RECEIVED -I 1000 -o ../raw_data/" + str(
    #     "evasive-spectre-memory")
    cmd = "perf stat -a -e branches,branch-misses,r412e,r4f2e,HW_INTERRUPTS.RECEIVED -I 1000 -o ../raw_data/" + str(
        "normal")
    command = cmd.split()
    sudoPassword = "passwd"  //input the password to switch to root mode.
    cmd1 = subprocess.Popen(['echo', sudoPassword], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)


def strss():
    cmd = "stress -m 1 --timeout 600"
    command = cmd.split()
    # Start the command, and it will run in the background.
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("The command has been started and is running in the background...")

    # Waiting for the command to finish.
    stdout, stderr = process.communicate()


def thread_list(number):  
    a = [2, 3, 4, 5, 6, 7]

    m = list(combinations(a, number))

    all = []
    name = []
    for i in m:
        list_i = []
        name_i = []
        # t1 = threading.Thread(target=attack.attack)
        # list_i.append(t1)
        name_i.append("t1")

        # tm = threading.Thread(target=strss)
        # list_i.append(tm)
        # name_i.append("tm")

        for j in range(len(i)):
            if i[j] == 2:
                t2 = threading.Thread(target=event_1.play_music)
                list_i.append(t2)
                name_i.append("t2")
            if i[j] == 3:
                t3 = threading.Thread(target=event_2.watch_the_vedio)
                list_i.append(t3)
                name_i.append("t3")
            if i[j] == 4:
                # t4 = threading.Thread(target=event_3.wps_write)
                # list_i.append(t4)
                name_i.append("t4")
            if i[j] == 5:
                t5 = threading.Thread(target=event_4.connect)
                list_i.append(t5)
                name_i.append("t5")
            if i[j] == 6:
                t6 = threading.Thread(target=event_5.play_snake_game)
                list_i.append(t6)
                name_i.append("t6")
            if i[j] == 7:
                # Launch LibreOffice's Python interpreter to run event_6.
                t7 = threading.Thread(target=use_event_6.libreoffice_thread)
                list_i.append(t7)
                name_i.append("t7")
        all.append(list_i)
        name_i = "".join(name_i)
        name.append(name_i)


    return all, name


def execute(num):  
    mistake_list = []
    thread, name = thread_list(num)

    n = 0

    for i in thread:

        start = time.time()
        for j in i:
            j.start()

        HPC()

        while time.time() - start < 598:
            count = 0
            thread_enumerate = threading.enumerate()
            for m in thread_enumerate:
                if '<Thread(' in str(m):
                    count = count + 1
            thread_count = threading.active_count()
            time.sleep(2)

        if count < num:
            mistake_list.append(name[n])

        os.system("sudo pkill -9 perf")
        n = n + 1
        print("mistake_list:", mistake_list)

        print(".....................")

        time.sleep(20)

    mylog = open('record.log', mode='a', encoding='utf-8')
    print("mistake_list:", mistake_list, file=mylog)
    mylog.close()
    print("over!!!!!!!!!!!!!")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    return mistake_list



if __name__ == "__main__":

    execute(6)
    print("the program is over!!!!!!")






