#import Required Modules
import os
import subprocess as sp
import time
import datetime

#store the Curreent time
start_time = time.time()

#get the current time
def getTime():
    return  datetime.datetime.now()

#Read The File and get ip address from
def AllServerlist(file_path):
    mylist=[line.rstrip('\n') for line in open(file_path) if line.rstrip('\n')!='']
    return mylist

def PingServer(hostname):
    return hostname,os.system("ping " + hostname)

#Ping using subprocess
def PingUsingSubprocess(hostname):
    status,result = sp.getstatusoutput("ping  -n 3 " + hostname)
    return status,result

#log While running ipaddress ping
def Log(ip,file,status):
    file.write('\n[{}]:[{}]:{}'.format(getTime(),status,ip))

#Input Output File Initilization
outputfile='output/{}.ods'.format(datetime.date.today()) #output file
file_path='input/serverlist.txt'    #input file
output_file='alllog.txt'    #for logging details


print('Output File path:{}'.format(os.path.abspath(outputfile)))

#open File For Writing Result
try:
    outfle = open(outputfile, 'w+')
    file = open(output_file, 'a+')
except:
    print('[error]Close Input/Output File First')
    exit(0)



outfle.write('Ip Address\tStatus')
print('Ping Started On {}'.format(getTime()))
print('\n{0:*^50s}'.format('Result'))

lines = AllServerlist(file_path)


try:
    for l in lines:
        status, response = PingUsingSubprocess(l)
        if response.find('Destination host unreachable') != -1 or response.find('Request timed out') != -1:
            value = "DOWN"
        elif(response.find('could not find host')!= -1):
            value='Host_Not_Found'
        elif(response.find('Reply from')!=-1):
            value='UP'
        elif(response.find('PING: transmit failed')!=-1):
            value='General_Failure'
        else:
            value = "Some_Thing_Wrong_Here"
        print('{}\t:\t{}'.format(l, value))
        Log(l,file,value)
        outfle.write('\n{}\t{}'.format(l, value))
except Exception as ex:
    print('Something went wrong check in alllog.txt file')
    file.write('{}'.format(ex))

finally:
    file.close()
    outfle.close()
print('\n{0:*^50s}\n'.format('End'))
#Final Message
print('Ping Completed On {}'.format(getTime()))
print("---Total {} seconds Elapsed ---".format((time.time() - start_time)))
