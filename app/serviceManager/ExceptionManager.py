import traceback


def print_exception_info(info_string, e):
    print(info_string)
    print(str(e))
    print(traceback.format_exc())
    print("END OF ERROR MESSAGE")
