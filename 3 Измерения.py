import MOKO
import MOSC
import MGPH
from MFRT import *
import random
from datetime import datetime
import time


#Region Ход измерений
#description: Выходное \nнапряжение;Выходной \nток;Входное \nнапряжение;Входное \nнапряжение\nна шунте\n

duration_sec = 60       # общее время измерений в секундах

start_time = time.time() #  время старта
KPD_sum = 0
# Uin_PS = MOKO.Report("Uin_PS", "get", "string", "", "float")
# Iin_PS = MOKO.Report("Iin_PS", "get", "string", "", "float")
# Uout_EL = MOKO.Report("Uout_EL", "get", "string", "", "float")
# Iout_EL = MOKO.Report("Iout_EL", "get", "string", "", "float")
#MOKO.Report("Results", "clear")
MOKO.Report("Results", "info", "table", "Номер \\nзамера#60;"
                                                             "Системное \\nвремя#120;"
                                                             "Время на \\nизмерения#80;"
                                                             "Входное \\nнапряжение, Вт#90;"
                                                             "Входной \\nток, А#60;"
                                                             "Входная \\nмощность, В#90;"
                                                             "Выходное \\nнапряжение, В#90;"
                                                             "Выходной \\nток, А#70;"
                                                             "Выходная \\nмощность, Вт#90;"
                                                             "КПД, %#70;")

#hesh Измерение: Uout;Iout;Uin;Uin_shunt
#hesh Запись: Uout;Iout;Uin;Uin_shunt

#MOKO.Driver('MaynuoM9714', 'set', 'Input = ON')

MOKO.Driver('Keysight66332A', 'set', 'OUTPUT = ON')

i = 0

while (time.time() - start_time) < duration_sec:
    #######################################################################################################
    ###################################№№№######## ИЗМЕРЕНИЕ ########№№№###################################
    #######################################################################################################
    i += 1
    MOKO.Program('tree', 'set', f'select = Измерение')
    MOKO.Program('tree', 'set', f'info = Номер итерации: {i} Uout = ... В; Iout = ... А; Uin = ... В; Iin = ... А')
    StartTime = 1 #time.time()

    Uout = MOKO.Driver('DMM6500_04582450', 'get', 'READ')
    Uout = ConvertFloatToString(value=Uout, reference_number='0,000', round_number=2)
    Uout = str(Uout).replace(",", ".")
    MOKO.Program('tree', 'set', f'info = Номер итерации: {i} Uout = {Uout} В; Iout = ... А; Uin = ... В; Iin = ... А')

    Iout = MOKO.Driver('DMM6500_04625545', 'get', 'READ')
    Iout = ConvertFloatToString(value=Iout, reference_number='0,000', round_number=2)
    Iout = str(Iout).replace(",", ".")
    MOKO.Program('tree', 'set', f'info = Номер итерации: {i} Uout = {Uout} В; Iout = {Iout} А; Uin = ... В; Iin = ... А')

    Uin = MOKO.Driver('HP34401A_GERMAN', 'get', 'READ')
    Uin = ConvertFloatToString(value=Uin, reference_number='0,000', round_number=2)
    Uin = str(Uin).replace(",", ".")
    MOKO.Program('tree', 'set', f'info = Номер итерации: {i} Uout = {Uout} В; Iout = {Iout} А; Uin = {Uin} В; Iin = ... А')

    Uin_sh = MOKO.Driver('HDM3065B_GERMAN', 'get', 'READ')
    Uin_sh = str(Uin_sh).replace(",", ".")
    Iin = 100 * float(Uin_sh) / 0.075
    Iin = ConvertFloatToString(value=Iin, reference_number='0,000', round_number=2)
    Iin = str(Iin).replace(",", ".")
    MOKO.Program('tree', 'set', f'info = Номер итерации: {i} Uout = {Uout} В; Iout = {Iout} А; Uin = {Uin}  В; Iin = {Iin} А')

    Pin = float(Uin)*float(Iin)
    Pin = (f"{Pin:.3f}")
    Pout = float(Uout)*float(Iout)
    Pout = (f"{Pout:.3f}")

    KPD = 1 #(Pout/Pin) * 100
    KPD_sum += KPD
    KPD = (f"{KPD:.3f}")
    TimeOfCompletion = time.time() - StartTime     # Время выполнения измерения
    TimeOfCompletion = (f"{TimeOfCompletion:.3f}")
    TimeOfCompletion = str(TimeOfCompletion).replace(".", ",")
    Uin = str(Uin).replace(".", ",")
    Iin = str(Iin).replace(".", ",")
    Pin = str(Pin).replace(".", ",")
    Uout = str(Uout).replace(".", ",")
    Iout = str(Iout).replace(".", ",")
    Pout = str(Pout).replace(".", ",")
    KPD = str(KPD).replace(".", ",")

    MOKO.Program('tree', 'set', 'chosen=passed')
    #######################################################################################################
    ########################################### ЗАПИСЬ В РЕПОРТ ###########################################
    #######################################################################################################
    MOKO.Program('tree', 'set', f'select = Запись')
    MOKO.Report("Results", "set", "table", str(i) + ";" +
                                                            str(datetime.now().time()) + ";" +
                                                            str(TimeOfCompletion)[:4] + ";" +
                                                            str(Uin) + ";" +
                                                            str(Iin) + ";" +
                                                            str(Pin) + ";" +
                                                            str(Uout) + ";" +
                                                            str(Iout) + ";" +
                                                            str(Pout) + ";" +
                                                            str(KPD))

    MOKO.Program('tree', 'set', 'chosen=passed')

    #######################################################################################################
    ########################################### ОБНУЛЕНИЕ ХЭШЕЙ ###########################################
    #######################################################################################################

    MOKO.Program('tree', 'set', f'select = Ход измерений')
    MOKO.Program('tree', 'set', 'chosen=empty')
    KPD_AV = KPD_sum / i
    KPD_AV = (f"{KPD_AV:.3f}")
MOKO.Program('tree', 'set', f'select = Измерение')
MOKO.Program('tree', 'set', 'chosen=passed')
MOKO.Program('tree', 'set', f'select = Запись')
MOKO.Program('tree', 'set', 'chosen=passed')
MOKO.Report("KPD_AV", "set", "string", str(KPD_AV + ' %'))
MOKO.Program('tree', 'set', f'info =  ')
#EndRegion Ход измерений


MOKO.EndScript('passed')