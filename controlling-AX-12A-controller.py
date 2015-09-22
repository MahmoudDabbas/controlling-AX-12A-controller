import serial
import time
import sys
import math

port = "/dev/ttyUSB0"	# define particular port used
ser = serial.Serial(port, 1000000)	# define serial port
ser.close() 	#close port if previously open
ser.open()	#open port
print ser.isOpen()	#make sure we could open the port!

# a function to evaluate the Higher Byte of the Goal Position Parameter
def GoalPositionValH(angle):
	if math.floor(angle*3.41)>256:
		return (int(math.floor(angle*3.41/256)))
	else:
		return (0)
# a function to evaluate the Lower Byte of the Goal Position Parameter
def GoalPositionValL(angle):
	"compute the Goal Position Val High Vaule of the angle parameter"
	
	if math.floor(angle*3.41)<256:
		return int(math.floor(angle*3.41))
	else:
		more = (int(math.floor(angle*3.41/256)))
		return (int(math.floor(angle*3.41-(more)*256)))

# calculate Check Sum
def checksum(id,length,Write_instruction,GoalPositionAddress,DegL,DegH):
	CHECKSUM = id+length+Write_instruction+GoalPositionAddress+DegL+DegH
	more = (int(math.floor(CHECKSUM/256)))
	return 255-(int(math.floor(CHECKSUM-(more)*256)))



start = [255,255] 	#start of an incoming Instruction packet
id = 13		#The unique ID of a Dynamixel unit.	
length = 5	#the length of the packet where its value is Number of parameters (N) + 2
Write_instruction = 3	#write instruction value
Read_instruction = 2	#Read instruction value
GoalPositionAddress = 30	#Goal Position Address Value

# a function to calculate the instruction packet
def  write_position(angle):
	DegH = GoalPositionValH(angle)
	DegL = GoalPositionValL(angle)
	CHECKSUM= checksum(id,length,Write_instruction,GoalPositionAddress,DegL,DegH)
	print "chechsum = ", CHECKSUM
	return "".join(map(chr,start+[id, length, Write_instruction, GoalPositionAddress, DegL, DegH, CHECKSUM]))

# a function to convert Degrees to Radians
def Deg2Rad (Deg):
	return Deg*3.141592654/180

# a function to convert  Radians to  Degrees
def Rad2Deg (Rad):
	return math.floor(Rad*180/3.141592654)

Time=0
ser.write(write_position(0+150)) # go to vertical position
period = .1	#total length in seconds of the period cycle
step = .001	#steps of updating the servo
counter=0	#some counter
while True:
	position_deg=150+math.floor(90*math.cos(Time/period)) #calculate the current degree angle by calculating hte cosine of the signal and adding 150 degrees as the zero position
	print "position_deg: ",position_deg-150
	ser.write(write_position(position_deg))	#output the angle to the servo
	time.sleep(step)	#sleep for he step time
	Time=Time+step		#update the time for the step
	counter=counter+period	#update the counter
	print "counter is : ",counter
ser.close()
