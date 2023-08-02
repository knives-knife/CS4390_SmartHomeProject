# CS4390_SmartHomeProject

The topic for the project this semester is to design and implement a network protocol for remote smart-home management. Here is my (slightly overengineered) solution.

# Project Description

## Requirements:

- Design an application layer protocol for two network entities: client (C) and server (S) to communicate. The protocol should be text-based and well documented. You should start designing and documenting the protocol before implementing a network application that uses this protocol. A protocol specification (refer to one of the RFCs on the IETF's web page for information on protocol documentation) must be submitted at the end of the project.

- The purpose of the protocol is to allow C to
1. get the status of the smart devices that S manages. These are those smart devices: two light switches named FR (Family Room) and K (Kitchen), and a thermostat named T. The status of a light switch should be ON or OFF, and that of the thermostat should be the current temperature settting, e.g. 76. C can ask S status of an individual device (e.g. FR) or of ALL devices.
2. ask S to set a switch (FR or K) to ON or OFF, or to set the thermostat T to a value, e.g. 80..  

- Use mininet to implement a network application that allows a user to control the devices across the network using the application protocol that you have designed. Obviously the application is consisted of two parts: a client C and a server S.

- C and S must run on different hosts simulated using mininet and use the protocol designed above for communications.
## Submission Requirements:

At the end of the semester, submit a ZIP file named MP_<first name>_l<ast name>.zip to elearning by the due date. The ZIP file must contain

1. A project report (in Word or PDF format) covering

&nbsp;&nbsp;&nbsp;&nbsp;a) a description of the program,

&nbsp;&nbsp;&nbsp;&nbsp;b) the challenges that you had  and how did you overcome them,

&nbsp;&nbsp;&nbsp;&nbsp;c) what you have learned by doing the project,

&nbsp;&nbsp;&nbsp;&nbsp;d) a discussion about algorithms and techniques used in the program,

&nbsp;&nbsp;&nbsp;&nbsp;and e) any suggestions you may have (optional).

2. A short video clip with audio narration demonstrating the network application in action. (If the video is too big you can post it on a website, e.g. youTube, and submit the link).

3. All codes that are needed to run your application.

4. A protocol specification document as mentioned above.

5. A design document describing your implementation of the network application.

Let me or the TA know if there is any questions or comments.

# How to Run

1. Make sure you have the Mininet VM installed and on your Mininet VM you have Python 3 (I used Python 3.6.9)
2. Upload the Python files to Mininet's default directory (should be `/home/mininet` for the default Mininet VM)
3. Start Mininet with the default topology (`sudo mn`) (default topology is two hosts connected by a switch)
4. On host 1, start the server in the background by running the command `h1 python3 server.py &` (h1 must be the host because the IP address of the server is hardcoded as 10.0.0.1)
5. On host 2, start the client by running the command `h2 python3 client.py`
6. When you're done, don't forget to kill the background process on h1 if the server is still running with the command `h1 kill %python`. Also don't forget to clean Mininet with the command `mn -c`. 

<br>
A video explaining the functionalities of the client has been provided. 
<br><br>
Happy Coding!
