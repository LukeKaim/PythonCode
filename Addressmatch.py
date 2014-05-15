#Code created by Luke Kaim 4/17/2014
#This is code is to help with address match with the County data.
#We are using address as a join column so the address has to match.
#I utilized an ArcPy update cursor for this.


# A python python dictionary also could have worked to update the addresses.



    
def main():
    try:
        #Import statement
        import arcpy,sys,traceback
        #Set environment
        arcpy.env.overwriteOutput = True
        from arcpy import env
        env.workspace =r"Z:\GenusZero_Projects\C\cimmeron\Resources\GenusZero\Geodatabase\project_Date.mdb"
        fc="ext_survey_existing_polygon1"
        #list the fields
        lstFields = arcpy.ListFields(fc)
        x = False
        fieldLength = 100
        counter=0
        #This is hard coded because it is faster than loop through every field. Below I have code to loop through every field though.
        fieldlist=[u'OBJECTID', u'Shape', u'OBJECTID_1', u'LOT_PRJCTD', u'LOT_ACTUAL', u'LOT_SOLD', u'PIN_1', u'FILING', u'TYPEDESC',\
                   u'TRACT_1', u'BLOCK_1', u'LOTNUM', u'OWNER_1', u'ADDRESS', u'STATE', u'ZIP', u'INCOMETYPE', u'CHECKED', u'PPM', u'HATCH_FILT', u'TOTALOVERL', u'INFILLDOTF',\
                   u'REBATE', u'DATESUBMIT', u'DATEAPPROV', u'DATESENTBA', u'WATERTAPFE', u'DISRICTCAP', u'AMOUNTYYDU', u'PARKFEEYES', u'PARKFEEAMO', u'LNAME', u'LADDRESS', u'TYPE2',\
                   u'GRADING_PH', u'TYPE3', u'LOTID', u'GZID', u'FILING_1', u'GRADINGDIR', u'WATERTAP_1', u'SUSTAINABI', u'ADDRESSNUM', u'GRADINGAND', u'QUALIFY_FO', u'REBATE_AMO',\
                   u'APPLIED_FO', u'BUILDERFEE', u'REBATEPROC', u'BUILDERPAY', u'TEXTSTRING', u'DOCNAME', u'DOCPATH', u'ROADNAME', u'SHAPE_LENG', u'FULLADDRES', u'LANDSCAPEA',\
                   u'DEMO_OWNER', u'LOTMANAGER', u'DEMO_CHECK', u'DEMO_DEPOS', u'DEMO_DISTR', u'DEMO_PARK_', u'DEMO_WATER', u'DEMO_SUSTA', u'DEMO_SOLAR', u'DEMO_SR_AP', u'DEMO_SR_CH',\
                   u'DEMO_BUILD', u'DEMO_PLAN_', u'DEMO_VISIB', u'DEMO_AREA_', u'DEMO_SHORT', u'DEMO_SH_01', u'DEMO_SH_02', u'HTML_LINK', u'DEMO_ADDRE', u'Shape_Length', u'Shape_Area',\
                   u'addressnew']
