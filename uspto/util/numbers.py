# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@ip-tools.org>

def guess_type_from_number(number):
    length = len(number)

    # 2017/0293197, 2017-0293197, US2017293197A1
    if length >= 11:
        type = 'publication'

    # 15431686
    elif length >= 8 and number.isdigit():
        type = 'application'

    # PP28532, D799980, RE46571, 3525666, 9788906
    else:
        type = 'patent'

    return type


def format_number_for_source(number, document_type):
    # FIXME: Compensate PBD vs. PEDS anomaly re. 2017/0293197 vs. US2017293197A1
    return number

