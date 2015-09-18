import sys
import datetime
import os
from pymongo import MongoClient
import socket
import logging, logging.handlers

logger = null

def getCompleteDatabaseBackup(dbName, backupTime):
    databaseName = dbName
    outputDirectory = "/opt/mongodump-"+backupTime
    commandToTakeCompleteDatabaseBackup = "mongodump --db "+databaseName+" --out "+outputDirectory
    logfun = logging.getLogger("logfun")
    logfun.debug("Creating Mongodb Complete Backup ")
    os.system(commandToTakeCompleteDatabaseBackup)
    return outputDirectory

def getCollectionWiseBackup(dbName, collectionName):
    databaseName = dbName
    commandToGetCollectionWiseBackup = "mongodump  --db "+databaseName+" --collection "+collectionName
    logfun = logging.getLogger("logfun")
    logfun.debug("Creating Mongodb Collection Backup ")
    os.system(commandToGetCollectionWiseBackup)
    outputDirectory = "dump/"
    return outputDirectory
    
def getNodeBackupS3Path(bucketName):
    nodeName = (socket.gethostname())
    nodeS3Path = "s3://"+bucketName+"/"+nodeName
    return nodeS3Path

def uploadMongoCompleteBackupToS3(dbName, bucketName, backupTime):
    getCompleteDatabaseBackupDirectory = getCompleteDatabaseBackup(dbName, backupTime)
    s3SyncDir = getNodeBackupS3Path(bucketName)
    s3SyncCommand = "aws s3 sync "+getCompleteDatabaseBackupDirectory+ " "+s3SyncDir+ "/mongoBackup/" + backupTime+"/"
    logfun = logging.getLogger("logfun")
    logfun.debug("Uploading Mongodb Complete Backup : <Local-2-S3>")
    logfun.debug(s3SyncCommand)
    os.system(s3SyncCommand)

def uploadMongoCollectionWiseBackupToS3(dbName, collectionName, bucketName, backupTime):
    getCollectionWiseBackupDirectory = getCollectionWiseBackup(dbName, collectionName)
    s3SyncDir = getNodeBackupS3Path(bucketName)
    s3SyncCommand = "aws s3 sync "+getCollectionWiseBackupDirectory+ " "+s3SyncDir+ "/mongoBackup/" + backupTime+"/"
    logfun = logging.getLogger("logfun")
    logfun.debug("Uploading Mongodb Collection Backup To S3 Bucket")
    os.system(s3SyncCommand)

def validateDatabase(dbName):
    client = MongoClient()
    databases = client.database_names()
    if dbName in databases:
        return True
    else:
        logfun = logging.getLogger("logfun")
        logfun.exception("Please Provide a Valid Database Name")
        return False

def validateDatabaseCollectionName(dbName, collectionName):
    client = MongoClient()
    collectionNames = client[dbName].collection_names()
    if collectionName in collectionNames:
        return True
    else:
        logfun = logging.getLogger("logfun")
        logfun.exception("Please Provide a Valid Collection Name")
        return False        

def instantiateLogger():
    
    global logger = logging.getLogger("logfun")
    logger.setLevel(logging.DEBUG)

    # This handler writes everything to a file.
    fileHandler = logging.FileHandler("/var/log/mongoBackup.log")
    formatter = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    


def main():
    instantiateLogger()
    dbName = sys.argv[1]
    bucketName = sys.argv[2]
    backupTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    optionToChooseCompleteOrCollectionWiseBackup = sys.argv[3]
    
    if optionToChooseCompleteOrCollectionWiseBackup == 'db':
        if validateDatabase(dbName): 
            uploadMongoCompleteBackupToS3(dbName, bucketName, backupTime)
    else:
        if optionToChooseCompleteOrCollectionWiseBackup == 'collection':
            if validateDatabase(dbName):
                collectionName = sys.argv[4]
                if validateDatabaseCollectionName(dbName, collectionName):
                    uploadMongoCollectionWiseBackupToS3(dbName, collectionName, bucketName, backupTime)
        else:
            logfun = logging.getLogger("logfun")
            logfun.exception("Please Provide a Valid Option to Perform: i.e db|collection")
            
# Make a global logging object.
x = logging.getLogger("logfun")
x.setLevel(logging.DEBUG)
    
# This handler writes everything to a file.
h1 = logging.FileHandler("/var/log/mongoBackup.log")
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h1.setFormatter(f)
h1.setLevel(logging.DEBUG)
x.addHandler(h1)    
               
main()



