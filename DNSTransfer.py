#!/bin/python3
# A Simple function that finds NS records, resolves their IP, and attempts a DNS Zone Transfer
import dns.zone
import dns.resolver
from tkinter import *
from tkinter import ttk

ns_servers = []
def dns_zone_xfer(address):
    """
    Takes address and prints data to console.
    """
   
   # Resolves Address
    ns_answer = dns.resolver.query(address, 'NS')
    for server in ns_answer:
        print("[*] Found NS: {}".format(server))
        ip_answer = dns.resolver.query(server.target, 'A')
        # Attempts Zone Transfer for Each IP
        for ip in ip_answer:
            print("[*] IP for {} is {}".format(server, ip))
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(str(ip), address))
                for host in zone:
                    print("[*] Found Host: {}".format(host))
            except Exception as e:
                print("[*] NS {} refused zone transfer!".format(server))
                continue


ws = Tk()
ws.title("DNS Zone Transfer Tool")
ws.geometry("400x250")

frame = Frame(ws)
userInput = Entry(frame, width=40, justify=CENTER)
userInput.grid(row=0, columnspan=3, padx=5, pady= 10)

Button(frame,text="start",command=lambda: dns_zone_xfer(userInput['text'])).grid(row=1, column=1)
frame.pack()
ws.mainloop()
