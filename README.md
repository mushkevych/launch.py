launch.py
=========

Python scripts to setup your virtual env + few convenient tools like configuration management, test runner, code analyzer

## description: ##

launch.py is almost a framework... tiny, convenient and very useful  
it features:
* daemonizer - all you need to run your code as a daemon is the full path of the starter method/function (such as workers.example_script_worker.main)
* django-style configuration management tool - settings.py
* single interface to install, run, test and analyze the project codebase
* "ironclad" support of virtual environment 
* roto logging, pid file tracking
* few other convenient tools

## usage: ##

* install virtual environment:  
./launch.py -i
* run test:   
./launch.py -t
* run PyLint:   
./launch.py -z
* start separate Python process by running either script's or class' starter method/function:  
./launch.py --run --app APPLICATION_NAME
* run the starter script/method within the same process, so you can see the output in the terminal:  
./launch.py --run --app APPLICATION_NAME --interactive

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

## how-to: ##

Script launcher: https://github.com/mushkevych/launch.py/wiki/launcher.script  

Class launcher: https://github.com/mushkevych/launch.py/wiki/launcher.class  

Logger: https://github.com/mushkevych/launch.py/wiki/logger  

Configuration: https://github.com/mushkevych/launch.py/wiki/settings.py

PyLint Integration: https://github.com/mushkevych/launch.py/wiki/PyLint-integration

Unit Test Integration: https://github.com/mushkevych/launch.py/wiki/UnitTest-Integration

Jenkins Integration: https://github.com/mushkevych/launch.py/wiki/Jenkins-Integration


