import MOKO

# Library version 2.10.24.1
# Added commands description at 24.10.2022

# **init**
# GraphInit() - this function initializes plugin MOKO Graph
# **set**
# WriteGraph() - this function shows lines in the graph
# WriteGraph() - this function shows lines in the graph
# AddLine() - this function adds a line in the plugin memory
# ChangeLine() - this function changes the line which has already added
# DeleteLine() - this function deletes lines
# HideLine() - this function hides lines
# ShowLine() - this function shows lines
# ShowLineOnly() - this function shows only chosen lines
# AddGraphSett() - this function sets graph settings
# Autoscale() - this function sets autoscale
# ScreenshotWindow() - this function makes a screenshot of the plugin front panel
# ScreenshotGraph() - this function makes a screenshot of the graph front panel
# Legend() - this function hides or shows the graph legend
# ClearGraph() - this function clears the graph
# **get**
# GetScreenshotWindow() - this function makes a screenshot of the plugin front panel and returns it in base64 format
# GetScreenshotGraph() - this function makes a screenshot of the graph front panel and returns it in base64 format


PLUGIN_NAME: str = "Graph"


###########################################################################################

    ################       ####        ##      ################      ##################
           ##              ## ##       ##             ##                     ##
           ##              ##  ##      ##             ##                     ##
           ##              ##   ##     ##             ##                     ##
           ##              ##    ##    ##             ##                     ##
           ##              ##     ##   ##             ##                     ##
           ##              ##      ##  ##             ##                     ##
           ##              ##       ## ##             ##                     ##
    ################       ##        ####      ################              ##

###########################################################################################


def GraphInit() -> None:
    """
        This function initializes plugin MOKO Graph

        :return: None

        >>> GraphInit()
    """
    MOKO.Plugin(PLUGIN_NAME, "init", "")

    # The next code strings was commented because of inoperability
    # server: str = "55001"
    # timeout: float = 10
    # with open('C:/MOKO SE/Settings/PluginsInfo.cnf') as file:
    #     for line in file:
    #         if line.find(PLUGIN_NAME) != -1:
    #             file.readline()
    #             file.readline()
    #             server: str = file.readline()
    #             server: str = server.split('"')[3]
    #             timeout: str = file.readline()
    #             timeout: float = int(timeout.split('"')[3]) / 1000
    #             break
    #
    # url: str = f"http://127.0.0.1:{server}/"
    # start_time = time.time()
    # WAIT_TIME = 10  # seconds
    # while time.time() - start_time < WAIT_TIME:
    #     try:
    #         res = requests.get(url + r'/get', timeout=timeout)
    #         MOKO.Stage(f"The plugin {PLUGIN_NAME} is working now")
    #         print(f"The plugin {PLUGIN_NAME} is working now")
    #         break
    #     except requests.exceptions.ConnectionError:
    #         print(f"The plugin {PLUGIN_NAME} isn't working now")
    # else:
    #     MOKO.Stage(f"The plugin {PLUGIN_NAME} isn't working now", 'error')
    #
    # time.sleep(1)


###########################################################################################

     #########      ###########      ##################
    ##              ##                       ##
    ##              ##                       ##
    ##              ##                       ##
     ########       #########                ##
            ##      ##                       ##
            ##      ##                       ##
            ##      ##                       ##
    #########       ###########              ##

###########################################################################################


def WriteGraph() -> None:
    """
        This function shows lines in the graph

        :return: None

        >>> WriteGraph()
    """
    MOKO.Plugin('Graph', 'set', "Write Graph")

def AddLine(name:str, ArrOy:list, ArrOx:list, LineWidth:str ="3", Color:str ="000000", Visible:str ="True") -> None:
    """
        This function adds a line in the plugin memory

        :param name: name of the line
        :param ArrOy: array of points for axis Oy
        :param ArrOx:  array of points for axis Ox
        :param LineWidth: width of the line
        :param Color: color of the line. Color is transmitted in hexadecimal representation (FFFFFF - white)
        :param Visible: visible of the line: True, False, Yes or No

        :return: None

        >>> AddLine("Sinus", [1,2,3,4], [2,5,7,1], "5", "00FF00", "True")
    """
    MOKO.Plugin('Graph', 'set', f"Add Line={name};{ArrOy};{ArrOx};{LineWidth};{Color};{Visible}")
    MOKO.Plugin('Graph', 'set', "Write Graph")

def ChangeLine(numLine:str, name:str, ArrOy:list, ArrOx:list,LineWidth:str ="3", Color:str ="000000", Visible:str ="True") -> None:
    """
        This function changes the line which has already added

        :param numLine: serial number or name of the line, which an user wants to change. The numbers begin with 0.
                        Also the user can pass the name of the line
        :param name: new name of the line
        :param ArrOy: new array of points for axis Oy
        :param ArrOx:  new array of points for axis Ox
        :param LineWidth: new width of the line
        :param Color: new color of the line. Color is transmitted in hexadecimal representation (FFFFFF - white)
        :param Visible: new parameter of visible of the line: True, False, Yes or No

        :return: None

        >>> ChangeLine("Sinus", "Plot 1",[6,1,4,3], [2,5,7,1], "3", "00FF00", "True")
        >>> ChangeLine(0, "Plot 1",[6,1,4,3], [2,5,7,1], "3", "00FF00", "True")
    """
    MOKO.Plugin('Graph', 'set', f"Change Line={numLine};{name};{ArrOy};{ArrOx};{LineWidth};{Color};{Visible}")

