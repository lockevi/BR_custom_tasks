# simple ATM controller



This project is a simple ATM controller implemented by using python3.

The *pdoc* generated more documents using docstrings in **./docs**.



## Installation

**Step 1**: Requirements
- Python >= 3.8.9
- pytest >= 7.11
- git

**Step 2**: Clone the project
```shell
git clone https://github.com/lockevi/BR_custom_tasks
```

**Step 3**: Make a virtual environment and activate it
```shell
cd ./BR_custom_tasks
python3 -m venv venv
source ./venv/bin/activate
```

**Step 4**: Install some packages using pip
```shell
pip install -r ./requirements.txt
```

---



## Run and Test

***app/main.py***  : Sample code which shows some basic flow of ATM controller
```shell
export PYTHONPATH=`pwd`
cd ./app
python3 main.py
```

***tests/\*.py*** : ***pytest*** was used for a lot of test cases. Simply run ***pytest*** at directory ***./tests***.
```shell
export PYTHONPATH=`pwd`
cd ./tests
pytest
```

---



## User Scenario & Thoughts

As an ATM user, I described a series of my behaviors in order.
As an ATM developer, I also tried to consider what ATM to do at same time.

#### 0. Insert card & Select an account
1. Put the card in
   - Is it registered card ?
2. Enter the PIN number
   - PIN is correct ?
3. Select account
   - Before selecting an account, **prepare** the information of **accounts list** from the bank.

#### A. Balance
4. Select "Check Balance" in the menu
5. Check the balance of the selected account
6. Get a receipt
   - **Print** a receipt
   - Flow ends. **Return** to initial state.

#### B. Deposit
4. Select "Deposit" in the menu
   - The **door** of money counter **opened**
5. Put the money in
   - The **door** of money counter **closed**
   - Count the money 
6. Check the money counted and Confirm again
   - **Update** the **account** using Bank API
   - Put the money into the cash bin
7. Get a receipt
   - **Print** a receipt
   - Flow ends. **Return** to initial state.

#### C. Withdraw
4. Select "Withdraw" in the menu
5. Input the amount of money to withdraw
   - Check amount <= balance 
   - Check amount <= available money in cash bin
   - **Update** the **account** using Bank API
   - Count the money
   - The **door** of money counter **opened**
6. Take the money
   - The **door** of money counter **closed** 
7. Get a receipt
   - **Print** a receipt
   - Flow ends. **Return** to initial state.



## More Assumptions

1. [Card] - [Bank] - [Accounts] relations
   - ONE card is linked to ONE bank only. (1:1)
   - ONE card can be linked to N accounts. (1:N)
2. The formats of card number and PIN number
   - CARD NUMBER is 8-digit number from 00000000 to 99999999.
   - PIN is 4-digit number from 0000 to 9999.
3. Simulations by the simple mock-up classes
   - Implementation of banking system is out of scope.
   - Hardwares, like card reader, cash bin, printer. .., will be defined only.
4. No PIN number in banking API or network packets
   - PIN should not be exposed in anywhere for security, 
   - Used token for access to banking API. (but hash function is not used now.)
5. Ignore event-driven functionalities
   - Detecting card insertion, Users' money moves in/out
   - Event handling is out of the scope to make a simpler problem.



## State Diagram





## Structure of the ATM controller

