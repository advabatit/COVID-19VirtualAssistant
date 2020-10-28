import xlsxwriter

def create_excel(questions, answers) -> None:
    """
    Function that creates excel table with all the questions and the answers
    Args:
        Nothing
    Return:
        Nothing
    """
    excel_file = xlsxwriter.Workbook('questions_and_answeres.xlsx')
    wsTransaction = excel_file.add_worksheet('questions_and_answeres')

    row_num = 0
    col_num = 0

    wsTransaction.write(row_num, col_num, 'Questions')
    wsTransaction.write(row_num, col_num + 1, 'Answers')

    for i in range(len(questions)):
        row_num += 1
        wsTransaction.write(row_num, col_num, questions[i])
        wsTransaction.write(row_num, col_num + 1, answers[i])

    print("Finished!")
    excel_file.close()

create_excel()