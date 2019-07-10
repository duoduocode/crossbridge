import openpyxl

from tc_convert.file_reader import get_tc_info_dict, get_tc_step_data_dict, get_ts_dict
from tc_convert.xml_writer import write_xml


def convert():
    ts_dict_total = {}

    wb = openpyxl.load_workbook('/home/xdtu/code/crossbridge/tc_format.xlsx')
    sheets = wb.get_sheet_names()

    for modulename in sheets:
        ws = wb.get_sheet_by_name(modulename)

        # 获取测试用例基本信息
        tc_info_dict = get_tc_info_dict(ws)
        print(tc_info_dict)

        # 获取测试用例步骤信息
        tc_step_data_dict = get_tc_step_data_dict(ws)
        print(tc_step_data_dict)

        ts_dict = {modulename:get_ts_dict(tc_step_data_dict, tc_info_dict)}

        ts_dict_total = dict(ts_dict_total, **ts_dict)

    # 写入xml
    write_xml(ts_dict_total, 'tc_format')


if __name__ == "__main__":
    convert()
