import sys
import datetime
import os
from pymongo import MongoClient
import logging
import tarfile

def createCompleteDatabaseBackup(database, backupTime, getInternalIP):
    databaseBackupLocation = "/tmp/mongodump-"+backupTime
    databaseBackupCommand = "mongodump --host "+getInternalIP+" --db "+database+" --out "+databaseBackupLocation
    logging.debug("Creating Mongodb Complete Backup on "+ databaseBackupLocation)
    os.system(databaseBackupCommand)
    return databaseBackupLocation
  
def createCollectionBackup(database, collectionName, backupTime, getInternalIP):
    databaseName = database
    databaseBackupLocation = "/tmp/mongodump-"+backupTime
    commandToGetCollectionWiseBackup = "mongodump --host "+getInternalIP+" --db "+databaseName+" --collection "+collectionName+" --out "+databaseBackupLocation
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

def uploadMongoBackupToS3(s3bucketName, nodeName, compressedFile, backupType):
    s3SyncDir = getNodeBackupS3Path(s3bucketName, nodeName)
    s3SyncCommand = "aws s3 cp "+compressedFile+ " "+s3SyncDir+"/"+backupType+"/" +compressedFile
    logging.debug("Uploading Mongodb Backup : <Local-2-S3>")
    logging.debug(s3SyncCommand)
    os.system(s3SyncCommand)

def validateDatabase(database, getInternalIP):
    client = MongoClient(getInternalIP)
    databases = client.database_names()
    if database in databases:
        return True
    else:
        logging.exception("Provided Database "+ database+ " Not exists...")
        print "Please Provide a Valid Database Name"
        return False

def validateDatabaseCollectionName(database, collectionName, getInternalIP):
    client = MongoClient(getInternalIP)
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
    backupType = sys.argv[4]
    backupTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    
    getInternalIPCommand = "ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'"
    getInternalIP = os.popen(getInternalIPCommand).read().strip()
    
    logging.basicConfig(filename='/tmp/mongoBackup.log',level=logging.DEBUG)
    
    if validateDatabase(database, getInternalIP): 
        if backupType == 'database':
            fileLocationForCompression = createCompleteDatabaseBackup(database, backupTime, getInternalIP)
            compressedFile = compressDatabaseBackup(database, backupTime, fileLocationForCompression)
            uploadMongoBackupToS3(s3bucketName, nodeName, compressedFile, backupType)
        else:
            if backupType == 'collection':
                collectionName = sys.argv[5]
                if validateDatabaseCollectionName(database, collectionName, getInternalIP):
                    fileLocationForCompression = createCollectionBackup(database, collectionName, backupTime, getInternalIP)
                    compressedFile = compressDatabaseBackup(database, backupTime, fileLocationForCompression)
                    uploadMongoBackupToS3(s3bucketName, nodeName, compressedFile, backupType)
            else:
                logging.exception("Provided Option to Perform is not Valid, please provide : i.e database|collection")
                print "Please Provide a Valid Option to Perform: i.e database|collection"
                           
main()



