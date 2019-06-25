#!/usr/bin/env python

# cron runs this Python script at reboot...

import smtplib
import time
import datetime
from ConfigParser import SafeConfigParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import logging
from scapy.all import *
import __main__ as main
import os

def send_sms(msgbody,timestamp):
   msg=MIMEMultipart()
   msg['From']=fromaddr
   msg['To']=toaddr
   msg['Subject']=subject
   msgbody=msgbody+"\nSent at "+timestamp+"."
   msg.attach(MIMEText(msgbody,'plain'))

   smtpserver=smtplib.SMTP(server,port)
   smtpserver.starttls()
   smtpserver.login(fromaddr,password)
   text=msg.as_string()
   smtpserver.sendmail(fromaddr,toaddr,text)
   smtpserver.quit()


def check_button(pkt):
  if pkt.haslayer(ARP):
    if pkt[ARP].op == 1: # who-has (request)
      print "\"who has\" request from "+ pkt[ARP].hwsrc
      #pkt[ARP].show()
      if pkt[ARP].hwsrc == mac1: # mac address of "poop bags" amazon dash button
        global t11
        t12=datetime.now()
        t13=t12-t11
        if t13.seconds>10: # minimum 10 seconds between button presses
          t11=t12  # save the time for later
          timestamp=t12.strftime("%H:%M:%S %m/%d/%Y")
          logging.info(name1+' Dash button pressed.')
          send_sms("The "+name1+" Amazon Dash Button has been pressed.",timestamp)
          print name1+" Dash button pressed."
          print "SMS sent at "+timestamp+"."

      elif pkt[ARP].hwsrc == mac2: # mac address of "coca cola" amazon dash button
        global t21
        t22=datetime.now()
        t23=t22-t21
        if t23.seconds>10: # minimum 10 seconds between button presses
          t21=t22  # save the time for later
          timestamp=t22.strftime("%H:%M:%S %m/%d/%Y")
          logging.info(name2+' Dash button pressed.')
          send_sms("The "+name2+" Amazon Dash Button has been pressed.",timestamp)
          print name2+" Dash button pressed."  
          print "SMS sent at "+timestamp+"."

      elif pkt[ARP].hwsrc == mac3: # mac address of "banana" amazon dash button
        global t31
        t32=datetime.now()
        t33=t32-t31
        if t33.seconds>10: # minimum 10 seconds between button presses
          t31=t32  # save the time for later
          timestamp=t32.strftime("%H:%M:%S %m/%d/%Y")
          logging.info(name3+' Dash button pressed.')
          send_sms("The "+name3+" Amazon Dash Button has been pressed.",timestamp)
          print name3+" Dash button pressed."
          print "SMS sent at "+timestamp+"."

# time when script starts
t11=datetime.now()
t21=datetime.now()
t31=datetime.now()

logfilename=os.path.splitext(main.__file__)[0]+".log"
logging.basicConfig(filename=logfilename,filemode='a',format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %H:%M:%S',level=logging.DEBUG)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # suppress scapy warning about ip6

# configuration file
inifilename=os.path.splitext(main.__file__)[0]+".ini" # dash_button_listener.ini
config=SafeConfigParser()
config.read(inifilename)
mac1=config.get('buttons','mac1')             # mac address of "Poop Bags" Dash button
mac2=config.get('buttons','mac2')             # mac address of "Coca Cola" Dash button
mac3=config.get('buttons','mac3')             # mac address of "Banana" Dash button
name1=config.get('buttons','name1')
name2=config.get('buttons','name2')
name3=config.get('buttons','name3')

toaddr=config.get('message','to')
fromaddr=config.get('message','from')
subject=config.get('message','subject')
server=config.get('message','server')
port=config.getint('message','port')
password=config.get('message','password')
body=config.get('message','body')

# continuously monitor for arp packets
print "Waiting..."
sniff(prn=check_button,filter="arp",store=0,count=0)  # count=0 means run forever

