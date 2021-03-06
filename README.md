# Subnet Allocator
Small utility scirpt to allocate subnets into instances
# How to use
It can be used as a standalone script or to be imported into other script as a class
## Setup
Make sure you have prerequisite packages
```bash
python3 -m pip install -r requirements.txt
```
## Sample input
```json
{
    "subnets": {
        "subnet-id1": {
            "az": "us-west-1a",
            "weight": 2
        },
        "subnet-id2": {
            "az": "us-west-1b",
            "weight": 4
        },
        "subnet-id3": {
            "az": "us-west-1c",
            "weight": 4
        },
        "subnet-id4": {
            "az": "us-west-1a",
            "weight": 7
        },
        "subnet-id5": {
            "az": "us-west-1a",
            "weight": 1
        },
        "subnet-id6": {
            "az": "us-west-1c",
            "weight": 4
        }
    },
    "instances": {
        "instance-id1" : "us-west-1a",
        "instance-id2" : "us-west-1b",
        "instance-id3" : "us-west-1b",
        "instance-id4" : "us-west-1a"
    }
}
```
## Standalone mode
```bash
$ ./subnetAllocator.py --help
usage: subnetAllocator.py [-h] -a {allocateSubnet,allocateSubnetWithWeight}
                          [{allocateSubnet,allocateSubnetWithWeight} ...] -f
                          FILE

optional arguments:
  -h, --help            show this help message and exit
  -a {allocateSubnet,allocateSubnetWithWeight} [{allocateSubnet,allocateSubnetWithWeight} ...], --action {allocateSubnet,allocateSubnetWithWeight} [{allocateSubnet,allocateSubnetWithWeight} ...]
                        action to be executed
  -f FILE, --file FILE  input file
```
## Import to another class
```python
from subnetAllocator import SubnetAllocator

with open('input.json') as inputFile:
    input = json.load(inputFile)
subnetAllocator = SubnetAllocator(input['subnets'], input['instances'])
subnetAllocator.allocate()
result = subnetAllocator.getResult()

subnetAllocator.allocateWithWeight()
result = subnetAllocator.getResult()
```
# Testing
Run `subnetAllocatorTest.py` inside `tests/` directory
```bash
./subnetAllocatorTest.py
```