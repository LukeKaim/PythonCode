##------------------------------------------------------------------------------------------------------------------------------------------------
##Created by Luke Kaim
##Final project for SIE 510 GIS Applications
##This code is meant to create a shapefile of points from a text file.
##Then those points that are created are tested that they are in the correct location.
##This is done two different ways. The first way is with nested search cursors and arcpy geometry. Then those points are inserted to a new shapefile.
##This new shapefile is used so that none of the original data is changed.
##The other way that this is done is with a spatial join and then an update cursor.
##Both workflows test all the input points against Country level of analysis and State level of analysis.
##This was done because the United States points had State as a field also. The smaller the area the better this method works. That is why I used both Country and State when I could.
##One would not want to query over Country and then State because one is changing the scale at which QA is taken place.
##The spatial join is much faster.
##------------------------------------------------------------------------------------------------------------------------------------------------

#Import  module
import arcpy, datetime

def deletefile(infile):
    #Function to delete file.
    #If statement to test if a file exists. If it does, then delete it.
    if arcpy.Exists(infile):
        arcpy.Delete_management(infile)

def globeSHP(infile):
    #This function creates an empty Shapefile that will be populated later.
    arcpy.CreateFeatureclass_management(workspace,infile,"POINT")#,spatial_reference=sr)
    #This adds fields to the empty Shapefile.
    arcpy.AddField_management(infile,"PointID","LONG","","","","","NON_NULLABLE","REQUIRED")
    arcpy.AddField_management(infile,"PointCNTRY","STRING","","","","","NON_NULLABLE","REQUIRED")
    arcpy.AddField_management(infile,"PointState","STRING","","","","","NULLABLE","REQUIRED")

def POINT(infile):
   #This function creates the an empty shapefile that will be used for the insert cursor. 
    arcpy.CreateFeatureclass_management(workspace,infile,"POINT")#,spatial_reference=sr)
    #This adds fields to the empty Shapefile.
    arcpy.AddField_management(infile,"PointID","LONG","","","","","NON_NULLABLE","REQUIRED")
    arcpy.AddField_management(infile,"PointCNTRY","STRING","","","","","NON_NULLABLE","REQUIRED")
    arcpy.AddField_management(infile,"PolyCNTRY","STRING","","","","","NULLABLE","REQUIRED")
    arcpy.AddField_management(infile,"PointState","STRING","","","","","NON_NULLABLE","REQUIRED")
    arcpy.AddField_management(infile,"PolyState","STRING","","","","","NON_NULLABLE","REQUIRED")
    arcpy.AddField_management(infile,"Missmatch","LONG","","","","","NULLABLE","REQUIRED")

def createShape(infile,outfile,inputfield):
    #This code creates a point shapefile from an input text file.
    # Create point
    point = arcpy.Point()
    #Open textfile
    textFile=open(infile,'r')
    #Read header
    headerLine = textFile.readline()
    #Split header line
    valueList = headerLine.split("\t")
    #Get index value for the header values that are needed.
    latValueIndex = valueList.index("Latitude")
    lonValueIndex = valueList.index("Longitude")
    pointID=valueList.index("ObsID")
    Country=valueList.index("Country\n")
    #Field names for the shapefile.
    field=inputfield
    
    with arcpy.da.InsertCursor(outfile,field) as cursor:
        # Insert cursor to insert the points into the shapefile.
        for line in textFile.readlines():
            #For loop to read in lines of the shapefile.
            segmentedLine=line.split("\t")
            #Split body.
            pointIDValue=segmentedLine[pointID]
            latValue=segmentedLine[latValueIndex]
            longValue=segmentedLine[lonValueIndex]
            countryValue=segmentedLine[Country]
            state=segmentedLine[Country]
            #print countryValue
            if "\n" in countryValue:
                #If statement to handle deleting line break to make the names correct. 
                countryValue= countryValue.rstrip("\n")
            if "\n" in state:
                state= countryValue.rstrip("\n")
                
                if "United States" in countryValue:
                    #If statement to handle concatenation of Country and State for the United States.
                    #Need to break apart “United States – Arizona” to “United States” and “Arizona”. This code does that.
                    countryValue=countryValue[:13] #+ "test" + countryValue[15:]
                    state=state[16:]
                else:            
                    # If it does not equal United States, then it is not a State so leave it empty.
                    state=""
                # This handles spelling errors.        
                if "Macedonia (FYROM)" in countryValue:
                    countryValue=countryValue[:9]
                elif "Cayman Is." in countryValue:
                    countryValue=countryValue[:6]+ " " +"Islands"
                elif "Trinidad & Tobago" in countryValue:
                    countryValue=countryValue[:8] + " " + "and" + " " + countryValue[-6:]
                    #print countryValue
                elif "The Netherlands" in countryValue:
                    countryValue=countryValue[-11:]
                    #print countryValue
                elif "The Bahamas" in countryValue:
                    countryValue=countryValue[-7:]
                    #print countryValue
                elif "Serbia & Montenegro" in countryValue:
                    countryValue=countryValue[:6]
                    #print countryValue
                point=arcpy.Point(longValue,latValue)
                #Create point
                row_values=[point,pointIDValue,countryValue,state]
                #Row values that will be inserted into the shapefile.
                #print row_values
                cursor.insertRow(row_values)
                #Insert the row into the cursor.

