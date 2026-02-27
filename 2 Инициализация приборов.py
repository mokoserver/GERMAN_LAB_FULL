import MOKO
import MOSC
import MGPH
import MFRT
import time

# Uin_PS = MOKO.Report("Uin_PS", "get", "string", "", "float")
# Iin_PS = MOKO.Report("Iin_PS", "get", "string", "", "float")
# Uout_EL = MOKO.Report("Uout_EL", "get", "string", "", "float")
# Iout_EL = MOKO.Report("Iout_EL", "get", "string", "", "float")


def InitDevice(name: str):
    MOKO.Driver(name, "init")
    # time.sleep(3)
    # MOKO.Driver(name, "Check")

    MOKO.Program('tree', 'set', 'chosen=passed')

#Region Инициализация
#description: Измеряемый \nпараметр;Диапазон \nизмерений; ID прибора; Примечания
#InitDevice("MaynuoM9714")         hesh Инициализация MaynuoM9714 (электронная нагрузка)
#InitDevice("Keysight66332A")      hesh Инициализация Keysight66332A (блок питания)

MOKO.Program('tree', 'set', f'select = Инициализация DMM6500_04582450')
InitDevice("DMM6500_04582450")    #hesh Инициализация DMM6500_04582450: Uout; 0 - 700 VAC; ...450

MOKO.Program('tree', 'set', f'select = Инициализация DMM6500_04625545')
InitDevice("DMM6500_04625545")    #hesh Инициализация DMM6500_04625545: Iout; 0 - 10 IAC; ...545

MOKO.Program('tree', 'set', f'select = Инициализация HP34401A')
InitDevice("HP34401A_GERMAN")     #hesh Инициализация HP34401A: Uin; 0 - 1000 VDC; ...910

MOKO.Program('tree', 'set', f'select = Инициализация HDM3065B')
InitDevice("HDM3065B_GERMAN")     #hesh Инициализация HDM3065B: Uin; 0 - 75 mVDC; ...612;Измерение на \nшунте путем\nрассчетов\n

#EndRegion Инициализация





#Region Настройка параметров
#description: Уст. \nпараметр;Диапазон \nустановки; ID прибора; Примечания
# hesh Настройка MaynuoM9714
# MOKO.Program('tree', 'set', f'select = Настройка MaynuoM9714')
# time.sleep(3)
# MOKO.Driver('MaynuoM9714', 'set', f'V = {Uout_EL}')
# time.sleep(3)
# MOKO.Driver('MaynuoM9714', 'set', f'I = {Iout_EL}')
# time.sleep(3)
# MOKO.Program('tree', 'set', 'chosen=passed')
# ###################################################################################
#
# hesh Настройка Keysight66332A
# MOKO.Program('tree', 'set', f'select = Настройка Keysight66332A')
#
# MOKO.Driver('Keysight66332A', 'set', 'OUTPUT = OFF')
# time.sleep(3)
# MOKO.Driver('Keysight66332A', 'set', f'VDC = {Uin_PS}')
# time.sleep(3)
# MOKO.Driver('Keysight66332A', 'set', f'IDC = {Iin_PS}')
# time.sleep(3)
# MOKO.Program('tree', 'set', 'chosen=passed')
# ###################################################################################

#hesh Настройка DMM6500_04582450: Function = VAC; 0 - 700 VAC; ...450

MOKO.Program('tree', 'set', f'select = Настройка DMM6500_04582450')

MOKO.Driver('DMM6500_04582450', 'set', 'Function = VAC')
time.sleep(3)
MOKO.Driver('DMM6500_04582450', 'set', 'Range = Auto')
time.sleep(3)

MOKO.Program('tree', 'set', 'chosen=passed')
###################################################################################

#hesh Настройка DMM6500_04625545: Function = IAC; 0 - 10 IAC; ...545

MOKO.Program('tree', 'set', f'select = Настройка DMM6500_04625545')

MOKO.Driver('DMM6500_04625545', 'set', 'Function = IAC')
time.sleep(3)
MOKO.Driver('DMM6500_04625545', 'set', 'Range = Auto')
time.sleep(3)

MOKO.Program('tree', 'set', 'chosen=passed')
###################################################################################

#hesh Настройка HP34401A: Function = VDC; 0 - 1000 VDC; ...910

MOKO.Program('tree', 'set', f'select = Настройка HP34401A')

MOKO.Driver('HP34401A_GERMAN', 'set', 'Function = VDC')
time.sleep(3)
MOKO.Driver('HP34401A_GERMAN', 'set', 'Range = Auto')
time.sleep(3)

MOKO.Program('tree', 'set', 'chosen=passed')
###################################################################################

#hesh Настройка HDM3065B: Function = VDC; 0 - 75 mVDC; ...612;Измерение на \nшунте путем\nрассчетов

MOKO.Program('tree', 'set', f'select = Настройка HDM3065B')

MOKO.Driver('HDM3065B_GERMAN', 'set', 'Function = VDC')
time.sleep(3)
MOKO.Driver('HDM3065B_GERMAN', 'set', 'scpi = SENS:VOLT:DC:RANG 0.1')

MOKO.Program('tree', 'set', 'chosen=passed')
###################################################################################

#EndRegion Настройка параметров

MOKO.EndScript('passed')