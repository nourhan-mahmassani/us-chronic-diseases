import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode,iplot
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time
import datetime as dt
import base64
from PIL import Image


st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#F5F5F5,#F5F5F5);
    color: black;
}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown("""<style> body {
    background-image: url("https://www.toptal.com/designers/subtlepatterns/patterns/spikes.png");
  background-repeat: repeat;


} </style>""", unsafe_allow_html=True)
st.markdown(""" <style>body {
  margin: 40px;
}

.box {
  background-color: #444;
  color: #fff;
  border-radius: 5px;
  padding: 20px;
  font-size: 150%;
}

.box:nth-child(even) {
  background-color: #ccc;
  color: #000;
}

.wrapper {
  width: 600px;
  display: grid;
  grid-gap: 10px;
  grid-template-columns: repeat(6, 100px);
  grid-template-rows: 100px 100px 100px;
  grid-auto-flow: column;
}</style>""",unsafe_allow_html=True)


# #######################################################################
@st.cache(allow_output_mutation=True,persist=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
DATA_URL = ('Output.csv')
@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)

    # del data['response']
    # del data['stratificationcategory3']
    # del data['stratificationcategory2']
    # del data['stratificationcategory1']
        #del data['stratificationid2']
    # del data['stratificationcategoryid3']
    # del data['stratification3']
    # del data['responseid']
    # del data['stratificationcategoryid2']
    # del data['stratificationid2']
#    del data['stratificationcategoryid3']
    # del data['stratificationid3']
    df=pd.DataFrame(data['geolocation'].str.strip('()')                               \
                   .str.split(', ', expand=True)                   \
                       .rename(columns={0:'latitude', 1:'longitude'}))
    data = pd.concat([data, df], axis=1)

    # first lets fix the type of each column in the dataframe


    data['yearend']=data['yearend'].apply(lambda x: pd.to_datetime(str(x), format='%Y'))
    data['yearstart']=data['yearstart'].apply(lambda x: pd.to_datetime(str(x), format='%Y'))
    data['latitude']=pd.to_numeric(data['latitude'])
    data['longitude']=pd.to_numeric(data['longitude'])
    #Convert to numeric using 'coerce' which fills bad values with 'nan'
    data['datavalue']=pd.to_numeric(data['datavalue'],errors='coerce')
    print(data.columns)

    return data


# Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# ####################################################################################################################################################################
#Create Mortality_df
Mortality_list=["Mortality with chronic obstructive pulmonary disease as underlying cause among adults aged >= 45 years",
"Mortality with diabetic ketoacidosis reported as any listed cause of death",
"Mortality from total cardiovascular diseases",
"Mortality with chronic obstructive pulmonary disease as underlying or contributing cause among adults aged >= 45 years",
"Mortality from coronary heart disease",
"Mortality from diseases of the heart",
"Mortality due to diabetes reported as any listed cause of death",
"Mortality from cerebrovascular disease (stroke)",
"Mortality with end-stage renal disease",
"Mortality from heart failure"]
Mortality_df=data.loc[(data['question'].isin(Mortality_list) ) & (data['stratificationcategoryid1']=='OVERALL') & (data['datavalueunit']=='cases per 100,000')& (data['datavaluetype']=='Age-adjusted Rate')]
Mortality_df["year"]=Mortality_df["yearend"].dt.year
#Create Hospitalization_df
Hospitalization_list=["Hospitalization for acute myocardial infarction" , "Hospitalization for heart failure among Medicare-eligible persons aged >= 65 years" , "Hospitalizations for asthma" , "Hospitalization for stroke" , "Hospitalization with diabetes as a listed diagnosis"]
Hospitalization_df=data.loc[(data['question'].isin(Hospitalization_list) ) & (data['stratificationcategoryid1']=='OVERALL') & (data['datavaluetype']=='Number')]
Hospitalization_df["year"]=Hospitalization_df["yearend"].dt.year
#Create Prevalence_df
Prevalence_list=["Prevalence of diagnosed diabetes among adults aged >= 18 years",
"Prevalence of high blood pressure among adults aged >= 18 years with diagnosed diabetes",
"Prevalence of depressive disorders among adults aged >= 18 years with diagnosed diabetes",
"Current asthma prevalence among adults aged >= 18 years",
"Asthma prevalence among women aged 18-44 years",
"Diabetes prevalence among women aged 18-44 years",
"Prevalence of chronic kidney disease among adults aged >= 18 years",
"Prevalence of high cholesterol among adults aged >= 18 years with diagnosed diabetes",
"High cholesterol prevalence among adults aged >= 18 years",
"Prevalence of gestational diabetes",
"Prevalence of pre-pregnancy diabetes"
  ]
