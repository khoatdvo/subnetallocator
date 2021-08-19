#!/usr/bin/python3
import unittest
import json
import sys

sys.path.append("..")
from subnetAllocator import SubnetAllocator

class TestSubnetAllocator(unittest.TestCase):
    def readInputFile(self, file):
        with open(file) as input_file:
            input = json.load(input_file)
        return input

    def test_allocatesubnet_normal(self):
        input = self.readInputFile('allocatesubnet_normal.json')
        subnetAllocator = SubnetAllocator(input['subnets'], input['instances'])
        subnetAllocator.allocate()
        result = subnetAllocator.getResult()
        expectedResult = {'subnet-id1': 'instance-id1', 'subnet-id4': 'instance-id4', 'subnet-id2': 'instance-id2', 'subnet-id5': 'instance-id3'}
        self.assertIsNotNone(result)
        self.assertDictEqual(result, expectedResult)

if __name__ == '__main__':
    unittest.main()