import MOKO

MOKO.Program('tree', 'set', f'info =  ')
#Region Настройка параметров
#hesh Ввод параметров
MOKO.Program('tree', 'set', f'select = Ввод параметров')

MOKO.Messenger("set", "Схема измерения.png", "Пожалуйста, соберите схему измерений в соответствии с рисунком!")
# Uin_PS = "11"
# Iin_PS = "3"
# Uout_EL = "5"
# Iout_EL = "2"

# #Uin_PS = MOKO.Messenger("get", "Входное напряжение", "Пожалуйста, введите величину входного напряжения, В", "str")
# MOKO.Report("Uin_PS", "info", "string", "Входное напряжение, В")
# MOKO.Report("Uin_PS", "set", "string", Uin_PS)
#
# #Iin_PS = MOKO.Messenger("get", "Входной ток", "Пожалуйста, введите величину входного тока, А", "str")
# MOKO.Report("Iin_PS", "info", "string", "Входной ток, А")
# MOKO.Report("Iin_PS", "set", "string", Iin_PS)
#
# #Uout_EL = MOKO.Messenger("get", "Выходное напряжение", "Пожалуйста, введите величину выходного напряжения, В", "str")
# MOKO.Report("Uout_EL", "info", "string", "Выходное напряжение, В")
# MOKO.Report("Uout_EL", "set", "string", Uout_EL)
#
# #Iout_EL = MOKO.Messenger("get", "Выходной ток", "Пожалуйста, введите величину выходного тока, А", "str")
# MOKO.Report("Iout_EL", "info", "string", "Выходной ток, А")
# MOKO.Report("Iout_EL", "set", "string", Iout_EL)


MOKO.Program('tree', 'set', 'chosen=passed')

#EndRegion Настройка параметровРегистрация образца


MOKO.EndScript("passed")