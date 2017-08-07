#!/usr/bin/python

import pickle
import sys

# Use this this to add convert new dictionaries(line delimited words) into pickle files
# Ex: python picklelize.py dict/Path output/path


class Picklelize:
    def __init__(self, path):
        self.path = path
        self.dict = dict()

    def load_dict(self):
        with open(self.path, 'r') as inFile:
            for line in inFile:
                if ''.join(sorted(line.rstrip('\n'))) not in self.dict:
                    self.dict[''.join(sorted(line.rstrip('\n')))] = [line.rstrip('\n')]
                else:
                    self.dict[''.join(sorted(line.rstrip('\n')))].append(line.rstrip('\n'))

    def dumpDict(self, pathName):
        pickle.dump(self.dict, pathName)

if __name__ == '__main__':
    pickleDict = Picklelize(sys.argv[1])
    pickleDict.load_dict()
    with open(sys.argv[2], 'wb') as outFile:
        pickleDict.dumpDict(outFile)