#This code actually loops through all the fileds. 
##        fieldlist=[]
##
##        for field in lstFields:
##            if field.name == "addressnew":
##                print "Field exists"
##                x = True
##                
##
##            #if x <> True:
##            else:
##                print "Field does not exist"
##                arcpy.AddField_management ("ext_survey_existing_polygon1","addressnew","TEXT""","",fieldLength)
##            fieldlist.append(field.name)
##        print fieldlist
        #Set index postion of field.
        x=fieldlist.index("addressnew")
        y=fieldlist.index("FULLADDRES")
        print x, " ", y
        #Create the update cursor
        with arcpy.da.UpdateCursor(fc,fieldlist) as cursor:
            for row in cursor:
                
                #row[x]=row[y]
               #split the column text on white space
                splitlist=row[y].split()
                #print splitlist
               #These address are hard coded because I had to go one at a time and correct the address. The County data was wrong, but because I was joining to the County data the addresses had to match.
                if splitlist==[u'17397', u'W.', u'95', u'th', u'Avenue'] or splitlist==[u'17437', u'W.', u'95', u'th', u'Avenue'] or splitlist==[u'17467', u'W.', u'95', u'th', u'Avenue']\
                   or splitlist==[u'17507', u'W.', u'95', u'th', u'Avenue']or splitlist==[u'17557', u'W.', u'95', u'th', u'Avenue']or splitlist==[u'17607', u'W.', u'95', u'th', u'Avenue']\
                   or splitlist==[u'17637', u'W.', u'95', u'th', u'Avenue'] or splitlist==[u'17667', u'W.', u'95', u'th', u'Avenue'] or splitlist==[u'17697', u'W.', u'95', u'th', u'Avenue']\
                   or splitlist==[u'17707', u'W.', u'95', u'th', u'Avenue'] or splitlist==[u'17717', u'W.', u'95', u'th', u'Avenue'] or splitlist==[u'17757', u'W.', u'95', u'th', u'Avenue']\
                   or splitlist==[u'17777', u'W.', u'95', u'th', u'Avenue'] or splitlist==[u'17817', u'W.', u'95', u'th', u'Avenue']\
                   or splitlist==[u'17937', u'W.', u'95', u'th', u'Avenue'] or splitlist==[u'18017', u'W.', u'95', u'th', u'Avenue']or splitlist==[u'18047', u'W.', u'95', u'th', u'Avenue']\
                   or splitlist==[u'17478', u'W.', u'95', u'th', u'Avenue'] or splitlist==['19984', 'W.', '94', 'th', 'Lane'] or splitlist==[u'17897', u'W.', u'95', u'th', u'Avenue']:
                    splitlist[4]="PL"
                    #print splitlist
                elif splitlist==[u'15879', u'W.', u'93rd', u'Pl']:
                    splitlist=[u"15879",u"W",u"93RD", u"AVE"]
                    #print "Yes"
                elif splitlist==[u'9497', u'Noble', u'Way']:
                    splitlist[0]="9494"
                elif splitlist==[u'9586', u'/', u'9576',u'Poppy',u"Way"]:
                    splitlist=[u"09576",u"POPPY",u"WAY"]
                elif splitlist==[u'16782', u'W.', u'95th', u'Lane', u'/', u'16785', u'W.', u'94th', u'Drive']:
                    splitlist=[u'16785', u'W.', u'94th', u'Drive']
                elif splitlist==[u'17150', u'W.', u'95th', u'Pl']:
                    splitlist=[u"17121",u"W",u"94TH",u"PL"]
                elif splitlist==[u'17305', u'W.', u'94', u'th', u'Avenue']:
                    splitlist=[u'17305', u'W', u'94TTH', u'AVE']
                elif splitlist==[u"9347",u"W.",u"93",u"rd","Avenue"] or splitlist==[u"9337",u"W.",u"93",u"rd","Avenue"] or splitlist==[u"9327",u"W.",u"93",u"rd","Avenue"]\
                     or splitlist==[u"9317",u"W.",u"93",u"rd","Avenue"] or splitlist==[u"9307",u"W.",u"93",u"rd","Avenue"]:
                        splitlist[1]="IRON"
                        splitlist[2]="MOUNTAIN"
                        splitlist[3]="WAY"
                        splitlist.remove(splitlist[4])
                elif  splitlist==[u"20136",u"W.",u"93",u"rd","Avenue"]:
                    splitlist=[u"20135",u"W",u"93RD",u"AVE"]
                elif splitlist==[u"9415",u"Lugram",u"Street"] or splitlist==[u"9425",u"Lugram",u"Street"] or splitlist==[u"9435",u"Lugram",u"Street"]\
                     or splitlist==[u"9424",u"Lugram",u"Street"] or splitlist==[u"9414",u"Lugram",u"Street"]:
                        splitlist[1]="INGRAM"
                        splitlist[2]="ST"
                elif splitlist==[u"9481",u"Umber",u"Way"]:
                    splitlist=[u"17358",u"W",u"95TH",u"AVE"]
                elif splitlist== [u'17359', u'W.', u'94', u'th', u'Drive']:
                    splitlist=[u'09461',u'UMBER',u"WAY"]
                elif splitlist==[u"9421", u"Umber", u"Way"]:
                    splitlist=[u'17360', u'W', u'94TH', u'DR']
                elif splitlist==[u'17357', u'W.', u'93', u'rd', u'Place']:
                    splitlist=[u'09401', u'UMBER', u'WAY']
                elif splitlist==[u'17928', u'W.', u'95', u'th', u'Avenue']:
                    splitlist[4]="DR"
                elif splitlist==[u'18048', u'W.', u'95', u'th', u'Avenue']:
                    splitlist=[u'09474', u'YANKEE', u'WAY']
                elif splitlist==[u'9374', u'Yankee', u'Way']:
                    splitlist=[u'18047', u'W', u'93RD', u'PL']
                elif splitlist==[u'18027', u'W.', u'93', u'rd', u'Place']:
                    splitlist=[u'18009', u'W', u'94TH', u'DR']
                elif splitlist==['19761', 'Gannett', 'Way']:
                    splitlist=['19761', 'W', '95TH', 'PL']
                elif splitlist==['19751', 'Gannett', 'Way']:
                    splitlist=['19751', 'W', '95TH', 'PL']
                elif splitlist==['9511', 'W.', '94', 'th', 'Place']:
                    splitlist=['09511', 'GANNETT', 'WAY']
                elif splitlist==['17769', 'W.', '95', 'th', 'Place']:
                    splitlist[4]="AVE"
                elif splitlist==['17847', 'W.', '95', 'th', 'Avenue']:
                    splitlist=['17857', 'W', '95TH', 'PL']
                elif splitlist==['19660', 'W.', '95', 'th', 'Place']:
                    splitlist=['17660', 'W', '95TH', 'PL']
                elif splitlist==[u'17977', u'W.', u'95', u'th', u'Avenue']:
                    splitlist=['17977', 'W', '93TH', 'PL']
                    
                #This is where I step through if the address is empty or has one string.
                if len(splitlist)>0:
                    if len(splitlist[0])==4:
                        counter+=1
                        #print counter
                        #Here I am adding a 0 to all addresses that only have 4 numbers in the number. The County added a 0 infront of addresses with 4 numbers.
                        postion0="0"+splitlist[0]
                    else:
                        postion0=splitlist[0]
                    index0=postion0

                    #This code handles if the address only has 2 strings and makes the corrections.
                    if len(splitlist)>1:
                        postion1=splitlist[1].upper()
                        if "W." in postion1:
                            postion1=postion1.rstrip(".")
                        index1=postion1
                        finallist=index0 +' '+ index1

                        #This makes the corrections if there are 3 strings.
                        if len(splitlist)>2:
                            postion2=splitlist[2].upper()
                            if "COURT" in postion2:
                                postion2="CT"
                            elif "STREET" in postion2:
                                postion2="ST"
                           
                            elif splitlist[2]=="94" or splitlist[2]=="95":                 
                                postion2=''.join([splitlist[2],splitlist[3].upper()])
                                splitlist.remove(splitlist[3])
                                                        
                            elif splitlist[2]=="93":
                                postion2=''.join([splitlist[2],splitlist[3].upper()])
                                splitlist.remove(splitlist[3])
                            elif "MOUTAIN" in postion2:
                                    postion2="MOUNTAIN"
                            index2=postion2
                            finallist=index0 +' '+ index1 +' '+ index2

                            #This handles if there are 4 strings in the address.
                            if len(splitlist)>3:
                                postion3=splitlist[3].upper()
                                                                   
                                if "PLACE" in postion3:
                                    postion3="PL"
                                                             
                                elif "AVENUE" in postion3:
                                    postion3="AVE"
                                    

                                elif "LANE" in postion3:
                                    postion3="LN"
                                
                                elif "DRIVE" in postion3:
                                    postion3="DR"
                                
                                    
                                index3=postion3
                                #This sets the final address
                                finallist=index0 + ' '+ index1 +' '+ index2 +' '+index3
                                #print splitlist
                                
                             

                        #print finallist
                        #This sets row[x]= to the finallist.        
                        row[x]=finallist
                        #This updates the address using the update cursor.
                    cursor.updateRow(row)
##                else:
##                    print "skip",row[0]                        
                  
            
               
                
        print "hello world"
         



        
    except:
        print arcpy.GetMessages()
        # Get the traceback object
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        # Concatenate information together concerning the error into a
        #   message string
        pymsg = tbinfo + "\n" + str(sys.exc_type)+ ": " + str(sys.exc_value)

        # Return python error messages for use with a script tool
        arcpy.AddError(pymsg)

        # Print Python error messages for use in Python/PythonWin
        print pymsg

if __name__ == '__main__':
    main()
    


        
