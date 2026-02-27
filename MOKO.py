'''     This library works for connecting user scripts and the program MOKO SE using HTTP requests.

        26.02.2021 The library was renamed to MOKO.py

        Library version: 1.5 dated 06.23.2021. Post requests format was changed for drivers.

        Documentation version: 1.2 - 02.03.2020.

        The version was changed 01.24.2022 for correct working start/pause/stop

        The version was changed 08.22.2022 for updating parsing function and moving repeated code in functions

        The version was changed 09.09.2022. A parameter type was changed to mode (except Stage) in json format.
        That's why all old projects won't work with the new version, there is no backward compatibility.

        Libraries 'requests' and 'json' are needed for working the library.

'''

import time
import requests
import json
import sys

requests = requests.Session()

_UrlStageWrite: str = 'http://localhost:55001/MOKOSE/stage/stagewrite'

_UrlAutoitWrite: str = 'http://localhost:55001/MOKOSE/system/autoitwrite'
_UrlAutoitRead: str = 'http://localhost:55001/MOKOSE/system/autoitread'

_UrlDriverWrite: str = 'http://localhost:55001/MOKOSE/system/driverwrite'
_UrlDriverRead: str = 'http://localhost:55001/MOKOSE/system/driverread'

_UrlPluginWrite: str = 'http://localhost:55001/MOKOSE/system/pluginwrite'
_UrlPluginRead: str = 'http://localhost:55001/MOKOSE/system/pluginread'

_UrlMessengerWrite: str = 'http://localhost:55001/MOKOSE/system/messengerwrite'
_UrlMessengerRead: str = 'http://localhost:55001/MOKOSE/system/messengerread'

_UrlReportWrite: str = 'http://localhost:55001/MOKOSE/system/reportwrite'
_UrlReportRead: str = 'http://localhost:55001/MOKOSE/system/reportread'

_UrlProgramWrite: str = 'http://localhost:55001/MOKOSE/system/programwrite'
_UrlProgramRead: str = 'http://localhost:55001/MOKOSE/system/programread'

_UrlUtilityWrite: str = 'http://localhost:55001/MOKOSE/system/utilitywrite'
_UrlUtilityRead: str = 'http://localhost:55001/MOKOSE/system/utilityread'

_UrlTelegramWrite: str = 'http://localhost:55001/MOKOSE/system/telegramwrite'
_UrlTelegramRead: str = 'http://localhost:55001/MOKOSE/system/telegramread'

_UrlCmdWrite: str = 'http://localhost:55001/MOKOSE/system/cmdwrite'
_UrlCmdRead: str = 'http://localhost:55001/MOKOSE/system/cmdread'

_UrlPortWrite: str = 'http://localhost:55001/MOKOSE/system/portwrite'
_UrlPortRead: str = 'http://localhost:55001/MOKOSE/system/portread'

_UrlProjectStateRead: str = 'http://localhost:55001/MOKOSE/status/projectstate'


###################################################################################################################

    ##          ##          ####        ##########      ##        ##
    ####      ####         ##  ##           ##          ####      ##
    ## ##    ## ##        ##    ##          ##          ## ##     ##
    ##  ##  ##  ##       ##      ##         ##          ##  ##    ##
    ##   ####   ##      ############        ##          ##   ##   ##
    ##    ##    ##      ##        ##        ##          ##    ##  ##
    ##          ##      ##        ##        ##          ##     ## ##
    ##          ##      ##        ##        ##          ##      ####
    ##          ##      ##        ##    ##########      ##       ###

###################################################################################################################

def CMD (mode: str, command: str) -> ...:
    check_project_state()

    URLWrite: str = _UrlCmdWrite
    URLRead: str = _UrlCmdRead

    command_to_send: str = '{"mode":"'+ str(mode)+'", "command":"'+str(command) +'"}'

    send_request(URLWrite, command_to_send)

    cmddata: str = check_status("cmd", mode, URLRead)
    return cmddata

def Port(name: str, mode: str, command: str = '', valuetype: str = 'string') -> ...:

    check_project_state()

    URLWrite: str = _UrlPortWrite
    URLRead: str = _UrlPortRead

    command_to_send: str = '{"name":"' + str(name) + '","mode":"' + str(mode) + '","command":"' + str(command) + '"}'
    send_request(URLWrite, command_to_send)

    portdata: str = check_status("port", mode, URLRead)
    print(f"portdata = {portdata}")
    return portdata



