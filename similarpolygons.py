#Import  module
import arcpy, datetime
#Set work space
from arcpy import env
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz


#Start timer
start= datetime.datetime.now()
print "Start"


def deletefile(infile):
    #Function to delete file.
    #If statement to test if a file exists. If it does, then delete it.
    if arcpy.Exists(infile):
        arcpy.Delete_management(infile)

def UpdateCursor(infile,fieldname):
    # Update the spatial join shapefile for the different match cases.
    with arcpy.da.UpdateCursor(infile,fieldname) as cursor:
        #Update cursor.
        for row in cursor:
            row[1]=row[0].area
            row[2]=row[0].length
            ext=row[0].extent
            extlower=ext.lowerLeft
            extup=ext.upperRight
            pointGeometry = arcpy.PointGeometry(extlower,"26919")
            pointGeometryList.append(pointGeometry)
            pointGeometry2 = arcpy.PointGeometry(extup,"26919")
            pointGeometryList2.append(pointGeometry2)
            #print ext
            #print "lowerleft", extlower
            #print "upper right", extup
            cursor.updateRow(row)

def UpdateCursor2(infile,fieldname):
    # Update the spatial join shapefile for the different match cases.
    with arcpy.da.UpdateCursor(infile,fieldname) as cursor:
        #Update cursor.
        for row in cursor:
            row[1]=row[0].area
            row[2]=row[0].length
            cursor.updateRow(row)

        
def UpdateCursor3(infile,test):
    # Update the spatial join shapefile for the different match cases.
    with arcpy.da.UpdateCursor(infile,test) as cursor:
        #Update cursor.
        for row in cursor:
            #row[2]=row[0].area
            #row[3]=row[0].length
            if row[8]!=-1:
                if row[9] !=-1:
                    row[10]=1
            denominatorArea=(row[4]+row[5])/2
            #print denominatorArea
            row[6]=row[2]/((row[4]+row[5])/float(2))
            row[7]=row[2]/((row[5]+row[4])/float(2))
            row[13]=row[3]/((row[11]+row[12])/float(2))
            row[14]=row[3]/((row[11]+row[12])/float(2))         
            #print("{0}, {1}, {2},{3}".format(row[6], row[7], row[13],row[14]))
            if infile==DissolveUnion:
                
                if len(row[15]) > len(row[16]):
                    row[15],row[16]=row[15],row[16]
                distances = range(len(row[15]) + 1)
                for index2,char2 in enumerate(row[16]):
                    newDistances= [index2+1]
                    for index1,char1 in enumerate(row[15]):
                        if char1 == char2:
                            newDistances.append(distances[index1])
                        else:
                            newDistances.append(1 + min((distances[index1],
                                                         distances[index1+1],
                                                         newDistances[-1])))
                    distances = newDistances
                    #print distances                            
                Ldistance=distances[-1]
                s= SequenceMatcher(None,row[15],row[16])
                stringRatio=s.ratio()
                #print stringRatio
                row[17]=Ldistance
                row[18]=stringRatio
                StringRat=fuzz.ratio(row[15], row[16])
                row[19]=StringRat/float(100)
                stringPartialRatio=fuzz.partial_ratio(row[15], row[16])
                row[20]=stringPartialRatio/float(100)
                StringTokenSort=fuzz.token_sort_ratio(row[15], row[16])
                row[21]=StringTokenSort/float(100)
                stringTokenSet=fuzz.token_set_ratio(row[15], row[16])
                row[22]=stringTokenSet/float(100)
                Average=(StringRat+stringPartialRatio+StringTokenSort+stringTokenSet)/4
                row[23]=Average/float(100)
                WeightedAverage=((.10*StringRat)+(.30*stringPartialRatio)+(.30*StringTokenSort)+(.30*stringTokenSet))/4
                row[24]= WeightedAverage/float(100)
                #print Average,WeightedAverage
                #print ("{0},{1},{2}".format(row[15],row[16],row[18]))
            cursor.updateRow(row)


def addfield1(infile):
    arcpy.AddField_management(infile,"areVGI","DOUBLE","30","30")                      
    arcpy.AddField_management(infile,"lengVGI","DOUBLE","30","30")      
def addfield2(infile):    
    arcpy.AddField_management(infile,"areGNIS","DOUBLE","30","30")
    arcpy.AddField_management(infile,"lengGNIS","DOUBLE","30","30")
