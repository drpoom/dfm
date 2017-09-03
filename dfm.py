#!/usr/bin/env python
# DFM: DevFee-Modifier
# Created by: drpoom
# License: GNU GPL v3, https://www.gnu.org/licenses/gpl-3.0.en.html
# Usage:
#    sudo python dfm.py
#    sudo python dfm.py &  # In order to run in background
#    

import logging
import json
import re
import nfqueue
import os
# import psutil  # TODO

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)  # Disable an annoying IPv6 warning in scapy
from scapy.all import IP, TCP, socket

logger = logging.getLogger('miner')

ports = ['9999']
method_list = ['mining.subscribe', 'eth_submitLogin']
delimeters = '.'
address_pass = [line.strip().lower() for line in open('address_pass.txt', 'r')]
address_filter = [line.strip().lower() for line in open('address_filter.txt', 'r')]

def callback(self, p):
    """
    Net Filter Callback
    """
    
    global logger
    data = p.get_data()
    packet = IP(data)

    # Get basic packet info
    payload = str(packet[TCP].payload)
    payload_len = len(packet[TCP].payload)
    
    if (len(payload) > 0):
        # Log Debug
        logger.debug("Text: " + payload)

        # Check for JSON
        try:
            # Decode JSON
            decoded = json.loads(payload)
            if(decoded["method"] in method_list):
                login, password = decoded["params"]
                logger.info("Stratum login found: " + login)

                # Split login elements
                # TODO: make string split more effective with RE
                # login_split = re.split(delimeters, login)
                login_split = login.split(delimeters)
                address = login_split[0].lower()
                rest = login_split[1:]
                
                logger.info("Wallet address found: " + address)

                # Check if Login is either pass/filter/unknown, and set flags
                flag_modify = False

                if address in address_pass:
                    logger.info("Address is in PASS list, do nothing.")

                elif address in address_filter:
                    logger.info("Address is in FILTER list, modifying..")
                    flag_modify = True
                
                else:
                    logger.warning("Address is unknown, adding to UNKNOWN list..")
                    # TODO: Option to either ignore the address, or append to filter
                    address_filter.append(address)
                    flag_modify = True

                # Modify login/address if the flag is set
                if flag_modify:

                    # Replace loging with 1st pass address and modify TCP/IP package
                    # TODO: Rejoin strings after splitting with more complex delimeters
                    decoded["params"][0] = ".".join([address_pass[0]] + rest)
                    # decoded["params"][1] = password  # unmodified password, for now
                    payload = json.dumps(decoded)
                    packet[TCP].payload = payload
                    packet[IP].len = packet[IP].len + (len(payload) - payload_len)  # Add/sub len difference
                    packet[IP].ttl = 64  # "Standard" linux TTL
                    del packet[TCP].chksum, packet[IP].chksum
                    p.set_verdict_modified(nfqueue.NF_ACCEPT, str(packet), len(packet))

                    logger.info("Package has been modified:" + payload)
 


        except ValueError:
            logger.debug("Not a JSON packet")
        
        except Exception as e:
            logger.error("Error detected: %s, %s" % (e.message, e.args))



def main():

    global logger
    logger = logging.getLogger('miner')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler('/var/tmp/miner.log')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler) 
    logger.addHandler(console_handler) 
    logger.setLevel(logging.INFO)  # Normal logging
    #logger.setLevel(logging.DEBUG)
    
    logger.info("Starting DevFee-Modifier..")

    # Kill existing processes
    # try:
    #     # Search and kill running processes with similar name
    #     for proc in psutil.process_iter():
    #         #print ("%s, %s" % (proc.name(), proc.cmdline()))
    #         if __file__ in proc.cmdline():
    #             if "python" in proc.cmdline():
    #                 logger.info("Found an existing Python process: " + " ".join(proc.cmdline()))
    #                 # proc.kill()
    #                 # TODO!!!
    # except:
    #     pass # Do nothing for now

    # Start iptable and create a queue for net filter
    os.system('iptables -A OUTPUT -p tcp --match multiport --dport ' + ",".join(ports) + ' -j NFQUEUE --queue-num 0')
    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)
    q.set_callback(callback)
    q.create_queue(0)

    # Blocking call, exit on keyboard interrupt
    try:
        q.try_run()

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt detected, terminating DevFee-Modifier..")
        
        logger.info("Saving address_filter.txt..")
        # Save address_filter.txt
        with open('address_filter.txt', 'w') as f:
            for i in address_filter:
                f.write(i + '\n')

        q.unbind(socket.AF_INET)
        q.close()


if __name__ == "__main__":
    main()