###################################################################################################################

             ##                ##          ##         ###################
           ##  ##              ##          ##                 ##
          ##    ##             ##          ##                 ##
         ##      ##            ##          ##                 ##
        ############           ##          ##                 ##
       ##          ##          ##          ##                 ##
      ##            ##         ##          ##                 ##
     ##              ##        ##############                 ##

###################################################################################################################


def Autoit(title: str, classname: str, method: str, attributes: str = 'void') -> ...:
    """
        This function causes a pop-up message to appear on the screen with an optional data entry field.

        :param str title: title application, choise on autoit
        :param str classname: name class autoit
        :param str method: name method command
        :param str attributes: attributes commands in autoit application
        :return: None if information incorrected, else string information, writing in application, choise on autoit

        **Examples:**

        **1.**
        We need to show an user message. Let's write the next command:

        >>> Autoit('Notepad.txt', 'Edit1', 'ControlGetText', '')

        The next string appears in terminal in case of successfull execution:

        ``b'{"title":"Notepad.txt","classname":"Edit1","method":"ControlGetText","attributes":""}'``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``


    """
    check_project_state()

    URLWrite: str = _UrlAutoitWrite
    URLRead: str = _UrlAutoitRead

    command_to_send: str = '{"title":"'+ str(title)+'", "classname":"'+str(classname) +'","method":"'+str(method) + '","attributes":"'+str(attributes)+'"}'

    send_request(URLWrite, command_to_send)

    autoitdata: str = check_status("autoit", method, URLRead)
    return autoitdata


###################################################################################################################

    ##########      ##################          ####
    ##                      ##                 ##  ##
    ##                      ##                ##    ##
    ##                      ##               ##      ##
    ##########              ##              ############
            ##              ##              ##        ##
            ##              ##              ##        ##
            ##              ##              ##        ##
    ##########              ##              ##        ##

###################################################################################################################


def Stage(stage_string: str, type: str = 'info') -> None:
    """
        This function writes a string in Stage.

        :param str stage_string: a string, writing in Stage.
        :param str type: string type in Stage (**Info**, **Error**, **Plugin**, **Driver**, **Report**, **Warning**). По умолчанию **Info**.
        :return: None

        **Examples:**

        **1.**
        We need to write a string **'Hello, World!'** in Stage. Let's write the next command:

        >>> Stage('Hello, World!')

        The next string appears in terminal in case of successfull execution:

        ``b'{"string": "Hello World!", "type":"info"}'``

        An Info string appears in the program MOKO SE Stage:

        ``Hello World!``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        **2.**
        We need to write an error string **'ERROR! Wrong request type!'** in Stage.

        If we specify the type of output string, the command will look like this:

        >>> Stage('ERROR! Wrong request type!', 'ERROR')

        The next string appears in terminal in case of successfull execution:

        ``b'{"string": "ERROR IN PYTHON LIBRARY! Wrong request type!", "type":"ERROR"}'``

        An error string appears in the program MOKO SE Stage:

        ``ERROR! Wrong request type!``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

    '+str(name)+'
    """
    check_project_state()
    URLWrite: str = _UrlStageWrite
    command_to_send: str = '{"string" :"'+str(stage_string)+'", "type":"'+str(type)+'"}'
    send_request(URLWrite, command_to_send)


###################################################################################################################

    #####           #######         ##########
    ##   ##         ##     ##           ##
    ##     ##       ##      ##          ##
    ##      ##      ##     ##           ##
    ##      ##      #######             ##
    ##      ##      ####                ##
    ##     ##       ## ##               ##
    ##   ##         ##   ##             ##
    #####           ##     ##       ##########

###################################################################################################################


