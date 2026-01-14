
def parse_data_size(string: str) -> int:
    size, datatype = string.split(" ")

    if datatype == "TB": return float(size) * 1024 * 1024 * 1024 * 1024
    elif datatype == "GB": return float(size) * 1024 * 1024 * 1024
    elif datatype == "MB": return float(size) * 1024 * 1024
    elif datatype == "KB": return float(size) * 1024 * 1024
    elif datatype == "B": return float(size)
    else: raise Exception("Неизвестный тип данных!")
