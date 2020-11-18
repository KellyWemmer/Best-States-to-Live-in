#!/usr/bin/env python
# coding: utf-8

# The purpose of this project is to find a state and county within the United States for us to buy a home.

# In[5]:


#Combine both CSV's and average rankings
#Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.express as px
import plotly.graph_objs as go 


# In[6]:


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# In[7]:


init_notebook_mode(connected=True)


# In[8]:


#downloaded from https://www.usnews.com/news/best-states/rankings
best = pd.read_csv('BestStates.csv')
best


# In[9]:


#Need to remove NAN
best = best.dropna(how='any')
best.info()


# In[10]:


# Abbreviate state names
def convert_state_name(name):
    code=str(name)
    us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
    return us_state_abbrev[code]

best['Code'] = best.State.apply(lambda x:convert_state_name(x)) 


# In[11]:


#Change order of columns in order of weight
best = best[['State', 'Code', 'Health Care', 'Economy', 'Natural Environment', 'Crime & Corrections', 'Opportunity', 'Fiscal Stability', 'Infrastructure', 'Education']]
best


# In[12]:


#downloaded from https://worldpopulationreview.com/state-rankings/states-with-lowest-cost-of-living
cheap = pd.read_csv('CheapestStates.csv')
cheap


# In[13]:


cheap = cheap[['State', 'costRank']]
cheap


# In[14]:


#Merge datasets
states = pd.merge(best, cheap, on='State', how='inner')
states.rename(columns={'costRank':'Cost Rank'}, inplace=True)
states['Cost Rank'] = states['Cost Rank'].astype(float)
states


# In[15]:


#Create chart of weights of best state categories

labels = 'Health Care', 'Economy', 'Crime & Corrections', 'Natural Environment', 'Opportunity', 'Fiscal Stability', 'Infrastructure', 'Education'
sizes = [16, 16, 14, 14, 12, 10, 10, 8]

fig1, ax1 = plt.subplots(figsize = (8,8))
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.title('Weighted Average of Best States Categories')

plt.show();


# In[16]:


#Create columns for weighted totals
states['Healthcare Weight'] = states['Health Care']*16
states['Economy Weight'] = states['Economy']*16
states['Crime Weight'] = states['Crime & Corrections']*14
states['Environment Weight'] = states['Natural Environment']*14
states['Opportunity Weight'] = states['Opportunity']*12
states['Fiscal Weight'] = states['Fiscal Stability']*10
states['Infrastructure Weight'] = states['Infrastructure']*10
states['Education Weight'] = states['Education']*8
states


# In[17]:


#Create column of weighted average of best city traits
states['Best States Weighted Average'] = (states.loc[:, 'Healthcare Weight':'Education Weight'].sum(axis=1))/100
states


# In[18]:


#Create average score of weighted best city score and cost of living score
states['Total Score'] = states[['Cost Rank', 'Best States Weighted Average']].mean(axis=1)
states.sort_values(by=['Total Score'])


# In[19]:


#Map the Lowest Cost of Living States
states['text1']= states['State']


# Color Scales Options<br>
# 
#             'aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
#              'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
#              'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
#              'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
#              'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
#              'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
#              'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
#              'orrd', 'oryel', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
#              'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor',
#              'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy',
#              'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral',
#              'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose',
#              'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'twilight',
#              'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd'.

# In[20]:


data1 = dict(type='choropleth',
            colorscale = 'agsunset',
            locations = states['Code'],
            z = states['Cost Rank'],
            locationmode = 'USA-states',
            text = states['text1'],
            marker = dict(line = dict(color = 'rgb(255,255,255)',width = 2)),
            #marker = set of nested dictionaries that define a marker rgb = red, green, blue
            #separates states with line thickness and color
            colorbar = {'title':"Cost of Living"}
            ) 


# In[21]:


layout1 = dict(title = 'State Rankings of Lowest Cost of Living',
              geo = dict(scope='usa', 
                         showlakes = True,
                         lakecolor = 'rgb(85,173,240)') 
             )


# In[22]:


choromap1 = go.Figure(data = [data1],layout = layout1)


# In[23]:


iplot(choromap1)


# In[24]:


#Map the Best states to live in ranking
states['text2']= states['State']


# In[25]:


data2 = dict(type='choropleth',
            colorscale = 'armyrose',
            locations = states['Code'],
            z = states['Best States Weighted Average'],
            locationmode = 'USA-states',
            text = states['text2'],
            marker = dict(line = dict(color = 'rgb(255,255,255)',width = 2)),
            #marker = set of nested dictionaries that define a marker rgb = red, green, blue
            #separates states with line thickness and color
            colorbar = {'title':"Best States"}
            ) 


# In[26]:


layout2 = dict(title = 'State Rankings of Best States to Live in',
              geo = dict(scope='usa', 
                         showlakes = True,
                         lakecolor = 'rgb(85,173,240)') 
             )


# In[27]:


choromap2 = go.Figure(data = [data2],layout = layout2)


# In[28]:


iplot(choromap2)


# In[29]:


#Map the average of Best States Ranking with Low Cost of Living
states['text']= states['State']+'<br>Cost Rank  ' + states['Cost Rank'].astype(str)+ '<br>Best States Average Rank '+states['Best States Weighted Average'].astype(str)
states['text']


# In[30]:


data = dict(type='choropleth',
            colorscale = 'viridis',
            locations = states['Code'],
            z = states['Total Score'],
            locationmode = 'USA-states',
            text = states['text'],
            marker = dict(line = dict(color = 'rgb(255,255,255)',width = 2)),
            #marker = set of nested dictionaries that define a marker rgb = red, green, blue
            #separates states with line thickness and color
            colorbar = {'title':"Average Ranking"}
            ) 


# In[31]:


layout = dict(title = 'Best States with Low Cost of Living',
              geo = dict(scope='usa', 
                         showlakes = True,
                         lakecolor = 'rgb(85,173,240)') 
             )


# In[32]:


choromap = go.Figure(data = [data],layout = layout)


# In[33]:


iplot(choromap)


# Washington, Oregon, and Colorado seem to be our preferences for states to live in.

# In[ ]:




