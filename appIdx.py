import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto

import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import *

import base64, os, glob

import geopy, folium
from geopy.geocoders import Nominatim
from functools import partial

cyto.load_extra_layouts()

# =========================================================================

def encodePict(aPath):
    with open(os.getcwd() + aPath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    encoded_image = "data:image/png;base64," + encoded_string
    return encoded_image

imgUKDW = 'figs/eduUKDW.png'
imgUKDWEnc = base64.b64encode(open(imgUKDW, 'rb').read())
imgUU = 'figs/eduUU.png'
imgUUEnc = base64.b64encode(open(imgUU, 'rb').read())
imgUOS = 'figs/eduUOS.png'
imgUOSEnc = base64.b64encode(open(imgUOS, 'rb').read())
imgUOE = 'figs/eduUOE.png'
imgUOEEnc = base64.b64encode(open(imgUOE, 'rb').read())
imgBel = 'figs/phoBel.jpg'
imgBelEnc = base64.b64encode(open(imgBel, 'rb').read())
imgProv = 'figs/provDM_simple.png'
imgProvEnc = base64.b64encode(open(imgProv, 'rb').read())
imgLin = 'figs/socLin.png'
imgLinEnc = base64.b64encode(open(imgLin, 'rb').read())
imgWeb = 'figs/socWeb.png'
imgWebEnc = base64.b64encode(open(imgWeb, 'rb').read())

dictSklTech = {
    "Data Analysis":["Data Management","Data Modeling","Statistics","Python","R","Databricks"],
    "Deep Learning":["Computer Vision","Graph Neural Network"],
    "Machine Learning":["Classification","Clustering","Regression"],
    "Provenance":["Prov Data Model","Information Theory"],
    "Graph":["Graph Modeling","Graph Analysis","Graph Neural Network","Graph DB","Bayesian Network"],
    "Project Management":["Agile","Communication","Consultation","Supervision","Presentation"],
    "Web Development":["HTML","CMS","API","MySQL DB","PHP MyAdmin","Apache Web Server","Google Cloud Platform"],
    "Programming Language":["Python","PySpark","R","Google Cloud Platform"],
    "Visualization":["Tableau","Plotly Dash","Google Cloud Platform"],
    "Version Control":["Git","Google Cloud Platform"],
    "Database":["MySQL DB","Graph DB","Google Cloud Platform"],
    "Cloud Platform":["Google Cloud Platform"],
}
dictExpSkl={
    "(Advanced)Data Manager":["Data Analysis","Database", "Project Management", 
                    "Programming Language","Version Control","Cloud Platform"],
    "Industrial Research Fellow":["Data Analysis","Deep Learning","Machine Learning",
                                   "Graph","Project Management","Provenance",
                                   "Programming Language","Version Control"],
    "Demonstrator (Mentor,Invigilator,Exam Support)":["Programming Language","Project Management"],
    "Administrative Assistant (Web Content)":["Web Development"],
    "Website and IT Officer":["Web Development"],
    "Researcher":["Data Analysis","Visualization","Provenance"],
    "Operations Assistant":["Project Management","Web Development"],
    "(Internship) Software developer":["Database","Web Development"],
    "Lecturer":["Project Management","Data Analysis","Graph","Visualization",],
    "(Part-time) Website Developer":["Web Development"]
}

lab=[]; sou=[]; tar=[]
# First level ----------------------
for k,v in dictExpSkl.items():
  if k not in lab:    
    lab.append(k)
  for i in v:
    if i not in lab: lab.append(i)

for k,v in dictSklTech.items():
  if k not in lab:    
    lab.append(k)
  for i in v:
    if i not in lab: lab.append(i)
# Second level ----------------------
for k,v in dictExpSkl.items():  
  for i in v:
    sou.append(lab.index(k))
    tar.append(lab.index(i))

for k,v in dictSklTech.items():  
  for i in v:
    sou.append(lab.index(k))
    tar.append(lab.index(i))


listLangLev = [[1,2,3,4,1],
               ["Basic","Intermediate","Professional","Native","Basic"]]
               

listProvGraph=[
    {'data': {'type':'agent','id': 'ukdw', 'label': 'Duta Wacana Christian University'}},
    {'data': {'type':'agent','id': 'uu', 'label': 'University of Utrecht'}}, 
    {'data': {'type':'agent','id': 'uos', 'label': 'University of Southampton'}},
    {'data': {'type':'agent','id': 'uoe', 'label': 'University of Exeter'}},
    {'data': {'type':'activity','id': 'stuBac', 'label': 'studying\nbachelor'}},
    {'data': {'type':'activity','id': 'stuMas', 'label': 'studying\nmaster'}},
    {'data': {'type':'activity','id': 'stuDoc', 'label': 'researching\ndoctoral'}},
    {'data': {'type':'activity','id': 'resPosDoc', 'label': 'consulting'}},
    {'data': {'type':'entity','id': 'dipBac', 'label': 'S.Kom'},'position':{'x':0,'y':0}},
    {'data': {'type':'entity','id': 'dipMas', 'label': 'M.Sc'},'position':{'x':0,'y':0}},
    {'data': {'type':'entity','id': 'dipDoc', 'label': 'PhD'},'position':{'x':0,'y':0}},

    {'data': {'type':'wIB','source': 'stuMas', 'target': 'stuBac'}},
    {'data': {'type':'wIB','source': 'stuDoc', 'target': 'stuMas'}},
    {'data': {'type':'wIB','source': 'resPosDoc', 'target': 'stuDoc'}},
    {'data': {'type':'wGB','source': 'dipBac', 'target': 'stuBac'}},
    {'data': {'type':'wGB','source': 'dipMas', 'target': 'stuMas'}},
    {'data': {'type':'wGB','source': 'dipDoc', 'target': 'stuDoc'}},
    {'data': {'type':'wAT','source': 'dipBac', 'target': 'ukdw'}},
    {'data': {'type':'wAT','source': 'dipMas', 'target': 'uu'}},
    {'data': {'type':'wAT','source': 'dipDoc', 'target': 'uos'}},
    {'data': {'type':'wAW','source': 'stuBac', 'target': 'ukdw'}},
    {'data': {'type':'wAW','source': 'stuMas', 'target': 'uu'}},
    {'data': {'type':'wAW','source': 'stuDoc', 'target': 'uos'}},
    {'data': {'type':'wAW','source': 'resPosDoc', 'target': 'uoe','edgeLength':0.01}}          
]

listProvStyle=[
    {'selector':'node','style': {'content':'data(label)','text-wrap':'wrap','text-max-width':'100',
                                'text-halign':'center','text-valign':'center','width':'label',                                 
                                 'font-size':'12','font-style':'bold',
                                 'color':'black','border-width':'2','border-color':'white',
                                 'compound-sizing-wrt-labels':'include',
                                 }},
    {'selector':'node[type="entity"]','style':{'background-color':'yellow','shape':'ellipse','width':'75','height':'20'}},
    {'selector':'node[type="agent"]','style':{'background-color':'orange','shape':'round-pentagon','width':'100','height':'30'}},
    {'selector':'node[type="activity"]','style':{'background-color':'blue','shape':'round-rectangle','width':'75','height':'30','color':'white'}},
    {'selector':'edge','style':{'curve-style':'unbundled-bezier',# The default curve style does not work with certain arrows
                                'target-arrow-shape':'vee','width':7,
                                'edge-distances':10,'border-width':2,'arrow-scale':1.5,
                                #'loop-direction':'-45deg',
                                #'loop-sweep':'-120deg',
                                'label':'data(label)','color':'purple',
                                'background-color':'white'
                                #'mid-target-arrow-shape':'triangle',
                                }},
    {'selector':'edge[type="wIB","wGB"]','style':{'target-arrow-color':'blue','target-arrow-shape':'vee','line-color':'blue'}},
    {'selector':'edge[type="wGB"]','style':{'target-arrow-color':'blue','target-arrow-shape':'vee','line-color':'blue'}},
    {'selector':'edge[type="wAT"]','style':{'target-arrow-color':'orange','target-arrow-shape':'vee','line-color':'orange'}},
    {'selector':'edge[type="wAW"]','style':{'target-arrow-color':'orange','target-arrow-shape':'vee','line-color':'orange'}}
]


styBut = {
  'background-color': '#4CAF50',
  'color': 'white',
  'padding': '4px',
  'text-align': 'center',
  'text-decoration': 'none',
  'font-size': '10px',
  'margin': '0px 2px',
  'border-radius': '3px 2px'
}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__) #for web in heroku
server = app.server #for web in heroku
app._favicon = "assets/favicon.ico"
app.title = "Belfrit Victor Batlajery"
app.config.suppress_callback_exceptions = True