Prevalence_df=data.loc[(data['question'].isin(Prevalence_list)) & (data['stratificationcategoryid1']=='OVERALL')]
Prevalence_df["year"]=Prevalence_df["yearend"].dt.year

# ######################################################################################################################################################################
## to hide the streamlit text in the bottom of the page
hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



data['year']=pd.DatetimeIndex(data['yearend']).year
data=data.dropna(subset=['datavalue'])
col1,col2=st.columns((4,1))
col2.image ('https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/US_CDC_logo.svg/1200px-US_CDC_logo.svg.png',width=200)
image=Image.open('title.png')
st.image(image)

st.sidebar.markdown("<h2> Table of Contents",unsafe_allow_html=True)
navigation=st.sidebar.radio('Navigate pages',['Data Overview','Mortality Data Analysis','Hospitalization Data Analysis', 'Prevalence Data Analysis'])
if navigation=='Data Overview':
    st.markdown("""<h2> <b>Data Information </h2>""",unsafe_allow_html=True)
    st.markdown("""<br><div>The dataset contains the following columns:</div><br>""",unsafe_allow_html=True)
    st.markdown("""<div role="tabpanel" aria-labelledby="tab-title-data_fields_-tab" style="display: block;"><div><div><div><table><tbody><tr><th>Name</th><th>Description</th><th>Type</th></tr><tr><td>Year_Start</td><td>Identifies the year when reporting started.</td><td>date</td></tr><tr><td>Year_End</td><td>Identifies the year when reporting ends.</td><td>date</td></tr><tr><td>State_Abbreviation</td><td>Two-character postal abbreviation for state name.</td><td>string</td></tr><tr><td>State_Name</td><td>Name of U.S State or District of Columbia.</td><td>string</td></tr><tr><td>Data_Source</td><td>Identifies the source from where the data is collected.</td><td>string</td></tr><tr><td>Topic</td><td>Identifies the Chronic Disease topic.</td><td>string</td></tr><tr><td>Question</td><td>Identifies Chronic Disease Indicator.</td><td>string</td></tr><tr><td>Data_Value_Unit</td><td>Identifies unit of the data value.</td><td>string</td></tr><tr><td>Data_Value_Type</td><td>Identifies the type of data value.</td><td>string</td></tr><tr><td>Data_Value</td><td>Identifies the actual value of the data. The responses that are in other form than numbers are:</td><td>string</td></tr><tr><td>Data_Value_Alt</td><td>Identifies the alternate data value. The responses that are in another form than numbers have been eliminated and replaced with blank values here.</td><td>number</td></tr><tr><td>Data_Value_Footnote</td><td>Identifies Footnotes for data values.</td><td>string</td></tr><tr><td>Low_Confidence_Limit</td><td>Lower Confidence Interval.</td><td>number</td></tr><tr><td>High_Confidence_Limit</td><td>Higher Confidence Interval.</td><td>number</td></tr><tr><td>Stratification_Category_1</td><td>Identifies the sampling category of the population.</td><td>string</td></tr><tr><td>Stratification1</td><td>Identifies the sampling sub category of the population.</td><td>string</td></tr><tr><td>Latitude</td><td>Identifies the geographical location Latitude.</td><td>number</td></tr><tr><td>Longitude</td><td>Identifies the geographical location Longitude.</td><td>number</td></tr><tr><td>Location_ID</td><td>Location identity.</td><td>string</td></tr><tr><td>Topic_ID</td><td>Short form of Chronic Disease Category.</td><td>string</td></tr><tr><td>Question_ID</td><td>Short form of Chronic Disease Indicator.</td><td>string</td></tr><tr><td>Data_Value_Type_ID</td><td>Represents the short form of the data value type.</td><td>string</td></tr><tr><td>Stratification_Category_ID1</td><td>Identifies the sampling category in short form.</td><td>string</td></tr><tr><td>Stratification_ID1</td><td>Identifies the sampling sub category in short form.</td><td>string</td></tr></tbody></table></div></div></div></div>""",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("Source: https://healthdata.gov/dataset/us-chronic-disease-indicators-cdi ",unsafe_allow_html=True)
    col1,col2=st.columns(2)

    if col1.checkbox('Show inforamtion for each column'):
        col1.write(data.describe())

        if col2.checkbox('Show indicators in the dataset'):
            col2.write(data.question.unique())
    Filtered_data=st.multiselect("Filter the data you want by selecting the columns you want",data.columns.tolist())
    st.write(data.filter(Filtered_data).head(25))

if navigation=='Mortality Data Analysis':

    st.markdown("""<h2><b>Mortality Data Analysis</h2>""",unsafe_allow_html=True)
    st.markdown("""<h3><p>A mortality rate is a measure of the frequency of occurrence of death in a defined population during a specified interval. Morbidity and mortality measures are often the same mathematically; it’s just a matter of what you choose to measure, illness or death. The formula for the mortality of a defined population, over a specified period of time.</p></h3>""",unsafe_allow_html=True)
    st.markdown("""<h3><b>Age-specific mortality rate</b></h3>""",unsafe_allow_html=True)
    st.markdown("""<p>An age-specific mortality rate is a mortality rate limited to a particular age group. The numerator is the number of deaths in that age group; the denominator is the number of persons in that age group in the population. In the United States in 2003, a total of 130,761 deaths occurred among persons aged 25–44 years, or an age-specific mortality rate of 153.0 per 100,000 25–44 year olds. Some specific types of age-specific mortality rates are neonatal, postneonatal, and infant mortality rates.</p>""",unsafe_allow_html=True)
    st.markdown("""<h3><b>The Mortality indicators are the following: </h3>""",unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    for i in Mortality_df.question.unique():
        st.markdown("""</n>-"""+str(i),unsafe_allow_html=True)
    st.markdown("""""",unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    st.markdown("""<h2> <b> Select the indicators you prefer""",unsafe_allow_html=True)

    col1,col2=st.columns((1,4))
    Mortality_indicators = col1.multiselect('Select the mortality indicators you want to analyze',Mortality_list)

    Mortality_countries=col1.multiselect('Select the country you want to analyze',Mortality_df.locationdesc.unique())
    Mortality_year_selected = col1.multiselect("Select years you want to analyze",Mortality_df.year.unique())


    if (Mortality_countries==[])|(Mortality_indicators==[])|(Mortality_year_selected==[]):
        st.markdown("""<h2 style='text-align:center; color: black;'> Please Fill All the Filters on the left to start Analysis</h2> """,unsafe_allow_html=True)
    else:
        Mortality_df_charts=Mortality_df.loc[(Mortality_df['question'].isin(Mortality_indicators))&((Mortality_df['year'].isin(Mortality_year_selected))&(Mortality_df['locationdesc'].isin(Mortality_countries)))]
        Mortality_df_map=Mortality_df.loc[(Mortality_df['question'].isin(Mortality_indicators))&((Mortality_df['year'].isin(Mortality_year_selected)))]

        Mortality_df_map=Mortality_df_map.groupby(["datavalueunit",'locationdesc','latitude','longitude'])['datavalue'].mean().reset_index()
        Mortality_df_map=Mortality_df_map.dropna(subset=['datavalue'])
        def map1():
            fig = px.scatter_mapbox(Mortality_df_map, lat="latitude", lon="longitude", hover_name="locationdesc", hover_data=["locationdesc", "datavalue","datavalueunit"],
                                size="datavalue",color_discrete_sequence=["red"], zoom=3, height=500,width=1300)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            col2.plotly_chart(fig)
        def map2():
            fig = px.scatter_mapbox(Mortality_df_map, lat="latitude", lon="longitude", hover_name="locationdesc", hover_data=["locationdesc", "datavalue","datavalueunit"],
                                    size="datavalue",color_discrete_sequence=["red"], zoom=3, height=500,width=1300)
            fig.update_layout(mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                        ]
                        }
                        ])
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            col2.plotly_chart(fig)
        mappings = col1.selectbox("Select the map you prefer ", ["detailed country map", "google earth map layout"], index=0, key=None)
        if(mappings == "detailed country map"):
            map1()
        if(mappings == "google earth map layout"):
            map2()

        st.markdown("""<br>""",unsafe_allow_html=True)
        st.markdown("""<br>""",unsafe_allow_html=True)
        col1,col2=st.columns(2)
        x=Mortality_df_map['locationdesc']
        y=Mortality_df_map['datavalue']
        sortx = [x for _,x in sorted(zip(y,x))]
        sorty = sorted(y,reverse=True)
        col1.markdown("""<h3><b> {} Age-adjusted Rate cases per 100,000 over US States </b>""".format(str(Mortality_indicators)[1:-1]),unsafe_allow_html=True)
        fig = px.bar(Mortality_df_map, x=sortx, y=sorty ,height=500,width=700)
        fig.update_layout(
        title="Age-adjusted Rate cases per 100,000 over US States <br>",
        xaxis_title="US States",
        yaxis_title="Age-adjusted Rate cases per 100,000",

         font=dict(
             family="Courier New, monospace",
             size=11,
             color="RebeccaPurple"
         )
     )

        col1.plotly_chart(fig)
        max_x = x[y.argmin()]
        col1.markdown("<b> {} has the highest  Age-adjusted Rate cases per 100,000  for {} </b>".format(str(max_x),str(Mortality_indicators)[1:-1]),unsafe_allow_html=True)
        Mortality_df_charts=Mortality_df_charts.groupby(['locationdesc','year','yearend'])['datavalue'].mean().reset_index()
        col2.markdown("""<b><h3> {} Age-adjusted Rate cases per 100,000 over {} in {} </b>""".format(str(Mortality_indicators)[1:-1],str(Mortality_year_selected),str(Mortality_countries)),unsafe_allow_html=True)
        x=Mortality_df_charts["year"]
        y=x=Mortality_df_charts["datavalue"]
        max_x = x[y.argmax()]
        fig = px.line(Mortality_df_charts, x=Mortality_df_charts["yearend"], y="datavalue", color='locationdesc')
        fig.update_layout(
        title="Age-adjusted Rate cases per 100,000 over US States <br> in the selected years ",
        xaxis_title="years",
        yaxis_title="Age-adjusted Rate cases per 100,000",

        font=dict(
         family="Courier New, monospace",
         size=11,
         color="RebeccaPurple"
        )
    )
        col2.plotly_chart(fig)



        maxvalue = Mortality_df_charts['datavalue'].max()
        minvalue = Mortality_df_charts['datavalue'].min()
        max_year=Mortality_df_charts["year"][Mortality_df_charts["datavalue"]==maxvalue].values[0]
        max_state=Mortality_df_charts["locationdesc"][Mortality_df_charts["datavalue"]==maxvalue].values[0]
        min_year=Mortality_df_charts["year"][Mortality_df_charts["datavalue"]==minvalue].values[0]
        min_state=Mortality_df_charts["locationdesc"][Mortality_df_charts["datavalue"]==minvalue].values[0]


        col2.markdown("<b> {} is the highest selected state for Mortality Age-adjusted Rate in {} were it reached {} </b>".format(max_state,max_year,maxvalue),unsafe_allow_html=True)
        col2.markdown("<b> {} is the lowest selected state for Mortality Age-adjusted Rate in {} were it reached {} </b>".format(min_state,min_year,minvalue),unsafe_allow_html=True)
