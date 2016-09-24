#!/usr/bin/env python
import os
import sys
import signal
import time
import random
from core import pycore
from core.misc import ipaddr
from core import service
from core.misc.xmlsession import opensessionxml

myservices_path = '/home/artur/core-scripts/myservices'
services = 'DefaultRoute|ServalRPCService|NetmonService'
# Start new core session
session = pycore.Session(persistent=True)
# IP range for dynamic links
addr_list = list(range(78, 255))
# currently uset IPs for dynamic links
cur_ptp_list = []
# Dict for node combinatios to connect different islands
islands = {
    12 : ([28, 29, 30, 31, 32], [37, 38, 39, 40, 41]),
    13 : ([5, 14, 23, 32], [6, 15, 24, 33]),
    14 : ([14, 23, 30, 31, 32], [42, 43, 44, 51]),
    23 : ([39, 40, 41, 50], [24, 33, 34]),
    24 : ([41, 50, 51], [42, 51, 60]),
    34 : ([33, 34, 35, 36], [42, 43, 44, 45])
}

random.seed(sys.argv[1])


def signal_handler(num, stack):
    pass


# Returns true in 25% of all cases
def should_change():
    return random.random() < 0.25


# Clear all dynamic links
def clear_islands():
    for ptp_addr in cur_ptp_list:
        # Write the IP back to the inital list
        addr_list.append(ptp_addr)
        # Get the corresponsing object
        ptp = session.objbyname("{}".format(ptp_addr))
        # Delete the PTP network
        session.delobj(ptp.objid)
    # Clear the list with used IPs
    del cur_ptp_list[:]


# Connect all islands together
def connect_all():
    # First clear everything
    clear_islands()
    for index, island in islands.items():
        for i in range(0, len(island[1])):
            # Get the first free IP
            tmp_addr = addr_list.pop(0)
            # Mark this IP as used
            cur_ptp_list.append(tmp_addr)
            # Create new nodes with the given IP
            ptp_node = session.addobj(cls = pycore.nodes.PtpNet, name="{}".format(tmp_addr))
            left_node = session.objbyname("n{}".format(island[0][i]))
            right_node = session.objbyname("n{}".format(island[1][i]))
            # Connect everython together
            left_node.newnetif(ptp_node, ['10.0.{}.1/24'.format(tmp_addr)])
            right_node.newnetif(ptp_node, ['10.0.{}.2/24'.format(tmp_addr)])


# Update cnt link with the given mode mode (add or remove) for two islands
def update_islands(mode, cnt, islands_tuple=None):
    if mode == "add":
        while cnt > 0:
            # Get the first free IP
            tmp_addr = addr_list.pop(0)
            # Mark this IP as used
            cur_ptp_list.append(tmp_addr)
            # Choose one random node of every islands
            node_num_left = random.choice(islands_tuple[0])
            node_num_right = random.choice(islands_tuple[1])
            # Create a new PTP node and get the existing CoreNodes with the given names
            ptp_node = session.addobj(cls = pycore.nodes.PtpNet, name="{}".format(tmp_addr))
            left_node = session.objbyname("n{}".format(node_num_left))
            right_node = session.objbyname("n{}".format(node_num_right))
            # Connect everything together
            left_node.newnetif(ptp_node, ['10.0.{}.1/24'.format(tmp_addr)])
            right_node.newnetif(ptp_node, ['10.0.{}.2/24'.format(tmp_addr)])
            cnt -= 1
    else:
        while cnt > 0:
            # Choose a random dynamic link and put it back to the initial list
            random.shuffle(cur_ptp_list)
            ret_addr = cur_ptp_list.pop(0)
            addr_list.append(ret_addr)
            # Get the link and delete it
            ptp = session.objbyname("{}".format(ret_addr))
            session.delobj(ptp.objid)
            cnt -= 1


# Create Islands topology
def build_islands():
    service.CoreServices(session).importcustom(myservices_path)

    opensessionxml(session, "topologies/islands.xml", True)
    
    try:
        while True:
            # Sleep 120 to 300 seconds (2 to 5 minutes)
            sleeptime = 120 + random.randint(0, 180)
            time.sleep(sleeptime)
            # If there are dynamic links and should_change returns true (25% probability) all dynamic links are cleared
            if should_change() and len(cur_ptp_list) != 0:
                clear_islands()
                continue
            # In 25% of all cases all islands are connected together
            if should_change():
                connect_all()
                continue
            # Flip a coin if dynamic links should be created or removed
            choice = bool(random.getrandbits(1))
            # How many dynamic links should be changed
            num_change_links = random.randint(2, 5)
            # First case: add two random islands
            # Second case: delte num_change_links dynamic links
            if choice:
                update_islands("add", num_change_links, islands[random.choice(islands.keys())])
            elif len(cur_ptp_list) >= num_change_links:
                update_islands("remove", num_change_links)
    except KeyboardInterrupt:
        session.shutdown()


# Create Chain topology (read and parse chain.xml and wait for ctrl-c)
def build_chain():
    signal.signal(signal.SIGINT, signal_handler)
    service.CoreServices(session).importcustom(myservices_path)
    
    opensessionxml(session, "topologies/chain.xml", True)
    
    signal.pause()

    session.shutdown()


# Create Hub topology
def build_hub():
    signal.signal(signal.SIGINT, signal_handler)
    service.CoreServices(session).importcustom(myservices_path)
    
    # Create hub node
    hub = session.addobj(cls=pycore.nodes.HubNode, name='hub')
    # Create 28 nodes, add the services, connect them to the hub and start the services.
    for i in range(1, 29):
        tmp = session.addobj(cls=pycore.nodes.CoreNode, name='n{}'.format(i))
        session.services.addservicestonode(tmp, '', services, verbose=False)
        tmp.newnetif(hub, ['10.0.0.{}/24'.format(i)])
        service.CoreServices(session).bootnodeservices(tmp)

    signal.pause()

    session.shutdown()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    if sys.argv[1] == 'chain':
        build_chain()
    elif sys.argv[1] == 'hub':
        build_hub()
    elif sys.argv[1] == 'islands':
        build_islands()
