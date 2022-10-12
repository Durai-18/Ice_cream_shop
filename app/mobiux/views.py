import csv, io
from datetime import datetime
from pyexpat.errors import messages
import requests
from django.shortcuts import render, redirect


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect


url ="https://www.mobiux.in/assignment/sales-data.txt"
response = requests.request("GET", url)
if response.status_code == 200:
	parsedData = (response.content).decode('utf8').replace("'", '"')	
	parsedCsv  = io.StringIO(parsedData)
	parsedList = list(csv.DictReader(parsedCsv))		

def home(request):
	return render(request, "home.html")
def storeTotalSales(request):
	storeTotalSales = 0
	for item in parsedList:
		storeTotalSales+= float(item["Total Price"])
	return render (request, "result.html", {"StoreTotalSales":storeTotalSales})

def monthWiseTotalSales(request):
	monthWiseTotalSales = {}
	for item in parsedList:
		month = datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%B")
		if month not in monthWiseTotalSales.keys():
			monthWiseTotalSales[month] = {"saleAmount": float(item["Total Price"])}
		else:
			monthWiseTotalSales[month]["saleAmount"] = monthWiseTotalSales[month]["saleAmount"] + float(item["Total Price"])	
	


	return render (request, "result.html", {"MonthWiseTotalSales":monthWiseTotalSales})



def mostPopularItem(request):
	mostPopularItem = {}
	for item in parsedList: 
		month   = datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%B")
		flavour = item["SKU"]
		if month not in mostPopularItem.keys():
			mostPopularItem[month] = {flavour: float(item["Quantity"])}
		else:
			if (mostPopularItem[month][list(mostPopularItem[month].keys())[0]]) < float(item["Quantity"]):
				mostPopularItem[month] = {flavour: float(item["Quantity"])} 
	return render (request, "result.html", {"MostPopularItem": mostPopularItem})
	


def mostRevenue(request):
	mostRevenue = {}
	for item in parsedList: 
		month   = datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%B")
		flavour = item["SKU"]
		val = float(item["Quantity"]) * float(item["Unit Price"])
		if month not in mostRevenue.keys():
			mostRevenue[month] = {flavour: val}
		else:
			if (mostRevenue[month][list(mostRevenue[month].keys())[0]]) < val:
				mostRevenue[month] = {flavour: val} 
	return render (request, "result.html", {"MostRevenue":mostRevenue})




def popularMaxMinAvg(request):
	mostPopularItem = {}
	for item in parsedList: 
		month   = datetime.strptime(item["Date"], "%Y-%m-%d").strftime("%B")
		flavour = item["SKU"]
		if month not in mostPopularItem.keys():
			mostPopularItem[month] = {flavour: float(item["Quantity"])}
		else:
			if (mostPopularItem[month][list(mostPopularItem[month].keys())[0]]) < float(item["Quantity"]):
				mostPopularItem[month] = {flavour: float(item["Quantity"])} 
	popularMaxMinAvg = {}
	for key,value in mostPopularItem.items():
		for item in parsedList:
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
			popularMaxMinAvg[month][flavour]["avg"] = popularMaxMinAvg[month][flavour]["avg"]["value"]//popularMaxMinAvg[month][flavour]["avg"]["count"]		
	return render (request, "result.html", {"PopularMaxMinAvg":popularMaxMinAvg})



from .models import mobiux_userregistration
import bcrypt

def signup_user(request):
	return render(request,'signup.html')
def signup_userRegistration_output(request):
	passwd = (request.POST.get('password')).encode('utf8')
	print(passwd)
	print(type(passwd))

	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(passwd, salt)
	print(hashed)
	print(type(hashed))


	print(bcrypt.checkpw(passwd, hashed))



	User = mobiux_userregistration(user_name=request.POST.get('user_name'), first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'), email=request.POST.get('email'),password=hashed, mobile = request.POST.get('mobile'))
	User.save()
	str1=request.POST.get('user_name')
	return render(request,'home.html',{'msg':str1})

def login(request):
	return render (request, 'login.html')

def logout(request):
	return redirect("signup_user")

import pymysql
# Create your views here.
def login_request(request):	
	try:
		user_name = (request.POST.get('user_name'))
		passwd = (request.POST.get('password')).encode('utf-8')
		print(passwd)
		print(type(passwd))


		connection=pymysql.connect(host='localhost', user='root', password='Durai@2599', database='mobiux')
		cur = connection.cursor()
		cur.execute("select password from mobiux_userregistration where user_name=%s ",user_name)
		row = cur.fetchone()
		db_password = (row[0])
		pw = (bytes(db_password[2:-1], 'utf8'))
		print(pw)
		print(type(pw))

		print(bcrypt.checkpw(passwd, pw))
		if bcrypt.checkpw(passwd, pw) == True:			
			cur.execute("select * from mobiux_userregistration where user_name=%s",user_name)
			row=cur.fetchone()
			if row == None:
				return render (request, "signup.html")
			else:
				return render(request, "home.html", {'msg':user_name}) 
		else:
			return render(request, "signup.html")
			

	except Exception as e:		
		return render ("Error!",f"Error due to {str(e)}")

