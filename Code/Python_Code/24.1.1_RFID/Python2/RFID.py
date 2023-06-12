#!/usr/bin/env python
########################################################################
# Filename    : RFID.py
# Description : Use MFRC522 read and write Mifare Card.
# auther      : www.freenove.com
# modification: 2021/1/1
########################################################################
import RPi.GPIO as GPIO
import MFRC522

# Create an object of the class MFRC522
mfrc = MFRC522.MFRC522()

def dis_ConmandLine():
	print "RC522>",
def dis_CardID(cardID):
	print "%2X%2X%2X%2X%2X>"%(cardID[0],cardID[1],cardID[2],cardID[3],cardID[4]),
def setup():
	print "Program is starting ... "	
	print "Press Ctrl-C to exit."
	pass
	
def loop():
	global mfrc
	while(True):
		dis_ConmandLine()
		inCmd = raw_input()
		print inCmd
		if (inCmd == "scan"):
			print "Scanning ... "
			mfrc = MFRC522.MFRC522()
			isScan = True
			while isScan:
				# Scan for cards    
				(status,TagType) = mfrc.MFRC522_Request(mfrc.PICC_REQIDL)
				# If a card is found
				if status == mfrc.MI_OK:
					print "Card detected"
				# Get the UID of the card
				(status,uid) = mfrc.MFRC522_Anticoll()				
				# If we have the UID, continue
				if status == mfrc.MI_OK:
					print "Card UID: "+ str(map(hex,uid))
					# Select the scanned tag
					if mfrc.MFRC522_SelectTag(uid) == 0:
						print "MFRC522_SelectTag Failed!"
					if cmdloop(uid) < 1 :
						isScan = False
		elif inCmd == "quit":
			destroy()
			exit(0)
		else :
			print "\tUnknown command\n"+"\tscan:scan card and dump\n"+"\tquit:exit program\n"
				
def cmdloop(cardID):
	pass
	while(True):
		dis_ConmandLine()
		dis_CardID(cardID)
		inCmd = raw_input()
		cmd = inCmd.split(" ")
		print cmd
		if(cmd[0] == "read"):
			blockAddr = int(cmd[1])
			if((blockAddr<0) or (blockAddr>63)):
				print "Invalid Address!"
			# This is the default key for authentication
			key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]			
			# Authenticate
			status = mfrc.MFRC522_Auth(mfrc.PICC_AUTHENT1A, blockAddr, key, cardID)
			# Check if authenticated
			if status == mfrc.MI_OK:
				mfrc.MFRC522_Readstr(blockAddr)
			else:
				print "Authentication error"
				return 0
				
		elif cmd[0] == "dump":
			# This is the default key for authentication
			key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
			mfrc.MFRC522_Dump_Str(key,cardID)
			
		elif cmd[0] == "write":
			blockAddr = int(cmd[1])
			if((blockAddr<0) or (blockAddr>63)):
				print "Invalid Address!"
			data = [0]*16
			if(len(cmd)<2):
				data = [0]*16
			else:	
				data = cmd[2][0:17]
				data = map(ord,data)
				if len(data)<16:
					data+=[0]*(16-len(data))
			# This is the default key for authentication
			key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]			
			# Authenticate
			status = mfrc.MFRC522_Auth(mfrc.PICC_AUTHENT1A, blockAddr, key, cardID)
			# Check if authenticated
			if status == mfrc.MI_OK:
				print "Before writing , The data in block %d  is: "%(blockAddr)
				mfrc.MFRC522_Readstr(blockAddr)
				mfrc.MFRC522_Write(blockAddr, data)
				print "After written , The data in block %d  is: "%(blockAddr)
				mfrc.MFRC522_Readstr(blockAddr)
			else:
				print "Authentication error"
				return 0
			
		elif cmd[0] == "clean":
			blockAddr = int(cmd[1])
			if((blockAddr<0) or (blockAddr>63)):
				print "Invalid Address!"
			data = [0]*16
			# This is the default key for authentication
			key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]			
			# Authenticate
			status = mfrc.MFRC522_Auth(mfrc.PICC_AUTHENT1A, blockAddr, key, cardID)
			# Check if authenticated
			if status == mfrc.MI_OK:
				print "Before cleaning , The data in block %d  is: "%(blockAddr)
				mfrc.MFRC522_Readstr(blockAddr)
				mfrc.MFRC522_Write(blockAddr, data)
				print "After cleaned , The data in block %d  is: "%(blockAddr)
				mfrc.MFRC522_Readstr(blockAddr)
			else:
				print "Authentication error"
				return 0
		elif cmd[0] == "halt":
			return 0
		else :
			print "Usage:\r\n" "\tread <blockstart>\r\n" "\tdump\r\n" "\thalt\r\n" "\tclean <blockaddr>\r\n" "\twrite <blockaddr> <data>\r\n"
				
def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # Ctrl+C captured, exit
		destroy()
 
	
