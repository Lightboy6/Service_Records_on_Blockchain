from dataclasses import dataclass
import streamlit as st
import datetime as datetime
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
class Block:
    vehicle_vin: int
    service_provider: Any
    odometer: int
    service_report: Any
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")

    def hash_block(self):
        sha = hashlib.sha256()

        vehicle_vin = str(self.vehicle_vin).encode()
        sha.update(vehicle_vin)

        service_provider = str(self.service_provider).encode()
        sha.update(service_provider)

        odometer = str(self.odometer).encode()
        sha.update(odometer)

        service_report = str(self.service_report).encode()
        sha.update(service_report)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        return sha.hexdigest()

# Create the data class PyChain


@dataclass
class PyChain:
    chain: List[Block]

    def add_block(self, block):
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
    print("Initializing Chain")
    return PyChain([Block(vehicle_vin="", service_provider= "", odometer="", service_report="" )])


pychain = setup()


input_service = st.text_input("Service Report")
input_odometer_reading = st.text_input("Odometer Reading")
input_service_tech = st.text_input("Service Technician")
input_vehicle_vin = st.text_input("Vehicle Vin")
#the review for how to create a website is under the second class with sub around minute 40

if st.button("Input Log"):
    prev_block = pychain.chain[-1]

   
    prev_block_hash = prev_block.hash_block()
    new_block = Block(vehicle_vin= input_vehicle_vin, odometer=input_odometer_reading, service_provider=input_service_tech, service_report=input_service, prev_hash=prev_block_hash)
    pychain.add_block(new_block)
##make it pretty and legible

pychain_df = pd.DataFrame(pychain.chain)
st.write(pychain_df)



## allow for service search

st.sidebar.write('# Service Lookup')
selected_block = st.sidebar.selectbox(
    "Which service event do you want to look up?", pychain.chain
)

st.sidebar.write(selected_block)

###########################################################
###########################################################
###########################################################
###########################################################

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/autoregistry_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_auto(auto_vin, auto_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(auto_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "vin": auto_vin,
        "make": auto_make,
        "price": initial_purchase_price,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_registration_renewal(registration_renewal):
    json_report = convert_data_to_json(registration_renewal)
    registration_ipfs_hash = pin_json_to_ipfs(json_report)
    return registration_ipfs_hash


st.title("AutoFax Registration System")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register New Vehicle Purchase
################################################################################
auto_brands = ["", "Audi", "Bentley",  "BMW", "Cadillac", "Chevy", "Chrysler", "Dodge", "Ferrari", "Ford", "Honda", "Hyundai", "Jaguar",
"Jeep", "Kia", "Lamborghini", "Lexus", "Mazda", "Mercedes-Benz", "Nissan", "Porsche", "Subaru", "Tesla", "Toyota"]

st.markdown("## Register New Vehicle Purchase")
auto_vin = st.text_input("Enter the VIN# of the vehicle")
auto_make = st.selectbox("Enter the vehicle make", options=auto_brands)
new_used = st.selectbox("New / Used", options=["","NEW", "USED"])
initial_purchase_price = st.text_input("Enter the initial purchase price")
auto_file = st.file_uploader("Upload Title", type=["jpg", "jpeg", "png"])
if st.button("Register Purchase"):
    auto_ipfs_hash = pin_auto(auto_vin, auto_file)
    auto_uri = f"ipfs://{auto_ipfs_hash}"
    tx_hash = contract.functions.registerPurchase(
        address,
        auto_vin,
        auto_make,
        new_used,
        int(initial_purchase_price),
        auto_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # st.write("Transaction receipt mined:")
    # st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Auto IPFS Gateway Link](https://ipfs.io/ipfs/{auto_ipfs_hash})")
    st.balloons()
st.markdown("---")




