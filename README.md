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
./launch.py -i*
* run test:   
./launch.py -t
* run PyLint:   
./launch.py -l
* start separate Python process by running script's main(*args) function:  
./launch.py --main --app APPLICATION_NAME
* call script's main(*args) function within the same process, so you can see the output in the terminal:  
./launch.py --main --app APPLICATION_NAME --interactive
* start separate Python process by creating an instance of a class and calling its start() method:  
./launch.py --run --app APPLICATION_NAME
* create an instance of a class and call its start() method within the same process, so you can see the output in the terminal:  
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

1. register it in **system.process_context.ProcessContext**:


    'your_script_app_name': _create_context_entry(  
            process_name='your_script_app_name',  
            classname='workers.YOUR_SCRIPT.main',  
            token='your_token',                     # this is used for logging  
            time_qualifier=QUALIFIER_REAL_TIME,     # just use this for now  
            exchange=EXCHANGE_UTILS),               # just use this for now  


2. start it as specified in **usage** section
