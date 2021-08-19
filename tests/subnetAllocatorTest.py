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
        input = self.readInputFile('test_normal.json')
        subnetAllocator = SubnetAllocator(input['subnets'], input['instances'])
        subnetAllocator.allocate()
        result = subnetAllocator.getResult()
        expectedResult = ['subnet-id1', 'subnet-id6']
        self.assertIsNotNone(result)
        self.assertListEqual(result['instance-id1'], expectedResult)

        subnetAllocator.allocateWithWeight()
        result = subnetAllocator.getResult()
        print(result)
        expectedResult = {'instance-id1': ['subnet-id4'], 'instance-id2': ['subnet-id2'], 'instance-id3': ['subnet-id3', 'subnet-id6'], 'instance-id4': ['subnet-id1', 'subnet-id5']}
        self.assertIsNotNone(result)
        self.assertDictEqual(result, expectedResult)

    def test_allocatesubnet_nosubnet(self):
        input = self.readInputFile('test_nosubnet.json')
        subnetAllocator = SubnetAllocator(input['subnets'], input['instances'])
        subnetAllocator.allocate()
        result = subnetAllocator.getResult()
        expectedResult = "Number of subnets is less than number of instances"
        self.assertIsNotNone(result)
        self.assertEqual(result, expectedResult)

    def test_allocatesubnet_noinstance(self):
        input = self.readInputFile('test_noinstance.json')
        subnetAllocator = SubnetAllocator(input['subnets'], input['instances'])
        subnetAllocator.allocate()
        result = subnetAllocator.getResult()
        expectedResult = "No instance available, nothing to do"
        self.assertIsNotNone(result)
        self.assertEqual(result, expectedResult)

if __name__ == '__main__':
    unittest.main()