if navigation=='Hospitalization Data Analysis':

    st.markdown("""<h2><b>Hospitalization Data Analysis</h2>""",unsafe_allow_html=True)
    st.markdown("""<h3><b>The Hospitalization indicators are the following: </b></h3>""",unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    for i in Hospitalization_df.question.unique():
        st.markdown("""</n>-"""+str(i),unsafe_allow_html=True)
    st.markdown("""""",unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    st.markdown("""<h2> <b> Select the indicators you prefer""",unsafe_allow_html=True)

    col1,col2=st.columns((1,4))
    Hospitalization_indicators = col1.multiselect('Hospitalization Indicators',Hospitalization_list)

    Hospitalization_countries=col1.multiselect('Select the country you want to analyze',Hospitalization_df.locationdesc.unique())

    Hospitalization_year_selected = col1.multiselect("Select Years",Hospitalization_df.year.unique())
    if (Hospitalization_countries==[])|(Hospitalization_indicators==[])|(Hospitalization_year_selected==[]):
        st.markdown("""<h2 style='text-align:center; color: black;'> Please Fill All the Filters on the left to start Analysis</h2> """,unsafe_allow_html=True)
    else:
        Hospitalization_df_charts=Hospitalization_df.loc[(Hospitalization_df['question'].isin(Hospitalization_indicators))&((Hospitalization_df['year'].isin(Hospitalization_year_selected))&(Hospitalization_df['locationdesc'].isin(Hospitalization_countries)))]
        Hospitalization_df_map=Hospitalization_df.loc[(Hospitalization_df['question'].isin(Hospitalization_indicators))&((Hospitalization_df['year'].isin(Hospitalization_year_selected)))]

        Hospitalization_df_map=Hospitalization_df_map.groupby(['locationdesc','latitude','longitude','datavaluetype'])['datavalue'].mean().reset_index()

        Hospitalization_df_map=Hospitalization_df_map.dropna(subset=['datavalue'])


        def map1():
            fig = px.scatter_mapbox(Hospitalization_df_map, lat="latitude", lon="longitude", hover_name="locationdesc", hover_data=["locationdesc", "datavalue",'datavaluetype'],
                                size="datavalue",color_discrete_sequence=["red"], zoom=3, height=500,width=1300)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            col2.plotly_chart(fig)
        def map2():
            fig = px.scatter_mapbox(Hospitalization_df_map, lat="latitude", lon="longitude", hover_name="locationdesc", hover_data=["locationdesc", "datavalue",'datavaluetype'],
                                    size="datavalue",color_discrete_sequence=["red"], zoom=3, height=500,width=1300)
            fig.update_layout(mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                        ]
                        }
                        ])
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            col2.plotly_chart(fig)
        mappings = col1.selectbox("Select the map you prefer ", ["detailed country map", "google earth map layout"], index=0, key=None)
        if(mappings == "detailed country map"):
            map1()
        if(mappings == "google earth map layout"):
            map2()

        st.markdown("""<br>""",unsafe_allow_html=True)
        st.markdown("""<br>""",unsafe_allow_html=True)
        col1,col2=st.columns(2)
        

        x=Hospitalization_df_map['locationdesc']
        y=Hospitalization_df_map['datavalue']
        print(Hospitalization_indicators)

        sortx = [x for _,x in sorted(zip(y,x))]
        sorty = sorted(y,reverse=True)
        col1.markdown("""<b> <h3> {} number over US States </b>""".format(str(Hospitalization_indicators)[1:-1]),unsafe_allow_html=True)
        fig = px.bar(Hospitalization_df_map, x=sortx, y=sorty ,height=500,width=700)
        fig.update_layout(
         title="Number over US States <br>",
         xaxis_title="US States",
         yaxis_title="Number",

         font=dict(
          family="Courier New, monospace",
          size=11,
          color="RebeccaPurple"
         )
     )

        col1.plotly_chart(fig)
        max_x = x[y.argmin()]
        col1.markdown("<b>{} has the highest number  for {} in {} </b>".format(str(max_x),str(Hospitalization_indicators)[1:-1],str(Hospitalization_year_selected)),unsafe_allow_html=True)

        Hospitalization_df_charts=Hospitalization_df_charts.groupby(['locationdesc','year','yearend'])['datavalue'].mean().reset_index()
        col2.markdown("""<h3> <b> {} Number over {} over {} </b> """.format(str(Hospitalization_indicators)[1:-1],str(Hospitalization_year_selected),str(Hospitalization_countries)),unsafe_allow_html=True)
        x=Hospitalization_df_charts["yearend"]
        y=Hospitalization_df_charts["datavalue"]
        max_x = x[y.argmax()]
        fig = px.line(Hospitalization_df_charts, x=Hospitalization_df_charts["yearend"], y="datavalue", color='locationdesc')
        fig.update_layout(
        title="Number over US States in the selected years ",
        xaxis_title="years",
        yaxis_title="Number",

        font=dict(
         family="Courier New, monospace",
         size=11,
         color="RebeccaPurple"
         )
     )
        col2.plotly_chart(fig)



        maxvalue = Hospitalization_df_charts['datavalue'].max()
        minvalue = Hospitalization_df_charts['datavalue'].min()
        max_year=Hospitalization_df_charts["year"][Hospitalization_df_charts["datavalue"]==maxvalue].values[0]
        max_state=Hospitalization_df_charts["locationdesc"][Hospitalization_df_charts["datavalue"]==maxvalue].values[0]
        min_year=Hospitalization_df_charts["year"][Hospitalization_df_charts["datavalue"]==minvalue].values[0]
        min_state=Hospitalization_df_charts["locationdesc"][Hospitalization_df_charts["datavalue"]==minvalue].values[0]


        col2.markdown("<b> {} is the highest selected state  in {} for {} to reach {} </b>".format(max_state,max_year,Hospitalization_indicators,maxvalue),unsafe_allow_html=True)
        col2.markdown("<b> {} is the lowest selected state   in {} for {} to reach {} </b>".format(min_state,min_year,Hospitalization_indicators,minvalue),unsafe_allow_html=True)
