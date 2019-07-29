import argparse
import sys
import time
import datetime
import json
import math
import random
import logging
from chirpsdk import ChirpConnect, CallbackSet, CHIRP_CONNECT_STATE

logging.basicConfig(filename='accesspoint.log',format='%(asctime)s %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
sdk = ChirpConnect()
chid = 7
device_no=''



class Callbacks(CallbackSet):

    def __init__(self):
    	self.temp=''
    	self.received=''
    	
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

    def on_received(self, payload, channel):
    	if payload is None :
       		logger.info('[ Failed to decode message! ]')
       		print('[ Failed to decode message! ]')
    	else:
    		global device_no
    		
    		self.temp = payload.decode('utf-8')
    		if '#' in self.temp:
    			global device_no
    			payload = self.temp.encode('utf-8')
    			sdk.send(payload)
    			device_no=self.temp
    			
    			
    			
    			
    		else:	
    			self.received = self.received + self.temp
    			logger.info('[ Received data ] %s',self.received)
    			print('[ Received data ]',self.received)
    			if channel==0 and channel!=chid:
    				with open('ch0'+device_no+'.json','a') as f0:
    					json.dump(self.temp,f0)
    			
    			if channel==1 and channel!=chid:
    				with open('ch1'+device_no+'.json','a') as f1:
    					json.dump(self.temp,f1)
    					
    			if channel==2 and channel!=chid:
    				with open('ch2'+device_no+'.json','a') as f2:
    					json.dump(self.temp,f2)
    					
    			if channel==3 and channel!=chid:
    				with open('ch3'+device_no+'.json','a') as f3:
    					json.dump(self.temp,f3)
    			if channel==4 and channel!=chid:
    				with open('ch4'+device_no+'.json','a') as f4:
    					json.dump(self.temp,f4)
    			if channel==5 and channel!=chid:
    				with open('ch5'+device_no+'.json','a') as f5:
    					json.dump(self.temp,f5)
    			if channel==6 and channel!=chid:
    				with open('ch6.'+device_no+'json','a') as f6:
    					json.dump(self.temp,f6)
    			
    	
    		
    def on_sent(self, payload, channel):
    	temp=payload.decode('utf-8')
    	""" Called when the entire chirp has belogging,infoen sent """
    	logger.info('Sent: {data} [ch{ch}]'.format(data=temp, ch=channel))
    	print('Sent: {data} [ch{ch}]'.format(data=temp, ch=channel))

                


def main(input_device, output_device,block_size, sample_rate):
    
    
    
    # Configure audio
    sdk.audio.input_device = input_device
    sdk.audio.output_device = output_device
    sdk.audio.block_size = block_size
    sdk.input_sample_rate = sample_rate
    sdk.output_sample_rate = sample_rate
    
    
    
    #getting channel number for device
   
    logger.info('[ MY CHANNEL ID IS ] : %d',chid)
    
    sdk.set_callbacks(Callbacks())
    logger.info('Protocol: {protocol} [v{version}]'.format(protocol=sdk.protocol_name,version=sdk.protocol_version))
    sdk.start(send=True, receive=True)
    sdk.transmission_channel=chid
    
    try:
        # Process audio streams
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Exiting')  
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='ChirpSDK Demo',
        epilog='Sends chirp payload, then continuously listens for chirps'
    )
    
    parser.add_argument('-i', type=int, default=None, help='Input device index (optional)')
    parser.add_argument('-o', type=int, default=None, help='Output device index (optional)')
    parser.add_argument('-b', type=int, default=4096, help='Block size (optional)')
    parser.add_argument('-s', type=int, default=44100, help='Sample rate (optional)')
    args = parser.parse_args()

    main(args.i, args.o, args.b, args.s)
