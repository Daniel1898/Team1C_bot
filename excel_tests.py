import openpyxl
wb = openpyxl.load_workbook(filename = 'E:\\python\\bot_v1\\test1.xlsx')




def get_question(n):
    n = n + 1
    sheet = wb['Лист1']
    result = sheet['A' + str(n+3*(n - 1))].value
    t = 1
    #vars = [sheet[k].value for k in range(n+3*(n - 1)+1, n+3*(n - 1)+4)
    for i in range(n+3*(n - 1)+1, n+3*(n - 1)+4):
        result += "\n\n" + str(t) + ')' + sheet['A' + str(i)].value
        t += 1
    return result

def getAnswer(n):
 #   sheet = rb.sheet_by_index(0)
    sheet = wb['Лист2']
    res = sheet['A' + str(n)]
    return str(res.value)