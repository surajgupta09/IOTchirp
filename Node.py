import argparse
import sys
import time
import datetime
import json
import math
import random
import logging

from chirpsdk import ChirpConnect, CallbackSet, CHIRP_CONNECT_STATE
logging.basicConfig(filename='node.log',format='%(asctime)s %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
sdk = ChirpConnect()
#chid = random.randint(0,6)
device_no='#2'
chid=1
cts=''

class Callbacks(CallbackSet):
    	
    def on_state_changed(self, previous_state, current_state):
        """ Called when the SDK's state has changed """
        logger.info('State changed from %s to %s',CHIRP_CONNECT_STATE.get(previous_state),CHIRP_CONNECT_STATE.get(current_state))
        print('State changed from {} to {}'.format(
            CHIRP_CONNECT_STATE.get(previous_state),
            CHIRP_CONNECT_STATE.get(current_state)))

    
    def on_receiving(self, channel):
    	""" Called when a chirp frontdoor is detected """
    	logger.info('Receiving data [%d]',channel)
    	print('Receiving data [ch{ch}]'.format(ch=channel))
    	
    	
    def on_received(self,payload,channel):
    	global device_no
    	global cts
    	check = payload.decode('utf-8')
    	if check==device_no:
    		cts=check

    	
    def on_sent(self, payload, channel):
    	temp=payload.decode('utf-8')
    	""" Called when the entire chirp has been sent """
    	logger.info('Sent: %s [%d]',temp, channel)
    	print('Sent: {data} [ch{ch}]'.format(data=temp, ch=channel))

                
                
def datasensor():
	global cts
	global device_no
	if device_no!=cts:
		
		#giving device id
		b=random.randint(30,40)
		time.sleep(b)
		payload=device_no.encode('utf-8')
		sdk.send(payload)
		
		
		
	if device_no==cts:
		#generate playload
		timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		pm01=225
		pm25=223
		pm10=267
		co2 = 325
		co=856
		no2 = 342
		humidity = 18
		temperature = 37
		
		content = {"time":timestamp,"PM01":pm01,"PM2.5":pm25,"PM10":pm10,"NO2":no2,"CO2":co2,"CO":co,"Humi":humidity,"Temp":temperature}
		
		#convering dictionary to json string
		json_str = json.dumps(content)
		print('JSON STRING : ')
		print(json_str)
		print(len(json_str))
		message = json_str.encode('utf-8')
		
		start = 0
		
		while start < len(message):
			
			if start + 7 < len(message):
				
				end = start + 7
			else :
			
				end = len(message)
			payload = sdk.new_payload(message[start:end])
			start = end
			sdk.send(payload)
			time.sleep(3.5)
		cts='#x'
		logger.info('Changing cts %s',cts)
		print('Changing cts',cts)
		a=random.randint(30,40);
		logger.info('in sleep for  : %s',a)
		print('in sleep for  : ',a)
		time.sleep(a)

def main(input_device, output_device,block_size, sample_rate):
    
    
    
    # Configure audio
    sdk.audio.input_device = input_device
    sdk.audio.output_device = output_device
    sdk.audio.block_size = block_size
    sdk.input_sample_rate = sample_rate
    sdk.output_sample_rate = sample_rate
    
    
    
    
    #getting channel number for device
    logger.info('[ MY CHANNEL ID IS ] : %d',chid)
   
    print('[ MY CHANNEL ID IS ] :',chid)
    
    sdk.set_callbacks(Callbacks())
    logging.info('Protocol: {protocol} [v{version}]'.format(protocol=sdk.protocol_name,version=sdk.protocol_version))
    print('Protocol: {protocol} [v{version}]'.format(protocol=sdk.protocol_name,version=sdk.protocol_version))
    sdk.start(send=True, receive=True)
    sdk.transmission_channel=chid
    
    try:
    	while(True):
    		datasensor()
    		time.sleep(5)
    		
    except KeyboardInterrupt:
    	print('exiting')
    sdk.stop()    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='ChirpSDK Demo',
        epilog='Sends a random chirp payload, then continuously listens for chirps'
    )
    
    parser.add_argument('-i', type=int, default=None, help='Input device index (optional)')
    parser.add_argument('-o', type=int, default=None, help='Output device index (optional)')
    parser.add_argument('-b', type=int, default=4096, help='Block size (optional)')
    parser.add_argument('-s', type=int, default=44100, help='Sample rate (optional)')
    args = parser.parse_args()

    main(args.i, args.o, args.b, args.s)
