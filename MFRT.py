import decimal
import math
from decimal import Decimal


def ConvertStringToFloat(value: str):
    """
        This function calls the transfer function from the СI system to the normal system

        :param value: str variable: input variable
        :return: translation value in type float
    """
    if not isinstance(value,  str):
        return float(value)
    library_object = MFRTLibrary(value=value)
    return library_object.get_prefix_in_value()


def ConvertFloatToString(value: (float, str, int), reference_number: str = None, resolution: int = 0,
                         delimiter: str = None, prefix: str = None, round_type: str = "NORMAL", round_number: int = 0,
                         type_value_result: str = "String"):
    """
        This function calls the transfer function from the normal system to the CI system

        :param value: float, string and int variable: translated number
        :param reference_number: string variable: a string number that will be the template to be converted
        :param resolution: integer variable: the number of zeros in the fractional part. Defaults to None
        :param delimiter: string variable: separator between number and fractional part. Defaults to None
        :param prefix: string variable: separator between number and fractional part. Defaults to None
        :param round_type: string variable: rounding method. Defaults to "NORMAL".
            Allowed values:"NORMAL", "UP", "DOWN"
        :param round_number: integer variable: number of decimal places to round off
        :param type_value_result: string variable: type variable input result. Defaults to "String".
            Allowed values:"Float", "String", "Decimal", "Integer"
        :return: translation value for output in definition
    """
    library_object = MFRTLibrary(
        value=value, reference_number=reference_number, resolution=resolution, delimiter=delimiter,
        prefix=prefix, round_type=round_type, round_number=round_number, type_value_result=type_value_result)
    value = library_object.translate_value()
    try:
        match library_object.type_value_result:
            case "String":
                return str(value)
            case "Integer":
                return int(value)
            case "Decimal":
                return Decimal(value)
            case "Float":
                return float(value)
            case _:
                return str(value)
    except ValueError:
        return str(value)


#######################################################################################################################


