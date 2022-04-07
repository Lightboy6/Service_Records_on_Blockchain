
# import required libraries
from dataclasses import dataclass
import streamlit as st
from datetime import datetime
from dataclasses import dataclass
from typing import Any, List
import pandas as pd
import hashlib
from dotenv import load_dotenv
from web3 import Web3
import os
import json
from pathlib import Path


from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

@dataclass
class ServiceRecord:

    technician_id: Any
    vehicle_id: Any
    event_id: Any




@dataclass
class Block:
    event_id: ServiceRecord.event_id
    vehicle_id: ServiceRecord.vehicle_id
    technician_id: ServiceRecord.technician_id
    
    
    

    service_date: str = datetime.utcnow().strftime('%H:%M:%S')
    prev_hash: str = '0'

    def hash_block(self):
        sha = hashlib.sha256()

        event_id_encoded = self.event_id.encode()
        sha.update(event_id_encoded)
        
        vehicle_id_encoded = self.vehicle_id.encode()
        sha.update(vehicle_id_encoded)

        technician_id_encoded = self.technician_id.encode()
        sha.update(technician_id_encoded)


        service_date_encoded = self.service_date.encode()
        sha.update(service_date_encoded)



        sha.update(self.prev_hash.encode())


        return sha.hexdigest()


##At this point^ my website run

@dataclass
class ServiceChain:
    chain: List[Block]

    def add_block(self, block):
        print('new block added')
        self.chain += [block]


st.markdown('# SHOW ME THE BLOCKFAX!')
st.markdown('## ENTER SERVICE RECORDS BELOW')


# add event identifier
#believe im creating a service records below
#technician_id = st.text_input('Technician')
#vehicle_id = st.text_input('Vehicle Vin#')
#event_id = st.text_input("Service Record")


# going to need an attribute that holds and records the time in specific format --> "timestamp"

# allow to cache inputted data
@st.cache(allow_output_mutation=True)
def setup():
    print("Start")
    genisis_block = Block(
        event_id=ServiceRecord(technician_id = '', vehicle_id = '', event_id='' )
        
    )

    return ServiceChain([genisis_block])
    return 


servicechain_live = setup()

technician_id = st.text_input("Technician")
vehicle_id = st.text_input('Vehicle Vin#')
event_id = st.text_input('Service Record')
#the review for how to create a website is under the second class with sub around minute 40
if st.button('Add Service'):
    prev_block = servicechain_live.chain[-1]

    prev_block_hash = prev_block.hash_block()

    new_block = Block(
        record=ServiceRecord(technician_id, vehicle_id, event_id),
        prev_hash = prev_block_hash
    )

    servicechain_live.add_block(new_block)

##make it pretty and legible
print(servicechain_live.chain)
servicechain_df = pd.DataFrame(servicechain_live.chain).astype(str)

st.write(servicechain_df)
