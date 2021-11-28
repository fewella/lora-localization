import time
import json
import threading
import subprocess

import algos

NO_DATA_READ      = -2
JSON_END_OBJECT   = -1

delta_read_time   = 5
rssi_store        = {} # rssi_store[gateway_id (str)] -> [rssi readings (arr of nums)]
rssi_store_mutex  = threading.Lock()


def follow(filename):
    f = open(filename, "r")
    f.seek(0,2) # Go to the end of the file
    prev = ""
    while True:
        line = f.readline()
        json_end = len(line) == 1 and "{" not in prev
        if not line:
            yield NO_DATA_READ
        elif json_end:
            yield JSON_END_OBJECT
        else:
            prev = line
            yield line


def extract_rssi(json_payload):
    try:
        data = json.loads(json_payload)
        rssi = data["data"]["rx_metadata"][0]["rssi"]
    except:
        print("failed read")
        rssi = None
    return rssi


def listen(gateway_id, output_filename):
    json_payload = ""
    rssi         = None
    for line in follow(output_filename):
        if line == NO_DATA_READ or line == JSON_END_OBJECT:
            if json_payload:
                print(json_payload)
                rssi = extract_rssi(json_payload)
            if rssi:
                rssi_store_mutex.acquire()
                rssi_store[gateway_id].append(rssi)
                print(rssi_store)
                rssi_store_mutex.release()
            json_payload = ""
            if line == NO_DATA_READ:
                time.sleep(delta_read_time)
        else:
            json_payload += line


if __name__ == "__main__":
    gateway_ids = [
        "afewell-gateway",
        "colin-gateway",
        "jimmys-gateway"
    ]

    traffic_filenames = [
        "output-1",
        "output-2",
        "output-3"
    ]

    cmd_login  = "ttn-lw-cli login"
    login_proc = subprocess.Popen(cmd_login, shell=True, stdout=subprocess.PIPE)
    login_proc.wait()
    
    threads = []
    for i in range(3):
        cmd_gateway_traffic = f"ttn-lw-cli events --gateway-id {gateway_ids[i]} > {traffic_filenames[i]}"
        proc = subprocess.Popen([cmd_gateway_traffic], shell=True, stdin=None, stdout=None, stderr=None)
        time.sleep(1)
        
        t = threading.Thread(target=listen, args=(gateway_ids[i], traffic_filenames[i], ))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