def DeleteLine(numLine:list) -> None:
    """
        This function deletes lines

        :param numLine: serial number or name of the line, which an user wants to delete. The numbers begin with 0.
                        Also the user can pass a list of lines' numbers or names. If the user wants to delete all lines,
                        he can pass "All"

        :return: None

        >>> DeleteLine("All")
        >>> DeleteLine([0,2,1,3])
        >>> DeleteLine(["Plot 1 ", "Plot 2", "Plot 3"])
        >>> DeleteLine(2)
    """
    MOKO.Plugin('Graph', 'set', f"Delete Line={numLine}")

def HideLine(numLine:list) -> None:
    """
        This function hides lines

        :param numLine: serial number or name of the line, which an user wants to hide. The numbers begin with 0.
                        Moreover the user can pass a list of lines' numbers or names. If the user wants to hide all lines,
                        he can pass "All"

        :return: None

        >>> HideLine("All")
        >>> HideLine([0,2,1,3])
        >>> HideLine(["Plot 1 ", "Plot 2", "Plot 3"])
        >>> HideLine(2)
    """
    MOKO.Plugin('Graph', 'set', f"Hide Line={numLine}")

def ShowLine(numLine:list) -> None:
    """
        This function shows lines

        :param numLine: serial number or name of the line, which an user wants to show. The numbers begin with 0.
                        Moreover the user can pass a list of lines' numbers or names. If the user wants to show all lines,
                        he can pass "All"

        :return: None

        >>> ShowLine("All")
        >>> ShowLine([0,2,1,3])
        >>> ShowLine(["Plot 1 ", "Plot 2", "Plot 3"])
        >>> ShowLine(2)
    """
    MOKO.Plugin('Graph', 'set', f"Show Line={numLine}")

def ShowLineOnly(numLine:list) -> None:
    """
        This function shows only chosen lines

        :param numLine: serial number or name of the line, which an user wants to show. The numbers begin with 0.
                        Moreover the user can pass a list of lines' numbers or names. The chosen lines will be shown
                        and the others will be hidden

        :return: None

        >>> ShowOnlyLine([0,2,1,3])
        >>> ShowOnlyLine(["Plot 1 ", "Plot 2", "Plot 3"])
        >>> ShowOnlyLine(2)
    """
    MOKO.Plugin('Graph', 'set', f"Show Line=Only;{numLine}")

def AddGraphSett(Value_OyOx:list, Name_Oy:str, Name_Ox:str, Autoscale:str = "Yes") -> None:
    """
        This function sets graph settings

        :param Value_OyOx: the list of [min,max,min,max] values of axises Oy and Ox respectively
        :param Name_Oy: the name of axis Oy
        :param Name_Ox: the name of axis Ox
        :param Autoscale: the parameter of the graph scaling. It can be:
                          OnlyOy - scaling only axis Oy;
                          OnlyOx - scaling only axis Ox;
                          No - off scaling;
                          Yes - on scaling

        :return: None

        >>> AddGraphSett([0,5,-10,10], "Амплитуда", "Частота, Гц", "No")
    """
    MOKO.Plugin('Graph', 'set', f"Add Graph Settings={Value_OyOx};{Name_Oy};{Name_Ox};{Autoscale}")

def Autoscale(mode:str = "Yes") -> None:
    """
        This function sets autoscale

        :param mode: the parameter of the graph scaling. It can be:
                          OnlyOy - scaling only axis Oy;
                          OnlyOx - scaling only axis Ox;
                          No - off scaling;
                          Yes - on scaling

        :return: None

        >>> Autoscale("OnlyOy")
        >>> Autoscale("OnlyOx")
        >>> Autoscale("No")
        >>> Autoscale("Yes")
    """
    MOKO.Plugin('Graph', 'set', f"Autoscale={mode}")

def ScreenshotWindow() -> None:
    """
        This function makes a screenshot of the plugin front panel. The screenshot is saved
        in "C:/MOKO SE/Plugins/MOKO Graph/screenshots/"

        :return: None

        >>> ScreenshotWindow()
    """
    MOKO.Plugin('Graph', 'set', f"Screenshot Window")

def ScreenshotGraph() -> None:
    """
        This function makes a screenshot of the graph front panel. The screenshot is saved
        in "C:/MOKO SE/Plugins/MOKO Graph/screenshots/"

        :return: None

        >>> ScreenshotGraph()
    """
    MOKO.Plugin('Graph', 'set', f"Screenshot Graph")

def Legend() -> None:
    """
        This function hides or shows the graph legend. If there are no lines in the graph, legend won't be shown

        :return: None

         >>> Legend()
    """
    MOKO.Plugin('Graph', 'set', "Legend")

def ClearGraph() -> None:
    """
        This function clears the graph

        :return: None

        >>> ClearGraph()
    """
    MOKO.Plugin('Graph', 'set', "Clear Graph")


###########################################################################################

     #########      ###########      ##################
    ##              ##                       ##
    ##              ##                       ##
    ##              ##                       ##
    ##    #####     #########                ##
    ##    #  ##     ##                       ##
    ##       ##     ##                       ##
    ##       ##     ##                       ##
     #########      ###########              ##

###########################################################################################


def GetScreenshotWindow() -> str:
    """
        This function makes a screenshot of the plugin front panel and returns it in base64 format. The screenshot is saved
        in "C:/MOKO SE/Plugins/MOKO Graph/screenshots/"

        :return: Returns the screeshot in base64 format

        >>> window_screen = GetScreenshotWindow()
    """
    screen = MOKO.Plugin('Graph', 'get', f"ScreenshotWindow", 'string')
    return screen

def GetScreenshotGraph() -> str:
    """
        This function makes a screenshot of the graph front panel and returns it in base64 format.
        The screenshot is saved in "C:/MOKO SE/Plugins/MOKO Graph/screenshots/"

        :return: Returns the screeshot in base64 format

        >>> graph_screen = GetScreenshotGraph()
    """
    screen = MOKO.Plugin('Graph', 'get', f"ScreenshotGraph", 'string')
    return screen