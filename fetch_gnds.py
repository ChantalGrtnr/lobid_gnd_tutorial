# Fetch GNDs for person names

# import libraries
import pandas as pd
import requests

# https://lobid.org/gnd/api
# https://d-nb.info/standards/elementset/gnd


# check if list in response has one or multiple entries
# extract entry if only one exists
def transform_response_list(response):
    if len(response) > 1:
        print("multiple entries available")
    else:
        response = response[0]
        return (response)

#%%
# get or set list of persons
persons = ['August Wilhelm von Schlegel', 'FEHLENDER_NAME', 'Christian Gottlob Heyne']

#%%
# initialize empty list
persons_data = []

# loop over persons and fetch data
for person in persons:

    # build url
    url = f"https://lobid.org/gnd/search?q={person}&filter=type:Person&format=json"

    # fetch url
    response = requests.get(url)

    # if response is available: extract data
    if response.status_code == 200:

        # convert to json
        data = response.json()

        # process results for personname,
        # note: one person can have multiple results (member-entries)
        members = data.get('member', [])
        if len(members) > 0:
            # process only first 5 results (by default, 10 are returned)
            for member in members[0:5]:

                # extract gnd
                member_gnd = member.get('gndIdentifier', [])
                member_gnd_link = member.get('id', [])
                member_name = member.get('preferredName', [])

                # extract gender
                gender_data = member.get('gender')
                gender = [gender['label'] for gender in gender_data]
                gender = transform_response_list(gender)

                # extract type
                type_data = member.get('type')
                type_person = [i for i in type_data if i == "Person"]
                type_person = transform_response_list(type_person)

                # append fetched data
                persons_data.append({
                    'person_name_fetched' : person,
                    'gnd': member_gnd,
                    'gnd_link' : member_gnd_link,
                    'person_name_suggested' : member_name,
                    'gender' : gender,
                    'type' :type_person
                }
                )

                del member_gnd, member_gnd_link, member_name, gender_data, gender, type_data, type_person

        # if no members available: add person name to list
        else:
            # add only person name
            persons_data.append({
                'person_name_fetched': person,
            })

# convert to pandas dataframe
persons_data = pd.DataFrame(persons_data)

# select top entry for persons
persons_data_top = persons_data.groupby('person_name_fetched').first().reset_index()