#Lines of code to help get field position. This is for reference only.
##PointField=["SHAPE@","PointID","PointCNTRY","PointState"]
##UnionField=["SHAPE@","CountryPly","StatePly"]
##QAshapefile=["SHAPE@XY","PointID","PointCNTRY","PolyCNTRY","PointState","PolyState","Missmatch"]
#MainCode("testbed2.shp",Union,"PointQC.shp",PointField,UnionField,QAshapefile)
    
def MainCode(shapefile1,shapefile2,shapefile3,field1,field2,field3,column):
    #Main function that creates 3 nested cursors. The first two are search cursors to get the address of each record.
    #The insert cursor is used to insert all records into a new shapefile so that the original shapefile is unchanged.
    with arcpy.da.SearchCursor(shapefile1,field1) as cursor:
        for row in cursor:
            with arcpy.da.SearchCursor(shapefile2,field2) as cursor2:
                for row2 in cursor2:
                    with arcpy.da.InsertCursor(shapefile3,field3) as cursor3:
                        if row[0].within(row2[0]):
                        #This is to test if a point is within a polygon.
                            if row[column]==row2[1]:
                                #If it is then the address name is tested against the polygon address name. 
                                True
                                point=row[0]
                                pointID=row[1]
                                PointCNTRY=row[column]
                                PolyCNTRY=row2[1]
                                PointState=row[3]
                                PolyState=row2[2]
                                test=0
                                #Set variables to the different rows. Test is set to 0 if true.
                            #print True
                            
                            elif row[colum]!=row2[1]:
                                # This elif handle if the addresses do not match.
                                False
                                point=row[0]
                                pointID=row[1]
                                PointCNTRY=row[colum]
                                PolyCNTRY=row2[1]
                                PointState=row[3]
                                PolyState=row2[2]
                                test=1
                            else:
                                point=row[0]
                                pointID=row[1]
                                PointCNTRY=row[colum]
                                PolyCNTRY=row2[1]
                                PointState=row[3]
                                PolyState=row2[2]
                                test=3         
                            print row[1],row[column],row2[1],test
                            row_values=[point,pointID,PointCNTRY,PolyCNTRY,PointState,PolyState,test]
                            #Row values. 
                            cursor3.insertRow(row_values)
                            #Insert cursor
                    
 
def SpatialJoin(infile,join,outfile):
    #This is to test a different workflow compared to the one above and see which one is faster. This method uses a spatial join. 
    arcpy.SpatialJoin_analysis(infile,join,outfile,"JOIN_ONE_TO_ONE","KEEP_ALL","","INTERSECT")
    #Add field to the spatial join that will be updated later.
    arcpy.AddField_management(outfile,"Missmatch2","LONG","","","","","NULLABLE","REQUIRED")
 
def UpdateCursor(infile,fieldname):
    # Update the spatial join shapefile for the different match cases.
    with arcpy.da.UpdateCursor(infile,fieldname) as cursor:
        #Update cursor.
        for row in cursor:
            #For loop to read over cursor.
            if row[0]==row[2]:
                #row[4]=1
                if row[1]!=row[3]:
                    row[4]=5
                else:
                    row[4]=4

            elif row[0]!=row[2]:
                #If address column does not equal polygon address column, then row missmatch equal 2.
                True
                row[4]=2
                if row[2] == " ":
                    row[4]=3
            
            #print row[2]
            cursor.updateRow(row)
            #Update row values into the cursor.
                          
print "Start"
#Overwrite environment parameters
arcpy.env.overwriteOutput = True
#Set work space
from arcpy import env
workspace=arcpy.env.workspace =r"C:\Users\Luke Kaim\Documents\University of Maine\Spring_2013\GIS_Application\finalproject"
#Declare variable names
stateSHP="USA_adm1.shp"
Country="Country.shp"
country2="world_country_admin_boundary_shapefile_with_fips_codes.shp"
Union="Union.shp"
#Union State polygon and Country polygon together. 
##arcpy.Union_analysis([Country,stateSHP],Union,"ALL")

#Function call to delete file if it already exists.
deletefile("globeAtNight.shp") and deletefile("Join.shp") #and deletefile("Union.shp")
deletefile("PointQC1.shp")

#Field names for the different shapefiles. 
PointField=["SHAPE@","PointID","PointCNTRY","PointState"]
UnionField=["SHAPE@","CountryPly","StatePly"]
QAshapefile=["SHAPE@XY","PointID","PointCNTRY","PolyCNTRY","PointState","PolyState","Missmatch"]
#Fields for the spatial join approach.
Join=["PointCNTRY","PointState","CountryPly", "StatePly","Missmatch2"]
         
#Function call that creates an empty shapefile.
globeSHP("globeAtNight.shp")
#Function call that creates an empty shapefile. This will be filled using the insert cursor.
POINT("PointQC1.shp")

#Function to create shapefile from text file.
createShape('GaN2012.txt',"globeAtNight.shp",PointField)

#Nested cursor workflow.
#Start timer
start= datetime.datetime.now()
#Function call main code. This is where the 3 nested cursors are called. This function does both levels of analysis.
MainCode("testbed3.shp",Union,"PointQC1.shp",PointField,UnionField,QAshapefile,2)

#End timer
end=datetime.datetime.now()
print "DONE nested search cursor", end-start
#This workflow took 1:55 hours.

#Spatial join workflow.
#Start new timer.
start1=datetime.datetime.now()
#Function call to do a spatial join between the points and the polygon.
SpatialJoin("globeAtNight.shp",Union,"Join.shp")
#Update cursor function. This adds the different missmatch values.
UpdateCursor("Join.shp",Join)
#End timer.
end1=datetime.datetime.now()
print "DONE updateJoin", end1-start1
print "END"
