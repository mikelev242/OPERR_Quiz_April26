"""
Below is my solution to all questions regarding the Boston Crash Data. To use the script the only thing you must do is change the
variable, workspace, in line 11 to reflect where you would like your files to be stored. 
"""

import urllib2, xlwt, sys, os, json, datetime, arcpy

arcpy.env.overwriteOutput = True

#Change code to reflect path where you want your files to be stored
workspace = 'C:\Users\g5210\Desktop\MikeLev'

#Below are the URL to the rest service and the query that we need to extract each record. Note the query is appended with each specific URL and a standard
#end URL. Each specific URL is created/retrieved in the getURL function
serviceURL = "http://gpd01.cityofboston.gov:6080/arcgis/rest/services/all_crashes_analysis/MapServer/6/"
query = "query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&objectIds="

#This step is necessary because we have over 1000 records and the service is only made to handle 1000 records at a time
#We will create unique URLs for each record and append it to a list that we will use to retrive the data.
def getURL(serviceURL, query, URLs, EndURL):
    # parse through the service and generate unique URLs
    MyURLList = []
    ID = ""
    count = 0
    for i in range(URLs[0], URLs[1]):
        # Create loop to create unique URLs 
        if count % 1000 == 0 and count != 0:
            MyURLList.append(serviceURL + query+ ID[:-1] + EndURL)
            ID = ""
        ID = ID + str(i) + ","
        count = count + 1
    MyURLList.append(serviceURL + query + ID[:-1] + EndURL)
    return MyURLList

def getData(URL):
    # Obtain the data using JSON and store data in a new list
    def myJson(data):
        for i in range(len(data['features'])):
            #Try/Except to check the format of the date field as requested by the question
            #use datetime add in to help in splitting the date from the time 
            try:
                checkDate = datetime.datetime.strptime(data['features'][i]['attributes']['Date'], "%m/%d/%Y %H:%M:%S %p")
            #check for other date formats.
            except:
                try:
                    checkDate = datetime.datetime.strptime(data['features'][i]['attributes']['Date'], "%m/%d/%Y %H:%M:%S")
                except:
                    checkDate = datetime.datetime.strptime(data['features'][i]['attributes']['Date'], "%m/%d/%Y")
            #parse data to get our required fields
            #date, time, mode, count, FID, incident were the request fields
            date = checkDate.date()
            time = checkDate.time()
            mode = data['features'][i]['attributes']['Mode']
            count = data['features'][i]['attributes']['Count']
            fid = data['features'][i]['attributes']['FID']
            incident = data['features'][i]['attributes']['Incident']
            latitude = data['features'][i]['geometry']['y']
            longitude = data['features'][i]['geometry']['x']
            #create key and value lists 
            key, value = ['latitude','longitude','date','time','count','incident','mode','fid'], [latitude,longitude,date,time,count,incident,mode,fid]
            #Retrieve only data for 2016
            if checkDate < datetime.datetime(2017, 01, 01) and checkDate > datetime.datetime(2016, 01, 01):
                MyData.append(dict(zip(key,value)))
            else:
                pass
    MyData = []
    for i in range(len(URL)):
        myJson(json.loads(urllib2.urlopen(URL[i]).read()))
    return MyData

#extract data to a csv in an unformatted version (question 3)
def Question3rawcsv(data, FilePath):
    MyFile = open(os.path.join(FilePath), 'a')
    MyFile.write("%s\n" % data)
    MyFile.write("\n")
    
#write to format requested in question 4
def Question4csv(data, FilePath):
    MyFile = open(os.path.join(FilePath), 'a')
    #create format
    MyFile.write("%s,%s,%s,%s,%s\n" % ('INCIDENT','DATE','MODE','COUNT',''))
    #create empty string to use to write to file
    myData = ""
    for i in range(len(data)):
        #populate string with data
        myData = myData +  str(data[i]['incident'])+','+str(data[i]['date'])+' '+str(data[i]['time'])+','+str(data[i]['mode'])+','+str(data[i]['count'])+','+'('+str(data[i]['latitude'])+','+str(data[i]['longitude'])+')'+'\n'
    #write file
    MyFile.write(myData)
    MyFile.close()

