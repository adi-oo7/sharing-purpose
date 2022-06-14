# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 03:15:25 2022

@author: skrish04
"""
import itertools
import psycopg2
from flask import Flask, request
import time,glob,csv,re,pandas as pd
from flask_cors import CORS, cross_origin
import os
import datetime
import time
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from os.path import exists
app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
import csv
from datetime import date, timedelta, datetime
import cx_Oracle
import psycopg2.extras
import numpy as np
# import platform
# if platform.system() == "Darwin":
#     cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/Downloads/instantclient_19_8")
# cx_Oracle.init_oracle_client(lib_dir=r"H:\pyhton env\instantclient_21_3") #Try commenting this but if it does not work, you have to change this according to the local Oracle instantclient location
version = "0.0.1"
cwd=os.getcwd()
init_path=os.path.join(cwd,"CSV_IIB")
# init_path+="/"
msst_init_path=os.path.join(cwd,"CSV_MSST")
rdpnt_init_path=os.path.join(cwd,"CSV_Redpoint")
tas_init_path=os.path.join(cwd,"CSV_TAS")

token = "Ll_YYTbc2wN4WnViqIszvKgXNpzfFVOG1BIjdBaJfylLpNC6Vk_80xjM8_jeXFA1tNAFEwOGN8agqkWF0PpkaQ=="
org = "Digital"
bucket = "TASAPILogs"

client = InfluxDBClient(url="http://bevas01vr.bcbsma.com:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

#init_path='/data/TestMyBlueObs/ProcessLogs/CSV/loggingData_'

def CSVAPIIdcheck(filename, API, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    fromDateTime=str(fromDate)+' '+fromHour+':'+fromMinutes+':00.000'
    toDateTime=str(toDate)+' '+toHour+':'+toMinutes+':59.999'
    df = pd.read_csv(filename, sep = ",", encoding= 'unicode_escape')
    df['dateTime']=df.dateTime.str.slice(0,23)
    df['dateTime']=pd.to_datetime(df['dateTime'], format='%Y-%m-%d %H:%M:%S.%f')
    mask = np.where((df['message'].str.contains(API, na=False)) & (df['dateTime']>=fromDateTime) & (df['dateTime']<=toDateTime))  #fromTimeStamp>= x <=toTimeStamp
    rows=df.loc[mask]
    return rows

def CSVUserIdcheck(filename,userId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    fromDateTime=str(fromDate)+' '+fromHour+':'+fromMinutes+':00.000'
    toDateTime=str(toDate)+' '+toHour+':'+toMinutes+':59.999'
    df = pd.read_csv(filename, sep = ",", encoding= 'unicode_escape')
    df['dateTime']=df.dateTime.str.slice(0,23)
    df['dateTime']=pd.to_datetime(df['dateTime'], format='%Y-%m-%d %H:%M:%S.%f')
    mask = np.where((df['userId']==userId) & (df['dateTime']>=fromDateTime) & (df['dateTime']<=toDateTime))  #fromTimeStamp>= x <=toTimeStamp
    rows=df.loc[mask]
    return rows

def CSVErrorIdcheck(filename,errorId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes): 
    fromDateTime=str(fromDate)+' '+fromHour+':'+fromMinutes+':00.000'
    toDateTime=str(toDate)+' '+toHour+':'+toMinutes+':59.999'
    df = pd.read_csv(filename, sep = ",", encoding= 'unicode_escape')
    df['dateTime']=df.dateTime.str.slice(0,23)
    df['dateTime']=pd.to_datetime(df['dateTime'], format='%Y-%m-%d %H:%M:%S.%f')
    mask = np.where((df['message'].str.contains(errorId, na=False)) & (df['dateTime']>=fromDateTime) & (df['dateTime']<=toDateTime))  #fromTimeStamp>= x <=toTimeStamp     
    rows=df.loc[mask]
    return rows

def CSVCheck_TAS(filename, synthID, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    fromDateTime=str(fromDate)+' '+fromHour+':'+fromMinutes+':00'
    toDateTime=str(toDate)+' '+toHour+':'+toMinutes+':59'
    df = pd.read_csv(filename, sep = ",", encoding= 'unicode_escape')
    df['dateTime']=df.dateTime.str.slice(0,23)
    df['dateTime']=pd.to_datetime(df['dateTime'], format='%Y-%m-%d %H:%M:%S.%f')
    mask = np.where((df['synthID']==synthID) & (df['dateTime']>=fromDateTime) & (df['dateTime']<=toDateTime))  #fromTimeStamp>= x <=toTimeStamp     
    rows=df.loc[mask]
    return rows

def msstCSVCheck(filename, searchStr, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    fromDateTime=str(fromDate)+' '+fromHour+':'+fromMinutes+':00'
    toDateTime=str(toDate)+' '+toHour+':'+toMinutes+':59'
    df = pd.read_csv(filename, sep = ",", encoding= 'unicode_escape')
    df['dateTime']=df.dateTime.str.slice(0,23)
    df['dateTime']=pd.to_datetime(df['dateTime'], format='%Y-%m-%d %H:%M:%S.%f')
    if searchStr=="":
        mask = np.where((df['dateTime']>=fromDateTime) & (df['dateTime']<=toDateTime))  #fromTimeStamp>= x <=toTimeStamp
    else:
        mask = np.where((df['message'].str.contains(searchStr, na=False)) & (df['dateTime']>=fromDateTime) & (df['dateTime']<=toDateTime))  #fromTimeStamp>= x <=toTimeStamp
    rows=df.loc[mask]
    return rows

def rdpntCSVCheck(filename, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    fromDateTime=str(fromDate)+' '+fromHour+':'+fromMinutes+':00'
    toDateTime=str(toDate)+' '+toHour+':'+toMinutes+':59'
    df = pd.read_csv(filename, sep = ",", encoding= 'unicode_escape')
    df['dateTime']=df.dateTime.str.slice(0,23)
    df['dateTime']=pd.to_datetime(df['dateTime'], format='%Y-%m-%d %H:%M:%S.%f')
    mask = np.where((df['dateTime']>=fromDateTime) & (df['dateTime']<=toDateTime))  #fromTimeStamp>= x <=toTimeStamp
    rows=df.loc[mask]
    return rows

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def cloud_get_json(userId,fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    conn = None
    delta = timedelta(days=1)
    fromDate=fromDate.strftime("%#m/%#d/%Y")
    toDate=toDate.strftime("%#m/%#d/%Y")
    fromTimeStamp=fromDate+" "+fromHour+':'+fromMinutes+':00'
    fromTimeStamp=datetime.strptime(fromTimeStamp,"%m/%d/%Y %H:%M:%S")
    fromTimeStamp=fromTimeStamp.strftime("%m/%d/%Y %I:%M:%S %p")
    toTimeStamp=toDate+" "+toHour+':'+toMinutes+':59'
    toTimeStamp=datetime.strptime(toTimeStamp,"%m/%d/%Y %H:%M:%S")
    toTimeStamp=toTimeStamp.strftime("%m/%d/%Y %I:%M:%S %p")
    print(fromTimeStamp)
    try:
        conn = psycopg2.connect(host="pcf-prod-digital-payload-logging.cluster-cjpirfm0wdey.us-east-1.rds.amazonaws.com", database="ppayloadlog", user="digitaladmin", password="R1PfnlM&3m&pV")
        cur = conn.cursor()
        cur.execute("select created_datetime, client_session_id, api_name, payload, user_id from transaction_logging where user_id = '"+userId+"' and created_datetime>='"+fromTimeStamp+"' and created_datetime<='"+toTimeStamp+"'")
        db=cur.fetchall()
        
        for row in db:
            json_str.append([row[0],row[1],row[2],row[3],row[4]])
            
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        json_str=[]
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
    df = pd.DataFrame (json_str, columns = ['dateTime', 'transID', 'api', 'message', 'userId'])
    return df.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    
def UserId_API_get_json(API, userId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    conn = None
    delta = timedelta(days=1)
    fromDate=fromDate.strftime("%#m/%#d/%Y")
    toDate=toDate.strftime("%#m/%#d/%Y")
    fromTimeStamp=fromDate+" "+fromHour+':'+fromMinutes+':00'
    fromTimeStamp=datetime.strptime(fromTimeStamp,"%m/%d/%Y %H:%M:%S")
    fromTimeStamp=fromTimeStamp.strftime("%m/%d/%Y %I:%M:%S %p")
    toTimeStamp=toDate+" "+toHour+':'+toMinutes+':59'
    toTimeStamp=datetime.strptime(toTimeStamp,"%m/%d/%Y %H:%M:%S")
    toTimeStamp=toTimeStamp.strftime("%m/%d/%Y %I:%M:%S %p")
    print(fromTimeStamp)
    try:
        conn = psycopg2.connect(host="pcf-prod-digital-payload-logging.cluster-cjpirfm0wdey.us-east-1.rds.amazonaws.com", database="ppayloadlog", user="digitaladmin", password="R1PfnlM&3m&pV")
        cur = conn.cursor()
        cur.execute("select created_datetime, client_session_id, api_name, payload, user_id from transaction_logging where user_id = '"+userId+"' and '"+API+"' LIKE '%' || api_path || '%' and created_datetime>='"+fromTimeStamp+"' and created_datetime<='"+toTimeStamp+"'")
        db=cur.fetchall()
        
        for row in db:
            json_str.append([row[0],row[1],row[2],row[3],row[4]])
            
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        json_str=[]
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
    df = pd.DataFrame (json_str, columns = ['dateTime', 'transID', 'api', 'message', 'userId'])
    return df.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    
def ErrorId_API_get_json(API, errorId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    conn = None
    delta = timedelta(days=1)
    fromDate=fromDate.strftime("%#m/%#d/%Y")
    toDate=toDate.strftime("%#m/%#d/%Y")
    fromTimeStamp=fromDate+" "+fromHour+':'+fromMinutes+':00'
    fromTimeStamp=datetime.strptime(fromTimeStamp,"%m/%d/%Y %H:%M:%S")
    fromTimeStamp=fromTimeStamp.strftime("%m/%d/%Y %I:%M:%S %p")
    toTimeStamp=toDate+" "+toHour+':'+toMinutes+':59'
    toTimeStamp=datetime.strptime(toTimeStamp,"%m/%d/%Y %H:%M:%S")
    toTimeStamp=toTimeStamp.strftime("%m/%d/%Y %I:%M:%S %p")
    print(fromTimeStamp)
    try:
        conn = psycopg2.connect(host="pcf-prod-digital-payload-logging.cluster-cjpirfm0wdey.us-east-1.rds.amazonaws.com", database="ppayloadlog", user="digitaladmin", password="R1PfnlM&3m&pV")
        cur = conn.cursor()
        if API.lower()=='all':
            cur.execute("select created_datetime, client_session_id, api_name, payload, user_id from transaction_logging where '"+API+"' LIKE '%' || api_path || '%' and created_datetime>='"+fromTimeStamp+"' and created_datetime<='"+toTimeStamp+"'")
            db=cur.fetchall()
        else:
            cur.execute("select created_datetime, client_session_id, api_name, payload, user_id from transaction_logging where '"+errorId+"' LIKE '%' || api_path || '%' and '"+API+"' LIKE '%' || api_path || '%' and created_datetime>='"+fromTimeStamp+"' and created_datetime<='"+toTimeStamp+"'")
            db=cur.fetchall()
        
        for row in db:
            json_str.append([row[0],row[1],row[2],row[3],row[4]])
            
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        json_str=[]
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
    df = pd.DataFrame (json_str, columns = ['dateTime', 'transID', 'api', 'message', 'userId'])
    return df.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    
def get_json(userId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    toDate1=toDate + timedelta(days=1)
    current_hour=int(fromHour)
    current_minute=int(fromMinutes)
    fullDay=23
    fullHour=59
    for current_date in daterange(fromDate, toDate1):
        if current_date!=fromDate:
            current_hour=00   
        if(current_date==toDate):
            fullDay=int(toHour)
        
        while(int(current_hour)<=fullDay):
            if(int(current_hour)<10):
                current_hour='0'+str(current_hour)
            if(int(current_hour)>=10):
                current_hour=str(current_hour)
            # current_date=current_date.strftime("%Y-%m-%d")
            if current_hour!=fromHour:
                current_minute=00   
            if(current_hour==toHour and current_date==toDate):
                fullHour=int(toMinutes)
            while(int(current_minute)<=fullHour):
                if(int(current_minute)<10):
                    current_minute='0'+str(current_minute)
                if(int(current_minute)>=10):
                    current_minute=str(current_minute)
                if(userId=='mvvk07@gmail.com'):
                    filename=os.path.join(init_path,str(current_date),'loggingData_mvvk_'+str(current_date)+"_"+ current_hour+'_'+current_minute+'.csv')
                else:
                    filename=os.path.join(init_path,str(current_date),'loggingData_'+str(current_date)+"_"+current_hour+'_'+current_minute+'.csv')
                if(exists(filename)):
                    print(filename)
                    output=CSVUserIdcheck(filename,userId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                    json_str.append(output)
                current_minute=int(current_minute) + 1
            current_hour=int(current_hour) + 1
    try:
        frame=pd.concat(json_str, axis=0, ignore_index=True)
        return frame.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    except:
        return ''
#output.to_json(path_or_buf = None, orient = 'records', date_format = '%Y-%m-%d', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
def error_json(errorId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    toDate1=toDate + timedelta(days=1)
    current_hour=int(fromHour)
    current_minute=int(fromMinutes)
    fullDay=23
    fullHour=59
    for current_date in daterange(fromDate, toDate1):
        if current_date!=fromDate:
            current_hour=00   
        if(current_date==toDate):
            fullDay=int(toHour)
        while(int(current_hour)<=fullDay):
            if(int(current_hour)<10):
                current_hour='0'+str(current_hour)
            if(int(current_hour)>=10):
                current_hour=str(current_hour)
            # current_date=current_date.strftime("%Y-%m-%d")
            if current_hour!=fromHour:
                current_minute=00   
            if(current_hour==toHour and current_date==toDate):
                fullHour=int(toMinutes)
            while(int(current_minute)<=fullHour):
                if(int(current_minute)<10):
                    current_minute='0'+str(current_minute)
                if(int(current_minute)>=10):
                    current_minute=str(current_minute)
                
                filename=os.path.join(init_path,str(current_date)+'/loggingData_mvvk_'+str(current_date)+"_"+ current_hour+'_'+current_minute+'.csv')
                if(os.path.exists(filename)):
                    print(filename)
                    output=CSVErrorIdcheck(filename,errorId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                    json_str.append(output)
                filename=os.path.join(init_path,str(current_date)+'/loggingData_'+str(current_date)+"_"+current_hour+'_'+current_minute+'.csv')
                if(os.path.exists(filename)):
                    print(filename)
                    output=CSVErrorIdcheck(filename,errorId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                    json_str.append(output)
                current_minute=int(current_minute) + 1
            current_hour=int(current_hour) + 1
    try:
        frame=pd.concat(json_str, axis=0, ignore_index=True)
        return frame.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    except:
        return ''

def API_json(API, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    toDate1=toDate + timedelta(days=1)
    current_hour=int(fromHour)
    current_minute=int(fromMinutes)
    fullDay=23
    fullHour=59
    for current_date in daterange(fromDate, toDate1):
        if current_date!=fromDate:
            current_hour=00   
        if(current_date==toDate):
            fullDay=int(toHour)
        while(int(current_hour)<=fullDay):
            if(int(current_hour)<10):
                current_hour='0'+str(current_hour)
            if(int(current_hour)>=10):
                current_hour=str(current_hour)
            # current_date=current_date.strftime("%Y-%m-%d")
            if current_hour!=fromHour:
                current_minute=00   
            if(current_hour==toHour and current_date==toDate):
                fullHour=int(toMinutes)
            while(int(current_minute)<=fullHour):
                if(int(current_minute)<10):
                    current_minute='0'+str(current_minute)
                if(int(current_minute)>=10):
                    current_minute=str(current_minute)
                
                filename=os.path.join(init_path,str(current_date)+'/loggingData_mvvk_'+str(current_date)+"_"+ current_hour+'_'+current_minute+'.csv')
                if(os.path.exists(filename)):  
                    output=CSVAPIIdcheck(filename, API, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                    json_str.append(output)
                filename=os.path.join(init_path,str(current_date)+'/loggingData_'+str(current_date)+"_"+current_hour+'_'+current_minute+'.csv')
                if(os.path.exists(filename)):
                    output=CSVAPIIdcheck(filename, API, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                    json_str.append(output)
                current_minute=int(current_minute) + 1
            current_hour=int(current_hour) + 1
    try:
        frame=pd.concat(json_str, axis=0, ignore_index=True)
        return frame.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    except:
        return ''

def tas_api_json(synthID, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    toDate1=toDate + timedelta(days=1)
    current_hour=int(fromHour)
    current_minute=int(fromMinutes)
    fullDay=23
    fullHour=59
    for current_date in daterange(fromDate, toDate1):
        if current_date!=fromDate:
            current_hour=00   
        if(current_date==toDate):
            fullDay=int(toHour)
        while(int(current_hour)<=fullDay):
            if(int(current_hour)<10):
                current_hour='0'+str(current_hour)
            if(int(current_hour)>=10):
                current_hour=str(current_hour)
            # current_date=current_date.strftime("%Y-%m-%d")
            if current_hour!=fromHour:
                current_minute=00   
            if(current_hour==toHour and current_date==toDate):
                fullHour=int(toMinutes)
            while(int(current_minute)<=fullHour):
                if(int(current_minute)<10):
                    current_minute='0'+str(current_minute)
                if(int(current_minute)>=10):
                    current_minute=str(current_minute)
                filename=os.path.join(tas_init_path,str(current_date)+'/tasLoggingData_'+str(current_date)+"_"+current_hour+'_'+current_minute+'.csv')
                print(filename)
                if(os.path.exists(filename)):
                    print(filename)
                    output=CSVCheck_TAS(filename, synthID, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                    print(output)
                    json_str.append(output)
                current_minute=int(current_minute) + 1
            current_hour=int(current_hour) + 1
    try:
        frame=pd.concat(json_str, axis=0, ignore_index=True)
        return frame.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    except:
        return ''


def msst_get_json(searchStr, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    toDate1=toDate + timedelta(days=1)
    current_hour=int(fromHour)
    current_minute=int(fromMinutes)
    fullDay=23
    fullHour=59
    for current_date in daterange(fromDate, toDate1):
        if current_date!=fromDate:
            current_hour=00   
        if(current_date==toDate):
            fullDay=int(toHour)
        
        while(int(current_hour)<=fullDay):
            if(int(current_hour)<10):
                current_hour='0'+str(current_hour)
            if(int(current_hour)>=10):
                current_hour=str(current_hour)
            # current_date=current_date.strftime("%Y-%m-%d")
            if current_hour!=fromHour:
                current_minute=00   
            if(current_hour==toHour and current_date==toDate):
                fullHour=int(toMinutes)
            while(int(current_minute)<=fullHour):
                if(int(current_minute)<10):
                    current_minute='0'+str(current_minute)
                if(int(current_minute)>=10):
                    current_minute=str(current_minute)
                filename=os.path.join(msst_init_path,str(current_date),'msstLoggingData_'+str(current_date)+"_"+current_hour+'_'+current_minute+'.csv')
                if(exists(filename)):
                    print(filename)
                    output=msstCSVCheck(filename, searchStr, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                    json_str.append(output)
                current_minute=int(current_minute) + 1
            current_hour=int(current_hour) + 1
    try:
        frame=pd.concat(json_str, axis=0, ignore_index=True)
        return frame.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    except:
        return ''

def rdpnt_get_json(fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes):
    json_str=[]
    toDate1=toDate + timedelta(days=1)
    current_hour=int(fromHour)
    current_minute=int(fromMinutes)
    fullDay=23
    fullHour=59
    for current_date in daterange(fromDate, toDate1):
        if current_date!=fromDate:
            current_hour=00   
        if(current_date==toDate):
            fullDay=int(toHour)
        
        while(int(current_hour)<=fullDay):
            if(int(current_hour)<10):
                current_hour='0'+str(current_hour)
            if(int(current_hour)>=10):
                current_hour=str(current_hour)
            # current_date=current_date.strftime("%Y-%m-%d")
            if current_hour!=fromHour:
                current_minute=00   
            if(current_hour==toHour and current_date==toDate):
                fullHour=int(toMinutes)
            while(int(current_minute)<=fullHour):
                if(int(current_minute)<10):
                    current_minute='0'+str(current_minute)
                if(int(current_minute)>=10):
                    current_minute=str(current_minute)
                filename=os.path.join(rdpnt_init_path,str(current_date),'rdpntLoggingData_'+str(current_date)+"_"+current_hour+'_'+current_minute+'.csv')
                if(exists(filename)):
                    print(filename)
                    output=rdpntCSVCheck(filename, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                    json_str.append(output)
                current_minute=int(current_minute) + 1
            current_hour=int(current_hour) + 1
    try:
        frame=pd.concat(json_str, axis=0, ignore_index=True)
        return frame.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
    except:
        return ''

@app.route('/getIIBErrorByUserId/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getIIBErrorByUserId():
    content = request.json
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    userId=content['userid'].lower()
    return get_json(userId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getTASErrorByUserId/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getTASErrorByUserId():
    content = request.json
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    userId=content['userid'].lower()
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    return cloud_get_json(userId,fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getTASLogsFromCSV/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getTASErrorLogsFromCSV():
    content = request.json
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    userId = content['userId']
    synthID=''
    try:

        dsn_tns = cx_Oracle.makedsn('BORAP08VA.BCBSMA.COM', '1531', service_name='PMYBLUE.BCBSMA.COM') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(user='PZN_PRODSUPP_USER01', password='cH4ng3_m#_20200224', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        c = conn.cursor()
        c.execute("select PROFILE_VALUE from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and PK_USER_ID in ('"+str(userId)+"')")
        #c.execute("select sys_synthid from PZNADMIN1.USER_PROFILE_MV where PK_USER_ID = '"+userId+"'")
        for row in c: 
            if row[0] !='':
                synthID=row[0]
        print(synthID)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    return tas_api_json(synthID, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getTASLogsFromInfluxDB/v3/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getTASErrorLogsFromInfluxDB():
    content = request.json
    #fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    #toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    fromDate = content['fromDate'].split('-')
    toDate = content['toDate'].split('-')
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    #range = content['range']
    searchStr = content['searchStr']
    synthID=''

    regExp_AlphaNumeric = re.compile("(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,15})$")
    regExp_Email = re.compile("[a-z0-9]+@[a-z]+\.[a-z]{2,3}")
    regExp_10DigitNum = re.compile("^\d{10}$")

    regExp_SynthId = re.compile("^[0-9a-zA-Z]{8}([0-9a-zA-Z]{4}){3}[0-9a-zA-Z]{12}[0-9a-zA-Z]{8}$")


    start=datetime(int(fromDate[0]),int(fromDate[1]),int(fromDate[2]),int(fromHour),int(fromMinutes)).strftime('%Y-%m-%dT%H:%M:%SZ')
    stop=datetime(int(toDate[0]),int(toDate[1]),int(toDate[2]),int(toHour),int(toMinutes)).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(start)
    print(type(start))

    if (re.search(regExp_AlphaNumeric, searchStr) or re.search(regExp_Email, searchStr) or re.search(regExp_10DigitNum, searchStr)):
        try:

            dsn_tns = cx_Oracle.makedsn('BORAP08VA.BCBSMA.COM', '1531', service_name='PMYBLUE.BCBSMA.COM') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
            conn = cx_Oracle.connect(user='PZN_PRODSUPP_USER01', password='cH4ng3_m#_20200224', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
            c = conn.cursor()
            c.execute("select PROFILE_VALUE from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and PK_USER_ID in ('"+str(searchStr)+"')")
            #c.execute("select sys_synthid from PZNADMIN1.USER_PROFILE_MV where PK_USER_ID = '"+userId+"'")
            for row in c: 
                if row[0] !='':
                    synthID=row[0]
            print(synthID)
            

        except cx_Oracle.DatabaseError as e:
            print("There is a problem with Oracle", e)
    elif (re.search(regExp_SynthId, searchStr)):
        synthID = searchStr
    else:
        return json.dumps([])

    query ='''from(bucket: "TASAPILogs")
  |> range(start: ''' + start + ''', stop: ''' + stop + ''')
  |> filter(fn: (r) => r["_measurement"] == "TASlogsData")
  |> filter(fn: (r) => r["synthID"]=="''' +synthID+'")'

    print(query)
    tables = (client.query_api().query_data_frame(query, org=org))
    print(type(tables))
    if len(tables)==0:
        return json.dumps([])
    else:
        
        #tables.rename(columns={'_time':'dateTime'},inplace=True)
        dateTimeList=[]
        for i in tables.index:
            print(type(tables["_time"][i]))
            dateTimeList.append(tables["_time"][i].to_pydatetime().strftime('%Y-%m-%d %H:%M:%S'))
        tables["dateTime"]=dateTimeList
        tables=tables[["synthID","transactionID","trackingID","apiName","_value","dateTime"]]
        tables.rename(columns={'_value':'message'},inplace=True)
        return tables.to_json(orient='records')

    

@app.route('/getIIBERRORBySynthId/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getIIBERRORBySynthId():
    content = request.json
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    synthID=content['synthID']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    fromHour = content['fromHour']
    toHour = content['toHour']
    t=''
    try:

        dsn_tns = cx_Oracle.makedsn('BORAP08VA.BCBSMA.COM', '1531', service_name='PMYBLUE.BCBSMA.COM') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(user='PZN_PRODSUPP_USER01', password='cH4ng3_m#_20200224', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        c = conn.cursor()
        c.execute("select * from MOBADMIN1.USER_PROFILE_MV where PROFILE_VALUE in ('"+str(synthID)+"')")
        #c.execute("select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='MOBADMIN1.USER_PROFILE_MV'")
        #print(c)
        for row in c:
            if row[0] !='':
                userId=row[0]
                t=get_json(userId,fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    return t

@app.route('/getTASSynthIDBySynthId/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getTASSynthIDBySynthId():
    content = request.json
    synthID=content['synthID']
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    t=''
    try:

        dsn_tns = cx_Oracle.makedsn('BORAP08VA.BCBSMA.COM', '1531', service_name='PMYBLUE.BCBSMA.COM') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(user='PZN_PRODSUPP_USER01', password='cH4ng3_m#_20200224', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        c = conn.cursor()
        c.execute("select PK_USER_ID from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and PROFILE_VALUE in ('"+str(synthID)+"')")
        #select PK_USER_ID from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and PROFILE_VALUE in ('E7B201C946E0AAEA768F6424A079F91A20BB6240')
        #c.execute("select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='MOBADMIN1.USER_PROFILE_MV'")
        #print(c)
        for row in c:
            print(row)
            if row[0] !='':
                userId=row[0]
                t=cloud_get_json(userId,fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    return t

@app.route('/getTASErrorByAPIAndSynthid/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getTASErrorByAPIAndSynthid():
    content = request.json
    API=content['API']
    synthID=content['synthID']
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    t=''
    try:

        dsn_tns = cx_Oracle.makedsn('BORAP08VA.BCBSMA.COM', '1531', service_name='PMYBLUE.BCBSMA.COM') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(user='PZN_PRODSUPP_USER01', password='cH4ng3_m#_20200224', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        c = conn.cursor()
        c.execute("select PK_USER_ID from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and PROFILE_VALUE in ('"+str(synthID)+"')")
        #select PK_USER_ID from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and PROFILE_VALUE in ('E7B201C946E0AAEA768F6424A079F91A20BB6240')
        #c.execute("select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='MOBADMIN1.USER_PROFILE_MV'")
        #print(c)
        for row in c:
            if row[0] !='':
                userId=row[0]
                if(API.lower()=="all"):
                    t=cloud_get_json(userId,fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
                else:
                    t=UserId_API_get_json(API, userId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    return t

@app.route('/getTASErrorByAPIAndErrorId/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getTASErrorByAPIAndErrorId():
    content = request.json
    API=content['API']
    errorId=content['errorId']
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    t=''
    return ErrorId_API_get_json(API, errorId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getTASErrorByAPIAndUserId/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getTASErrorByAPIAndUserId():
    content = request.json
    API=content['API']
    userId=content['userId']
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    t=''
    if(API.lower()=="all"):
        return cloud_get_json(userId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)
    else:
        return UserId_API_get_json(API, userId, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getSynthIDByUserId/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getSynthIDByUserId():
    content = request.json
    userId=content['userId']
    synthId=''
    try:

        dsn_tns = cx_Oracle.makedsn('BORAP08VA.BCBSMA.COM', '1531', service_name='PMYBLUE.BCBSMA.COM') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(user='PZN_PRODSUPP_USER01', password='cH4ng3_m#_20200224', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        c = conn.cursor()
        c.execute("select PROFILE_VALUE from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and PK_USER_ID in ('"+str(userId)+"')")
        #c.execute("select sys_synthid from PZNADMIN1.USER_PROFILE_MV where PK_USER_ID = '"+userId+"'")
        for row in c: 
            if row[0] !='':
                synthId=row[0]
        print(synthId)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    return synthId

@app.route('/getUserIdBySynthId/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getUserIdBySynthId():
    content = request.json
    synthID=content['synthID']
    print(synthID)
    userId=''
    try:

        dsn_tns = cx_Oracle.makedsn('BORAP08VA.BCBSMA.COM', '1531', service_name='PMYBLUE.BCBSMA.COM') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(user='PZN_PRODSUPP_USER01', password='cH4ng3_m#_20200224', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        c = conn.cursor()
        c.execute("select PK_USER_ID from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and  PROFILE_VALUE in ('"+str(synthID)+"')")
        #c.execute("select sys_synthid from PZNADMIN1.USER_PROFILE_MV where PK_USER_ID = '"+userId+"'")
        for row in c: 
            if row[0] !='':
                userId=row[0]
        print(userId)
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    return userId

@app.route('/getIIBErrorByAPI/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getIIBErrorByAPI():
    content = request.json
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    API=content['API']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    return API_json(API, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getIIBERRORByError/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getIIBERRORBySErrorId():
    content = request.json
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    errorId=content['errorId']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    return error_json(errorId,fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getMSSTLogs/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getMSSTLogs():
    content = request.json
    searchStr = content['searchStr']
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    return msst_get_json(searchStr, fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getRedpointLogs/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getRedpointLogs():
    content = request.json
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    return rdpnt_get_json(fromDate, fromHour, fromMinutes, toDate, toHour, toMinutes)

@app.route('/getLines/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getLines():
    lis=[]
    content = request.json
    fromLine=int(content['fromLine'])
    file=int(content['fileName'])
    with open(file, "r") as text_file:
        for line in itertools.islice(text_file, fromLine-1, 1000):
            lis.append(line)

    return json.dumps(lis)

@app.route('/getStatus/v2/', methods=['get'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getStatus():
    return "Status: Running V "+version

@app.route('/getFileLogs/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getFileLogs():
    content = request.json
    file=content['fileName']
    df = pd.read_csv(file, sep = ",", encoding= 'unicode_escape')
    return df.to_json(path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)

@app.route('/getFileNames/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getFileNames():
    content = request.json
    fromHour = content['fromHour']
    toHour = content['toHour']
    fromMinutes = content['fromMinutes']
    toMinutes = content['toMinutes']
    fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    json_str=[]
    toDate1=toDate + timedelta(days=1)
    current_hour=int(fromHour)
    current_minute=int(fromMinutes)
    fullDay=23
    fullHour=59
    for current_date in daterange(fromDate, toDate1):
        if current_date!=fromDate:
            current_hour=00   
        if(current_date==toDate):
            fullDay=int(toHour)
        while(int(current_hour)<=fullDay):
            if(int(current_hour)<10):
                current_hour='0'+str(current_hour)
            if(int(current_hour)>=10):
                current_hour=str(current_hour)
            # current_date=current_date.strftime("%Y-%m-%d")
            if current_hour!=fromHour:
                current_minute=00   
            if(current_hour==toHour):
                fullHour=int(toMinutes)
            while(int(current_minute)<=fullHour):
                if(int(current_minute)<10):
                    current_minute='0'+str(current_minute)
                if(int(current_minute)>=10):
                    
                    current_minute=str(current_minute)
                    filename=os.path.join(init_path,str(current_date)+'/loggingData_mvvk_'+str(current_date)+"_"+ current_hour+'_'+current_minute+'.csv')
                    print(filename)
                    if(exists(filename)):
                      json_str.append(filename) 
                    filename=os.path.join(init_path,str(current_date)+'/loggingData_'+str(current_date)+"_"+current_hour+'_'+current_minute+'.csv')
                    if(exists(filename)):
                      json_str.append(filename)
                      
                current_minute=int(current_minute) + 1
            current_hour=int(current_hour) + 1  
    try:
        
        #frame=pd.concat(json_str, axis=0, ignore_index=True)
        return json.dumps(json_str) #path_or_buf = None, orient = 'records', date_format = 'iso', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None
    except:
        return '[]' 

@app.route('/getSynthUrl/v2/', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getSynthUrl():
    content = request.json
    # API=content['API']
    userId=content['userId']
    # fromHour = content['fromHour']
    # toHour = content['toHour']
    # fromMinutes = content['fromMinutes']
    # toMinutes = content['toMinutes']
    # fromDate= datetime.strptime(content['fromDate'], '%Y-%m-%d').date()
    # toDate= datetime.strptime(content['toDate'], '%Y-%m-%d').date()
    t=''
    try:
        dsn_tns = cx_Oracle.makedsn('BORAP08VA.BCBSMA.COM', '1531', service_name='PMYBLUE.BCBSMA.COM') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(user='PZN_PRODSUPP_USER01', password='cH4ng3_m#_20200224', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        c = conn.cursor()
        # PK_USER_ID sys_synthid
        c.execute("select PROFILE_VALUE from PZNADMIN1.USER_PROFILE_MV where PROFILE_KEY_NAME = 'sys_synthid' and PK_USER_ID in ('"+str(userId)+"')")
        #c.execute("select sys_synthid from PZNADMIN1.USER_PROFILE_MV where PK_USER_ID = '"+userId+"'")
        for row in c: 
            if row[0] !='':
                synthID=row[0]
        print(synthID)
        url = 'https://logrocket.bcbsma.com/bcbsma/internal-network-prod/sessions?filters=[{"id":"r1l-ZFJtq","type":"userID","operator":{"name":"is","type":"IS","hasStrings":true,"autocompleteEnabled":true},"strings":["' + synthID + '"]}]&timeRange=1646853760'
        return url

    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)
    return t

app.run()
