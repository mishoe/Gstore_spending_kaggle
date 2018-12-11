import pickle
import seaborn as sns
import pandas as pd
from datetime import datetime
import holidays
from workalendar import europe,america,oceania,africa,asia
from bdateutil import isbday
import numpy as np
date_col = 'date'


#data = pd.read_csv('data/test_v2.csv')

#train data from 8/1/2016 - 8/1/2017
data = pd.read_pickle('data/train.p')
#test_data from  8/2/2017 - 4/30/2018
#test_data = pd.read_pickle('data/test.p')


#sns.distplot(data['visitStartTime'])
date = list(map(lambda x: datetime.strptime(str(x), '%Y%m%d'),data[date_col]))

def generate_date_based_cols(data,date_col):
    dates = list(map(lambda x: datetime.strptime(str(x), '%Y%m%d'),data[date_col]))
    data['DayOfMonth'] = list(map(lambda x: x.day,dates))
    data['DayOfWeek'] = list(map(lambda x: x.isoweekday(),dates))
    data['Month']= list(map(lambda x: x.month,dates))
    data['isBusinessDay'] = list(map(lambda x: 1*isbday(x),dates))
    return data

data = generate_date_based_cols(data,date_col)

ad_content_merch_list = ['gear','merchandise','sunglass','toy','apparel','paraphernalia','stickers','shirt','swag','bag']
data['geoNetwork_networkDomain']= list(map(lambda x:x.lower().replace('.',' ')
                                                if x!=None else None
                                                 ,data['geoNetwork_networkDomain']))
data['address_extention'] = list(map(lambda x: x[x.find('.'):].replace('.','_') if x.find('.')!=-1 else None,data['geoNetwork_networkDomain']))
data['has_dot_com'] = list(map(lambda x: 1 if x.lower().__contains__('.com') else 0 ,data['geoNetwork_networkDomain']))
data['has_dot_net'] = list(map(lambda x: 1 if x.lower().__contains__('.net') else 0 ,data['geoNetwork_networkDomain']))
data['trafficSource_referralPath_seq'] = list(map(lambda x:x.replace('/','::'),data['trafficSource_referralPath']))
data['trafficSource_isTrueDirect'] = list(map(lambda x:0 if x==None else 1,data['trafficSource_isTrueDirect']))

#.translate(None, '0123456789')
data['trafficSource_adContent']= list(map(lambda x:x.lower().replace('{keyword:','')
                                                 .translate({ord(c):'' for c in '0123456789?{}/%!'})
                                                if x!=None else None
                                                 ,data['trafficSource_adContent']))
data['trafficSource_adContent_google']= list(map(lambda x:1 if x!=None and x.lower().__contains__('google') else 0
                                                 ,data['trafficSource_adContent']))
data['trafficSource_campaign_AW']= list(map(lambda x:1 if x!=None and x.lower().__contains__('aw') else 0
                                                 ,data['trafficSource_campaign']))

data['trafficSource_source']= list(map(lambda x:x.lower().replace('.',' ')
                                                 .replace(':',' ')
                                                if x!=None else None
                                                 ,data['trafficSource_source']))
col_dict = {'cat_cols':['channelGrouping','socialEngagementType','device_operatingSystem',
                        'device_browser','device_isMobile','device_deviceCategory','geoNetwork_subContinent',
                        'geoNetwork_metro','networkDomain','geoNetwork_continent','geoNetwork_region','geoNetwork_country',
                        'trafficSource_referralPath','trafficSource_adContent','trafficSource_medium'],
            'cat_from_text_cols':['trafficSource_referralPath_seq'],
            'zero_impute_cols':['DayOfMonth','DayOfWeek','Month','isBusinessDay','has_dot_com','has_dot_net',
                                'trafficSource_adContent_google','trafficSource_campaign_AW','trafficSource_isTrueDirect',
                                'totals_bounces','totals_hits','totals_newVisits','totals_pageviews','totals_visits','visitNumber'],
            'text_cols':['trafficSource_keyword','geoNetwork_networkDomain','trafficSource_source']}

all_used_cols = [col for key in col_dict.keys() for col in col_dict.get(key)]
set(data.columns) - set(all_used_cols)