def addfield3(infile):
    arcpy.AddField_management(infile,"IntType","LONG")
    arcpy.AddField_management(infile,"vgiOVER_A","DOUBLE","30","30")
    arcpy.AddField_management(infile,"gnisOVER_A","DOUBLE","30","30")
    arcpy.AddField_management(infile,"intersect","LONG")
    arcpy.AddField_management(infile,"vgiOVER_L","DOUBLE","30","30")
    arcpy.AddField_management(infile,"gnisOVER_L","DOUBLE","30","30")
    if infile == DissolveUnion:
        arcpy.AddField_management(infile,"LDistance","LONG")
        arcpy.AddField_management(infile,"SequenceM","DOUBLE","30","30")
        arcpy.AddField_management(infile,"StringRat","DOUBLE","30","30")
        arcpy.AddField_management(infile,"StringPar","DOUBLE","30","30")
        arcpy.AddField_management(infile,"StrSort","DOUBLE","30","30")
        arcpy.AddField_management(infile,"StrSet","DOUBLE","30","30")
        arcpy.AddField_management(infile,"StringAvg","DOUBLE","30","30")
        arcpy.AddField_management(infile,"WeightAvg","DOUBLE","30","30")

def JoinField(infile,in_field,join_table,join_field,fields):
    arcpy.JoinField_management(infile,in_field,join_table,join_field,fields)

    
 
#Overwrite environment parameters
arcpy.env.overwriteOutput = True
workspace=arcpy.env.workspace =r"C:\Users\Luke Kaim\Documents\University of Maine\Spring_2013\similar_feature\Test_results\test4"
#Declare variable names
VGI_file="VGI.shp"
GNIS_file="GNIS.shp"
##arcpy.env.workspace = arcpy.GetParameterAsText(0)
###Declare variable names
##VGI_file=arcpy.GetParameterAsText(1)
##GNIS_file=arcpy.GetParameterAsText(2)
##FID_VGI=arcpy.GetParameterAsText(3)
##FID_GNIS=arcpy.GetParameterAsText(4)
##VGI_FeatureName=arcpy.GetParameterAsText(5)
##GNIS_FeatureName=arcpy.GetParameterAsText(6)
VGInew="VGICopy.shp"
GNISnew="GNISCopy.shp"
VGIboundingbox="VGIboundingbox.shp"
GNISboundingbox="GNISboundingbox.shp"
UnionShape=r"FileGDB.gdb\UnionShape"
UnionBoundingBox=r"FileGDB.gdb\UnionBoundingBox"
DissolveUnion=r"FileGDB.gdb\DissolveUnion"
DissolveUnionBoundingBox=r"FileGDB.gdb\DissolveUnionBoundingBox"
VGILowerLeft="VGILowerLeft.shp"
VGIUpperRight="VGIUpperRight.shp"
GNISLowerLeft="GNisLowerLeft.shp"
GNISUpperRight="GNISUpperRight.shp"
pointGeometryList = []
pointGeometryList2 = []
filename="FileGDB.gdb"
FID_VGI="FID_VGICopy"
FID_GNIS="FID_GNISCopy"
VGI_FeatureName="VGIName"
GNIS_FeatureName="GNISName"
FID_VGIboundingBox="FID_VGIboundingbox"
FID_GNISboundingBox="FID_GNISboundingbox"
Max_FID_GNIS="MAX_FID_GNISCopy"
Max_FID_GNIS_BoundingBox="MAX_FID_GNISboundingbox"
Clip_Shape=r"FileGDB.gdb\ClipAll"
Clip_BoundingBox=r"FileGDB.gdb\ClipAllBoundingBox"




deletefile(VGInew) and deletefile(GNISnew) and deletefile(VGIboundingbox) and deletefile(GNISboundingbox)
deletefile(filename) and deletefile("ResultsUnion.dbf") and deletefile("ResultsUnionBoundingbox.dbf")
print "finished1"

arcpy.CreateFileGDB_management(arcpy.env.workspace,filename)
arcpy.CopyFeatures_management(VGI_file,VGInew)
arcpy.CopyFeatures_management(GNIS_file,GNISnew)
arcpy.FeatureEnvelopeToPolygon_management(VGI_file,VGIboundingbox,"MULTIPART")
arcpy.FeatureEnvelopeToPolygon_management(GNIS_file,GNISboundingbox,"MULTIPART")