def Driver(name: str, mode: str, command: str = 'void', valuetype: str = 'string') -> ...:
    """
        This function works with drivers.

        :param str name: driver name
        :param str mode: command mode (**'get'**, **'set'**, **'init'**, **'close'**)
        :param str command: executable command
        :param str valuetype: **(only for mode = 'get')** Data type, received from d driver. Default *string*.
        :return: None (if mode = **'set'**) or received data from a driver if mode = **'get'**)

        **Examples:**

        **1.**
        We need to initialize the driver SMBV100A. Let's write the next command:

        >>> Driver('SMBV100A', 'init', '')

        The next string appears in terminal in case of successfull execution:

        ``b'{"name": "SMBV100A", "mode": "init", "command": ""}'``

        The initialize window should appears on a screen (interface choice).

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        **2.**
        We need to reset the instrument SMBV100A. Let's write the next command:

        >>> Driver('SMBV100A', 'set', 'reset')

        The next string appears in terminal in case of successfull execution:

        ``b'{"name": "SMBV100A", "mode": "set", "command": "reset"}'``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        **3.**
        We need to read random value from ExDriver (example driver). Let's write the next command:

        >>> Driver('ExDriver', 'get', 'random', 'float')

        The next string appears in terminal in case of successfull execution:

        ``b'{"name": "Test", "mode": "get", "command": "test"}'``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        If valuetype = 'void' and mode = 'get', the error will appear and will be shown in MOKO SE Stage
    """
    check_project_state()

    URLWrite: str = _UrlDriverWrite
    URLRead: str = _UrlDriverRead

    command_to_send: str = '{"name":"' + str(name) + '","mode":"' + str(mode) + '","command":"' + str(command) + '"}'
    send_request(URLWrite, command_to_send)

    drvdata: str = check_status("driver", mode, URLRead)
    return parse_data(drvdata, mode, valuetype)



###################################################################################################################

    #######         ##                  ##         ##
    ##     ##       ##                  ##         ##
    ##      ##      ##                  ##         ##
    ##     ##       ##                  ##         ##
    #######         ##                  ##         ##
    ##              ##                  ##         ##
    ##              ##                  ##         ##
    ##              ##                  ##         ##
    ##              #############       #############

###################################################################################################################


def Plugin(name: str, mode: str, command: str = 'void', valuetype: str = 'void') -> ...:

    """
        This function works with plugins.

        :param str name: plugin name
        :param str mode: command mode (**'get'**, **'set'**, **'init'**)
        :param str command: executed command
        :param str valuetype: (only for mode = **'get'**) data type receiving from a plugin. Default *void*.
        :return: None (if mode = **'set'**) or received data from a plugin (if mode = **'get'**)

        **Examples:**

        **1.**
        We need to initialize the plugin NMEA0183. Let's write the next command:

        >>> Plugin("NMEA0183", "init", "")

        The next string appears in terminal in case of successfull execution:

        ``b'{"name": "NMEA0183", "mode": "init", "command": ""}'``

        The plugin windowm should appear in a screen

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        **2.**
        We need to reset the plugin NMEA0183 protocols. Let's write the next command:

        >>> Plugin("NMEA0183", "set", "ProtocolReset=True")

        The next string appears in terminal in case of successfull execution:

        ``b'{"name": "NMEA0183", "mode": "set", "command": "ProtocolReset=True"}'``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        **3.**
        We need to read coordinate determination time from the plugin NMEA0183. Let's write the next command:

        >>> Plugin('NMEA0183', 'get','CoordinatesValidTime', 'float')

        The next string appears in terminal in case of successfull execution:

        ``b'{"name": "NMEA0183", "mode": "get", "command": "CoordinatesValidTime"}'``

        The function should return time in seconds:

        ``0 (but it is an error for the plugin NMEA0183 command)``

        or for instance:

        ``17.56``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        If valuetype = 'void' and mode = 'get', the error will appear and will be shown in MOKO SE Stage
    """
    # Проверка состояния проекта: Старт/Стоп/Пауза
    check_project_state()

    URLWrite: str = _UrlPluginWrite
    URLRead: str = _UrlPluginRead

    command_to_send: str = '{"name":"' + str(name) + '","mode":"' + str(mode) + '","command":"' + str(command) + '"}'
    send_request(URLWrite, command_to_send)

    plgdata: str = check_status("plugin", mode, URLRead)
    return parse_data(plgdata, mode, valuetype)


###################################################################################################################

    ##          ##      ############        ##########
    ####      ####      ##                  ##
    ## ##    ## ##      ##                  ##
    ##  ##  ##  ##      ##                  ##
    ##   ####   ##      ########            ##########
    ##    ##    ##      ##                          ##
    ##          ##      ##                          ##
    ##          ##      ##                          ##
    ##          ##      ############        ##########

