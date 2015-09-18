#!/usr/bin/python
import sys
import socket
import os
from os import listdir
from os.path import isfile, join
from pymongo import MongoClient


def getS3Path(bucketName, filePath):
    s3Path = "s3://"+bucketName+"/" + filePath
    return s3Path


def downloadDumpFileFromS3(bucketName, dumpFile):
    dumpFile = dumpFile + ".gz"
    dumpS3Path = getS3Path(bucketName, dumpFile)
    downloadMongoDumpCommand = "aws s3 cp " +  dumpS3Path + " /tmp/" + dumpFile
    os.system(downloadMongoDumpCommand)
#    print downloadMongoDumpCommand

def extractDumpFile(dumpFile):
    compressedDumpFile = "/tmp/" + dumpFile + ".tar.gz"

    extractCommand = "rm -rf /tmp/mongorestore;mkdir /tmp/mongorestore; tar -xvzf " + compressedDumpFile + " -C /tmp/mongorestore; rm -f " + compressedDumpFile
    os.system(extractCommand)
#    print extractCommand

def restoreDumpInMongoDB(dumpFIle):
    dumpRestoreCommand = "mongorestore /tmp/mongorestore/" + dumpFile
    os.system(dumpRestoreCommand)
#    print dumpRestoreCommand

def cleanDatabaseBeforeImportCollections():
    mongodatabaseInstanceConnection = MongoClient()
    databaseName = dbName
    for collection in getCollectionList():
        collectionName = collection.split('.')[0]
        mongodatabaseInstanceConnection[databaseName].drop_collection(collectionName)   

def validateDatabase():
    client = MongoClient()
    databases = client.database_names()
    if any(dbName in s for s in databases):
        print "*************"
    else:
        print "Please Provide a Valid Database Name"
    
def main():
    if optionToCleanUPCollectionBeforeRestore == 'restoreDatabaseWithCleanUP':
        validateDatabase()
        cleanDatabaseBeforeImportCollections()
        downloadDumpFileFromS3(bucketName, dumpFile)
	extractDumpFile(dumpFile)
        restoreDumpInMongoDB(dumpFile)
   else:
        print "Please Select Database Clean-up before Restore Operation"
        
dbName = sys.argv[1]
restorePoint = sys.argv[2]
bucketName = sys.argv[3] 
optionToCleanUPCollectionBeforeRestore = sys.argv[4]
dumpFile = sys.argv[5]

main()
