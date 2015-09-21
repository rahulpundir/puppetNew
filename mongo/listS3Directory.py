
import os
import sys

def getS3Path(bucketName, S3SubDirectory):
    s3Path = "s3://"+bucketName+"/" + S3SubDirectory
    return s3Path

def listS3Directory(bucketName, S3SubDirectory, backupType):
    s3Directory = getS3Path(bucketName, S3SubDirectory)
    listCommand = "aws s3 ls "+s3Directory+"/"+backupType+"/"
    print listCommand
    os.system(listCommand)

def main():
    bucketName = sys.argv[1]
    S3SubDirectory = sys.argv[2]
    backupType = sys.argv[3]
    listS3Directory(bucketName, S3SubDirectory, backupType)

main()