###################################################################################################################


def Messenger(mode: str, head: str = '', body: str = '', valuetype: str = 'void', delaytime: str = 'void') -> ...:
    """
        This function causes a pop-up message to appear on the screen with an optional data entry field.

        :param str mode: command mode (**'get'**, **'set'**)
        :param str head: message head.
        :param str body: message content.
        :param str valuetype: **(only for mode = 'get')** data type received from a message window. Default *void*.
        :param str delaytime: *(if it is needed)* delay time in seconds.
        :return: None (if mode = **'set'**) or entered data from a message window (if mode = **'get'**)

        **Examples:**

        **1.**
        We need to show an user message. Let's write the next command:

        >>> Messenger('set', 'Info', 'Please connect the device and launch NMEA0183 plugin.')

        The next string appears in terminal in case of successfull execution:

        ``b'{"mode": "set", "head": "Info", "body": "Please connect the device and launch NMEA0183 plugin."}'``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        **2.**
        We need to show a message for user to enter a number. Let's write the next command:

        >>> Messenger('get', 'First number', 'Please, enter the first number', 'int')

        The next string appears in terminal in case of successfull execution:

        ``b'{"mode": "get", "head": "First number", "body": "Please, enter the first number"}'``

        The function should return entered number, for example:

        ``123``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        If valuetype = 'void' and mode = 'get', the error will appear and will be shown in MOKO SE Stage.

        **3.**
        We need to show a message that the script execution is delayed by 15 minutes.

        if we need a delay in a message, it is done like the next example:

        >>> Messenger('set', 'Info', 'Please, wait for 15 minutes', 'void', str(15*60))

        The next string appears in terminal in case of successfull execution:

        ``b'{"mode": "set", "head": "Info", "body": "Please, wait for 15 minutes", "time": "900"}'``


        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

    """
    check_project_state()

    URLWrite: str = _UrlMessengerWrite
    URLRead: str = _UrlMessengerRead

    if (delaytime == 'void'):
        command_to_send: str = '{"mode":"'+str(mode)+'","head":"'+str(head)+'","body":"'+str(body)+'","value":"'+str(valuetype)+'"}'
    else:
        command_to_send: str = '{"mode":"'+str(mode)+'","head":"'+str(head)+'","body":"'+str(body)+'","time":"'+str(delaytime)+'"}'

    send_request(URLWrite, command_to_send)

    msgdata: str = check_status("messenger", mode, URLRead)
    return parse_data(msgdata, mode, valuetype)


###################################################################################################################

    ######          ############        #######
    ##    ##        ##                  ##     ##
    ##     ##       ##                  ##      ##
    ##   ##         ##                  ##     ##
    ## ##           ######              #######
    ####            ##                  ##
    ## ##           ##                  ##
    ##   ##         ##                  ##
    ##     ##       ############        ##

###################################################################################################################


def Report(name: str, mode: str, kind: str = 'string', data: str = '', valuetype: str = 'void') -> ...:
    """
        This function works with data in a report.

        :param str name: report name and bookmark name in a document-template Microsoft Word
        :param str mode: command mode
        :param str kind: type of record in a report (**string**, **table** and **picture**)
        :param str data: data written to the report
        :param str valuetype: (only for mode = 'get') data type received from a report. Default *void*.
        :return: None (if mode = **'set'**) or received data from a report (if mode = **'get'**)

        **Examples:**

        **1.**
        We need to output the string *'FgsFds'* to the report. Let's write the next command:

        >>> Report("rep1",'set', 'string', 'FgsFds')

        The next string appears in case of successfull execution in the terminal:

        ``b'{"name": "rep1", "mode": "set", "kind": "string", "data": "FgsFds"}'``

        The element 'rep1' should appear in the table 'Report names' in the tab 'Report' in the program MOKO SE. By clicking on this element, the *FgsFds* line should appear in the 'Reports' table.

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        **2.**
        We need to output 3 strings in the report table. Let's write the next command:

        >>> Report("rep2",'set', 'table', 'FgsFds, fgsfds, etc')

        The next string appears in case of successfull execution in the terminal:

        ``b'{"name": "rep2", "mode": "set", "kind": "table", "data": "FgsFds, fgsfds, etc"}'``

        The element 'rep2' should appear in the table 'Report names' in the tab 'Report' in the program MOKO SE. By clicking on this element in the 'Reports' table, three columns in one row should be filled with the values 'FgsFds', 'fgsfds' and 'etc' respectively.

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

    """
    check_project_state()

    URLWrite: str = _UrlReportWrite
    URLRead: str = _UrlReportRead

    command_to_send: str = '{"name":"'+str(name)+'","mode":"'+str(mode)+'", "kind":"'+str(kind)+'", "data":"'+str(data)+'"}'
    send_request(URLWrite, command_to_send)

    repdata: str = check_status("report", mode, URLRead)
    return parse_data(repdata, mode, valuetype)


