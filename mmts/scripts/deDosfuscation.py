# -*- coding: utf-8 -*-
# @Time    :   2021/01/08 11:03:35
# @Author  :   ddvv
# @Site    :   https://ddvvmmzz.github.io/
# @File    :   deDosfuscation.py
# @Software:   Visual Studio Code
# @Desc    :   None


import sys
import re

upper_low = ['echo', 'set', 'explorer', 'temp']


def de_dosfuscation_step_one(dosfuscation_str):
    de_dosfuscation_str = dosfuscation_str.replace('^', '')

    return de_dosfuscation_str


def de_dosfuscation_step_two(dosfuscation_str):
    # 查找%
    find_percent = [m.start() for m in re.finditer('%', dosfuscation_str)]
    if not find_percent:
        return dosfuscation_str
    find_percent_1 = find_percent[0::2]
    find_percent_2 = find_percent[1::2]
    # 查找=
    find_equ = [m.start() for m in re.finditer('=', dosfuscation_str)]
    if max(find_equ) < min(find_percent):
        return dosfuscation_str
    
    # 移除=号list两端的%%对
    # to do

    # 查找空值等号,等号后面跟着的第偶数个%
    find_equ.extend(find_percent_2)
    find_equ.sort()
    find_match = [find_equ[i + 1] - find_equ[i] for i in range(0, len(find_equ) - 1)]
    min_value = min(find_match)
    min_index = find_match.index(min_value)
    index = find_equ[min_index]
    percent_2_index = find_equ[min_index + 1]
    for p1 in find_percent_1:
        if index < p1 < percent_2_index:
            return dosfuscation_str
    # 查找变量名
    colon_index = dosfuscation_str[:index].rfind(':')
    if colon_index < 0:
        return dosfuscation_str
    if colon_index < find_equ[min_index - 1]:
        return dosfuscation_str
    var_name = dosfuscation_str[colon_index+1:index]
    # 相同变量名检测
    conflict_var_index = dosfuscation_str[percent_2_index:].find(var_name)
    replace_start_index = colon_index
    offset_dlt = 0
    if conflict_var_index > 0:
        conflict_var_index += percent_2_index
        next_var_index = dosfuscation_str[:conflict_var_index].rfind('%')
        next_var = dosfuscation_str[next_var_index+1:conflict_var_index-1]
        replace_start_index = dosfuscation_str[:replace_start_index].find(next_var)
        offset_dlt = find_equ[min_index+1] - colon_index - 1
        # print('maybe has var conflict')
    replace_str = dosfuscation_str[find_equ[min_index]+1:find_equ[min_index+1]]
    dosfuscation_str = dosfuscation_str[:colon_index+1] + dosfuscation_str[find_equ[min_index+1]:]
    dosfuscation_str = dosfuscation_str[:replace_start_index].replace(var_name, replace_str)+dosfuscation_str[replace_start_index:]
    return de_dosfuscation_step_two(dosfuscation_str)


def de_dosfuscation_step_three(dosfuscation_str):
    find_set = re.search('set (.*?)=(.*?)(&{1,2}|\s&{1,2})', dosfuscation_str, re.IGNORECASE)
    if not find_set:
        return dosfuscation_str
    var_name = find_set.group(1).replace('"', '')
    var_value = find_set.group(2).replace('"', '')
    start_index = find_set.start()
    end_index = find_set.end()
    # dosfuscation_str = dosfuscation_str.replace(find_set.group(), var_value)
    dosfuscation_str = dosfuscation_str[:start_index] + dosfuscation_str[end_index:]
    dosfuscation_str = dosfuscation_str.replace('%%%s:%%' % var_name, var_value)
    dosfuscation_str = dosfuscation_str.replace('%%%s%%' % var_name, var_value)
    dosfuscation_str = dosfuscation_str.replace('!%s!' % var_name, var_value)
    dosfuscation_str = dosfuscation_str.replace(':%s' % var_name, ':%s' % var_value)
    dosfuscation_str = dosfuscation_str.replace('%%%s' % var_name, '%%%s' % var_value)
    return de_dosfuscation_step_three(dosfuscation_str)


def de_dosfuscation_step_four(dosfuscation_str):
    find_set = re.search('%(.*?):~(.*?),(.*?)%', dosfuscation_str, re.IGNORECASE)
    if not find_set:
        return dosfuscation_str
    var_name = find_set.group(1).replace('"', '')
    start_index = int(find_set.group(2), 10)
    len_index = int(find_set.group(3), 10)
    dosfuscation_str = dosfuscation_str.replace(find_set.group(), var_name[start_index: start_index + len_index])
    return de_dosfuscation_step_four(dosfuscation_str)


def de_dosfuscation_step_five(dosfuscation_str):
    for ul in upper_low:
        replace_str_list = re.findall(ul, dosfuscation_str, re.IGNORECASE)
        if replace_str_list:
            for rs in replace_str_list:
                dosfuscation_str = dosfuscation_str.replace(rs, ul)

    return dosfuscation_str


def de_dosfuscation_work(mix_str):
    c = de_dosfuscation_step_one(mix_str)
    c = de_dosfuscation_step_two(c)
    c = de_dosfuscation_step_three(c)
    c = de_dosfuscation_step_four(c)
    c = de_dosfuscation_step_five(c)

    return c


def main():
    if 2 != len(sys.argv):
        print('not found target file.')
        exit(0)
    filename = sys.argv[1]
    print('start process %s file.' % filename)
    new_name = filename + '.clear'
    with open(filename, 'r') as f:
        Dosfuscation_cmds = f.readlines()
    clear_list = []
    for dc in Dosfuscation_cmds:
        dc = dc.strip()
        # 混淆判定逻辑
        if dc.count('^') > 0 or (dc.count('%') > 4 and ' for ' not in dc)or 'set ' in dc:
            clear_str = de_dosfuscation_work(dc)
            clear_list.append(clear_str)
            print('dedosfuscation cmd: {0}'.format(clear_str))
    print('process finished.')
    if len(clear_list) > 0:
        print('clear CMDs save in %s file' % new_name)
        with open(new_name, 'w') as f:
            f.write('\n'.join(clear_list))
    else:
        print('not find Dosfuscation CMD.')


if __name__ == '__main__':
    main()