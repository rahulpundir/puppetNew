import sys
import datetime
import os
from pymongo import MongoClient
import socket

def getCollectionNames(dbName):
    client = MongoClient()
    collectionNames = client[dbName].collection_names()
    return collectionNames

def getCompleteDatabaseBackup(dbName, backupTime):
    databaseName = dbName
    outputDirectory = "/opt/mongodump-"+backupTime
    commandToTakeCompleteDatabaseBackup = "mongodump --db "+databaseName+" --out "+outputDirectory
    os.system(commandToTakeCompleteDatabaseBackup)
    return outputDirectory

def getNodeBackupS3Path(bucketName):
    nodeName = (socket.gethostname())
    nodeS3Path = "s3://"+bucketName+"/"+nodeName
    return nodeS3Path

def uploadMongoCollectionsToS3(dbName, bucketName, backupTime):
    getCompleteDatabaseBackupDirectory = getCompleteDatabaseBackup(dbName, backupTime)
    s3SyncDir = getNodeBackupS3Path(bucketName)
    s3SyncCommand = "aws s3 sync "+getCompleteDatabaseBackupDirectory+ " "+s3SyncDir+ "/mongoBackup/" + backupTime+"/"
    print "Uploading Mongodb Complete Backup : <Local-2-S3>"
    print s3SyncCommand
    os.system(s3SyncCommand)

def validateDatabase(dbName):
    client = MongoClient()
    databases = client.database_names()
    if any(dbName in s for s in databases):
        print "*******************"
    else:
        print "Please Provide a Valid Database Name"

def main():
    dbName = sys.argv[1]
    bucketName = sys.argv[2]
    backupTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    validateDatabase(dbName)
    uploadMongoCollectionsToS3(dbName, bucketName, backupTime)

main()