###################################################################################################################

    ##         ##   ##################
    ##         ##           ##
    ##         ##           ##
    ##         ##           ##
    ##         ##           ##
    ##         ##           ##
    ##         ##           ##
    ##         ##           ##
    #############           ##

###################################################################################################################


def Utility(name: str, mode: str, command: str = 'void', valuetype: str = 'void') -> ...:

    """
        This function works with utilities.

        :param str name: utulity name
        :param str mode: command mode (**'get'**, **'set'**)
        :param str command: executable command
        :param str valuetype: (only if mode = **'get'**) data type received from a utility. Default *void*.
        :return: None (if mode = **'set'**) or received data from a utility (if mode = **'get'**)

        **Examples:**

        **1.**
        We need to show an user window in the CSM_GNSS utility. Let's write the next command:

        >>> Utility('CSM_GNSS', 'set', 'info')

        The next string appears in case of successfull execution in the terminal:

        ``b'{"name": "CSM_GNSS", "mode": "set", "command": "info"}'``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        **2.**
        We need to get temperature from the CSM_GNSS utility. Let's write the next command:

        >>> Utility('CSM_GNSS', 'get', 'temperature', 'float')

        The next string appears in case of successfull execution in the terminal:

        ``b'{"name": "CSM_GNSS", "mode": "get", "command": "temperature"}'``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        If valuetype = 'void' and mode = 'get', the error will appear and will be shown in MOKO SE Stage
    """
    check_project_state()

    URLWrite: str = _UrlUtilityWrite
    URLRead: str = _UrlUtilityRead

    command_to_send: str = '{"name" :"' + str(name) + '", "mode":"' + str(mode) + '", "command":"' + str(command) + '"}'
    send_request(URLWrite, command_to_send)

    utldata: str = check_status("utility", mode, URLRead)
    return parse_data(utldata, mode, valuetype)


###################################################################################################################

    #######         ######          #############
    ##     ##       ##    ##        ##         ##
    ##      ##      ##     ##       ##         ##
    ##     ##       ##   ##         ##         ##
    #######         ## ##           ##         ##
    ##              ####            ##         ##
    ##              ## ##           ##         ##
    ##              ##   ##         ##         ##
    ##              ##     ##       #############

###################################################################################################################


def Program(name: str, mode: str, command: str, valuetype: str = 'void') -> ...:
    """
        This function manages the MOKO SE program (scripts, projects, etc.)

        :param str name: type name to be controlled ('script', 'project', etc.)
        :param str mode: command mode (now only **'set'**).
        :param str command: executable command
        :param str valuetype: (only for mode = 'get') type of received data. Default *void*.
        :return: None (if mode = **'set'**) or received data (if mode = **'get'**)

        **Examples:**

        **1.**
        We need to let the server know that the script is over. Let's write the next command:

        >>> Program('script', 'set', 'done')

        The next string appears in case of successfull execution in the terminal:

        b'{"name": "script", "mode": "set", "command": "done"}'

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        If valuetype = 'void' and mode = 'get', the error will appear and will be shown in MOKO SE Stage
    """
    check_project_state()

    URLWrite: str = _UrlProgramWrite
    URLRead: str = _UrlProgramRead

    command_to_send: str = '{"name":"' + str(name) + '","mode":"' + str(mode) + '","command":"' + str(command) + '"}'
    send_request(URLWrite, command_to_send)

    progdata: str = check_status("program", mode, URLRead)
    return parse_data(progdata, mode, valuetype)

def EndScript(command: str = 'done') -> None:
    """
        Required function that must be at the end of every script. Lets the server know that the script is finished.

        :param command: executable command
        :return: None
    """
    Program('script','set',command)
    sys.exit()


