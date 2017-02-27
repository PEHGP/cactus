#!/usr/bin/env python

#Copyright (C) 2009-2011 by Benedict Paten (benedictpaten@gmail.com)
#
#Released under the MIT license, see LICENSE.txt
import unittest
import sys
import os
import shutil
import xml.etree.ElementTree as ET

from sonLib.bioio import TestStatus
from sonLib.bioio import system
from sonLib.bioio import getLogLevelString
from sonLib.bioio import getTempDirectory

from cactus.shared.test import getCactusInputs_random
from cactus.shared.test import getCactusInputs_blanchette
from cactus.shared.test import runWorkflow_multipleExamples
from cactus.shared.test import silentOnSuccess

from cactus.shared.common import cactusRootPath
from sonLib.bioio import getTempFile

from cactus.shared.common import cactus_call

from toil.job import Job

class TestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tempDir = getTempDirectory(os.getcwd())

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.tempDir)
        
    @silentOnSuccess
    @unittest.skip("")
    def testCactus_Random_Greedy(self):
        testCactus_Random(self, "greedy")

    @silentOnSuccess
    @unittest.skip("")
    def testCactus_Random_Blossum(self):
        testCactus_Random(self, "blossom5")

    @silentOnSuccess
    @unittest.skip("")
    def testCactus_Random_MaxCardinality(self):
        testCactus_Random(self, "maxCardinality")

    @silentOnSuccess
    @unittest.skip("")
    def testCactus_Random_MaxWeight(self):
        testCactus_Random(self, "maxWeight")

    @silentOnSuccess
    @unittest.skip("")
    def testCactus_Blanchette_Blossum(self):
        testCactus_Blanchette(self, "blossom5")

    @silentOnSuccess
    def testCuTest(self):
        options = Job.Runner.getDefaultOptions(os.path.join(self.tempDir, "tmpToil"))
        Job.Runner.startToil(Job.wrapJobFn(_testCuTestFn), options)

def _testCuTestFn(job):
    cactus_call(job, parameters=["referenceTests", getLogLevelString()])

def testCactus_Blanchette(self, matchingAlgorithm):
    configFile = getConfigFile(matchingAlgorithm)
    runWorkflow_multipleExamples(getCactusInputs_blanchette, 
                                 testRestrictions=(TestStatus.TEST_SHORT,), inverseTestRestrictions=True, 
                                 buildReference=True,
                                 configFile=configFile)
    os.remove(configFile)

def testCactus_Random(self, matchingAlgorithm):
    configFile = getConfigFile(matchingAlgorithm)
    runWorkflow_multipleExamples(getCactusInputs_random, 
                                 testNumber=TestStatus.getTestSetup(), 
                                 buildReference=True,
                                 configFile=configFile)
    os.remove(configFile)
    
def getConfigFile(matchingAlgorithm="greedy"):
    tempConfigFile = getTempFile(rootDir="./", suffix=".xml")
    config = ET.parse(os.path.join(cactusRootPath(), "cactus_config.xml")).getroot()
    #Set the matching algorithm
    config.find("reference").attrib["matching_algorithm"] = matchingAlgorithm
    #Now print the file..
    fileHandle = open(tempConfigFile, 'w')
    ET.ElementTree(config).write(fileHandle)
    fileHandle.close()
    return tempConfigFile

if __name__ == '__main__':
    unittest.main()
