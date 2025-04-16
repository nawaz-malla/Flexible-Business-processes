# Flexible-Business-processes

# Simple BPMN Choreography Smart Contract on Algorand

This project implements a simplified Business Process Model and Notation (BPMN) choreography pattern as a smart contract on Algorand Blockchain. It defines a message-passing choreography between two parties, `Party A` and `Party B` and more in the updated choreography.

---

## 🧠 Overview

The smart contract models a BPMN choreography with the following:

### Participants
- **Admin**: Controls updates and deletion of the contract.
- **Party A**: Initiates the process by sending `msg1`.
- **Party B**: Responds with `msg2` if the process conditionally branches to `task2`.
- **party C**: Responds with `msg3` if the process conditionally branches to `task3`.

### BPMN Flow Elements
- `start1`: Begins the process.
- `task1`: Executed by Party A, sends `msg1`.
- `xor1`: Branches to either `task2` or `end2` based on `msg1_param_x`.
- `task2`: Executed by Party B, sends `msg2`.
- `task3`: Executed by Party C, sends `msg3`.
- `end1`: Successful completion.
- `end2`: Alternate completion.

---





### Pre-requisites

- [Python 3.12](https://www.python.org/downloads/) or later
- [Docker](https://www.docker.com/) (only required for LocalNet)

> For interactive tour over the codebase, download [vsls-contrib.codetour](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour) extension for VS Code, then open the [`.codetour.json`](./.tours/getting-started-with-your-algokit-project.tour) file in code tour extension.

### Initial Setup

#### 1. Clone the Repository
Start by cloning this repository to your local machine.

#### 2. Install Pre-requisites
Ensure the following pre-requisites are installed and properly configured:

- **Docker**: Required for running a local Algorand network. [Install Docker](https://www.docker.com/).
- **AlgoKit CLI**: Essential for project setup and operations. Install the latest version from [AlgoKit CLI Installation Guide](https://github.com/algorandfoundation/algokit-cli#install). Verify installation with `algokit --version`, expecting `2.0.0` or later.

#### 3. Bootstrap Your Local Environment
Run the following commands within the project folder:

- **Install Poetry**: Required for Python dependency management. [Installation Guide](https://python-poetry.org/docs/#installation). Verify with `poetry -V` to see version `1.2`+.
- **Setup Project**: Execute `algokit project bootstrap all` to install dependencies and setup a Python virtual environment in `.venv`.
- **Configure environment**: Execute `algokit generate env-file -a target_network localnet` to create a `.env.localnet` file with default configuration for `localnet`.
- **Start LocalNet**: Use `algokit localnet start` to initiate a local Algorand network.

### Development Workflow

#### Terminal
Directly manage and interact with your project using AlgoKit commands:

1. **Build Contracts**: `algokit project run build` compiles all smart contracts. You can also specify a specific contract by passing the name of the contract folder as an extra argument.
For example: `algokit project run build -- hello_world` will only build the `hello_world` contract.
2. **Deploy**: Use `algokit project deploy localnet` to deploy contracts to the local network. You can also specify a specific contract by passing the name of the contract folder as an extra argument.
For example: `algokit project deploy localnet -- hello_world` will only deploy the `hello_world` contract.




