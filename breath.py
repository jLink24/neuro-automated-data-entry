from csv import reader
from NeuroData import NeuroData
import xlsxwriter

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


# Create workbook
workbook = xlsxwriter.Workbook('Neuro_data.xlsx')
worksheet = workbook.add_worksheet()
list = []

# Open csv file
with open("./test-data/data.csv") as file:
    for i,row in enumerate(reader(file)):
        if i > 0:
            other_keys_pressed = False
            key_presses = []
            for key_press in row[4]:
                if key_press == 'left':
                    key_presses.append(1)
                elif key_press == 'right':
                    key_presses.append(0)
                else:
                    key_presses.append(3)
                    other_keys_pressed = True

            data = NeuroData(row[14], row[7], row[8], row[9], row[10], row[11],
                             row[12], row[13], row[0], row[1], row[2], row[3],
                             key_presses, other_keys_pressed)
            list.append(data)
# sort list by date
# then sort date ranges by

# do i need to find the max number of key presses?

# Write headers
write_headers(worksheet)

row = 1
col = 0

for i,data in enumerate(list):
    worksheet.write(row, col, data.ID)
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
    row += 1


workbook.close()
