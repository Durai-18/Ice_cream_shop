import requests
import csv, io, json
from datetime import datetime

class iceCreamParlour():
	def __init__(self, parsedList):
		self.parsedList = parsedList

	def storeTotalSales(self):
		storeTotalSales = 0
		for item in self.parsedList:
			storeTotalSales+= float(item["Total Price"])
		return {"storeTotalSales":storeTotalSales}


	def monthWiseTotalSales(self):
		monthWiseTotalSales = {}
		for item in self.parsedList:
			month = datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%B")
			if month not in monthWiseTotalSales.keys():
				monthWiseTotalSales[month] = {"saleAmount": float(item["Total Price"])}
			else:
				monthWiseTotalSales[month]["saleAmount"] = monthWiseTotalSales[month]["saleAmount"] + float(item["Total Price"])
		return {"monthWiseTotalSales":monthWiseTotalSales}


	def mostPopularItem(self):
		mostPopularItem = {}
		for item in self.parsedList: 
			month   = datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%B")
			flavour = item["SKU"]
			if month not in mostPopularItem.keys():
				mostPopularItem[month] = {flavour: float(item["Quantity"])}
			else:
				if (mostPopularItem[month][list(mostPopularItem[month].keys())[0]]) < float(item["Quantity"]):
					mostPopularItem[month] = {flavour: float(item["Quantity"])} 
		return {"mostPopularItem":mostPopularItem}


	def mostRevenue(self):
		mostRevenue = {}
		for item in self.parsedList: 
			month   = datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%B")
			flavour = item["SKU"]
			val = float(item["Quantity"]) * float(item["Unit Price"])
			if month not in mostRevenue.keys():
				mostRevenue[month] = {flavour: val}
			else:
				if (mostRevenue[month][list(mostRevenue[month].keys())[0]]) < val:
					mostRevenue[month] = {flavour: val} 
		return {"mostRevenue":mostRevenue}

def popularMaxMinAvg(self):
		popularOfMonth = self.mostPopularItem()
		popularMaxMinAvg = {}
		for key,value in popularOfMonth["mostPopularItem"].items():
			for item in self.parsedList:
				month   = datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%B")
				if key != month or (item["SKU"] not in value.keys()):
					continue
				else:
					if month not in popularMaxMinAvg.keys():
						popularMaxMinAvg[month] = { item["SKU"]: {
							"max":float(item["Quantity"]),
							"min":float(item["Quantity"]),
							"avg":{"value": float(item["Quantity"]), "count":1 }} 
						} 
					else:
						# calculating maximum
						if (popularMaxMinAvg[month][item["SKU"]]["max"]) < float(item["Quantity"]):
							popularMaxMinAvg[month][item["SKU"]]["max"] = float(item["Quantity"])
						# calculating minimum 
						if (popularMaxMinAvg[month][item["SKU"]]["min"]) > float(item["Quantity"]):
							popularMaxMinAvg[month][item["SKU"]]["min"] = float(item["Quantity"]) 	
						# gathering data for average calculation
						popularMaxMinAvg[month][item["SKU"]]["avg"]["value"] += float(item["Quantity"])
						popularMaxMinAvg[month][item["SKU"]]["avg"]["count"] += 1
		# calculating average
		for month in popularMaxMinAvg.keys():
		    for flavour in popularMaxMinAvg[month].keys():
		        popularMaxMinAvg[month][flavour]["avg"] = popularMaxMinAvg[month][flavour]["avg"]["value"]/popularMaxMinAvg[month][flavour]["avg"]["count"]		
        return popularMaxMinAvg


def main():
	url ="https://www.mobiux.in/assignment/sales-data.txt"
	print("Processing input data..")
	response = requests.request("GET",url)
	if response.status_code == 200:
		parsedData = (response.content).decode('utf8').replace("'", '"')	
		parsedCsv  = io.StringIO(parsedData)
		parsedList = list(csv.DictReader(parsedCsv))
		iceCreamParlourObj = iceCreamParlour(parsedList)
		
		while True:
			option = int(input("Select any number from 1 to 5 :\n1. Total sales of the store.\n2. Month wise sales totals.\n3. Most popular item (most quantity sold) in each month.\n4. Items generating most revenue in each month.\n5. For the most popular item, find the min, max and average number of orders each month\n\nYour option =>  "))
			if option == 1:
				storeTotalSales = iceCreamParlourObj.storeTotalSales()
				print(json.dumps( storeTotalSales,sort_keys=True, indent=4))
			elif option == 2: 
				monthWiseTotalSales = iceCreamParlourObj.monthWiseTotalSales()
				print(json.dumps( monthWiseTotalSales,sort_keys=True, indent=4))
			elif option ==3:
				mostPopularItem = iceCreamParlourObj.mostPopularItem()
				print(json.dumps( mostPopularItem,sort_keys=True, indent=4))
			elif option ==4:
				mostRevenue = iceCreamParlourObj.mostRevenue()
				print(json.dumps( mostRevenue,sort_keys=True, indent=4))				
			elif option ==5:
				popularMaxMinAvg = iceCreamParlourObj.popularMaxMinAvg()
				print(json.dumps( popularMaxMinAvg,sort_keys=True, indent=4))
			else:
				print("you have entered a wrong option..")
			print("#################################################################################################")
	else:
		print("Error while reading data from API!")

if __name__ == "__main__":
	main()