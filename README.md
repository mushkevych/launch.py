launch.py
=========

Python scripts to setup your virtual env + few convenient tools like configuration management, test runner, code analyzer

## description: ##

launch.py is almost a framework... tiny, convenient and very useful
it features:
* django-style configuration management tool - settings.py
* single interface to install, run, test and analyze the project codebase
* "ironclad" support of virtual environment 
* roto logging, pid file tracking 
* few other convenient tools

## usage: ##

* install virtual environment:  
*./launch.py -i*
* run test:   
*./launch.py -t
* run PyLint:   
*./launch.py -l
* run Python script with main method:   
*./launch.py --main --app APPLICATION_NAME
* run app as a daemon:   
*./launch.py --run --app APPLICATION_NAME


## license: ##

BSD license. Refer to LICENSE for details.

## metafile: ##

    /launch.py            main executing file  
    /process_starter.py   utility to start worker in daemon mode  
    /settings.py          configuration management  
    /scripts/             folder contains shell scripts  
    /system/              folder contains useful system-level modules  
    /tests/               folder contains unit test  
    /vendors/             folder contains Python libraries required for the project and installed in Python Virtual Environment  
    /worker/              folder of actual project's code  