# PAGE: Index ==================================================================
index_page = html.Div(id='index_page', children=[
    dcc.Input(id='fakeInput', value='22', type='text', 
                        size='5', minLength=1, maxLength=2, debounce=False,
                        disabled=False, readOnly=False, required=True, style={'visibility':'hidden'}),
    html.H1('Belfrit Victor Batlajery', 
          style={'textAlign': 'center', 'color': '#0171b0'}),
    html.Br(),

    # First line -----------------------------------------        
    html.Div([
        html.Div([
          html.Div([
              html.Div(cyto.Cytoscape(
                id='ProvGraph', zoom=0.5, userZoomingEnabled=False,
                elements = listProvGraph,
                layout={'name':'cola','fit':False,'EdgeLength':5,
                        'nodeOverlap':0,
                        'randomize': True,
                        'nodeRepulsion': 1000,
                        'idealEdgeLength': 10,
                        'gravity': 0.01},
                style={'height':'260px',
                       'width':'100%'},
                stylesheet = listProvStyle
            ),style={'margin-left':'-100%','left': 0,'top':50})
          ]),            
          html.Img(src='data:image/png;base64,{}'.format(imgProvEnc.decode()),
                   style={'width':'300px','margin-top':'-100px',
                          'border':'1px solid yellow','position':'relative'}),
        ], className="five columns",style={'border':'0px solid yellow','float':'left','width':'400px','height':'310px'}),
        html.Div([
            html.Div("Educational provenance", 
                      style={'color':'#bac80b','font-size':'25px'}),            
            html.Div([
                html.A([
                  html.Img(src='data:image/png;base64,{}'.format(imgUKDWEnc.decode()),style={'width':'22px'})
                ], href="https://www.ukdw.ac.id/akademik/fakultas-teknologi-informasi/informatika/", target="_blank"),
                html.A([
                  html.Img(src='data:image/png;base64,{}'.format(imgUUEnc.decode()),style={'width':'30px'})
                ], href="https://www.uu.nl/masters/en/business-informatics", target="_blank"),
                html.A([
                  html.Img(src='data:image/png;base64,{}'.format(imgUOSEnc.decode()),style={'width':'30px'}),
                ], href="https://www.wais.ecs.soton.ac.uk/", target="_blank"),
                html.A([
                  html.Img(src='data:image/png;base64,{}'.format(imgUOEEnc.decode()),style={'width':'22px'})
                ], href="http://intranet.exeter.ac.uk/emps/staff/bb432", target="_blank"),
                html.A([
                  html.Img(src='data:image/png;base64,{}'.format(imgLinEnc.decode()), style={'width':'30px'})
                ], href="http://nl.linkedin.com/in/belfritvictorbatlajery", target="_blank", style={'margin-left':'30px'}),
                html.A([
                  html.Img(src='data:image/png;base64,{}'.format(imgWebEnc.decode()), style={'width':'28px'})
                ], href="http://qillbel.org/personal/", target="_blank")
            ])
        ], className="seven columns",style={'border':'0px solid yellow','width':'370px','line-height':'63px','vertical-align':'middle','float':'right'}),
        html.Div([
            html.P(["Hi, I'm Belfrit and here is my resume. Finish with my Bachelor Degree in \
                    Technic Informatic, I continued my Master Degree in Business Informatics. Then, I \
                    pursued my Doctoral Degree that focused on Information Provenance, Risk and Graph Modelling. \
                    I have modelled my academic journey with the standardized provenance data model, ", 
                    html.A("PROV-DM", href="https://www.w3.org/TR/prov-dm/",target="_blank",style={'color':'cyan'}),
                    ", displayed on the left-hand side. \
                    I used to work as an Industrial Research Fellow at the University of Exeter-England, delivering research-based \
                    projects to local businesses in the area of information provenance, data analysis, and machine and (graph) deep learning. \
                    Then I moved to the NHS England as a Data Manager processing and surfacing data to make it available \
                    for use for insights and researches. These days, I'm working as an Advanced Data Engineer overviewing their cloud \
                    infrastructure to facilitate their analysts. In addition, I'm delivering some online courses (i.e. ",
                    html.A("teaching", href="http://qillbel.org/personal/index.php?content=tea",target="_blank",style={'color':'cyan'}),") \
                    to undergrad students in Indonesia."]),            
        ], style={'border':'0px solid yellow','float':'right','padding':'0px 25px 0px 0px','width':'380px','color':'#ffffff','font-size':'10px',
                 'line-height':'15px','text-align':'justify'},className="seven columns"),
    ], className="twelve columns", style={'border':'0px solid red','margin-left':'10px','height':'320px'}),
    html.Br(),

    # Second line -----------------------------------------        
    html.Div([        
        dcc.Graph(id='ExpSkl')
    ], className="twelve columns", style={'border':'0px solid blue',                                       'margin-top':'-20px'}),
    html.Br(),
    html.Br(),
    html.Br(),

    # Fifth line -----------------------------------------
    html.Div("Social and cultural background", 
             className="twelve columns", style={'border':'0px solid blue',                                          
                                          'color':'#bac80b','font-size':'25px',
                                            'margin-bottom':'10px'}),
    html.Div([
        html.Div([
            html.Span("Kidz Klub Leeds",style=styBut),
            html.Span("Exeter Southernhay Child Contact Centre",style=styBut),
            html.Br(),
            html.Span("Southampton City and Region Action to Combat Hardship",style=styBut),
            html.Br(),
            html.Span("Perkampungan Ngebong Sarkem",style=styBut),
            html.Span("Perkampungan Sosial Pingit",style=styBut),            
            html.Br(),                                    
            html.Span("Mengasuh Anak Tani",style=styBut),
            html.Span("Yayasan Brayat Pinuji",style=styBut),
            html.Span("Yayasan Bina Asih Leleani",style=styBut),           
        ],style={'border':'0px solid purple','float':'left','margin':'5px 0px 0px 20px'},className="five columns"),
        html.Div([
            html.P(["I enjoy ",
                    html.A("volunteering", href="http://qillbel.org/personal/index.php?content=vol",target="_blank",style={'color':'cyan'}),
                    " in the local area where I live. Among many cities that I have visited, \
                    I always look for local charities where I can contribute on the regular basis. \
                    I find volunteering provides a friendly, warm, and supportive atmosphere, \
                    which can be a way to create a network and build up your confidence. \
                    And occasionally, I raise money through some running events as I like to run for ",
                    html.A("my exercise", href="https://www.mapmyrun.com/profile/52185242/",target="_blank",style={'color':'cyan'}),                    
                    ". Doing this allows me to understand more about social life and cultural diversity \
                    around me."], style={'color':'#ffffff','font-size':'10px','line-height':'15px','text-align':'justify'})
        ],style={'border':'0px solid purple','float':'right','padding':'0px 15px 0px 0px','width':'400px'},className="seven columns")
    ], className="twelve columns", style={'border':'0px solid red','margin-bottom':'5px','height':'100px'}),
    html.Br(),

    # Sixth line -----------------------------------------        
    html.Div([
        html.Div(dcc.Graph(id='Lang'), style={'border':'0px solid purple','float':'left','width':'250px','margin':'-15px 0px 0px 20px'},className="four columns"),
        html.Div(
            html.Iframe(srcDoc=open('qMap.html','r').read(), style={'width':'480px','height':'200px'}), 
            style={'border':'0px solid purple','width':'500px','float':'right','margin-right':'10px'},className="eight columns"),
    ], className="twelve columns", style={'border':'0px solid red','height':'255px','margin-top':'0px'}),
    #html.Br(),
    
    html.H6('-BVB-',style={'textAlign': 'center', 'color': '#0171b0'}),
    # Last line -----------------------------------------
    #dcc.Link('x', href='/')
])
@app.callback(
    [Output(component_id='ExpSkl',component_property='figure'),
     Output(component_id='Lang',component_property='figure')],
    Input(component_id='fakeInput',component_property='value')
    )