def Question5CSV(data, FilePath):
    MyFile = open(os.path.join(FilePath), 'a')
    #createFormat
    MyFile.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ('status/scripts','REPORTID','USERID','REPORTTYPEID','ADDEDBY','HOSTID','LATITUDE','LONGITUDE','RADIUSIMPACT','DESCRIPTION','PRICE','REPORTSTATUSID','DATE','TIME','CREATEDTIME','LASTMODIFIEDTIME','ADDRESS','TOTALNUMBERINJURED','TOTALNUMBERKILLED','VEHICLETYPECODE'))
    myData = ""
    for i in range(len(data)):
        #populate string with data - only populated fields are lat, long, date, and time. Commas and spaces used to enter blank fields
        myData = myData +  ',,,,,,'+str(data[i]['latitude'])+','+str(data[i]['longitude'])+',,,,,'+str(data[i]['date'])+','+str(data[i]['time'])+',,,,,,'+'\n'
    MyFile.write(myData)
    MyFile.close()

#write format from question 5 to an excel file instead of csv
def createEditableExcelQuestion5(data):
    excelworkbook = xlwt.Workbook()
    sheet = excelworkbook.add_sheet('question5')
    sheet.write(0,0,"status/scripts")
    sheet.write(0,1,"REPORTID")
    sheet.write(0,2,"USERID")
    sheet.write(0,3,"REPORTTYPEID")
    sheet.write(0,4,"ADDEDBY")
    sheet.write(0,5,"HOSTID")
    sheet.write(0,6,"LATITUDE")
    sheet.write(0,7,"LONGITUDE")
    sheet.write(0,8,"RADIUSIMPACT")
    sheet.write(0,9,"DESCRIPTION")
    sheet.write(0,10,"PRICE")
    sheet.write(0,11,"REPORTSTATUSID")
    sheet.write(0,12,"DATE")
    sheet.write(0,13,"TIME")
    sheet.write(0,14,"CREATEDATETIME")
    sheet.write(0,15,"LASTMODIFIEDTIME")
    sheet.write(0,16,"ADDRESS")
    sheet.write(0,17,"TOTALNUMBERINJURED")
    sheet.write(0,18,"TOTALNUMBERKILLED")
    sheet.write(0,19,"VEHICLETYPECODE")

    num = 1
    for i in range(len(data)):
        sheet.write(num,0,"")
        sheet.write(num,1,"")
        sheet.write(num,2,"")
        sheet.write(num,3,"")
        sheet.write(num,4,"")
        sheet.write(num,5,"")
        sheet.write(num,6,data[i]['latitude'])
        sheet.write(num,7,data[i]['longitude'])
        sheet.write(num,8,"")
        sheet.write(num,9,"")
        sheet.write(num,10,"")
        sheet.write(num,11,"")
        sheet.write(num,12,str(data[i]['date']))
        sheet.write(num,13,str(data[i]['time']))
        sheet.write(num,14,"")
        sheet.write(num,15,"")
        sheet.write(num,16,"")
        sheet.write(num,17,"")
        sheet.write(num,18,"")
        sheet.write(num,19,"")
        num = num + 1
    excelworkbook.save(workspace + '\BostonCrashQuestion5Excelabc.xls')
        

#Call your functions to get files
if __name__ == '__main__':
    #note argument [0,9229] reflects the total number of records, or each URL created
    URLs = getURL(serviceURL,query, [0,9229], "&outFields=*&outSR=102100")
    data = getData(URLs)
    Question3rawcsv(data,workspace + '\\rawdataabc.csv')
    Question4csv(data,workspace + '\Q4abc.csv') 
    Question5CSV(data,workspace + '\Q5CSVabc.csv')
    createEditableExcelQuestion5(data)

