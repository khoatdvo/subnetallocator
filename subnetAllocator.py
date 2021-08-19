#!/usr/bin/python3
import argparse
import json
from enum import Enum
import logging
import binpacking

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

    def __rawAZToEnum(self, rawAZ):
        az = rawAZ[-1]
        if az == 'a' or az == 'A':
            return REGION.A
        elif az == 'b' or az == 'B':
            return REGION.B
        else:
            return REGION.C

    def __inputCheck(self):
        result = True
        if len(self.subnets) < len(self.instances):
            message = "Number of subnets is less than number of instances"
            logging.error(message)
            self.__result = message
            result = False
        elif len(self.instances) == 0:
            message = "No instance available, nothing to do"
            logging.error(message)
            self.__result = message
            result = False
        return result

    def getResult(self):
        return self.__result

    def allocateWithWeight(self):
        if not self.__inputCheck():
            return
        reindexSubnetAsAZ = {}
        for key, value in self.subnets.items():
            reindexSubnetAsAZ[key] = value['weight']
        logging.debug('reindexSubnetAsAZ is: {}'.format(reindexSubnetAsAZ))

        bins = binpacking.to_constant_bin_number(reindexSubnetAsAZ,len(self.instances))
        logging.debug('bins is: {}'.format(bins))

        for index, (id, zone) in enumerate(self.instances.items()):
            self.__result.update({
                id: [subnet for subnet in bins[index].keys()]
            })

    def allocate(self):
        if not self.__inputCheck():
            return
        reindexSubnetAsAZ = {}
        reindexInstanceAsAZ = {}
        for az in REGION:
            reindexSubnetAsAZ[az] = []
            reindexInstanceAsAZ[az] = []

        for key, value in self.subnets.items():
            reindexSubnetAsAZ[self.__rawAZToEnum(value['az'])].append(key)

        for key, value in self.instances.items():
            reindexInstanceAsAZ[self.__rawAZToEnum(value)].append(key)

        logging.debug('reindexSubnetAsAZ is: {}'.format(reindexSubnetAsAZ))
        logging.debug('reindexInstanceAsAZ is: {}'.format(reindexInstanceAsAZ))

        leftOverInstances = []
        leftOverSubnets = []
        for az in REGION:
            reindexSubnetAsAZ[az].extend(leftOverSubnets)
            reindexInstanceAsAZ[az].extend(leftOverInstances)
            lenSubnetList = len(reindexSubnetAsAZ[az])
            lenInstanceList = len(reindexInstanceAsAZ[az])
            for index, instance in enumerate(reindexInstanceAsAZ[az]):
                self.__result.update({
                    instance: [reindexSubnetAsAZ[az][index]]
                })
            if lenSubnetList > lenInstanceList:
                leftOverSubnets = reindexSubnetAsAZ[az][lenInstanceList:]
                leftOverInstances = []
            elif lenSubnetList < lenInstanceList:
                leftOverInstances = reindexInstanceAsAZ[az][lenSubnetList:]
                leftOverSubnets = []
            else:
                leftOverInstances = []
                leftOverSubnets = []

        logging.debug("leftOverSubnets is: {}".format(leftOverSubnets))
        for i in range(len(self.__result) % len(leftOverSubnets) + 1):
            for instance, subnetList in self.__result.items():
                if len(leftOverSubnets) > 0:
                    subnetList.append(leftOverSubnets.pop())

def main(args):
    with open(args.file) as inputFile:
        input = json.load(inputFile)
    subnets = input['subnets']
    instances = input['instances']
    if 'allocateSubnet' in args.action:
        subnetAllocator = SubnetAllocator(subnets, instances)
        subnetAllocator.allocate()
        logging.info("allocateSubnet result is: {}".format(subnetAllocator.getResult()))
    if 'allocateSubnetWithWeight' in args.action:
        subnetAllocator = SubnetAllocator(subnets, instances)
        subnetAllocator.allocateWithWeight()
        logging.info("allocateSubnetWithWeight result is: {}".format(subnetAllocator.getResult()))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', nargs="+", required=True, help="action to be executed", choices=('allocateSubnet', 'allocateSubnetWithWeight'))
    parser.add_argument('-f', '--file', required=True, type=str, help='input file')

    args = parser.parse_args()
    main(args)
