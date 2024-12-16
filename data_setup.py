
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import json
import pandas as pd
import os

# Current year
current_year = datetime.now().year

# Year 12 months before
twelve_months_ago = datetime.now() - relativedelta(months=12)
year_before_twelve_months = twelve_months_ago.year


class LaborData():

    api_details = {"Civilian Labor Force (Seasonally Adjusted)" :  "LNS11000000",
                    "Civilian Employment (Seasonally Adjusted)" : "LNS12000000",
                    "Civilian Unemployment (Seasonally Adjusted)" : "LNS13000000",
                    "Unemployment Rate (Seasonally Adjusted)" : "LNS14000000",
                    "Total Nonfarm Employment - Seasonally Adjusted" : "CES0000000001",
                    "Total Private Average Weekly Hours of All Employees - Seasonally Adjusted" : "CES0500000002",
                    "Total Private Average Weekly Hours of Prod. and Nonsup. Employees - Seasonally Adjusted" : "CES0500000007",
                    "Total Private Average Hourly Earnings of All Employees - Seasonally Adjusted" : "CES0500000003",
                    "Total Private Average Hourly Earnings of Prod. and Nonsup. Employees - Seasonally Adjusted" : "CES0500000008"}
    

    def __init__(self,owner):

        self.owner = owner

        self.__initial_complete=False
    


    def __initial_data_setup(self):

        'sets initial data into csv files from one year back'

        # Folder name
        folder_name = "data"

        # Check if the folder exists, and create it if not
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # api call
        
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": list(LaborData.api_details.values()),
                        "registrationkey":"a6c97b6640ab45489a842ab39eb27c7f",
        "startyear":str(year_before_twelve_months),"endyear":current_year})
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

        # creating dataframe

        json_data = json.loads(p.text)

        seried_tables={}

        for serial_id in LaborData.api_details.values():

            data_obj = [x for x in json_data['Results']['series'] if x['seriesID'] ==serial_id]

            df_table = pd.DataFrame.from_dict(data_obj[0]['data'],orient='columns')

            seried_tables[serial_id]=df_table

            df_table.to_csv('data/'+serial_id+'.csv',index=False)
        
        self.__initial_complete=True

        return {'status':"Success"}
    

    def fulfill_incremantal_load(self):

        # api call        
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": list(LaborData.api_details.values()),'latest':True,"registrationkey":"a6c97b6640ab45489a842ab39eb27c7f"})
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

        json_data = json.loads(p.text)

        for serial_id in LaborData.api_details.values():

            data_obj = [x for x in json_data['Results']['series'] if x['seriesID'] ==serial_id]

            orig_table = pd.read_csv('data/'+serial_id+'.csv')

            df_table = pd.DataFrame.from_dict(data_obj[0]['data'],orient='columns')

            # Append df2 to df1
            combined_df = pd.concat([orig_table, df_table], ignore_index=True)

            combined_df.loc[:,'year']=combined_df['year'].astype(str)

            # Remove duplicates based on 'col1' and 'col2'
            unique_df = combined_df.drop_duplicates(subset=['year','periodName'])

            # print(unique_df.sort_values(by=['year','periodName']))

            unique_df.to_csv('data/'+serial_id+'.csv',index=False)

        
        return {"status":"Incremental Successful"}
    

    def data_setup(self):

        if self.__initial_complete==False:

            print('running initial load')

            self.__initial_data_setup()
        
        else:

            self.fulfill_incremantal_load()

            print('running initial load')
        
        return {"status":"Data refreshed"}




   
if __name__ =='__main__':

    instance = LaborData(owner='developer')

    instance.data_setup()
