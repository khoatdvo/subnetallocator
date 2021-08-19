#!/usr/bin/python3
import argparse
import json
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)

class REGION(Enum):
    A = 1
    B = 2
    C = 3

class SubnetAllocator:
    def __init__(self, subnets, instances):
        self.subnets = subnets
        self.instances = instances
        self.__result = {}

    def rawAZToEnum(self, rawAZ):
        az = rawAZ[-1]
        if az == 'a' or az == 'A':
            return REGION.A
        elif az == 'b' or az == 'B':
            return REGION.B
        else:
            return REGION.C

    def getResult(self):
        return self.__result

    def allocate(self):
        reindexSubnetAsAZ = {}
        reindexInstanceAsAZ = {}
        for az in REGION:
            reindexSubnetAsAZ[az] = []
            reindexInstanceAsAZ[az] = []

        for key, value in self.subnets.items():
            reindexSubnetAsAZ[self.rawAZToEnum(value['az'])].append(key)

        for key, value in self.instances.items():
            reindexInstanceAsAZ[self.rawAZToEnum(value)].append(key)

        logging.debug('reindexSubnetAsAZ is '.format(reindexSubnetAsAZ))
        logging.debug('reindexInstanceAsAZ is '.format(reindexInstanceAsAZ))

        leftOverInstances = []
        leftOverSubnets = []
        for az in REGION:
            reindexSubnetAsAZ[az].extend(leftOverSubnets)
            reindexInstanceAsAZ[az].extend(leftOverInstances)
            lenSubnetList = len(reindexSubnetAsAZ[az])
            lenInstanceList = len(reindexInstanceAsAZ[az])
            self.__result.update(dict(zip(reindexSubnetAsAZ[az], reindexInstanceAsAZ[az])))
            if lenSubnetList > lenInstanceList:
                leftOverSubnets = reindexSubnetAsAZ[az][lenInstanceList:]
            elif lenSubnetList < lenInstanceList:
                leftOverInstances = reindexInstanceAsAZ[az][lenSubnetList:]

def main(args):
    with open(args.file) as input_file:
        input = json.load(input_file)
    subnets = input['subnets']
    instances = input['instances']
    if 'allocateSubnet' in args.action:
        subnetAllocator = SubnetAllocator(subnets, instances)
        subnetAllocator.allocate()
        logging.info("allocateSubnet result is: {}".format(subnetAllocator.getResult()))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', nargs="+", required=True, help="action to be executed", choices=('allocateSubnet', 'allocateSubnetWithWeight'))
    parser.add_argument('-f', '--file', required=True, type=str, help='input file')

    args = parser.parse_args()
    main(args)
