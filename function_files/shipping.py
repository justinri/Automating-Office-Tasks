import easypost, time
from function_files.send_email import sendEmail
from datetime import date
easypost.api_key = 'removed...'

### Shipping Email-to
#email_to = [removed...]
email_to = ["removed..."]

def getTrackingInfo(trackNum, whichShipComp):
    tracker = easypost.Tracker.create(
              tracking_code=trackNum,
              carrier=whichShipComp)
    return tracker

def checkShip(trackNum, whichShipComp, jobBOSSdata, today):
    ### Getting ship-to information from JobBOSS
    packlist = jobBOSSdata[8]
    cityJB = jobBOSSdata[3].upper()
    stateJB = jobBOSSdata[4].upper()
    print(cityJB)
    print(stateJB)
    print(packlist)
    print(whichShipComp)
    print(trackNum)
    # print("-------------------------")

    ### We currently due not support shippments to mexico
    if stateJB.upper() == "MEX": return 0
    
    # tracker = getTrackingInfo(trackNum, "UPS")
    # print(tracker)    

    
    ### Getting ship-to information from Easyport API
    tracker = getTrackingInfo(trackNum, whichShipComp)
    time.sleep(0.05) ### Stopping for using the API too fast 	
    try: 
        trackerInfo = tracker["carrier_detail"]["destination_location"].replace(",","").split()
    except TypeError:
        try:
            if whichShipComp == "FedEX":                ### If the carrier is not FedEX it could be DHLExpress, both use just numbers
                tracker = getTrackingInfo(trackNum, "DHLExpress") 
                trackerInfo = tracker["carrier_detail"]["destination_location"].replace(",","").split()
            else: raise TypeError()
        except TypeError:
            print("Add what to do if shipping city is not there")
            whyEmail = "API ship city Error"
            emailContent = [packlist, trackNum]





    ### Uncomment
            # sendEmail(whyEmail, emailContent, today, email_to)
            return 0
 
    # print(trackerInfo)
    try:
        if trackerInfo[2] == "US":
            city = trackerInfo[0].upper()
            state = trackerInfo[1].upper()
        elif trackerInfo[3] == "US":     ### Meaning the city has gap in its' name. E.g., Del Rio, TX
            city = " ".join(trackerInfo[:2]).upper()
            state = trackerInfo[2].upper()
            
    except IndexError:   ### Shipment may be outside the US, thus then we are only confirming country is correct
            countryJB = jobBOSSdata[7]
            if countryJB == trackerInfo[0][-3:-1]:
                city = cityJB
                state = stateJB

    print("-------Tracking Number Data--------")
    print(city)
    print(state)
    print("-------------------------")
    ### Checking to ensure the ship location is correct
    if city != cityJB or state != stateJB:
        whyEmail = "Shipping Error"
        emailContent = [packlist, [city, state], [cityJB, stateJB]]
        print(city, ",", state)
        print(cityJB, ",", stateJB, packlist)

    # print(cityJB, stateJB, countryJB, packlist)

        # sendEmail(whyEmail, emailContent, email_to, today)	
    return 0

####***************************************************************************/
def checkTracking(cursor, today, table_Packlist_Detail, table_Packlist_Header, table_Address):
    """This function checks if the tracking number's ship-to city matches the sales order ship-to city. If it does not, an warning email will be send."""
    ### creating a small data set to look over, i.e., optimizing
    table_Packlist_Header = [item for item in table_Packlist_Header if str(item[6]).split()[0] == str(today)]
    packlistNums = [item[0] for item in table_Packlist_Header]
    table_Packlist_Detail = [item for item in table_Packlist_Detail if item[2] in packlistNums and item[12] != None]

    ### for testing
    # table_Packlist_Detail = [table_Packlist_Detail[1]]

    jobBOSSdata = []
    for row in table_Packlist_Detail:
        packlistNum_Detail = row[2]
        # if "11697" != packlistNum_Detail: continue ### For testing
        for row2 in table_Packlist_Header:
            packlistNum_header = row2[0]
            if packlistNum_Detail == packlistNum_header:
                customerNum_Packlist_Header = row2[1]
                AddressCode_Packlist_Header = row2[3]
                shipMethod_Packlist_Header = row2[4]
                for row3 in table_Address:
                    if row3[1] == AddressCode_Packlist_Header and row3[2] == customerNum_Packlist_Header:
                        # TrackingNum = 1
                        Line1 = row3[8]
                        Line2 = row3[9]
                        city = row3[10]
                        state = row3[11]
                        Zip = row3[12]
                        Name = row3[13]
                        Country = row3[14]
                        jobBOSSdata.append([row[12], Line1, Line2, city, state, Zip, Name, Country, packlistNum_header, shipMethod_Packlist_Header])
                        break

    for row in jobBOSSdata:
        trackNum = str(row[0])
        ### Checking what company the tracking number goes to
        ### Source: https://en.wikipedia.org/wiki/Tracking_number
        ### UPS numbers normally start with 1Z, for domestic packages.
        if  trackNum[1].upper() == 'Z': whichShipComp = "UPS"	

        ### If the tracking says "parcel", than no tracking is given
        elif "par" in trackNum.lower(): return 0

        ### FedEx Ground and Express tracking numbers are 12 digits (with the ability to expand to 14
        elif len(trackNum) >= 12 or len(trackNum) <= 14: whichShipComp = "FedEX"	

        elif len(trackNum) >= 20 or len(trackNum) <= 22: print(trackNum)

        ### If no tracking number is giving, nothing to check
        else: return 0
            
        checkShip(trackNum, whichShipComp, row, today)
    return 0
