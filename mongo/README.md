
### mongo

mongo directory contains script releted to mongo database.

[mongoBackup.py] : Mongodb Backup script, Takes <DATABASE_NAME>, <S3_BUCKET_NAME>, <NODE_NAME>, <database|collection> as user input & triggers mongodump against provided DATABASE.

  * DATABASE_NAME: Mongo database name on which dump will trigger.
  * S3_BUCKET_NAME: Amazon S3 Bucket Name i.e cassandra-backup-dir, This is the S3 base directory which holds backup.
  * NODE_NAME: Subdirectory as identifier for backup i.e <HOSTNAME>|<MongoBackupDir>
  * database|collection: Option to choose complate database backup or collection backup i.e database or collection


```bash

# Trigger Complate Backup ( i.e. python mongoBackup.py <DATABASE_NAME> <S3_BUCKET_NAME> <NODE_NAME> database )
python mongoBackup.py test cassandra-backup-dir sandip database

# Trigger Collection Backup ( i.e. python mongoBackup.py <DATABASE_NAME> <S3_BUCKET_NAME> <NODE_NAME> collection <COLLECTION_NAME>)
python mongoBackup.py test cassandra-backup-dir sandip collection testData

```


[mongoRestoreScript.py] : Mongodb Restore script, Takes <DATABASE_NAME>, <RESTORE_POINT>, <S3_BUCKET_NAME>, <restoreDatabaseWithCleanUP/restoreDatabaseWithOutCleanUP> as user input & triggers mongoimport against provided DATABASE.

```bash
# Trigger Restore ( i.e. <mongoRestoreScript.py> <DATABASE_NAME> <RESTORE_POINT> <S3_BUCKET_NAME> <restoreDatabaseWithCleanUP/restoreDatabaseWithOutCleanUP> )
python mongoRestoreScript.py test 20150916135055 cassandra-backup-dir restoreDatabaseWithCleanUP

python mongoRestoreScript.py test 20150916135055 cassandra-backup-dir restoreDatabaseWithOutCleanUP

```




[mongoBackup.py]:https://github.com/OpsTree/Scripts/blob/master/mongo/mongoBackup.py
[mongoRestoreScript.py]:https://github.com/OpsTree/Scripts/blob/master/mongo/mongoRestoreScript.py



