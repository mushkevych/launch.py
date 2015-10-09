launch.py
=========
[![Build Status](https://travis-ci.org/mushkevych/launch.py.svg)](https://travis-ci.org/mushkevych/launch.py)  

Python scripts to setup your virtual env + few convenient tools like configuration management, test runner, code analyzer

## description: ##

launch.py is almost a framework... tiny, convenient and very useful  
it features:

* daemonizer - all you need to run your code as a daemon is the full path of the starter method/function (such as `workers.example_script_worker.main`)
* django-style configuration management tool - settings.py
* single interface to install, run, test and analyze the project codebase
* "ironclad" support for virtual environment
* works with both Python 2.7+ and Python 3.3+
* roto logging, pid file tracking
* few more convenient tools

## usage: ##

* install virtual environment for Python 2.7+:  
`python2 launch.py install` 
* install virtual environment for Python 3.3+:  
`python3 launch.py install` 
* run test:   
`./launch.py test`
* run PyLint:   
`./launch.py test --pylint`
* start separate Python process by running either script's or class' starter method/function:  
`./launch.py start PROCESS_NAME`
* run the starter script/method within the same process, so you can see the output in the terminal:  
`./launch.py start PROCESS_NAME --console`

## license: ##

[Modified BSD License.](http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22Revised_BSD_License.22.2C_.22New_BSD_License.22.2C_or_.22Modified_BSD_License.22.29)  
Refer to LICENSE for details.

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