###################################################################################################################

    ####################    #############    ##
             ##             ##               ##
             ##             ##               ##
             ##             ##               ##
             ##             ########         ##
             ##             ##               ##
             ##             ##               ##
             ##             ##               ##
             ##             #############    #############

###################################################################################################################


def Telegram(role: str, mode: str, command: str, valuetype: str = 'void') -> ...:
    """
        This function works with Telegram

        :param str role: belonging to the group that messages are sent to (alpha, beta, gamma, delta (developer))
        :param str mode: command mode (**'get'**, **'set'**)
        :param str command: executable command
        :return: None (if mode = **'set'**) of received data from Telegram (if mode = **'get'**)

        **Examples:**

        **1.**
        We need to get a message from Telegram-bot (MOKO SE BOT). Let's write the next command:

        >>> Telegram('alpha', 'set', 'Hello, I\\'m a bot!')

        The next string appears in case of successfull execution in the terminal:

        ``b'{"role": "alpha", "mode": "set", "command": "Hello, I'm a bot!"}'``

        Else if the command isn't executed you will see the next string in a terminal:

        ``b'<!DOCTYPE html><html><head><title>Bad Request</title></head><body><h2>Access Error: 400 -- Bad Request</h2><pre>Bad Request</pre></body></html>'``

        If valuetype = 'void' and mode = 'get', the error will appear and will be shown in MOKO SE Stage
    """
    check_project_state()

    URLWrite: str = _UrlTelegramWrite
    URLRead: str = _UrlTelegramRead

    command_to_send: str = '{"role":"' + str(role) + '","mode":"' + str(mode) + '","command":"' + str(command) + '"}'
    send_request(URLWrite, command_to_send)

    tgmdata: str = check_status("telegram", mode, URLRead)
    return parse_data(tgmdata, mode, valuetype)


###################################################################################################################

    ##        ##    ############    ##              ######
    ##        ##    ##              ##              ##    ##
    ##        ##    ##              ##              ##    ##
    ##        ##    ##              ##              ##  ##
    ############    ######          ##              ####
    ##        ##    ##              ##              ##
    ##        ##    ##              ##              ##
    ##        ##    ##              ##              ##
    ##        ##    ############    #############   ##

###################################################################################################################


def check_project_state() -> None:
    """
        This function checks project state

        :return: None
    """
    URLPSRead: str = _UrlProjectStateRead
    projectstate: str = ''
    while (projectstate.lower() != 'run'):
        serverstate = requests.get(URLPSRead)
        JSONprojectstate = json.loads(serverstate.content)
        projectstate: str = JSONprojectstate.get('projectstate')
        if (projectstate.lower() == 'stop'):
            sys.exit()
        if projectstate.lower() == 'pause':
            time.sleep(0.05)

def check_status(system: str, mode: str, URLRead: str) -> str:
    """
        This function checks MOKO SE status (ready or busy) and status code
        (if data was received bad more than 9 time, the error will appear)

        :param str system: called function (Driver, Program, ...)
        :param str mode: command mode ('get', 'set', 'init', 'close', ...)
        :param str URLRead: URL for getting data from a server
        :return: Data from a server. If badresponse > 9, an empty string wll return
    """
    data: str = ""
    badresponse: int = 0
    status: str = "none"
    while ((status.lower() != 'ready') and (badresponse < 10)):
        response = requests.get(URLRead)
        if (response.status_code != 200):
            Stage("ERROR IN PYTHON LIBRARY! BAD RESPONSE CODE! " + str(response.status_code), 'error')
            print("ERROR IN PYTHON LIBRARY! BAD RESPONSE CODE! " + str(response.status_code) + '\n' +
                  str(10 - badresponse) + ' TRIES LEFT')
            badresponse += 1
        else:
            y = json.loads(response.content)
            status: str = y.get(f'{system}status')
            if (mode.lower() == 'get' or 'check'):
                data: str = y.get(f'{system}data')
        if system in ['messenger', 'driver', 'plugin', 'utility', 'program']:
            time.sleep(0.05)

    if is_bad_response(badresponse): return ""
    return data