addfield1(VGInew)
addfield2(GNISnew)
addfield1(VGIboundingbox)
addfield2(GNISboundingbox)

FnameVGI=["SHAPE@","areVGI","lengVGI"]
FnameGNIS=["SHAPE@","areGNIS","lengGNIS"]
UpdateCursor(VGInew,FnameVGI)
arcpy.CopyFeatures_management(pointGeometryList, VGILowerLeft)
arcpy.CopyFeatures_management(pointGeometryList2, VGIUpperRight)
pointGeometryList = []
pointGeometryList2 = []
UpdateCursor(GNISnew,FnameGNIS)
arcpy.CopyFeatures_management(pointGeometryList, GNISLowerLeft)
arcpy.CopyFeatures_management(pointGeometryList2, GNISUpperRight)
#start1= datetime.datetime.now()
UpdateCursor2(VGIboundingbox,FnameVGI)
end1=datetime.datetime.now()
#print "finished cursor", end1-start1
UpdateCursor2(GNISboundingbox,FnameGNIS)
arcpy.Union_analysis([VGInew,GNISnew],UnionShape,"ALL")
arcpy.Union_analysis([VGIboundingbox,GNISboundingbox],UnionBoundingBox,"ALL")


arcpy.Dissolve_management(UnionShape,DissolveUnion,FID_VGI,[[FID_GNIS,"MAX"]])
arcpy.Dissolve_management(UnionBoundingBox,DissolveUnionBoundingBox,FID_VGIboundingBox,[[FID_GNISboundingBox,"MAX"]])
arcpy.Clip_analysis(DissolveUnion,GNISnew,Clip_Shape)
arcpy.Clip_analysis(DissolveUnionBoundingBox,GNISboundingbox,Clip_BoundingBox)


JoinField(DissolveUnion,FID_VGI,VGInew,"FID","")
JoinField(DissolveUnion,Max_FID_GNIS,GNISnew,"FID","")
JoinField(DissolveUnion,FID_VGI,Clip_Shape,FID_VGI,"")

JoinField(DissolveUnionBoundingBox,FID_VGIboundingBox,VGIboundingbox,"FID","")
JoinField(DissolveUnionBoundingBox,Max_FID_GNIS_BoundingBox,GNISboundingbox,"FID","")
JoinField(DissolveUnionBoundingBox,FID_VGIboundingBox,Clip_BoundingBox,FID_VGIboundingBox,"")


addfield3(DissolveUnion)
addfield3(DissolveUnionBoundingBox)
Fnameunion=["SHAPE@","IntType","Shape_Area_1","Shape_Length_1","areVGI","areGNIS","vgiOVER_A","gnisOVER_A",FID_VGI,Max_FID_GNIS\
            ,"intersect","lengVGI","lengGNIS","vgiOVER_L","gnisOVER_L",VGI_FeatureName,GNIS_FeatureName,"LDistance","SequenceM","StringRat"\
            ,"StringPar","StrSort","StrSet","StringAvg","WeightAvg"]
FnameBoundingBox=["SHAPE@","IntType","Shape_Area_1","Shape_Length_1","areVGI","areGNIS","vgiOVER_A","gnisOVER_A",FID_VGIboundingBox,Max_FID_GNIS_BoundingBox\
            ,"intersect","lengVGI","lengGNIS","vgiOVER_L","gnisOVER_L"]
UpdateCursor3(DissolveUnion,Fnameunion)
UpdateCursor3(DissolveUnionBoundingBox,FnameBoundingBox)
arcpy.Near_analysis(VGILowerLeft,GNISLowerLeft)
arcpy.Near_analysis(VGIUpperRight,GNISUpperRight)
JoinField(VGILowerLeft,"FID",UnionShape,FID_VGI,"")
JoinField(VGIUpperRight,"FID",UnionShape,FID_VGI,"")
    ##Faster then this
    ##JoinField(UnionShape,FID_VGI,VGILowerLeft,"OBJECTID") and JoinField(UnionShape,FID_GNIS,VGIUpperRight,"OBJECTID")
arcpy.TableToDBASE_conversion([DissolveUnion,DissolveUnionBoundingBox,VGILowerLeft,VGIUpperRight],workspace)
end=datetime.datetime.now()
print "finished2", end-start




    


