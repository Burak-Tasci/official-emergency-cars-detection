from Json2PascalVoc.Converter import Converter
import glob
import json

for file in glob.glob("./*.json"):
    data = json.load(open(file))
    filename = data["asset"]["name"][:-4]
    filename = ".\\"+filename+".xml"
    print(file)
    open(filename,"w")
    Converter.convertJsonToPascal(file,filename)

