### mongo
mongo directory contains script releted to mongo database.

mongoBackup.py : Mongodb Backup script, Takes <DATABASE_NAME>, <S3_BUCKET_NAME> as user input & triggers mongoexport against provided DATABASE.

```bash
# Trigger Backup ( i.e. <mongoBackup.py> <DATABASE_NAME> <S3_BUCKET_NAME> )
python mongoBackup.py test cassandra-backup-dir
```


mongoRestoreScript.py : Mongodb Restore script, Takes <DATABASE_NAME>, <RESTORE_POINT>, <S3_BUCKET_NAME>, <restoreDatabaseWithCleanUP/restoreDatabaseWithOutCleanUP> as user input & triggers mongoimport against provided DATABASE.

```bash
# Trigger Restore ( i.e. <mongoRestoreScript.py> <DATABASE_NAME> <RESTORE_POINT> <S3_BUCKET_NAME> <restoreDatabaseWithCleanUP/restoreDatabaseWithOutCleanUP> )
python mongoRestoreScript.py test 20150916135055 cassandra-backup-dir restoreDatabaseWithCleanUP

python mongoRestoreScript.py test 20150916135055 cassandra-backup-dir restoreDatabaseWithOutCleanUP

```

[mongoBackup.py]:https://github.com/OpsTree/Scripts/mongo/mongoBackup.py
[mongoRestoreScript.py]:https://github.com/OpsTree/Scripts/mongo/mongoRestoreScript.py
