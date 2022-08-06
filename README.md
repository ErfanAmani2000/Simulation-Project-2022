# Call Center Simulation Project
The purpose of this code is to simulate a casual call center with 
two experts, three amateur, and two technical servers. we prepared
this for the "Introduction to Simulation" course project; which was 
instructed by Dr. Nafise Sedghi. For this code to be completed we 
also appreciate Mr. Shahmoradi for his constructive and helpful 
advice.

In this simulation, all service times are based on exponential 
distribution, and all inter-arrival times are Poisson distribution 
with different mean parameters. in the presented call center, we
have three subsystems. The first one is when a user call and with attention
to the fact that the user type (whether he/she is a normal or special
user) and queue are different, one of an expert of amateur servers will serve him/her.
The second subsystem is the call-back mechanism. In a specific condition, the user can 
leave the queue and require a call-back option; this option will make servers call him 
on the 2nd or 3rd shift of the day, whenever they are idle. The third subsystem
is technical call. when a user ends their call with one of the servers (
expert or amateur) he/she can demand to be connected to technical servers
to solve his/her technical issues.

On a random day of each month, disruption occurs. As a result users inter
arrival times change that should be modeled.

We use Object-Oriented Programming and develop a class for this simulation.
the only reason is to initialize the class with some essential parameters 
and in the third phase when we need to make a statistical comparison between 
two configurations of the system, a class would make that easy.