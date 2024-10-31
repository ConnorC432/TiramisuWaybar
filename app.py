import os
import json
import subprocess
import threading
import time
import queue


wait_time = 1


def read_lines(process, process_queue):
    for line in process.stdout:
        notif_json = json.loads(line.strip())
        notif = f"\uf0f3  {notif_json['summary'][:50]} | {notif_json['body'][:100]}"
        process_queue.put(notif)
    process.stdout.close()


def clear_notif():
    print("\uf0f3", flush=True)


def main():
    tiramisu_process = subprocess.Popen(
        "/usr/bin/tiramisu -j",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    process_queue = queue.Queue()

    thread = threading.Thread(target=read_lines, args=(tiramisu_process, process_queue))
    thread.start()

    last_notif = time.time()
    timed_out = True

    while True:
        if not process_queue.empty():
            print(process_queue.get(), flush=True)
            timed_out = False
            last_notif = time.time()

        elif time.time() - last_notif > wait_time and not timed_out:
            timed_out = True
            clear_notif()

        else:
            time.sleep(0.1)


if __name__ == "__main__":
    os.system("killall tiramisu")
    print("\uf0f3", flush=True)
    main()