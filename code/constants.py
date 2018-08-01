
# mode = "EMA"
mode = "DS02"

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

elif mode == "DS02":
    int2tags = ['NA', '/location/location/contains', '/people/person/nationality', '/people/person/place_lived', '/business/company/founders', '/people/deceased_person/place_of_death', '/business/person/company', '/location/us_county/county_seat', '/business/company/place_founded', '/people/person/place_of_birth', '/film/film/featured_film_locations', '/people/person/children', '/location/neighborhood/neighborhood_of', '/location/country/administrative_divisions', '/location/country/capital', '/people/ethnicity/included_in_group', '/people/place_of_interment/interred_here', '/location/administrative_division/country', '/time/event/locations', '/location/de_state/capital', '/location/us_state/capital', '/business/company_advisor/companies_advised', '/people/person/religion', '/people/deceased_person/place_of_burial', '/people/person/ethnicity', '/sports/sports_team/location', '/broadcast/content/location', '/film/film_festival/location', '/location/it_region/capital', '/business/shopping_center_owner/shopping_centers_owned', '/people/person/profession', '/business/company/major_shareholders', '/location/in_state/legislative_capital', '/location/in_state/administrative_capital', '/business/business_location/parent_company', '/people/family/members', '/location/jp_prefecture/capital', '/film/film_location/featured_in_films', '/people/family/country', '/business/company/locations', '/people/ethnicity/includes_groups', '/business/company/advisors', '/people/profession/people_with_this_profession', '/location/br_state/capital', '/location/cn_province/capital', '/broadcast/producer/location', '/location/fr_region/capital', '/people/ethnicity/geographic_distribution', '/location/province/capital', '/location/in_state/judicial_capital', '/business/shopping_center/owner', '/location/mx_state/capital']
    tags2int = {'NA':0, '/location/location/contains':1, '/people/person/nationality':2, '/people/person/place_lived':3, '/business/company/founders':4, '/people/deceased_person/place_of_death':5, '/business/person/company':6, '/location/us_county/county_seat':7, '/business/company/place_founded':8, '/people/person/place_of_birth':9, '/film/film/featured_film_locations':10, '/people/person/children':11, '/location/neighborhood/neighborhood_of':12, '/location/country/administrative_divisions':13, '/location/country/capital':14, '/people/ethnicity/included_in_group':15, '/people/place_of_interment/interred_here':16, '/location/administrative_division/country':17, '/time/event/locations':18, '/location/de_state/capital':19, '/location/us_state/capital':20, '/business/company_advisor/companies_advised':21, '/people/person/religion':22, '/people/deceased_person/place_of_burial':23, '/people/person/ethnicity':24, '/sports/sports_team/location':25, '/broadcast/content/location':26, '/film/film_festival/location':27, '/location/it_region/capital':28, '/business/shopping_center_owner/shopping_centers_owned':29, '/people/person/profession':30, '/business/company/major_shareholders':31, '/location/in_state/legislative_capital':32, '/location/in_state/administrative_capital':33, '/business/business_location/parent_company':34, '/people/family/members':35, '/location/jp_prefecture/capital':36, '/film/film_location/featured_in_films':37, '/people/family/country':38, '/business/company/locations':39, '/people/ethnicity/includes_groups':40, '/business/company/advisors':41, '/people/profession/people_with_this_profession':42, '/location/br_state/capital':43, '/location/cn_province/capital':44, '/broadcast/producer/location':45, '/location/fr_region/capital':46, '/people/ethnicity/geographic_distribution':47, '/location/province/capital':48, '/location/in_state/judicial_capital':49, '/business/shopping_center/owner':50, '/location/mx_state/capital':51}