def page_index(fakeInput):
  figExpSkl = go.Figure()
  sankey1Tra = go.Sankey(
    arrangement = "fixed",
    node = {"label":lab},
    link = {"source":sou,"target":tar,"value":[.1]*len(sou),"color":'rgba(0,255,255,0.1)'},
    hoverinfo = 'none')
  
  figExpSkl.add_trace(sankey1Tra)
  figExpSkl.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': '#2f4050',
    'font_color':'white','font_size':8,    
    'margin':dict(l=20, r=20, t=30, b=20),
  })
  figExpSkl.update_layout(
    title={
        'text': "Work experience and skills",
        'font_size':25,
        'font_color':'#bac80b',
        'y':0.9, 'x':0.3,
        'xanchor': 'center',
        'yanchor': 'top'})
  figExpSkl.update_layout(modebar_remove=['zoom','pan','lasso','select2d'])
  figExpSkl.layout.xaxis.fixedrange = True
  figExpSkl.layout.yaxis.fixedrange = True

  # ----------------------------------------------------
  figLang = go.Figure()
  radar1Tra = go.Scatterpolar(
    name = "Language",
    r = [1,4,3,4,1],
    #text = listLangLev[1],
    theta = ["Dutch", "Javanese", "English","Indonesian","Dutch"],
    mode="lines+markers", line_color='indianred',
    marker=dict(color='lightslategray', size=8, symbol='square'),    
  )
  figLang.add_trace(radar1Tra)
  figLang.update_traces(fill='toself',fillcolor='rgba(0, 0, 255, 0.4)')
  figLang.update_layout(polar={"radialaxis":{"tickmode":"array",
                                        "tickvals":listLangLev[0],
                                        "ticktext":listLangLev[1],
                                        "gridcolor":"grey"},
                              "angularaxis": {"color":"white"}})
  figLang.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': '#2f4050',
    'font_color':'black','font_size':8,    
    'margin':dict(l=40, r=40, t=20, b=20),
    'height':250
  })
  figLang.update_layout(modebar_remove=['zoom','pan','lasso','select2d'],dragmode=False)
  
  
  return figExpSkl, figLang


# PROG: Update the index========================================================
app.layout = html.Div([    
    html.Div(id='All_pages', children=[index_page])
], style={'margin':'5px auto','background-color':'#2f4050','textAlign':'center','width':'820px',
         'font-family':'Arial, Helvetica, sans-serif'})


if __name__ == '__main__':
    app.run_server(debug=True)