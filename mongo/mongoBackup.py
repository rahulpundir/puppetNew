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
  
def createCollectionBackup(database, collectionName, backupTime):
    databaseName = database
    databaseBackupLocation = "/opt/mongodump-"+backupTime
    commandToGetCollectionWiseBackup = "mongodump  --db "+databaseName+" --collection "+collectionName+" --out "+databaseBackupLocation
    logging.debug("Creating Mongodb Collection Backup ")
    os.system(commandToGetCollectionWiseBackup)
    return databaseBackupLocation

def compressDatabaseBackup(database, backupTime, compressDirectoryLocation):
    compressedFileName = database+"-"+backupTime+".tar.gz"
    tar = tarfile.open(compressedFileName, "w:gz")
    sourceDirecotry = compressDirectoryLocation+"/"+database+"/"
    tar.add(sourceDirecotry, arcname=database)
    tar.close()
    return compressedFileName
    
def getNodeBackupS3Path(s3bucketName, nodeName):
    nodeS3Path = "s3://"+s3bucketName+"/"+nodeName
    return nodeS3Path

def uploadMongoBackupToS3(s3bucketName, nodeName, compressedFile):
    s3SyncDir = getNodeBackupS3Path(s3bucketName, nodeName)
    s3SyncCommand = "aws s3 cp "+compressedFile+ " "+s3SyncDir+"/"+compressedFile
    logging.debug("Uploading Mongodb Backup : <Local-2-S3>")
    logging.debug(s3SyncCommand)
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
            fileLocationForCompression = createCompleteDatabaseBackup(database, backupTime)
            compressedFile = compressDatabaseBackup(database, backupTime, fileLocationForCompression)
            uploadMongoBackupToS3(s3bucketName, nodeName, compressedFile)
        else:
            if chooseCompleteOrCollectionWiseBackupOption == 'collection':
                collectionName = sys.argv[5]
                if validateDatabaseCollectionName(database, collectionName):
                    fileLocationForCompression = createCollectionBackup(database, collectionName, backupTime)
                    compressedFile = compressDatabaseBackup(database, backupTime, fileLocationForCompression)
                    uploadMongoBackupToS3(s3bucketName, nodeName, compressedFile)
            else:
                logging.exception("Provided Option to Perform is not Valid, please provide : i.e database|collection")
                print "Please Provide a Valid Option to Perform: i.e database|collection"
                           
main()



