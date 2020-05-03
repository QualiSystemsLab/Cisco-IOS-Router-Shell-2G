### Shell Extension Demo
- forked from:
    - https://github.com/QualiSystems/Cisco-IOS-Router-Shell-2G

- This is a demo to show how to extend the load firmware command default file system option.
- Steps:
    - checkout branch of relevant tagged release, in this example 2.0.1 
    - create "custom_load_firmware_runner.py" file to override default ciscofirmware runner
    - See this file for example of inheriting and over-riding the base class implementations
    - replace the import in driver.py for FirmwareRunner from CiscoFirmwareRunner to custom implementation. The same alias can be kept
    - add file_system param to load_firmware command in driver.py
     - pass the parameter into CustomFirmwareRunner class
    - add param definition in drivermetada.xml
   

# Cisco-IOS-Router-Shell
[![Build status](https://travis-ci.org/QualiSystems/Cisco-IOS-Router-Shell-2G.svg?branch=dev)](https://travis-ci.org/QualiSystems/Cisco-IOS-Router-Shell-2G)
[![Coverage Status](https://coveralls.io/repos/github/QualiSystems/Cisco-IOS-Router-Shell-2G/badge.svg)](https://coveralls.io/github/QualiSystems/Cisco-IOS-Router-Shell-2G)
[![Dependency Status](https://dependencyci.com/github/QualiSystems/Cisco-IOS-Router-Shell-2G/badge)](https://dependencyci.com/github/QualiSystems/Cisco-IOS-Router-Shell-2G)
[![Stories in Ready](https://badge.waffle.io/QualiSystems/Cisco-IOS-Router-Shell-2G.svg?label=ready&title=Ready)](http://waffle.io/QualiSystems/Cisco-IOS-Router-Shell-2G)

<p align="center">
<img src="https://github.com/QualiSystems/devguide_source/raw/master/logo.png"></img>
</p>

# Cisco IOS Router Shell Gen 2
This Shell supports all Cisco IOS Routers.

A CloudShell Shell implements integration of a device model, application or other technology with CloudShell. A Shell consists of a data-model that defines how the device and its properties are modeled in CloudShell along with an automation that enables interaction with the device via CloudShell.

This Shell provides you with connectivity and management capabilities such as save and restore configurations, structure autoload functionality, upgrading firmware etc.
