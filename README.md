# void - Visnjan Observatory Image Database

![v0.0.1](https://img.shields.io/badge/version-0.0.1-blue.svg)
[![CircleCI](https://circleci.com/gh/astrohr/void.svg?style=shield)](https://circleci.com/gh/astrohr/void)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8a3cfe48e7104832bb5170751f720718)](https://www.codacy.com/app/astrohr/void?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=astrohr/void&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/astrohr/void/branch/master/graph/badge.svg)](https://codecov.io/gh/astrohr/void)


## Setup

### PostgreSQL

#### Ubuntu / Debian

  * `cd` into `setup` folder
  * Run `bash install_requirements.sh` and press [ENTER] to continue
  * Execute the following commands:
      1. `sudo -i -u postgres`
      2. `createuser <user> -P --interactive`
  * Answer "n" to superuser and "y" to other questions
  * Create a new database: `createdb <db_name>`
  * Run `Setup.py <db> (--user=USER) (--passwd=PASSWORD) (--src=IMAGES_FOLDER_PATH) [--host=HOST] [--port=PORT]`
  * `dataset` folder contains sample images and can used for testing: `--src dataset`

#### Mac

Using Homebrew for simplicity, not required.

1. Install [Homebrew](https://brew.sh/)
2. Install PostgreSQL
   ```bash
   brew install postgres
   ```
   * or `brew upgrade postgres` if already installed
3. Permission for for OS X Mojave:
   ```bash
   sudo mkdir /usr/local/Frameworks
   sudo chown $(whoami):admin /usr/local/Frameworks 
   ```
3. Install PostGIS
   ```bash
   brew install postgis
   ```
4. Start the service:
   ```bash
   brew services start postgresql
   ```

### void package

#### virtual environment

It is a bad idea to use global Python installation. Here we are making a 
virtual environment using [pyenv](https://github.com/pyenv/pyenv), but any 
similar solution will work. 

```bash
brew install pyenv
pyenv install 3.7.1
pyenv virtualenv 3.7.1 void
cd somewhere
mkdir void_project
cd void_project
pyenv local void
```

### source code

If you just wish to use void, download and install the release package:
```bash
curl -OL https://github.com/astrohr/void/archive/0.0.1.tar.gz
tar -xvzf 0.0.1.tgz
cd void-0.0.1
pip install .
```

For development, checkout the repo instead:

```bash
git clone git@github.com:frnhr/void.git .
pip install -e .[dev]
```

### Testing

Two ways to run tests manually:
 * run tests as a python module: `python -m void.tests` 
 * run directly: `void/tests/__main__.py`

## Usage

...
