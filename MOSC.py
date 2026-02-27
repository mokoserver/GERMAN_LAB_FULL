'''
        MOKO Server Control
        This library contains functions for controlling MOKO SE functions, reports and utilities
        Many of these functions are the legacy of MOKO's previous projects
        First version from 26.02.2021
        The library was renamed to MOSC.py 15.03.2021
        The library was changed 09.02.2022

        The library depends on MOKO.py
'''

import MOKO
import os
import sys
from datetime import datetime

#####################################
#                FORMATTING
#####################################

round_3 = '{:.' + str(3) + 'f}'

# %F0%9F%8F%B4%E2%80%8D%E2%98%A0%EF%B8%8F


def script_name() -> str:
    """
        This function returns executable script name

        :return: Executable script name
    """
    scriptname = os.path.basename(sys.argv[0])
    return scriptname

def stars(word: str) -> str:
    """
        This function fills a string with asterisks

        :param word: getting word
        :return: format string with asterisks and the word in the middle of the string (till 15 symbols)
    """
    formated_string = '{:*^15}'.format(word)
    return formated_string

def center_50(message: str) -> str:
    """
        This function fills a string with asterisks

        :param message: getting message
        :return: format string with asterisks and the message in the middle of the string (till 50 symbols)
    """
    return ('{:*^50}'.format(message))

def stage_header(test_name: str, GOST_point: str) -> None:
    """
        This function fills MOKO SE stage fields.

        :param test_name: name of measurements
        :param GOST_point: GOST point
        :return:
    """
    MOKO.Stage(center_50('*'))
    MOKO.Stage(center_50(' Measurements of ' + test_name + ' '))
    MOKO.Stage(center_50(' check point ' + GOST_point + ' '))
    MOKO.Stage(center_50('*'))
    MOKO.Stage(" ")

def format_header(header: str) -> str:
    """
        This function calculate width of a column and returns header string for a table

        :param header: column name
        :return: Header string
    """
    h = header.split('\\n')
    len_max = 0
    for i in h:
        if len(i) > len_max:
            len_max = len(i)
    return header + '#' + str(len_max * 7.5) + ';'

def table_headers(table_data: list, table_headers: list) -> str:
    """
        This function calculate widths of all columns and returns header string for a table

        :param table_data: data from MOKO SE table
        :param table_headers: headers for MOKO SE table
        :return: Header string for all columns
    """
    headers = ""
    for i in range(len(table_data[0].split(","))):
        max_len = len(table_headers[i])
        column = [string.split(",")[i] for string in table_data]
        for cell in column:
            split_cell = cell.split("\n")
            split_cell_lens = [len(item) for item in split_cell]
            if max_len < max(split_cell_lens): max_len = max(split_cell_lens)

        headers += f"{table_headers[i]}#{max_len * 7.5};"
    return headers

################################################
#                SCRIPT CONTROL AND STATE
################################################

def Delay(minutes: int) -> None:
    """
        This function delays script execution time

        :param minutes: minutes
        :return: None
    """
    MOKO.Stage('Delay script execution time for ' + str(minutes) + ' minutes')
    MOKO.Messenger('set', 'Info', "Please, wait for " + str(minutes) + " minutes while taking a measurement", 'void',
                   str(minutes * 60))

def Done() -> None:
    """
        This function makes report name ScriptState with string "Done"

        :return: None
    """
    MOKO.Report('ScriptState', 'set', 'string', 'Done')

def Passed():
    """
        This function makes report name ScriptState with string "Passed"

        :return: None
    """
    MOKO.Report('ScriptState', 'set', 'string', 'Passed')

def Failed():
    """
        This function makes report name ScriptState with string "Failed"

        :return: None
    """
    MOKO.Report('ScriptState', 'set', 'string', 'Failed')

def ScriptState() -> None:
    """
        This function gets string ScriptState from MOKO SE and depending on the content sets script execution result

        :return: None
    """
    state = MOKO.Report('ScriptState', 'get', 'string', 'string', 'string')
    if state == 'Done':
        MOKO.EndScript('done')
    elif state == 'Passed':
        MOKO.EndScript('passed')
    else:
        MOKO.EndScript('failed')

#####################################
#                TREE & HESH
#####################################

def hesh_failed() -> None:
    """
        This function sets a hash to pass with an error

        :return: None
    """
    MOKO.Program('tree', 'set', 'chosen=failed')

def hesh_passed() -> None:
    """
        This function sets a hash to pass without any errors

        :return: None
    """
    MOKO.Program('tree', 'set', 'chosen=passed')

def status_tree(hesh: str) -> bool:
    """
        This function selects tree hesh and checks it content

        :return: True if hesh status not equal 'canceled' else False
    """
    MOKO.Program('tree', 'set', 'select = ' + hesh)
    status = MOKO.Program('tree', 'get', 'hesh ' + hesh, 'string')
    if status != 'canceled':
        return True
    return False

# Обновления 23.11.2022 Johnny Respect


def get_hashes_status(hesh: str) -> str:
    status = MOKO.Program('tree', 'get', 'hesh ' + hesh, 'string')
    return status


def HeshStatus(hesh: str) -> bool:
    """
        This function selects tree hesh and checks it content

        :return: True if hesh status not equal 'canceled' else False
    """
    MOKO.Program('tree', 'set', 'select = ' + hesh)
    status = MOKO.Program('tree', 'get', 'hesh ' + hesh, 'string')
    if status == 'empty':
        return True
    return False


