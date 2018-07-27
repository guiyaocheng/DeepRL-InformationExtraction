
# mode = "EMA"
mode = "DS"

if mode == "Shooter":
    #for Shooter DB
    int2tags = ['shooterName','killedNum', 'woundedNum', 'city']
    tags2int = {'TAG':0,\
    'shooterName':1, \
    'killedNum':2, \
    'woundedNum':3, \
    'city' : 4 }

elif mode == "EMA":
    # for EMA
    int2tags = \
    ['Affected-Food-Product',\
    'Produced-Location',\
    'Adulterant(s)']
    tags2int = \
    {'TAG':0,\
    'Affected-Food-Product':1, \
    'Produced-Location':2, \
    'Adulterant(s)':3}
    int2citationFeilds = ['Authors', 'Date', 'Title', 'Source']
    generic = ["city", "centre", "county", "street", "road", "and", "in", "town", "village"]

elif mode == "DS":
    int2tags = ['relation','entity_1','entity_2']
    tags2int = {'TAG':0,  'relation':1, 'entity_1':2, 'entity_2':3}