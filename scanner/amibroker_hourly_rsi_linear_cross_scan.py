import win32com.client as wcl
import time

AmiDatabase = "C:\\AFFeed\\Amibroker\\AmiData"
print("Start Loading Application......")
AB = wcl.Dispatch( 'Broker.Application')
print("Application. Loaded.....")
print("Start Loading DB......")
AB.LoadDatabase(AmiDatabase)
print("DB Loaded......")
rsi_hourly_scanner = "D:\\PycharmProjects\\StockAnalysis\\afl\\rsi_linear_crossover_scanner.apx"

try:
	print("Loading Scanner.....")
	NewA = AB.AnalysisDocs.Open(rsi_hourly_scanner)
	print("Scanner Loaded....")
	if (NewA):
		print("Started Running Analysis.....")
		NewA.Run(0) #// start backtest asynchronously
		while (NewA.IsBusy):
			print("Waiting.....")
			time.sleep(5) #// check IsBusy every 0.5 second
		NewA.Export("test.html") # export result list to HTML file
		print("Completed")
	NewA.Close() # close new Analysis
except Exception as ex:
	print("Exception: ")
	print(ex)

