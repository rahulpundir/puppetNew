#!/usr/bin/python
import sys
import os
from pymongo import MongoClient
import tarfile
import logging

def getS3Path(bucketName, S3SubDirectory):
    s3Path = "s3://"+bucketName+"/" + S3SubDirectory
    return s3Path


def downloadDumpFileFromS3(bucketName, S3SubDirectory, restoreFileName):
    S3Path = getS3Path(bucketName, S3SubDirectory)
    S3FileLocation = S3Path+ "/"+restoreFileName
    downloadS3File = "aws s3 cp " +S3FileLocation+ " /tmp/" 
    print downloadS3File
    os.system(downloadS3File)
    

def extractDumpFile(database, restoreFileName):
    compressedDumpFileLocation = "/tmp/" + restoreFileName
    sourceFile = tarfile.open(compressedDumpFileLocation)
    sourceFile.extractall()
    sourceFile.close()

def restoreCompleteDumpInMongoDB(databse):
    dumpRestoreCommand = "mongorestore " + databse
    os.system(dumpRestoreCommand)

def dropDatabase(database):
    mongodatabaseInstanceConnection = MongoClient()
    mongodatabaseInstanceConnection.drop_database(database)
    
def validateDatabase(database):
    client = MongoClient()
    databases = client.database_names()
    if database in databases:
        return True
    else:
        logging.exception("Provided Database "+ database+ " Not exists...")
        print "Please Provide a Valid Database Name"
        return False
    
def main():
    database = sys.argv[1]
    restoreFileName = sys.argv[2]
    bucketName = sys.argv[3] 
    S3SubDirectory = sys.argv[4]
    optionToCleanUPCollectionBeforeRestore = sys.argv[5]
    
    if validateDatabase(database):
        if optionToCleanUPCollectionBeforeRestore == 'restoreDatabaseWithCleanUP':
            downloadDumpFileFromS3(bucketName, S3SubDirectory, restoreFileName)
            extractDumpFile(database, restoreFileName)
            dropDatabase(database)
            restoreCompleteDumpInMongoDB(database)
            
        else:
            print "Please Select Database Clean-up before Restore Operation"

main()
