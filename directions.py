import urllib.request
import json
import pandas as pd


baseUrl = "https://maps.googleapis.com/maps/api/directions/json?"

def get_time(p1,p2):
    origin = ",".join(map(str, p1))
    dest = ",".join(map(str, p2))
    url = baseUrl + "origin=" + origin + "&destination=" + dest + "&key=AIzaSyBj9QH_Jh9n13CKOk_Dxi7YjvdvCIBzwXk"
    result = json.loads(urllib.request.urlopen(url).read().decode())
    print(result["routes"][0]["legs"][0]["duration"]["value"])
    return result["routes"][0]["legs"][0]["duration"]["value"]


def convert_time(t):
    t = int(t)
    hours = int(t/3600)
    t = t%3600
    mins = int(t/60)
    t = t%60
    seconds = t
    print(hours,mins,seconds)
    return'{0:02d}'.format(hours) + ":" + '{0:02d}'.format(mins) + ":" + '{0:02d}'.format(seconds)

file = "C:/Users/NWatson/Desktop/3398-SCO west midlands box thresholds/Project Schedule - West Midlands Motorway Box - 3398SCO V7 (PF Comments).xlsx"
result = []
df = pd.read_csv("results.csv")
sites = df["Origin"].unique()
for orig in sites:
    for dest in sites:
        if orig != dest:
            if not df[(df["Origin"] == orig) & (df["Destination"] == dest)].values.tolist() in result:
                result.append(df[(df["Origin"] == orig) & (df["Destination"] == dest)].values.tolist())
            if not df[(df["Origin"] == dest) & (df["Destination"] == orig)].values.tolist() in result:
                result.append(df[(df["Origin"] == dest) & (df["Destination"] == orig)].values.tolist())

result = [item[0] for item in result]
df = pd.DataFrame(result)
print(df)
df.to_csv("formatted results.csv")


exit()
###
### below code downloads the direction data
###
df = pd.read_excel(file,sheetname="Project Detail (BT)")
df["Site No."] = df["Site No."].astype(str)
sites = df[["Site No.","Latitude","Longitude"]].values.tolist()
print(sites)
result = []#pd.DataFrame(columns=["Origin","Destination","Time"])
for origin in sites[:35]:
    for destination in sites[:35]:
        if origin != destination:
            t = get_time(origin[1:],destination[1:])
            result.append([origin[0],destination[0],t])
df = pd.DataFrame(result)
df.columns=["Origin","Destination","Time"]
df["Time"]=df["Time"].apply(convert_time)
print(df)
df.to_csv("results.csv")
exit()



p1 = [52.514065,-1.979323]
p2 = [52.318967,-2.096683]


get_time(p1,p2)
exit()

#print(result["routes"])

for v in result["routes"]:
    print(v["legs"])
    for leg in v["legs"]:
        print(leg["duration"])