#####################################
#                UTILITY CONTROL
#####################################

def Report_Chek_Forcibly(report_name, utility, report_type='string'):
    NEM = 'And nothing else matters'
    Report = MOKO.Report(report_name, 'get', report_type, report_type, report_type)
    if Report.startswith(NEM):
        Report = MOKO.Utility(utility, 'get', report_name, report_type)
        if Report == '':
            Report = MOKO.Messenger('get', 'Please, enter the value', 'Enter the value of ' + report_name, report_type)
        MOKO.Report(report_name, 'set', report_type, Report)
    MOKO.Utility(utility, 'set', report_name + ' ' + Report)
    return Report


def Report_to_Utility(report_name, utility, report_type='string'):
    ECM = 'Empty case in memory'
    Report = MOKO.Report(report_name, 'get', report_type, report_type, report_type)
    if not Report.startswith(ECM):
        MOKO.Utility(utility, 'set', report_name + ' ' + Report)
    return Report


def Utility_to_Report(report_names: [list, str], utility: str, report_type: str = 'string') -> str:
    """
        This function gets data from utility and sets it in MOKO SE Report

        :param report_names: names for utility commands and reports
        :param utility: utility
        :param report_type: report type

        :return: reports data
    """
    if report_type == 'strings':
        reports_names = ''
        data_reports = ''
        for i in report_names:
            reports_names += i + ';'
            report = MOKO.Utility(utility, 'get', i, 'string')
            data_reports += report + ';'
        MOKO.Report(reports_names, 'set', report_type, data_reports)
    else:
        report = MOKO.Utility(utility, 'get', report_names, 'string')
        MOKO.Report(report_names, 'set', report_type, report)
        return report
    return data_reports


#####################################
#                REPORTS
#####################################

def table_report(report_name: str, result: list) -> None:
    """
        This function getting array of elements and creating tabular report, elements of array set to string

        :param report_name: report name
        :param result: table data

        :return: none
    """
    dataString = str('')
    for i in result:
        element = str(i)
        dataString += (element + ';')
    dataString = dataString[0:-1]
    MOKO.Report(report_name, 'set', 'table', dataString)

#####################################
#       Test iteration structure
#####################################

# Test function should have standard input & output:
# input -- [list of input parameters], HESH
# output -- [list of output parameters, where [0] element is a result of trial 'Good'/'Normal'/'Bad']
def iteration_structure(test_function, iterations = 3): # Decorator of iteration function
    def wrapper(input_paremeters, test_hesh):   # Wrapper of the function
        test_result = 0
        if status_tree(test_hesh):      # Checking up hesh
            test_iterator = 0           # Setting test iteration counter to 0
            while test_iterator < iterations:    # While cycle for trial
                # Here should be actual trial block, but in this example a user will choose trial's result
                test_result = test_function(input_paremeters, test_hesh)
                # This part sets up script's status after trial's result check, but you can use your local variable
                if test_result[0] == 'Good':
                    Done()
                    test_iterator = iterations
                elif test_result[0] == 'Normal':
                    Passed()
                    test_iterator = iterations
                # Here comes the iteration part, if trial's result is unsatisfactory
                elif test_result[0] == 'Bad':
                    Failed()
                    test_iterator += 1  # Incrementing iteration counter
                    if test_iterator == iterations:
                        # Asking the user for reiteration of the trial
                        reiteration = MOKO.Messenger('get', 'Test result is unsatisfactory', 'Would you like to restart?', 'boolean')
                        if reiteration:
                            test_iterator = 0
        return test_result
    return wrapper

def formated_value(value: str, ndigits: int) -> str:
    """
        This function formats input value according to ndigits and returns it

        :param value: input value
        :param ndigits: a number of simbols after comma
        :return: Formated value
    """
    try:
        value_format: float = round(float(value.replace(",", ".")), ndigits)
        value_format: str = str(value_format).replace('.', ',')
        value_ndigits: int = len(value_format.split(',')[-1])
        if value_ndigits < ndigits:
            value_format += (ndigits-value_ndigits)*'0'
    except:
        value_format: str = value
    return value_format


def InitScriptExecutionTime() -> None:
    """
            This function initializes the table with script execution time

            :return: None
        """

    MOKO.Report("ScriptExecutionTime", "info", "table", "Название скрипта#350;"
                                                        "Start time#100;"
                                                        "Stop time#100;"
                                                        "Время исполнения#150")

def ScriptExecutionTime (StartTime: datetime) -> None:
    """
        This function calculates script executable time and reports it

        :param StartTime: start time of a script
        :return: None
    """
    TimeOfCompletion: str = str(datetime.now() - StartTime)     # Время выполнения скрипта
    ScriptName: str = os.path.basename(sys.argv[0])             # Имя скрипта
    report_name: str = ScriptName.split(" ")[0]                 # Example: 6.6.3 ... renamed to 6_6_3_time
    StartTime = str(StartTime)
    StopTime = str(datetime.now())
    RepTimeOfCompletion: str = TimeOfCompletion[:TimeOfCompletion.find(".")]
    RepStartTime: str = StartTime[str(StartTime).find(" "):str(StartTime).find(".")]
    RepStopTime: str = StopTime[str(StopTime).find(" "):str(StopTime).find(".")]

    MOKO.Report("ScriptExecutionTime", "set", "table", str(ScriptName) + ";" +
                                                       RepStartTime + ";" +
                                                       RepStopTime + ";" +
                                                       RepTimeOfCompletion)