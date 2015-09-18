import sys
import datetime
import os
from pymongo import MongoClient
import socket

def getCompleteDatabaseBackup(dbName, backupTime):
    databaseName = dbName
    outputDirectory = "/opt/mongodump-"+backupTime
    commandToTakeCompleteDatabaseBackup = "mongodump --db "+databaseName+" --out "+outputDirectory
    os.system(commandToTakeCompleteDatabaseBackup)
    return outputDirectory

def getCollectionWiseBackup(dbName, collectionName):
    databaseName = dbName
    commandToGetCollectionWiseBackup = "mongodump  --db "+databaseName+" --collection "+collectionName
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
    print "Uploading Mongodb Complete Backup : <Local-2-S3>"
    print s3SyncCommand
    os.system(s3SyncCommand)

def uploadMongoCollectionWiseBackupToS3(dbName, collectionName, bucketName, backupTime):
    getCollectionWiseBackupDirectory = getCollectionWiseBackup(dbName, collectionName)
    s3SyncDir = getNodeBackupS3Path(bucketName)
    s3SyncCommand = "aws s3 sync "+getCollectionWiseBackupDirectory+ " "+s3SyncDir+ "/mongoBackup/" + backupTime+"/"
    os.system(s3SyncCommand)

def validateDatabase(dbName):
    client = MongoClient()
    databases = client.database_names()
    if dbName in databases:
        return True
    else:
        print "Please Provide a Valid Database Name"
        return False

def main():
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
                uploadMongoCollectionWiseBackupToS3(dbName, sys.argv[4], bucketName, backupTime)
        else:
            print "Please Provide a Valid Option to Perform: i.e db|collection"
               
main()



