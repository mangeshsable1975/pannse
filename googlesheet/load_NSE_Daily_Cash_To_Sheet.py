import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import csv
from googleapiclient import discovery

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('BiGBANGHolidays-044e176b1f66.json', scope)
client = gspread.authorize(creds)

worksheet = client.open('Stock Data')

FUTURE_DATA_DIRECTORY = "D:\\Data_Files\\TESTING"
#Read Directory

#service = discovery.build('Stock Data',credentials=creds)

for dirpath, dnames, fnames in os.walk(FUTURE_DATA_DIRECTORY):
		for files in fnames:
			file_path = os.path.join(FUTURE_DATA_DIRECTORY,files)
			current_sheet = worksheet.add_worksheet(files,500,15)
			with open(file_path) as input_file:
				csv_reader = csv.reader(input_file, delimiter=',')
				line_count = 1
				for row in csv_reader:
					current_sheet.insert_row(row,line_count)
					line_count += 1

