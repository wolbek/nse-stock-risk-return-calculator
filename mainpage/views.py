from django.shortcuts import render
import pandas as pd
import numpy as np
import yfinance as yf
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def home(request):      
    return render(request,'mainpage/home.html')

@api_view(['POST'])
def priceOfStock(request):    
    stock=request.POST['stock'].strip()+".NS"    
    data = yf.download(stock, period=request.POST['time'])
    if len(data)==0:
        return Response({"status":0})
    data['Date']=data.index
    outputData={
        "status":1,
        "price":data['Close'],
        "date":data['Date']
    }
    return Response(outputData)  

@api_view(['POST'])
def dailyReturnsOfStock(request):
    stock=request.POST['stock'].strip()+".NS"   
    alldata = yf.download(stock, period='max')   
    data = yf.download(stock, period=request.POST['time'])   
    if len(data)==0:
        return Response({"status":0}) 
    data=alldata[-len(data)-1:]
          
    data['simple_returns']=round((data['Close']/data['Close'].shift(1))-1,5)*100   
    data=data[1:]
    data['Date']=data.index
    outputData={
        "status":1,
        "simple_returns":data['simple_returns'],
        "date":data['Date']
    }
    return Response(outputData)

@api_view(['POST'])
def growthComparisonOfStocks(request): 
    stocks=request.POST['stocks'].split(",")
    stocks=[s.strip()+".NS" for s in stocks]
    
    array=pd.DataFrame() 
    for stock in stocks:
        alldata = yf.download(stock, period='max')['Close'] 
        data =yf.download(stock, period=request.POST['time'])['Close']
        if len(data)==0:
            return Response({"status":0})  
        data=alldata[-len(data)-1:]  
        array[stock]=data
    
    array=array/array.iloc[0]*100
    data['Date']=data.index
    outputData={
        "status":1,
        "array":array,
        "date":data['Date'],
        "tickers":stocks
    }
    return Response(outputData)  

@api_view(['POST'])
def riskOfStock(request):   
    stock=request.POST['stock'].strip()+".NS"  
    alldata = yf.download(stock, period='max')   
    data = yf.download(stock, period=request.POST['time'])    
    if len(data)==0:
        return Response({"status":0})
    data=alldata[-len(data)-1:] 
 
    data['log_returns']=np.log(data['Close']/data['Close'].shift(1))
    data=data[1:]
    variance=data['log_returns'].var()*(len(data)-1)
    std_dvn=variance**0.5
    risk=std_dvn*100
    outputData={
        "status":1,
        "risk":risk,
    }
    return Response(outputData)

@api_view(['POST'])
def compoundInterest(request):   
    amount=float(request.POST['initialAmount'])
    yearsInvested=int(request.POST['yearsInvested'])
    rateOfInterest=float(request.POST['rateOfInterest'])
    amount=amount*(1+rateOfInterest/100)**yearsInvested
    outputData={
        "totalEarnings":amount,
    }
    return Response(outputData)
   
@api_view(['POST'])
def totalReturnsOfStock(request):   
    stock=request.POST['stock'].strip()+".NS"   
    data = yf.download(stock, period=request.POST['time'])   
    
    if len(data)==0:
        return Response({"status":0})    

    # Not taking dividends of the interval    

    total_returns=((data.iloc[-1,3]-data.iloc[0,3])/data.iloc[0,3])*100
    outputData={
        "status":1,
        "total_returns":total_returns,
    }
    return Response(outputData)


   


