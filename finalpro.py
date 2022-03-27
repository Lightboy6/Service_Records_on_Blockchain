
# import required libraries
from dataclasses import dataclass
import streamlit as st
from datetime import datetime
from dataclasses import dataclass
from typing import Any, List
import pandas as pd
import hashlib


@dataclass
class ServiceRecord:

    technician_id: Any
    vehicle_id: Any
    event_id: Any

@dataclass
class Block:
    record: ServiceRecord
    service_date: str = datetime.utcnow().strftime('%H:%M:%S')
    prev_hash: str = '0'

    def hash_block(self):
        sha = hashlib.sha256()

        service_date_encoded = self.service_date.encode()
        sha.update(service_date_encoded)

        record = str(self.record).encode()

        sha.update(record)

        sha.update(self.prev_hash.encode())

        return sha.hexdigest()


##At this point^ my website run

@dataclass
class ServiceChain:
    chain: List[Block]

    def add_block(self, block):
        self.chain += [block]


st.markdown('# SHOW ME THE BLOCKFAX!')
st.markdown('## ENTER SERVICE RECORDS BELOW')


# add event identifier
#believe im creating a service records below
technician_id = st.text_input('Technician')
vehicle_id = st.text_input('Vehicle Vin#')
event_id = st.text_input("Service Record")


# going to need an attribute that holds and records the time in specific format --> "timestamp"

# allow to cache inputted data
st.cache(allow_output_mutation=True)
def setup():
    genisis_block = Block(
        record= ServiceRecord(technician_id = 'Jiffy Lube', vehicle_id = 'honda civic', event_id='oil change' )
    )

    return ServiceChain([genisis_block])


servicechain_live = setup()

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

servicechain_df = pd.DataFrame(servicechain_live.chain).astype(str)

st.write(servicechain_df)

## allow for service search

st.sidebar.write('# Service Lookup')
selected_block = st.sidebar.selectbox(
    "Which service event do you want to look up?", servicechain_live.chain
)

st.sidebar.write(selected_block)