class MFRTLibrary:
    round_types_list = ["NORMAL", "UP", "DOWN"]
    type_values_allowed_list = ["String", "Float", "Decimal", "Integer"]
    list_prefix_english = ['P', 'T', 'G', 'M', 'k', '-', 'm', 'u', 'n', 'p', 'f']
    list_prefix_russian = ['П', 'Т', 'Г', 'М', 'к', '-', 'м', 'мк', 'н', 'п', 'ф']
    
    def __init__(self, value: (float, str, int), reference_number: str = None, resolution: int = None,
                 delimiter: str = None, prefix: str = None, round_type: str = round_types_list[0],
                 round_number: int = 0, type_value_result: str = type_values_allowed_list[0]):

        self.__value = value
        self.__reference_number = reference_number
        self.__resolution = resolution if resolution > 0 else 0
        self.__delimiter = delimiter
        self.__prefix = prefix
        self.__prefix_value = None
        self.type_value_result = (type_value_result if type_value_result in self.type_values_allowed_list
                                  else self.type_values_allowed_list[0])
        self.__get_prefix, self.__check = False, False
        self.__round_number = round_number
        self.__round_type = round_type if round_type in self.round_types_list else self.round_types_list[0]
        self.__translate_value = self.__reference_number if self.__reference_number else self.__value

    def get_prefix_in_value(self):
        """
            The function of converting a number to normal form and the function of obtaining a prefix

            :return: a float number if the function was called to translate a number, otherwise returns the
            prefix of the number
        """
        if self.__translate_value[-2:] in self.list_prefix_english + self.list_prefix_russian:
            ind = 2
        elif self.__translate_value[-1:] in self.list_prefix_english + self.list_prefix_russian:
            ind = 1
        else:
            ind = 0
        self.__prefix_value = self.__translate_value[-ind:] if ind != 0 else '-'
        self.__get_delimiter_value(ind=ind)
        try:
            self.__translate_value = Decimal(self.__translate_value)
        except decimal.InvalidOperation:
            return self.__value
        if self.__get_prefix:
            self.__get_prefix = False
            return self.__prefix_value
        self.__translate_value = self.__translate_value * self.__create_translation_constant()
        return float(f'{self.__translate_value:.14f}')

    def __create_translation_constant(self):
        """
            The function of obtaining a float value,
            increasing or decreasing the translated number by the number of times

            :return: a float value in which it is worth increasing or decreasing the number for translation
        """
        if self.__prefix_value in self.list_prefix_english and self.__prefix_value != '-':
            list_prefix = self.list_prefix_english
        elif self.__prefix_value in self.list_prefix_russian and self.__prefix_value != '-':
            list_prefix = self.list_prefix_russian
        else:
            return Decimal(1.0)
        index = list_prefix.index(self.__prefix_value)
        len_lst_prefix = len(list_prefix)
        const_resolution = (len_lst_prefix // 2 - index) * 3
        return Decimal(round(10 ** const_resolution, (len(list_prefix) - 1) // 2 * 3))

    def translate_value(self):
        """
            Function to convert from float or int to CI

            :return: translation value for output in definition
        """
        if not self.__reference_number and not self.__resolution and not self.__delimiter and not self.__prefix:
            if isinstance(self.__value, (int | float)):
                self.__value = round(self.__rounded_value(value=Decimal(self.__value)))
            return str(self.__value)
        if isinstance(self.__value, (float, int)):
            if isinstance(self.__value, int):
                self.__value = f'{Decimal(self.__value):.14f}'.split('.')[0]
            else:
                self.__value = Decimal(self.__value)
                if 'e' in str(self.__value) and not self.__resolution and not self.__reference_number:
                    self.__resolution = int(str(self.__value)[-2:])
                elif not self.__resolution and not self.__reference_number:
                    self.__resolution = len(str(self.__value).split('.')[1])
                self.__value = f'{Decimal(self.__value):.14f}'
                self.__value = self.__value.split('.')[0] + '.' + self.__value.split('.')[1]
        elif isinstance(self.__value, str) and not self.__reference_number and not self.__resolution:
            delimiter_value = next((x for x in self.__value[1:] if not x.isdigit() and not x.isalpha()), None)
            if delimiter_value:
                self.__resolution = len(self.__value.split(delimiter_value)[1])
            else:
                self.__resolution = 0
        if not self.__reference_number:
            self.__check = True
            if self.__check_prefix_in_value():
                try:
                    Decimal(self.__value)
                except ValueError:
                    self.__translate_value = self.__value
                    self.__value = self.get_prefix_in_value()
                return self.__check_zeros_after_point_in_string()
            return self.__value
        else:
            if not self.__prefix:
                self.__get_prefix = True
                self.__prefix = self.get_prefix_in_value()
            else:
                self.__check = True
                if not self.__check_prefix_in_value():
                    return self.__value
            if not self.__check_prefix_in_value():
                return self.__value
            return self.__translate_variable_reference_number_and_prefix()

    def __translate_variable_not_reference_number(self):
        """
             Function to convert from value in out format when absent reference_number

             :return: translated number
        """
        if self.__resolution:
            self.__delimiter = next((x for x in self.__value[1: len(self.__value)] if not x.isdigit()), None)
            self.__get_prefix = True
            self.__translate_value = self.__value
            self.__prefix = self.get_prefix_in_value()
            if self.__delimiter:
                self.__value = self.__value.replace(self.__delimiter, '.')
                self.__value = self.__value[:-len(self.__prefix)] if self.__prefix != '-' else self.__value
            self.__value = f'{Decimal(self.__value):.14f}'.split('.')
            return (self.__value[0] + f"{self.__delimiter if self.__delimiter else '.'}" +
                    self.__value[1][:self.__resolution])
        else:
            return self.__rounded_value(self.__value)

    def __translate_variable_reference_number_and_prefix(self):
        """
            Function to convert from value in out format when there is a reference_number

            :return: translated number
        """
        if self.__prefix:
            self.__translate_value = self.__value
            self.__value = self.get_prefix_in_value()
            delimiter_reference_number = next((x for x in self.__reference_number[1: -(len(self.__prefix))]
                                               if not x.isdigit()), None)
            if not self.__delimiter and not delimiter_reference_number:
                return self.__check_zeros_after_point_in_string()
            self.__delimiter = self.__delimiter if self.__delimiter else delimiter_reference_number
            if not self.__resolution:
                if self.__prefix != "-" and delimiter_reference_number:
                    self.__resolution = len(self.__reference_number.split(delimiter_reference_number)[1]) - len(
                        self.__prefix)
                elif delimiter_reference_number:
                    self.__resolution = len(self.__reference_number.split(delimiter_reference_number)[1])
                else:
                    self.__resolution = 0
            return self.__check_zeros_after_point_in_string()
        self.__value = self.__rounded_value(self.__value)
        return self.__translate_variable_not_reference_number()

    def __check_zeros_after_point_in_string(self):
        """
            Converting a number from float to string

            :return: translation value for output in definition
        """
        if self.__prefix:
            self.__prefix_value = self.__prefix
        translation_cost = self.__create_translation_constant()
        translation_value = self.__rounded_value(Decimal(Decimal(self.__value) / Decimal(translation_cost)))
        formatted_translation_value = f'{Decimal(translation_value):.14f}'.split('.')
        if not self.__prefix:
            self.__prefix = ''
        else:
            self.__prefix = '' if self.__prefix in '-' or not self.__prefix_value else self.__prefix
        if not self.__delimiter or not self.__resolution:
            if self.__resolution:
                return (formatted_translation_value[0] + '.' + formatted_translation_value[1][:self.__resolution] +
                        self.__prefix)
            return formatted_translation_value[0] + self.__prefix
        if len(formatted_translation_value[1]) < self.__resolution:
            self.__resolution = len(formatted_translation_value[1])
        return (formatted_translation_value[0] + self.__delimiter + formatted_translation_value[1][:self.__resolution] +
                self.__prefix)

    def __check_prefix_in_value(self):
        if self.__check:
            self.__check = False
            if (self.__prefix not in self.list_prefix_english + self.list_prefix_russian) and self.__prefix:
                return False
            return True
        if self.__prefix in self.list_prefix_english:
            self.__list_prefix = self.list_prefix_english
        else:
            self.__list_prefix = self.list_prefix_russian
        return True

    def __get_delimiter_value(self, ind: int = None):
        delimiter_value = next(
            (x for x in self.__translate_value[1: -(len(self.__prefix_value))] if not x.isdigit()), None)
        self.__translate_value = self.__translate_value[:-ind] if ind != 0 else self.__translate_value
        if delimiter_value:
            self.__translate_value = self.__translate_value.replace(delimiter_value, '.')

    def __rounded_value(self, value: Decimal):
        if self.__round_number:
            if self.__round_type == self.round_types_list[0]:
                value = Decimal(round(value, self.__round_number))
            elif self.__round_type == self.round_types_list[1]:
                value = Decimal(
                    math.ceil(value * 10 ** Decimal(self.__round_number)) / Decimal(10 ** self.__round_number))
            elif self.__round_type == self.round_types_list[2]:
                value = Decimal(
                    math.floor(value * 10 ** Decimal(self.__round_number)) / Decimal(10 ** self.__round_number))
        else:
            if self.__round_type == self.round_types_list[1]:
                value = Decimal(math.ceil(value))
            elif self.__round_type == self.round_types_list[2]:
                value = Decimal(math.floor(value))
        return value
