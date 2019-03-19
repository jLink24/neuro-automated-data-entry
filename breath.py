from csv import reader
from NeuroData import NeuroData
from datetime import datetime
import ast
import os
import xlsxwriter

MAX_KEY_PRESSES = 73
FILLER_VALUE = 2

def write_headers(worksheet):
    row = 0
    col = 0
    worksheet.write(row, col, "ID")
    worksheet.write(row, col + 1, "attention.response")
    worksheet.write(row, col + 2, "attention.rt")
    worksheet.write(row, col + 3, "awareness.response")
    worksheet.write(row, col + 4, "awareness.rt")
    worksheet.write(row, col + 5, "date")
    worksheet.write(row, col + 6, "expName")
    worksheet.write(row, col + 7, "session")
    worksheet.write(row, col + 8, "trials.thisRepN")
    worksheet.write(row, col + 9, "trials.thisTrialN")
    worksheet.write(row, col + 10, "trials.thisN")
    worksheet.write(row, col + 11, "trials.thisIndex")
    for i in range(MAX_KEY_PRESSES):
        worksheet.write(row, col + 12 + i, "key.press.{0}".format(i+1))
    worksheet.write(row, col + 12 + MAX_KEY_PRESSES, "other.keys.pressed?")
    worksheet.write(row, col + 13 + MAX_KEY_PRESSES, "key.type")

def dateToTimestamp(date):
    return datetime.strptime(date[:-5], "%Y_%b_%d").strftime("%Y-%m-%d-") + date[-4:]

def getSortKey(data):
    return data.std_date

def getSecondSortKey(data):
    return data.trials_thisN

def sortByDateRange(list):
    # Calculate indices for date range and perform the sort and sew back up

    lo = 0
    for i in range(len(list)-1):
        if i+1 == len(list) or list[i].date != list[i+1].date:
            list[lo:i+1] = sorted(list[lo:i+1], key=getSecondSortKey)
            lo = i+1

def main():
    # Create workbook
    print("\t>Creating xlsx output file...")
    workbook = xlsxwriter.Workbook('Neuro_data.xlsx')
    worksheet = workbook.add_worksheet()
    list = []

    # Need to make this work with multiple files
    for filename in os.listdir(os.path.join(os.getcwd(),"test-data/")):
        # Open csv file
        print("\t>Opening data file...")
        with open("./test-data/" + filename) as file:
            print("\t>Processing file: {0}".format(filename))
            for i,row in enumerate(reader(file)):
                if i > 0:
                    other_keys_pressed = 0
                    key_presses = []
                    for key_press in ast.literal_eval(row[4]):
                        if key_press == 'left':
                            key_presses.append(1)
                        elif key_press == 'right':
                            key_presses.append(0)
                        else:
                            key_presses.append(3)
                            other_keys_pressed = 1

                    data = NeuroData(row[14], row[7], row[8], row[9], row[10], row[11],
                                     dateToTimestamp(row[11]), row[12], row[13], row[0],
                                     row[1], row[2], row[3], key_presses, other_keys_pressed)
                    list.append(data)

    # sort list by date
    print("\t>Sorting entries by date...")
    list.sort(key=getSortKey)

    # then sort date ranges by trials_thisN
    print("\t>Sorting same date entries by parameter: (trials.thisN)...")
    sortByDateRange(list)

    print("\t>Writing to output file...")
    # Write headers
    write_headers(worksheet)

    row = 1
    col = 0
    for i,data in enumerate(list):
        worksheet.write(row, col, data.ID.zfill(4))
        worksheet.write(row, col + 1, data.attention_response)
        worksheet.write(row, col + 2, data.attention_rt)
        worksheet.write(row, col + 3, data.awareness_response)
        worksheet.write(row, col + 4, data.awareness_rt)
        worksheet.write(row, col + 5, data.date)
        worksheet.write(row, col + 6, data.expName)
        worksheet.write(row, col + 7, data.session)
        worksheet.write(row, col + 8, data.trials_thisRepN)
        worksheet.write(row, col + 9, data.trials_thisTrialN)
        worksheet.write(row, col + 10, data.trials_thisN)
        worksheet.write(row, col + 11, data.trials_thisIndex)
        # Write key presses
        for i,key_press in enumerate(data.key_presses):
            worksheet.write(row, col + i + 12, key_press)
        # Add filler value to columns
        nFillerValues = MAX_KEY_PRESSES-len(data.key_presses)
        for i in range(nFillerValues):
            worksheet.write(row, col + len(data.key_presses) + i + 12, FILLER_VALUE)
        worksheet.write(row, col + MAX_KEY_PRESSES + 12, data.other_keys_pressed)
        if data.other_keys_pressed == 1:
            worksheet.write(row, col + MAX_KEY_PRESSES + 13, "space")
        row += 1

    print("\t>Closing workbook...")
    workbook.close()

if __name__ == '__main__':
    main()
