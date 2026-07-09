import socket, ipaddress
import struct, psutil, sys

def UDP_Socket(ip, port=0, iface="", timeout=0, allGroups=False, mcastLoopbackEnable=True):
    ipAddr = ipaddress.IPv4Address(ip)
    if ipAddr.is_multicast:
        return UDP_Multicast_Socket(ip, port, iface, timeout, allGroups, mcastLoopbackEnable)
    else:
        return UDP_Unicast_Socket(ip, port, timeout)

class UDP_Unicast_Socket():
    def __init__(self, ip, port=0, timeout=0, allGroups=False):
        self.addr_port = (ip, port)
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sd.settimeout(timeout)
        if allGroups:
            self.sd.bind((ip, port))
#        else:
#            self.sd.bind(("0.0.0.0", port))

    def recv(self, maxBytes=1000) -> bytes:
        """Receives a packet sent to the port given at instantiation"""
        payload, address = self.sd.recvfrom(maxBytes)
        return payload

    def send(self, payload, port=None) -> None:
        """Sends bytes over socket. If no port is specified, uses the port given at instantiation"""
        if port == None:
            self.sd.sendto(payload, self.addr_port)
        else:
            self.sd.sendto(payload, (self.addr_port[0], port))

class UDP_Multicast_Socket(UDP_Unicast_Socket):
    def __init__(self, group, port, iface="", timeout=0, allGroups=False, mcastLoopbackEnable=True):
        """group: An IP address in the multicast range
           port: Port number for the socket connection"""
        print("Multicast socket for GROUP: %s:%d on NIC: %s. All groups %s"%(group, port, iface, allGroups))
        super().__init__(group, port, timeout, allGroups)

        # Set maximum hops to 1 to prevant the packet from leaving the local network
        max_hops = struct.pack('b', 1)
        self.sd.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, max_hops)

        # Select NIC to be used
        if str(iface) == "":
            ### Find the default NIC to use
            iface = socket.gethostbyname( socket.gethostname() )
        self.sd.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(iface))

        # Make socket a member of the multicast group
        mreq = struct.pack('4s4s', socket.inet_aton(group), socket.inet_aton(iface))
        self.sd.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Disable/Enable loop
        mcastLoopbackEnable = struct.pack('b', mcastLoopbackEnable)
        self.sd.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, mcastLoopbackEnable)
