import pandas


def __write_data(path, data_ALL):
    df = pandas.DataFrame()
    df.to_excel(path)
    writer = pandas.ExcelWriter(path)
    data = pandas.DataFrame(data_ALL).set_index(["id"])
    data.to_excel(writer, sheet_name='sheet1')
    writer.save()