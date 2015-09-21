#!/usr/bin/python
import sys
import os
from pymongo import MongoClient
import tarfile
import logging

def getS3Path(s3Directory):
    s3Path = "s3://"+s3Directory
    return s3Path


def downloadDumpFileFromS3(s3Directory, restoreFileName):
    S3Path = getS3Path(s3Directory)
    S3FileLocation = S3Path+ "/"+restoreFileName
    downloadS3File = "aws s3 cp " +S3FileLocation+ " /tmp/" 
    os.system(downloadS3File)
    

def extractDumpFile(database, restoreFileName):
    compressedDumpFileLocation = "/tmp/" + restoreFileName
    sourceFile = tarfile.open(compressedDumpFileLocation)
    sourceFile.extractall()
    sourceFile.close()

def restoreDumpInMongoDB(database):
    dumpRestoreCommand = "mongorestore " + database
    os.system(dumpRestoreCommand)

def dropDatabase(database):
    mongodatabaseInstanceConnection = MongoClient()
    mongodatabaseInstanceConnection.drop_database(database)
    
def dropCollection(database, collection):
    mongodatabaseInstanceConnection = MongoClient()
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

def restoreMongoDatabase(databaseCleanupOption, s3Directory, restoreFileName, database):
    if databaseCleanupOption == 'withcleanup':
        downloadDumpFileFromS3(s3Directory, restoreFileName)
        extractDumpFile(database, restoreFileName)
        dropDatabase(database)
        restoreDumpInMongoDB(database)
    else:
        if databaseCleanupOption == 'withoutcleanup':
            downloadDumpFileFromS3(s3Directory, restoreFileName)
            extractDumpFile(database, restoreFileName)
            restoreDumpInMongoDB(database)
        else:
            print "Please Select Database Clean-up option before Restore Operation i.e withcleanup|withoutcleanup"     
    
def restoreMongoCollection(collection, databaseCleanupOption, s3Directory, restoreFileName, database):
    if databaseCleanupOption == 'withcleanup':
        downloadDumpFileFromS3(s3Directory, restoreFileName)
        extractDumpFile(database, restoreFileName)
        dropCollection(database, collection)
        restoreDumpInMongoDB(database)
    else:
        if databaseCleanupOption == 'withoutcleanup':
            downloadDumpFileFromS3(s3Directory, restoreFileName)
            extractDumpFile(database, restoreFileName)
            restoreDumpInMongoDB(database)
        else:
            print "Please Select Database Clean-up option before Restore Operation i.e withcleanup|withoutcleanup"
    
    
def main():
    database = sys.argv[1]
    restoreFileName = sys.argv[2]
    s3Directory = sys.argv[3]
    restoreType = sys.argv[4]
    databaseCleanupOption = sys.argv[5]
    
    if validateDatabase(database):
        if restoreType == 'database':
            restoreMongoDatabase(databaseCleanupOption, s3Directory, restoreFileName, database)
        else:
            if restoreType == 'collection':
                collection = sys.argv[6]
                if validateDatabaseCollectionName(database, collection):
                    restoreMongoCollection(collection, databaseCleanupOption, s3Directory, restoreFileName, database) 


main()






