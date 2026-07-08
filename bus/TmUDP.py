"""
 * BusUDP.py
 * Created on: 8 April 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

try:
    from modules.UDP_Socket import UDP_Socket
except:
    from UDP_Socket import UDP_Socket

class TmUDP():
    def __init__(self, tm, ip, port, nic_ip, loopbackEnable=True):
        self.tm = tm
        print("TM on: %s:%d via NIC: %s"%(ip, port, nic_ip))
        self.socket = UDP_Socket(
            ip=ip,     #< Listen/send IP
            port=port,   #< Listen/send port (use 0 to automatic assign)
            iface=nic_ip, #< NIC to use on local machine
            mcastLoopbackEnable=loopbackEnable,
        )

    def send(self):
        pkt = self.tm.serialize()
        self.socket.send(pkt)

    def recv(self):
        try:
            data = self.socket.recv()
            self.tm.deserialize(data)
        except BlockingIOError:
            pass
            #print("### Incorrect packet received ###")
        return self.tm
        
    def get(self):
        return self.tm
