# Stack Smash!
The objective of the Stack Smashing project is to find the vulnerability in the provided code, and then use an attack string and shellcode to expose that vulnerability and compromise the server. To prove we compromised the server, we had to change a file hosted on the server.

# Our approach
## Vulnerability
The vulnerability in the webserver.c is in the following segment of code. The argument of check_filename_length (len) is passed in as byte type, rather than as an int:
```python
int check_filename_length(byte len) {
  if (len < 100) {
    return 1;
  }
  return 0;
}
```
This means that the length of the string can actually be longer than 100 bytes, as long as the length of the attack string % 256 <100. Because of this vulnerability and that the filename buffer is 100 bytes, we can pass in an attack string longer than 100 bytes, "pass" the check_filename_length function, and overflow the buffer and overwrite the return address to point to our NOPs/shellcode. 

## Attack String
Our attack string was composed of three elements in the following order:
 - address: This is the new return address that points to somewhere in our NOPs, so that our shellcode could then execute.
 - NOPs: These acted as a sort of "error buffer" for estimating where the shellcode was in the stack and where to point the return address
 - shell code: This code would open a shell, so that we could then modify a file on the server (from: http://shell-storm.org/shellcode/files/shellcode-836.php)

This string was wrapped in 'echo -e GET /' and 'HTTP'

# Running the code
## Set up

 - run `make build_webserver` to build the webserver
 - run `make run_webserver` which runs the webserver on port 9264

## Computing new addresses

The function in `compute_address.py` computes new addresses based on the 
number printed by the webserver.

## Hacking

 - Modify `hacker.py` to tweak the number of noops and return addresses to check
 - Run ``python3 hacker.py` | nc localhost 9264` in another terminal window
 - If a shell opens, you've won!
 - Run `vim index.html` in the new shell and modify the file.

To test against the attack server run ``python3 hacker.py` | nc 310test.cs.duke.edu 9264`

To netcat into the shell:

 - `netcat -vv 310test.cs.duke.edu 19264`

To reset the webserver:

 - `echo "hi" | nc 310test.cs.duke.edu 9265`
 
## Project Take-Aways
 - We formed a better understanding of the memory layout of a process by trying to overflow the stack of the running server.
 - We initially had issues determining the order in which we concatenated the different aspects of the attack string.  At first, we used the order of return address values repeated, then noops, and then the shell code.  We then figured out that the noops needed to go between the other two parts of the string to operate correctly.
 - Some testing was then done to determine the number of return addresses and noops required as well as the address value that landed our return address in the noop portion of the overflowed memory which allowed us to hack the local instance of the server.  The same tactics were then used on the remote server.
 - Overall, this was an informative project that gave us a better understanding of how stacks are structured and, in our case, how they can be exploited.
- In terms of our experience with the project, the project description was a little unclear to us at the beginning.  This and conflicting information from TAs lead to some confusion, but we were eventually able to figure out what we needed to do and how to implement it.

