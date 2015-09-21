
import os
import sys

def getS3Path(bucketName, S3SubDirectory):
    s3Path = "s3://"+bucketName+"/" + S3SubDirectory
    return s3Path

def listS3Directory(bucketName, S3SubDirectory):
    s3Directory = getS3Path(bucketName, S3SubDirectory)
    listCommand = "aws s3 ls "+s3Directory+"/"
    os.system(listCommand)

def main():
    bucketName = sys.argv[1]
    S3SubDirectory = sys.argv[2]
    listS3Directory(bucketName, S3SubDirectory)

main()
