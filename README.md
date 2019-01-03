# Setup

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a9070bd712544239ac5b43f3f5e58ba9)](https://app.codacy.com/app/astrohr/void?utm_source=github.com&utm_medium=referral&utm_content=astrohr/void&utm_campaign=Badge_Grade_Dashboard)

* ```cd``` into ```setup``` folder
* Run ```bash install_requirements.sh``` and press [ENTER] to continue

* Execute the following commands:
    1. ```sudo -i -u postgres```
    2. ```createuser <user> -P --interactive```

* Answer "n" to superuser and "y" to other questions
* Create a new database: ```createdb <db_name>```

* Run ```Setup.py <db> (--user=USER) (--passwd=PASSWORD) (--src=IMAGES_FOLDER_PATH) [--host=HOST] [--port=PORT]```

* ```dataset``` folder contains sample images and can used for testing: ```--src dataset```
