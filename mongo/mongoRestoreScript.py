#!/usr/bin/python
import sys
import os
from pymongo import MongoClient
import tarfile
import logging

def getS3Path(bucketName, nodeName):
    s3Path = "s3://"+bucketName+"/"+nodeName
    return s3Path


def downloadDumpFileFromS3(bucketName, nodeName, restoreFileName, restoreType):
    S3Path = getS3Path(bucketName, nodeName)
    S3FileLocation = S3Path+ "/"+restoreType+"/"+restoreFileName
    downloadS3File = "aws s3 cp " +S3FileLocation+ " /tmp/"
    logging.debug("Downloading Mongo Backup From "+ S3FileLocation) 
    os.system(downloadS3File)
    

def extractDumpFile(database, restoreFileName):
    compressedDumpFileLocation = "/tmp/" + restoreFileName
    sourceFile = tarfile.open(compressedDumpFileLocation)
    logging.debug("Extracting Backup at " +os.getcwd())
    sourceFile.extractall()
    sourceFile.close()

def restoreDumpInMongoDB(database):
    dumpRestoreCommand = "mongorestore " + database
    logging.debug("Restoring Mongo Backup on Database " +database )
    os.system(dumpRestoreCommand)

def dropDatabase(database):
    mongodatabaseInstanceConnection = MongoClient()
    logging.debug("Droping Mongo Database " +database )
    mongodatabaseInstanceConnection.drop_database(database)
    
def dropCollection(database, collection):
    mongodatabaseInstanceConnection = MongoClient()
    logging.debug("Droping Mongo Collection "+collection+" From Database " +database )
    mongodatabaseInstanceConnection[database].drop_collection(collection)
    
    
def validateDatabase(database):
    client = MongoClient()
    databases = client.database_names()
    if database in databases:
        return True
    else:
        logging.exception("Provided Database "+ database+ " Not exists...")
        print "Please Provide a Valid Database Name"
        return False

def validateDatabaseCollectionName(database, collection):
    client = MongoClient()
    collectionNames = client[database].collection_names()
    if collection in collectionNames:
        return True
    else:
        logging.exception("Provided Collection "+ collection +" not exists in Database "+database )
        print "Please Provide a Valid Collection Name"
        return False

def restoreMongoDatabase(databaseCleanupOption, bucketName, nodeName, restoreFileName, database, restoreType):
    if databaseCleanupOption == 'withcleanup':
        downloadDumpFileFromS3(bucketName, nodeName, restoreFileName, restoreType)
        extractDumpFile(database, restoreFileName)
        dropDatabase(database)
        restoreDumpInMongoDB(database)
    else:
        if databaseCleanupOption == 'withoutcleanup':
            downloadDumpFileFromS3(bucketName, nodeName, restoreFileName, restoreType)
            extractDumpFile(database, restoreFileName)
            restoreDumpInMongoDB(database)
        else:
            print "Please Select Database Clean-up option before Restore Operation i.e withcleanup|withoutcleanup"     
    
def restoreMongoCollection(collection, databaseCleanupOption, bucketName, nodeName, restoreFileName, database, restoreType):
    if databaseCleanupOption == 'withcleanup':
        downloadDumpFileFromS3(bucketName, nodeName, restoreFileName, restoreType)
        extractDumpFile(database, restoreFileName)
        dropCollection(database, collection)
        restoreDumpInMongoDB(database)
    else:
        if databaseCleanupOption == 'withoutcleanup':
            downloadDumpFileFromS3(bucketName, nodeName, restoreFileName, restoreType)
            extractDumpFile(database, restoreFileName)
            restoreDumpInMongoDB(database)
        else:
            print "Please Select Database Clean-up option before Restore Operation i.e withcleanup|withoutcleanup"
    
    
def main():
    database = sys.argv[1]
    restoreFileName = sys.argv[2]
    bucketName = sys.argv[3]
    nodeName = sys.argv[4]
    restoreType = sys.argv[5]
    databaseCleanupOption = sys.argv[6]
    
    logging.basicConfig(filename='/var/log/mongoRestore.log',level=logging.DEBUG)
    
    if validateDatabase(database):
        if restoreType == 'database':
            restoreMongoDatabase(databaseCleanupOption, bucketName, nodeName, restoreFileName, database, restoreType)
        else:
            if restoreType == 'collection':
                collection = sys.argv[7]
                if validateDatabaseCollectionName(database, collection):
                    restoreMongoCollection(collection, databaseCleanupOption, bucketName, nodeName, restoreFileName, database, restoreType) 


main()

