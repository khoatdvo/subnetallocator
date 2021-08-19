# Subnet Allocator
Small utility scirpt to allocate subnets into instances
# How to use
It can be used as a standalone script or to be imported into other script as a class

Sample input format in json:
```json
{
    "subnets": {
        "subnet-id1": {
            "az": "us-west-1a",
            "weight": 0
        },
        "subnet-id2": {
            "az": "us-west-1b",
            "weight": 0
        },
        "subnet-id3": {
            "az": "us-west-1c",
            "weight": 0
        },
        "subnet-id4": {
            "az": "us-west-1a",
            "weight": 0
        },
        "subnet-id5": {
            "az": "us-west-1a",
            "weight": 0
        },
        "subnet-id6": {
            "az": "us-west-1c",
            "weight": 0
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
```
# Testing
Run `subnetAllocatorTest.py` inside `tests/` directory
```bash
./subnetAllocatorTest.py
```