if navigation=='Prevalence Data Analysis':
    st.markdown("""<h2><b>The Prevalence Data Analysis</h2>""",unsafe_allow_html=True)
    st.markdown("""<h3><b>The Prevalence indicators are the following: </h3>""",unsafe_allow_html=True)

    st.markdown("""<br>""",unsafe_allow_html=True)

    for i in Prevalence_df.question.unique():
        st.markdown("""</n>-"""+str(i),unsafe_allow_html=True)
    st.markdown("""""",unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    st.markdown("""<h2> <b> Select the indicators you prefer""",unsafe_allow_html=True)


    col1,col2=st.columns((1,4))
    Prevalence_indicators = col1.multiselect('Select the prevalence Indicators you want to analyze',Prevalence_list)

    Prevalence_countries=col1.multiselect('Select the country you want to analyze',Prevalence_df.locationdesc.unique())

    Prevalence_year_selected = col1.multiselect("Select years you want to analyze",Prevalence_df.year.unique())



    if (Prevalence_countries==[])|(Prevalence_indicators==[])|(Prevalence_year_selected==[]):
        st.markdown("""<h2 style='text-align:center; color: black;'> Please Fill All the Filters on the left to start Analysis</h2> """,unsafe_allow_html=True)
    else:
        Prevalence_df_charts=Prevalence_df.loc[(Prevalence_df['question'].isin(Prevalence_indicators))&((Prevalence_df['year'].isin(Prevalence_year_selected))&(Prevalence_df['locationdesc'].isin(Prevalence_countries)))]
        Prevalence_df_map=Prevalence_df.loc[(Prevalence_df['question'].isin(Prevalence_indicators))&((Prevalence_df['year'].isin(Prevalence_year_selected)))]

        Prevalence_df_map=Prevalence_df_map.groupby(['locationdesc','latitude','longitude','datavalueunit'])['datavalue'].mean().reset_index()

        Prevalence_df_map=Prevalence_df_map.dropna(subset=['datavalue'])
        def map1():
            fig = px.scatter_mapbox(Prevalence_df_map, lat="latitude", lon="longitude", hover_name="locationdesc", hover_data=["locationdesc", "datavalue",'datavalueunit'],
                                size="datavalue",color_discrete_sequence=["red"], zoom=3, height=500,width=1300)
            fig.update_layout(mapbox_style="carto-positron")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            col2.plotly_chart(fig)
        def map2():
            fig = px.scatter_mapbox(Prevalence_df_map, lat="latitude", lon="longitude", hover_name="locationdesc", hover_data=["locationdesc", "datavalue",'datavalueunit'],
                                    size="datavalue",color_discrete_sequence=["red"], zoom=3, height=500,width=1300)
            fig.update_layout(mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                        ]
                        }
                        ])
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            col2.plotly_chart(fig)

        st.markdown("""<br>""",unsafe_allow_html=True)
        st.markdown("""<br>""",unsafe_allow_html=True)
        mappings = col1.selectbox("Select the map you prefer ", ["detailed country map", "google earth map layout"], index=0, key=None)
        if(mappings == "detailed country map"):
            map1()
        if(mappings == "google earth map layout"):
            map2()

        st.markdown("""<br>""",unsafe_allow_html=True)
        st.markdown("""<br>""",unsafe_allow_html=True)
        col1,col2=st.columns(2)

        x=Prevalence_df_map['locationdesc']
        y=Prevalence_df_map['datavalue']
        sortx = [x for _,x in sorted(zip(y,x))]
        sorty = sorted(y,reverse=True)
        col1.markdown("""<h3> {} percentage over US States""".format(str(Prevalence_indicators)[1:-1]),unsafe_allow_html=True)
        fig = px.bar(Prevalence_df_map, x=sortx, y=sorty ,height=500,width=700)
        fig.update_layout(
        title="Percentage over US States <br>",
        xaxis_title="US States",
        yaxis_title="Percentage",

        font=dict(
            family="Courier New, monospace",
            size=11,
            color="RebeccaPurple"
        )
    )

        col1.plotly_chart(fig)
        max_x = x[y.argmin()]
        col1.markdown("<b> {} has the highest percentage  for {} in {} </b>".format(max_x,str(Prevalence_indicators)[1:-1],str(Prevalence_year_selected)),unsafe_allow_html=True)

        Prevalence_df_charts=Prevalence_df_charts.groupby(['locationdesc','year','yearend'])['datavalue'].mean().reset_index()
        col2.markdown("""<h3> {}Percentage over {} over {}""".format(str(Prevalence_indicators)[1:-1],str(Prevalence_year_selected),str(Prevalence_countries)),unsafe_allow_html=True)
        x=Prevalence_df_charts["yearend"]
        y=Prevalence_df_charts["datavalue"]
        max_x = x[y.argmax()]
        fig = px.line(Prevalence_df_charts, x=Prevalence_df_charts["yearend"], y="datavalue", color='locationdesc')
        fig.update_layout(
        title="Percentage over US States in the selected years ",
        xaxis_title="years",
        yaxis_title=" Percentage",

        font=dict(
            family="Courier New, monospace",
            size=11,
            color="RebeccaPurple"
        )
    )
        col2.plotly_chart(fig)



        maxvalue = Prevalence_df_charts['datavalue'].max()
        minvalue = Prevalence_df_charts['datavalue'].min()
        max_year=Prevalence_df_charts["year"][Prevalence_df_charts["datavalue"]==maxvalue].values[0]
        max_state=Prevalence_df_charts["locationdesc"][Prevalence_df_charts["datavalue"]==maxvalue].values[0]
        min_year=Prevalence_df_charts["year"][Prevalence_df_charts["datavalue"]==minvalue].values[0]
        min_state=Prevalence_df_charts["locationdesc"][Prevalence_df_charts["datavalue"]==minvalue].values[0]


        col2.markdown("<b> {} is the highest selected state  in {} for {} to reach {} % </b>".format(max_state,max_year,Prevalence_indicators,maxvalue),unsafe_allow_html=True)
        col2.markdown("<b> {} is the lowest selected state   in {} for {} to reach {} % </b>".format(min_state,min_year,Prevalence_indicators,minvalue),unsafe_allow_html=True)


ft = """
<style>
a:link , a:visited{
color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

#page-container {
  position: relative;
  min-height: 10vh;
}

footer{
    visibility:hidden;
}

.footer {
position: relative;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #808080; /* theme's text color hex code at 50 percent brightness*/
text-align: left; /* you can replace 'left' with 'center' or 'right' if you want*/
}
</style>

<div id="page-container">

<div class="footer">
<p style='font-size: 0.875em;'>Made with <a style='display: inline; text-align: left;' href="https://streamlit.io/" target="_blank">Streamlit</a><br 'style= top:3px;'>
with <img src="https://em-content.zobj.net/source/skype/289/red-heart_2764-fe0f.png" alt="heart" height= "10"/><a style='display: inline; text-align: left;' href="https://www.linkedin.com/in/nourhan-mahmassani-878b23189/" target="_blank"> by Nourhan Mahmassani</a></p>
</div>

</div>
"""
st.write(ft, unsafe_allow_html=True)



