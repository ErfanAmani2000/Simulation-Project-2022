# Call Center Simulation Project

## Overview

This project simulates a call center environment with three types of servers: experts, amateurs, and technical support. It was developed for the "Introduction to Simulation" course under the guidance of Dr. Nafise Sedghi. We also thank Mr. Shahmoradi for his constructive and helpful advice.

## Simulation Details

In this simulation:

- **Service times** are modeled using an exponential distribution.
- **Inter-arrival times** follow a Poisson distribution with varying mean parameters.
  
The call center is divided into three subsystems:

1. **User Calls**: Depending on the user type (normal or special) and queue status, calls are directed to expert or amateur servers.
2. **Call-Back Mechanism**: Users can opt for a call-back if they leave the queue under certain conditions. Servers will call back the user during the 2nd or 3rd shift whenever they are idle.
3. **Technical Calls**: After finishing a call with an expert or amateur server, users can be connected to technical servers for additional support.

Additionally, a disruption affects user inter-arrival times on a random day each month, which is incorporated into the model.

## Project Structure

The simulation is implemented using Object-Oriented Programming (OOP). The use of classes allows for easy initialization with essential parameters and facilitates statistical comparisons between different system configurations.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YourUsername/CallCenterSimulation.git
    cd CallCenterSimulation
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
