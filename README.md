# Setup
* ```cd``` into ```setup``` folder
* Run ```bash install_requirements.sh``` and press [ENTER] to continue

* Execute the following commands:
    1. ```sudo -i -u postgres```
    2. ```createuser <user> -P --interactive```

* Answer "n" to superuser and "y" to other questions
* Create a new database: ```createdb <db_name>```

* Run ```Setup.py <db> (--user=USER) (--passwd=PASSWORD) (--src=IMAGES_FOLDER_PATH) [--host=HOST] [--port=PORT]```

```dataset``` contains sample images you can pass ```--src dataset```
