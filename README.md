# mm
Mining Monitor

Quick and dirty

Tested on Win10 should work on Linux as well

Python2 or Python3

TODO: Lots

Currently the only dependency is twilio library

HOW TO INSTALL: pip install twilio>=6.0.0

You must set a few globals for this to work properly

_________________________________________________________________________________


_MIN_HASTRATE = 10        #Minimum hashrate to check for

_PHONE = '+15555555555'   #Cell Phone number to text if problem occurs

_SMSDELAY = 300.0         #In Seconds the delay to wait between emergency text messages

_REFRESHRATE = 30         #In Seconds the rate at which this monitor will check your mining rigs webserver

_TWILIO_PHONE = "+17777777777"  #Your Twilio Phone number

_TWILIO_ACCOUNTSID = "ACccccccccccccccccccccccccc"       #Your Twilio Account SID

_TWILIO_TOKEN = "1ad1ad1ad1ad1ad1ad1ad1ad1ad1ad"         #Your Twilio Token

for _MINERS update the address and ID params only

I am sure I missed stuff you need to know. 
