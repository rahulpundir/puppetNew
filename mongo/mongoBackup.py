import sys
import datetime
import os
from pymongo import MongoClient
import logging
import tarfile

def createCompleteDatabaseBackup(database, backupTime):
    databaseBackupLocation = "/opt/mongodump-"+backupTime
    databaseBackupCommand = "mongodump --db "+database+" --out "+databaseBackupLocation
    logging.debug("Creating Mongodb Complete Backup on "+ databaseBackupLocation)
    os.system(databaseBackupCommand)
    return databaseBackupLocation
  
def getCollectionWiseBackup(database, collectionName):
    databaseName = database
    commandToGetCollectionWiseBackup = "mongodump  --db "+databaseName+" --collection "+collectionName
    logging.debug("Creating Mongodb Collection Backup ")
    os.system(commandToGetCollectionWiseBackup)
    outputDirectory = "dump"
    return outputDirectory

def compressCreatedCompleteDatabaseBackup(database, backupTime, compressDirectoryLocation):
    compressedFileName = database+"-"+backupTime+".tar.gz"
    tar = tarfile.open(compressedFileName, "w:gz")
    sourceDirecotry = compressDirectoryLocation+"/"+database+"/"
    print sourceDirecotry
    tar.add(sourceDirecotry, arcname=database)
    tar.close()
    return compressedFileName
    
def getNodeBackupS3Path(bucketName, nodeName):
    nodeS3Path = "s3://"+bucketName+"/"+nodeName
    return nodeS3Path

def uploadMongoCompleteBackupToS3(database, bucketName, backupTime, nodeName):
    getCompleteDatabaseBackupDirectory = compressCreatedCompleteDatabaseBackup(database, backupTime, createCompleteDatabaseBackup(database, backupTime))
    s3SyncDir = getNodeBackupS3Path(bucketName, nodeName)
    s3SyncCommand = "aws s3 cp "+getCompleteDatabaseBackupDirectory+ " "+s3SyncDir+"/"+getCompleteDatabaseBackupDirectory
    logging.debug("Uploading Mongodb Complete Backup : <Local-2-S3>")
    logging.debug(s3SyncCommand)
    os.system(s3SyncCommand)

def uploadMongoCollectionWiseBackupToS3(database, collectionName, bucketName, backupTime, nodeName):
    getCollectionWiseBackupDirectory = compressCreatedCompleteDatabaseBackup(database, backupTime, getCollectionWiseBackup(database, collectionName))
    s3SyncDir = getNodeBackupS3Path(bucketName, nodeName)
    s3SyncCommand = "aws s3 cp "+getCollectionWiseBackupDirectory+ " "+s3SyncDir+ "/"+getCollectionWiseBackupDirectory
    logging.debug("Uploading Mongodb Collection Backup To S3 Bucket")
    os.system(s3SyncCommand)

def validateDatabase(database):
    client = MongoClient()
    databases = client.database_names()
    if database in databases:
        return True
    else:
        logging.exception("Provided Database "+ database+ " Not exists...")
        print "Please Provide a Valid Database Name"
        return False

def validateDatabaseCollectionName(database, collectionName):
    client = MongoClient()
    collectionNames = client[database].collection_names()
    if collectionName in collectionNames:
        return True
    else:
        logging.exception("Provided Collection "+ collectionName +" not exists in Database "+database )
        print "Please Provide a Valid Collection Name"
        return False        


def main():
    database = sys.argv[1]
    s3bucketName = sys.argv[2]
    nodeName = sys.argv[3]
    backupTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    chooseCompleteOrCollectionWiseBackupOption = sys.argv[4]
    
    logging.basicConfig(filename='/var/log/mongoBackup.log',level=logging.DEBUG)
    
    if validateDatabase(database): 
        if chooseCompleteOrCollectionWiseBackupOption == 'database':
            uploadMongoCompleteBackupToS3(database, s3bucketName, backupTime, nodeName)
        else:
            if chooseCompleteOrCollectionWiseBackupOption == 'collection':
                collectionName = sys.argv[5]
                if validateDatabaseCollectionName(database, collectionName):
                    uploadMongoCollectionWiseBackupToS3(database, collectionName, s3bucketName, backupTime, nodeName)
            else:
                logging.exception("Provided Option to Perform is not Valid, please provide : i.e database|collection")
                print "Please Provide a Valid Option to Perform: i.e database|collection"
                           
main()



