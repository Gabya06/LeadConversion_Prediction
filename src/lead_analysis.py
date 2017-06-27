import pandas as pd
import numpy as np
import re
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
# from functions import login_salesforce, get_SF_data
from loadvar import *
from title_functions import *
from sklearn import preprocessing

conn_SF = login_salesforce()
today = dt.today()


q = "select l.FirstName, l.LastName, l.Title, l.Title_Score__c, l.Job_Title_Match__c, l.email, "
q += "l.CreatedDate, l.IsConverted, l.Status, l.CountryCode, l.CurrencyIsoCode, l.Number_of_Employees__c, "
q += "l.Department__c, l.Eloqua_Score_Card__c, l.Communication_Status__c, l.Community_Registered_User__c, "
q += "l.University_Registered_User__c, l.University_Steward__c, l.HasOptedOutofEmail, "
q+=  "l.Industry, l.Industry_Wave__c, l.Company, "
q += "l.Last_Responded_Campaign_Type__c, l.Last_Responded_Date__c, l.LastActivityDate, l.Latest_Campaign__c, "
q += "l.Lead_Type__c, l.LeadSource, l.LeanData__Reporting_Matched_Account__c, "
q += "l.LeanData_Matched_Account_Owner__c, l.LeanData_Matched_US_Region__c, l.Managed_By__c, "
q += "l.OwnerId, u.Name as lead_owner, u.Division as lead_owner_division, u.Department as lead_owner_dept, "
q += "l.Phone, l.Phone_No_2__c, l.Previously_Active_Sequence__c, l.Use_Case__c, l.Website "
q += "from dbo.Lead l "
q += "inner join dbo.[User] as u "
q += 'on l.OwnerId = u.Id'


df_leads = get_SF_data(connection=conn_SF, query_string=q)

# remove columns where more than 70% info is missing
empty_cols = pd.DataFrame(data = df_leads.isnull().sum()/df_leads.shape[0], columns = ['perc_empty'])
empty_cols = empty_cols.reset_index()
cols_remove = empty_cols[empty_cols.perc_empty >.7]['index']
df_leads = df_leads.drop(cols_remove, axis=1)

# add grouped industry
df_leads['grouped_industry'] = df_leads.Industry.map(lambda x: industry_map.get(x,'Other'))
# add updated lead source
df_leads['lead_source_updated'] = df_leads.LeadSource.map(lambda x: lead_source_mapping.get(x))

# add if there is a lean Data account
df_leads['has_leanData_acct'] = [0 if pd.isnull(i) else 1 for i in df_leads.LeanData__Reporting_Matched_Account__c]
# add if there is a phone number
df_leads['has_phone'] = [0 if pd.isnull(i) else 1 for i in df_leads.Phone]
#df_leads.Phone.str.replace('\+1.','').value_counts().tail()

df_leads['email_sig'] = ['Missing' if (i == None or pd.isnull(i)) else i for i in df_leads.email]
df_leads['email_sig'] = ['Missing' if i =='Missing' else re.findall('@.+', i)[0] for i in df_leads.email_sig]
df_leads['email_sig'] = df_leads.email_sig.map(lambda  x: x.replace('@', ''))
    #df_leads.email_sig.map(lambda x: re.findall('@.+', x))
# df_leads['email_sig'] = ['Missing' if i =='Missing' else i[0] for i in df_leads.email_sig]
# is email in blacklist
df_leads['email_blacklisted'] = [1 if i in blacklist else 0 for i in df_leads.email_sig]
# convert dates
df_leads.CreatedDate = df_leads.CreatedDate.map(lambda  x: np.datetime64(x))
df_leads.LastActivityDate = df_leads.LastActivityDate.map(lambda  x: np.datetime64(x))
# add quarter created
df_leads['quarterCreated'] = df_leads.CreatedDate.dt.to_period('Q-SEP')

# was lead active more than 2 weeks ago?
two_wks_ago = today - relativedelta(days = 2)
df_leads['active_over_2wks_ago'] = df_leads.LastActivityDate < two_wks_ago

# title into bins
df_leads.Title_Score__c = [np.int(i) if not pd.isnull(i) else np.nan for i in df_leads.Title_Score__c]
df_leads['title_score_bin'] = pd.cut(df_leads.Title_Score__c, bins = 5, right = False)

# add job level
df_leads.Title.map(lambda title: get_title_points(title=title, level_list= levels, **title_mapping_args))

# is 1st name missing
df_leads['missing_firstname'] = [1 if pd.isnull(i) else 0 for i in df_leads.FirstName]

# is title missing
df_leads['missing_title'] = [1 if pd.isnull(i) else 0 for i in df_leads.Title]

# response
df_leads['IsConverted_2'] = [1 if True else 0 for x in df_leads.IsConverted]

# look only at US Data
df_us = df_leads[df_leads.CountryCode == 'US']
df_us = df_us.drop('CountryCode',axis=1)

# fill in rest of columns with missing values/NAs:
cols_dates = ['CreatedDate','LastActivityDate']
for c in df_leads.drop(cols_dates, axis =1).columns:
    nulls = df_leads[c].isnull().sum()
    if nulls >0:
        print c, df_leads[c].dtype, df_leads[c].isnull().sum()
        df_leads[c] = df_leads[c].fillna('missing')

##TODO: encode labels


# to encode labels
le = preprocessing.LabelEncoder()
le.fit(df_leads.CountryCode)
le.transform(df_leads.CountryCode)

conn_SF.close()