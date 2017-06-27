from functions import *

stages = ['Prospect', 'Qualified', 'Buying Process id.', 'Short List', 'Chosen Vendor', 'Negotiation/Review',
          'PO In Progress', 'Closed Won']
lost = ['Closed Deferred', 'Closed Lost']
# open stages
stages_open = list(set(stages) - set(lost) - set(['Closed Won']))

not_pipeline = ['Qualified','Qualification','Prospect','Re-Qualify']

# dict to order stages
stage_order = dict(zip(stages, xrange(0, len(stages))))

industry_map = {
    "Asset Management": "Financial Services",
    "Banking": "Financial Services",
    "Insurance": "Financial Services",
    "Financial Services: Other": "Financial Services",
    "Healthcare Payer": "Healthcare",
    "Healthcare Provider": "Healthcare",
    "Healthcare Payer and Provider": "Healthcare",
    "Technology": "Technology",
    "Government: Federal": "Federal",
    "Government": "Federal",
    "Government: State and Local": "Federal",
    "Life Sciences": "Life Sciences"}


# reporting dates for board reports - when opportunity Snapshot was run
rpt_dates_1 = ['10-15-2015','1-14-2016','4-14-2016','7-14-2016','10-14-2016','1-13-2017','4-14-2017','7-14-2017']
rpt_dates_1 = [pd.to_datetime(x) for x in rpt_dates_1]
rpt_dates_1 = [x.date() for x in rpt_dates_1]
rpt_dates_2 =['10-1-2015','11-5-2015','12-3-2015','1-7-2016','2-4-2016','3-3-2016','4-7-2016','5-5-2016','6-2-2016',
             '7-7-2016','8-5-2016','9-2-2016','10-7-2016','11-4-2016','12-2-2016','1-6-2017','2-3-2017','3-3-2017','4-7-2017',
             '5-5-2017','6-2-2017','7-7-2017','8-4-2017','9-1-2017']
rpt_dates_2 = [pd.to_datetime(x) for x in rpt_dates_2]
rpt_dates_2 = [x.date() for x in rpt_dates_2]

# dictionary with quarterly reporting dates
qt_rpt_dates = {
    pd.Period('2017Q1', freq = 'Q-SEP'):pd.to_datetime('2016-10-14').date(),
    pd.Period('2017Q2', freq = 'Q-SEP'):pd.to_datetime('2017-01-13').date(),
    pd.Period('2017Q3', freq = 'Q-SEP'):pd.to_datetime('2017-04-14').date(),
    pd.Period('2017Q4', freq = 'Q-SEP'):pd.to_datetime('2017-07-14').date()
}

qt_start_end_dates = {
    pd.Period('2017Q1', freq = 'Q-SEP'): [pd.to_datetime('2016-10-01').date(), pd.to_datetime('2016-12-31').date()],
    pd.Period('2017Q2', freq = 'Q-SEP'): [pd.to_datetime('2017-01-01').date(), pd.to_datetime('2017-03-31').date()],
    pd.Period('2017Q3', freq = 'Q-SEP'): [pd.to_datetime('2017-04-01').date(), pd.to_datetime('2017-06-30').date()],
    pd.Period('2017Q4', freq = 'Q-SEP'): [pd.to_datetime('2017-07-01').date(), pd.to_datetime('2017-09-30').date()]
}



# Field Event - leave as is bc John didnt update in SF per Marketing request to leave as is
lead_mapping = {'Rep List': 'Sales Rep',
                'Rep Sourced Social': 'SDR'}  #, 'Field Event':'Collibra Event'}

# Sales and Marketing sources
lead_source_mapping ={
    'Advertisement': 'Marketing', # this shouldnt be used anymore - old
    'Content Syndication': 'Marketing',
    'Direct Mail': 'Marketing',
    'Email': 'Marketing',
    'Field Event' : 'Marketing',
    'Paid Search': 'Marketing',
    'RainKing':'Marketing', # this shouldnt be used anymore - old
    'Seminar/Conference': 'Marketing',
    'Social Media': 'Marketing',
    'TechTarget': 'Marketing',
    'Webinar': 'Marketing',
    'Website': 'Marketing',
    'Database': 'Sales',  # this shouldnt be used anymore - old
    'External Referral': 'Sales', # this shouldnt be used anymore - old
    'Jigsaw': 'Sales',  # this shouldnt be used anymore - old
    'Partner': 'Sales',
    'Other': 'Sales', # this shouldnt be used anymore - old
    'Sales Operations':'Sales',
    'Sales Rep':'Sales',
    'SDR':'Sales',
    'University':'tbd'}

# these are the marketing sources - anything else is other
marketing_sources = ['Seminar/Conference', 'Website','Content Syndication', 'Paid Search',
                     'Webinar','Email','Field Event','Social Media']


# email blacklist for University and Community
blacklist = ["aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com","google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com","live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk","email.com", "games.com", "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com","lavabit.com", "love.com", "outlook.com", "pobox.com", "rocketmail.com","safe-mail.net", "wow.com", "ygm.com", "ymail.com", "zoho.com", "fastmail.fm","yandex.com","bellsouth.net", "charter.net", "comcast.net", "cox.net", "earthlink.net", "juno.com","btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk","ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk","virgin.net", "wanadoo.co.uk", "bt.com","sina.com", "qq.com", "naver.com", "hanmail.net", "daum.net", "nate.com", "yahoo.co.jp", "yahoo.co.kr", "yahoo.co.id", "yahoo.co.in", "yahoo.com.sg", "yahoo.com.ph","hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr", "sfr.fr", "neuf.fr", "free.fr","gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de", "web.de", "yahoo.de","mail.ru", "rambler.ru", "yandex.ru", "ya.ru", "list.ru","hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be", "telenet.be","hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar","hotmail.com", "gmail.com", "yahoo.com.mx", "live.com.mx", "yahoo.com", "hotmail.es", "live.com", "hotmail.com.mx", "prodigy.net.mx", "msn.com","yahoo.com.br", "hotmail.com.br", "outlook.com.br", "uol.com.br", "bol.com.br", "terra.com.br", "ig.com.br", "itelefonica.com.br", "r7.com", "zipmail.com.br", "globo.com", "globomail.com", "oi.com.br"]



# fix number of employees
num_emp_dict ={
    '1-100': 'less_than_100',
    '101-500': 'less_than_500',
    '501-1,500': 'less_than_1500',
    '1,501-5,000': 'less_than_50k',
    '5,001-10,000': 'less_than_10k',
    '10000+': 'more_than_10k',
    '10,001+': 'more_than_10k',
    'missing': 'missing_emp',
    'Unknown': 'missing_emp'
}