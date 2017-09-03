# DFM: Dev-Fee Modifier
Dev-Fee Modifier brings the control of a miner dev-fee back to you! This ensure that you have full control over your own software, and allow the users to monitor if the fee is higher than advertised.

Depending on the configurations, users can completely remove dev-fee if intended. The choice is yours.

This software is still in beta vesion, contributions in the form of coding or donations are very welcomed.


# Donation:
* BTC: 1E6nAQ6x61SCnTtgxn7TYNT4p3q3SiZXkA
* ETH: 0xe87a5b228a8cf327caf4a74cc2e0a5886d0bd9f5

# Prerequisites in Ubuntu 16.04:
```bash
  sudo apt install python python-nfqueue python-scapy -y
```

# Installation:
* git clone https://github.com/drpoom/dfm.git
* Or simply download the project and extract to your local folder

# Usage:
```bash
  sudo python dfm.py
  # Or 'sudo python dfm.py&' to run in background 
```

# Configuration:
* TODO: Make a configuration file. It is currently hard-coded.
  * Port: 9999
* Address:
  * Add your own address to the first line in address_pass.txt. All unknown addresses will be filtered and replaced with the first address in address_pass.txt.
  

# Tested For
* Ethereum
  * Claymore 10 in Ubuntu 16.04
  * Claymore 9.x in Ubuntu 16.04
  * ccminer in Ubuntu 16.04
* Zcash
  * EBWFmner is tested (to validate '-nofee' option)

# License
* GNU GPL v3 https://www.gnu.org/licenses/gpl-3.0.en.html
