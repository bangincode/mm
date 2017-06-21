import sys
import time
import threading
from time import gmtime, strftime
from twilio.rest import Client
import socket, select, string
try:
    #Python 2
    import urllib2
except:
    #Python 3+
    import urllib


_HASHRATE = " "           #Init global LEAVE BE
_MIN_HASTRATE = 10        #Minimum hashrate to check for
_PHONE = '+15555555555'   #Cell Phone number to text if problem occurs
_SMSDELAY = 300.0         #In Seconds the delay to wait between emergency text messages
_REFRESHRATE = 30         #In Seconds the rate at which this monitor will check your mining rigs webserver
_TWILIO_PHONE = "+17777777777"  #Your Twilio Phone number
_TWILIO_ACCOUNTSID = "ACccccccccccccccccccccccccc"       #Your Twilio Account SID
_TWILIO_TOKEN = "1ad1ad1ad1ad1ad1ad1ad1ad1ad1ad"         #Your Twilio Token

_MINERS = [{'address': 'http://127.0.0.1:3333', 'ID': 'Gaming Sys', 'hashrate': 0, 'sendSMS': False, 'status': ' ', 'smsDelayOn': False},
           {'address': 'http://192.168.1.101:3333', 'ID': 'Mining Rig 1', 'hashrate': 0, 'sendSMS': False, 'status': ' ', 'smsDelayOn': False},
           {'address': 'http://192.168.0.106:3333', 'ID': 'Mining Rig 2', 'hashrate': 0, 'sendSMS': False, 'status': ' ', 'smsDelayOn': False},
           {'address': 'http://192.168.1.102:3333', 'ID': 'Mining Rig 3', 'hashrate': 0, 'sendSMS': False, 'status': ' ', 'smsDelayOn': False}]


def updateConsole(message, refresh, skip):
    global _MINERS
    timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    if refresh:
        sys.stdout.write('                                                                                     ' + '\r')
        sys.stdout.write(timeStamp + "| " + message + '\r')
        sys.stdout.flush()
    elif skip:
        sys.stdout.write('                                                                                     ' + '\r')
        sys.stdout.write('\n')
        sys.stdout.flush()
    else:
        sys.stdout.write('                                                                                     ' + '\r')
        sys.stdout.write(timeStamp + "| " + message + '\n')
        sys.stdout.flush()

def assignMinerID(id):

    updateConsole("[+] Assigned MinerID: " + id, False, False)

def getEthminerData(miner):
    #THIS WILL ONLY WORK WITH ETHMINER WEB SERVER
    minerAddress = miner['address']
    minerID = miner['ID']
    minerHashrate = 0

    try:
        try:
            #Python 2
            response = urllib2.urlopen(minerAddress)
        except:
            # Python 3+
            response = urllib.urlopen(minerAddress)

        html = str(response.read())
        data = html.split(']')
        data = data[0].split('[')
        data = data[1].split(',')
        data = data[2].split(';')
        data = data[0].split('"')
        minerHashrate = int(data[1])

        #if data.find(';') < 0:
            #result = data
        #EXPERIMENTAL MULTI GPU
        #else:
        #    result = " "
        #    for each in range(0, data.find(';') + 1):
        #        result = result + each

        response.close()
    except:
        updateConsole("[-] FAILED TO CONNECT TO  " + str(minerID) + "  ETHMINER WEBSERVER", False, False)
        minerHashrate = 0


    miner['hashrate'] = minerHashrate

def checkHashrate(miner):
    global _MIN_HASTRATE
    
    if miner['hashrate'] > _MIN_HASTRATE:
        miner['status'] = 'GREEN'
    else:
        miner['status'] = 'RED'

def checkStatus(miner):
    if miner['status'] == 'GREEN':
        miner['sendSMS'] = False
    elif miner['status'] == 'RED':
        if miner['sendSMS']:
            updateConsole("[-] MINING SYSTEM PROBLEM: Sending SMS", False, False)
            try:
                sendSMS(miner)
            except:
                updateConsole('[-] Failed to send EMERGENCY SMS', False, False)
        elif not miner['sendSMS']:
            if not miner['smsDelayOn']:
                #If this is the first indication of a problem then sendSMS on next iter
                # (Unless status becomes green during the waitInterval function
                miner['sendSMS'] = True

def sendSMS(miner):
    global _TWILIO_TOKEN
    global _TWILIO_ACCOUNTSID
    global _TWILIO_PHONE

    if not miner['smsDelayOn']:
        message = miner['ID'] + "has reported a problem"

        client = Client(_TWILIO_ACCOUNTSID, _TWILIO_TOKEN)

        client.messages.create(to=_PHONE, from_=_TWILIO_PHONE, body=message)

        miner['smsDelayOn'] = True
        miner['sendSMS'] = False

        updateConsole("[+] EMERGENCY SMS SENT TO " + _PHONE, False, False)

        threading.Timer(_SMSDELAY, set_sms_sent_delay, [miner]).start()

def set_sms_sent_delay(miner):
    #print '[DEBUG] ++ SET_SMS_SENT_DELAY'
    miner['smsDelayOn'] = False

def waitInterval():
    global _REFRESHRATE
    time.sleep(_REFRESHRATE)

def mainLoop():
    global _MINERS
    updateConsole(" ", False, True)
    updateConsole("[+] Starting Mining Monitor Application", False, False)

    for miner in _MINERS:
        assignMinerID(miner['ID'])

    updateConsole("[+] Wait Interval Set to: " + str(_REFRESHRATE), False, False)

    while 1:
        for miner in _MINERS:
            getEthminerData(miner)
            checkHashrate(miner)
            checkStatus(miner)

        text = '\n  '
        for miner in _MINERS:
            text =  text + '[' + str(miner['ID'])+ '] ' + "Hashrate(" + str(miner['hashrate']) + ')' + " Status(" + str(miner['status']) + ')' + '  \n  '

        text = text[:len(text) - 3]
        updateConsole(text, False, False)

        waitInterval()


mainLoop()