def parse_data(data: str, mode: str, valuetype: str = 'void') -> ...:
    """
        This function parses the received ata depending on valuetype.

        :param str data: received data
        :param str mode: command mode ('get', 'set', 'init', 'close', ...)
        :param str valuetype: data type, received from something (only if mode = "get")
        :return: Data of the type specified in valuetype
    """
    if mode.lower() not in ["get", "check", "init"]: return None

    splitter: str = ";"
    if is_semicolon_error(data, splitter, valuetype): return None

    data: str = check_data(data, splitter)

    if valuetype.lower() == 'boolean':
        data: str = data.split(splitter)[0]
        return True if data.lower() == "true" else False
    elif valuetype.lower() == 'float':
        data: str = data.split(splitter)[0]
        return float(data.replace(",", "."))
    elif valuetype.lower() == 'int':
        data: str = data.split(splitter)[0]
        data: str = data.split(".")[0]
        return int(data.split(",")[0])
    elif valuetype.lower() == 'arrayboolean':
        return to_list(bool, data, splitter)
    elif valuetype.lower() == 'arrayfloat':
        return to_list(float, data, splitter)
    elif valuetype.lower() == 'arrayint':
        return to_list(int, data, splitter)
    elif valuetype.lower() == 'arraystring':
        return to_list(str, data, splitter)
    else: # Используется в качестве valuetype = 'string'
        return data.split(splitter)[0]

def check_data(data: str, splitter: str = ";") -> str:
    """
        This function checks received data. If there is the character ';' at the end of the data,
        the character will be deleted

        :param str data: received data
        :param str splitter: character to split
        :return: Checked data
    """
    if data.rfind(splitter) == len(data)-1:
        data: str = data[:-1]
    return data

def to_list(func, data: str, splitter: str = ";") -> ...:
    """
        This function splits entered data creating a list

        :param func: a function that is related to the data (int(), float(), ...)
        :param str data: received data
        :param str splitter: character to split
        :return: A list of values with type specified in func() => (int, float, ...)
    """
    split_data: list = data.split(splitter)
    result: list = []
    for spl in split_data:
        if func is bool:
            result.append(True if spl.lower() == "true" else False)
        elif func is int:
            spl: str = spl.split(".")[0]
            result.append(func(spl.split(",")[0]))
        elif func is float:
            result.append(func(spl.replace(",", ".")))
        else:
            result.append(func(spl))
    return result

def is_semicolon_error(data: str, splitter: str, valuetype: str) -> bool:
    """
        This function checks the presence of two splitter characters at the end of the input.

        :param str data: received data
        :param str splitter: character to split
        :param str valuetype: specified value type
        :return: Will print the error in the console and in the program MOKO SE Stage and return True,
                 if there are 2 characters splitter at the end of the data, else - False
    """
    if data[-2:] == f"{2*splitter}":
        Stage(f'ERROR IN PYTHON LIBRARY!','error')
        Stage(f'INPUT DATA CONTAINS MORE THAN 1 \'\'{splitter}\'\' AT THE END!', 'error')
        Stage(f'DATA: {data}     =>     VALUETYPE: {valuetype.upper()}', 'error')
        print(f'ERROR IN PYTHON LIBRARY!')
        print(f'INPUT DATA CONTAINS MORE THAN 1 \'\'{splitter}\'\' AT THE END!')
        print(f'DATA: {data}     =>     VALUETYPE: {valuetype.upper()}')
        return True
    return False

def is_bad_response(badresponse: int) -> bool:
    """
        This function checks server responses. if data was received bad more than 9 time

        :param int badresponse: the number of bad responses
        :return: Will print the error in the console and in the program MOKO SE Stage and return True,
                 if badresponses more than 9, else - False
    """
    if (badresponse >= 10):
        Stage("ERROR IN PYTHON LIBRARY! FUNCTION EXIT BECAUSE OF BAD RESPONSES", 'error')
        print("ERROR IN PYTHON LIBRARY! FUNCTION EXIT BECAUSE OF BAD RESPONSES")
        return True
    return False



def send_request(URLWrite: str, request: str) -> None:
    """
        This function sends requests to a server

        :param str URLWrite: URL for sending data to a server
        :param request: send request in json format
        :return: None
    """
    headers: dict = {'Content-Type': 'application/json; charset=utf-8'}
    response = requests.post(URLWrite, headers=headers, data=request.encode('utf-8'))
    print(response.content)