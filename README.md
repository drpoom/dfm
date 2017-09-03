# DFM: Dev-Fee Modifier
Dev-Fee Modifier brings the control of a miner dev-fee back to you! This ensure that you have full control over your own software, and allow the users to monitor if the fee is higher than advertised.

Depending on the configurations, users can completely remove dev-fee if intended. The choice is yours.

This software is still in beta vesion, contributions in the form of coding or donations are very welcomed.

Donation:
  BTC: 
  ETH: 0xe87a5b228a8cf327caf4a74cc2e0a5886d0bd9f5


Installation in Ubuntu 16.04:
  sudo apt install python python-nfqueue python-scapy -y

Usage:
  sudo python dfm.py
  # Or 'sudo python dfm.py&' to run in background 

Hint:
  Add your own address to the first line in address_pass.txt. All unknown addresses will be filtered and replaced with the first address in address_pass.txt.


