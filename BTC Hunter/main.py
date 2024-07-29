import os
import ecdsa
import hashlib
import base58
import requests
import bitcoin

keep_running = True
address = ""

print("Start Bitcoin Hunting")
print("---------------------")

def generate_private_key():
    return os.urandom(32)

def private_key_to_wif(private_key):
    extended_key = b"\x80" + private_key
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    return base58.b58encode(extended_key + checksum)

def private_key_to_public_key(private_key):
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    return bytes.fromhex("04") + verifying_key.to_string()

#Check the balance from blockchain api
def check_balance():
  private_key = generate_private_key()
  wif_private_key = private_key_to_wif(private_key).decode()
  public_key = private_key_to_public_key(private_key).hex()
  address = bitcoin.pubkey_to_address(public_key)
  try:
    response = requests.get("https://blockchain.info/balance", params={"active": address})
    response.raise_for_status()
    data = response.json()
    final_balance=float(data[address]["final_balance"])
    print("WIF Private Key:",wif_private_key)
    print("Public Key",public_key)
    print("Address :",address)
    print("Balance:", final_balance)
    print("---------------------")
    if final_balance != 0:
        with open('FoundAddress.txt', 'a') as f:
            f.write("\n",wif_private_key)
            print("Donate to HCMLXOX:bc1qnk0ftxa4ep296phhnxl5lv9c2s5f8xakpcxmth")
  except Exception as e:
    print("Error:Please Check your Network Connection")
    print(e)

#Start Programme
while keep_running:
    check_balance()
