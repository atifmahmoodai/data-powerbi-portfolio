"""Generate native PBIP sources for 11 additional analytics demos."""
from pathlib import Path
import sys,json,csv,io,zlib,base64,uuid
ROOT=Path(__file__).resolve().parent/'opportunity-demos';SCHEMA='https://developer.microsoft.com/json-schemas/fabric/item/'
SPECS={
'11-overdue-collections':[('Outstanding Balance','SUM(Data[actual])','"PKR "#,0'),('Overdue Invoices','CALCULATE(COUNTROWS(Data), Data[status] <> "Current")','#,0'),('Overdue Balance','CALCULATE(SUM(Data[actual]), Data[status] <> "Current")','"PKR "#,0'),('Average Days Overdue','AVERAGE(Data[extra])','0.0')],
'12-job-profitability':[('Job Revenue','SUM(Data[actual])','"PKR "#,0'),('Direct Cost','SUM(Data[cost])','"PKR "#,0'),('Gross Profit','SUM(Data[actual]) - SUM(Data[cost])','"PKR "#,0'),('Gross Margin','DIVIDE([Gross Profit], [Job Revenue])','0.0%')],
'13-budget-forecasting':[('Actual Spend','SUM(Data[actual])','"PKR "#,0'),('Budget','SUM(Data[target])','"PKR "#,0'),('Budget Variance','SUM(Data[target]) - SUM(Data[actual])','"PKR "#,0'),('Variance Percent','DIVIDE([Budget Variance], [Budget])','0.0%')],
'14-manufacturing-waste':[('Good Output Units','SUM(Data[units])','#,0'),('Material Cost','SUM(Data[cost])','"PKR "#,0'),('Waste Cost Proxy','SUM(Data[cost]) * AVERAGE(Data[extra]) / 100','"PKR "#,0'),('Average Reject Rate','DIVIDE(AVERAGE(Data[extra]), 100)','0.0%')],
'15-construction-analytics':[('Earned Value','SUM(Data[actual])','"PKR "#,0'),('Planned Value','SUM(Data[target])','"PKR "#,0'),('Actual Cost','SUM(Data[cost])','"PKR "#,0'),('Schedule Variance','[Earned Value] - [Planned Value]','"PKR "#,0')],
'16-demand-planning':[('Observed Units','SUM(Data[units])','#,0'),('Forecast Units','SUM(Data[target])','#,0'),('Unit Variance','SUM(Data[units]) - SUM(Data[target])','#,0'),('Short Cover SKU Periods','CALCULATE(COUNTROWS(Data), Data[status] = "Short cover")','#,0')],
'17-multi-branch':[('Net Sales','SUM(Data[actual])','"PKR "#,0'),('Sales Target','SUM(Data[target])','"PKR "#,0'),('Direct Cost','SUM(Data[cost])','"PKR "#,0'),('Gross Profit','SUM(Data[actual]) - SUM(Data[cost])','"PKR "#,0')],
'18-marketing-analytics':[('Attributed Revenue','SUM(Data[actual])','"PKR "#,0'),('Ad Spend','SUM(Data[cost])','"PKR "#,0'),('ROAS','DIVIDE([Attributed Revenue], [Ad Spend])','0.00x'),('Conversions','SUM(Data[units])','#,0')],
'19-field-service-analytics':[('Service Jobs Logged','COUNTROWS(Data)','#,0'),('SLA Breaches','CALCULATE(COUNTROWS(Data), Data[status] = "SLA breach")','#,0'),('Service Revenue','SUM(Data[actual])','"PKR "#,0'),('Service Cost','SUM(Data[cost])','"PKR "#,0')],
'20-business-central-reporting':[('Net Ledger Amount','SUM(Data[actual]) - SUM(Data[cost])','"PKR "#,0'),('Ledger Lines','COUNTROWS(Data)','#,0'),('Review Lines','CALCULATE(COUNTROWS(Data), Data[status] = "Review")','#,0'),('Control Variance','SUM(Data[actual]) - SUM(Data[target])','"PKR "#,0')],
'21-power-bi-repair-toolkit':[('Readiness Score','AVERAGE(Data[actual])','0.0'),('Checks Reviewed','COUNTROWS(Data)','#,0'),('Issues','CALCULATE(COUNTROWS(Data), Data[status] IN {"Review", "Fail"})','#,0'),('Failed Checks','CALCULATE(COUNTROWS(Data), Data[status] = "Fail")','#,0')]}
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'astra-opportunities/'+s))
def dump(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def literal(v):return {'expr':{'Literal':{'Value':"'"+v.replace("'","''")+"'" if isinstance(v,str) else str(v)+'D'}}}
def field(name,is_measure=False):return {('Measure' if is_measure else 'Column'):{'Expression':{'SourceRef':{'Entity':'Data'}},'Property':name}}
def projection(name,is_measure=False):return {'field':field(name,is_measure),'queryRef':'Data.'+name,'nativeQueryRef':name}
def main():
 for slug, measures in SPECS.items():
  root=ROOT/slug; demo=json.loads((root/'model.json').read_text()); data=demo['rows']; cols=list(data[0]); native=root/'PowerBI';model=native/'Model.SemanticModel';report=native/'Dashboard.Report';definition=report/'definition'
  csvpath=root/'data.csv';csvtext=csvpath.read_text();compress=zlib.compressobj(wbits=-15);payload=base64.b64encode(compress.compress(csvtext.encode())+compress.flush()).decode()
  typed=[]; columns=[]
  for c in cols:
   vals=[r.get(c) for r in data]
   typ='string' if c=='period' else 'decimal' if all(isinstance(v,(int,float)) or v is None for v in vals) else 'string'
   mtyp={'dateTime':'type date','decimal':'Currency.Type','string':'type text'}[typ]
   typed.append('{"'+c+'", '+mtyp+'}'); columns.append(dict(name=c,dataType=typ,sourceColumn=c,summarizeBy='none',lineageTag=uid(slug+'/'+c)))
  expression=['let',f'    Sample = Binary.Decompress(Binary.FromText("{payload}", BinaryEncoding.Base64), Compression.Deflate),','    Source = if DataMode = "Demo" then Sample else File.Contents(DataFolder),','    Parsed = Table.PromoteHeaders(Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]), [PromoteAllScalars=true]),','    Typed = Table.TransformColumnTypes(Parsed, {'+', '.join(typed)+'}, "en-US")','in','    Typed']
  meas=[dict(name=n,expression=e,formatString=f,displayFolder='Analytics',description=n,lineageTag=uid(slug+'/measure/'+n)) for n,e,f in measures]
  table=dict(name='Data',lineageTag=uid(slug+'/Data'),columns=columns,measures=meas,partitions=[dict(name='Data',mode='import',source=dict(type='m',expression=expression))])
  tmodel=dict(name='Model',compatibilityLevel=1567,model=dict(culture='en-US',defaultPowerBIDataSourceVersion='powerBI_V3',sourceQueryCulture='en-US',tables=[table],expressions=[dict(name='DataMode',kind='m',expression='"Demo" meta [IsParameterQuery=true, List={"Demo", "CSV"}, DefaultValue="Demo", Type="Text", IsParameterQueryRequired=true]'),dict(name='DataFolder',kind='m',expression='"C:/Astra/'+slug+'/data.csv" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]')],annotations=[dict(name='__PBI_TimeIntelligenceEnabled',value='0')]))
  dump(model/'model.bim',tmodel);dump(model/'definition.pbism',{'$schema':SCHEMA+'semanticModel/definitionProperties/1.0.0/schema.json','version':'1.0','settings':{}})
  dump(native/'Dashboard.pbip',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json','version':'1.0','artifacts':[{'report':{'path':'Dashboard.Report'}}],'settings':{'enableAutoRecovery':True}})
  dump(report/'definition.pbir',{'$schema':SCHEMA+'report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../Model.SemanticModel'}}})
  dump(definition/'version.json',{'$schema':SCHEMA+'report/definition/versionMetadata/1.0.0/schema.json','version':'2.0.0'})
  dump(definition/'report.json',{'$schema':SCHEMA+'report/definition/report/3.1.0/schema.json','themeCollection':{'customTheme':{'name':'AstraTheme','type':'RegisteredResources','reportVersionAtImport':{'visual':'2.1.0','page':'2.0.0','report':'3.1.0'}}},'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'AstraTheme','path':'AstraTheme.json','type':'CustomTheme'}]}]})
  dump(report/'StaticResources/RegisteredResources/AstraTheme.json',{'name':'Astra Analytics','dataColors':['#0B6E61','#1E4E79','#E3A331','#C65749','#70877C'],'background':'#F3F6F5','foreground':'#18332D','tableAccent':'#0B6E61'})
  page='overview';dump(definition/'pages/pages.json',{'$schema':SCHEMA+'report/definition/pagesMetadata/1.0.0/schema.json','pageOrder':[page],'activePageName':page})
  dump(definition/f'pages/{page}/page.json',{'$schema':SCHEMA+'report/definition/page/2.0.0/schema.json','name':page,'displayName':'Overview','displayOption':'FitToPage','width':1280,'height':800})
  pdir=definition/f'pages/{page}/visuals';idx=0
  def visual(vtype,title,x,y,w,h,roles=None):
   nonlocal idx
   idx+=1;name=f'{page}_v{idx:02d}'
   cfg={'visualType':vtype,'drillFilterOtherVisuals':True,'visualContainerObjects':{'title':[{'properties':{'show':literal(True),'text':literal(title)}}]}}
   if roles: cfg['query']={'queryState':{r:{'projections':ps} for r,ps in roles.items()}}
   if vtype=='textbox': cfg['objects']={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':title,'textStyle':{'fontFamily':'Segoe UI Semibold','fontSize':'24pt','color':'#18332d'}}]}]}}]} 
   dump(pdir/name/'visual.json',{'$schema':SCHEMA+'report/definition/visualContainer/2.1.0/schema.json','name':name,'position':{'x':x,'y':y,'width':w,'height':h,'z':idx,'tabOrder':idx},'visual':cfg})
  visual('textbox',demo['title'],24,12,1232,55,{})
  for j,(n,_,_) in enumerate(measures):visual('card',n,24+j*312,82,294,105,{'Values':[projection(n,True)]})
  visual('clusteredBarChart',demo['chartTitle']+' by '+demo['groupLabel'],24,220,600,255,{'Category':[projection('group')],'Y':[projection(measures[0][0],True)]})
  visual('lineChart','Trend by period',640,220,616,255,{'Category':[projection('period')],'Y':[projection(measures[0][0],True)]})
  visual('tableEx','Detail and exceptions',24,495,1232,270,{'Values':[projection(x) for x in ['period','group','item','status','actual','cost','target','units']]})
  dump(definition/'report.json',{'$schema':SCHEMA+'report/definition/report/3.1.0/schema.json','themeCollection':{'customTheme':{'name':'AstraTheme','type':'RegisteredResources','reportVersionAtImport':{'visual':'2.1.0','page':'2.0.0','report':'3.1.0'}}},'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'AstraTheme','path':'AstraTheme.json','type':'CustomTheme'}]}]})
  dump(report/'StaticResources/RegisteredResources/AstraTheme.json',{'name':'Astra Analytics','dataColors':['#0B6E61','#1E4E79','#E3A331','#C65749','#70877C'],'background':'#F3F6F5','foreground':'#18332D','tableAccent':'#0B6E61'})
  (native/'measures.dax').write_text('\n\n'.join(n+' =\n'+e for n,e,_ in measures)+'\n')
  (native/'README.md').write_text(f'# {demo["title"]} · Power BI\n\nOpen `Dashboard.pbip` with Power BI Desktop on Windows. Demo mode embeds synthetic records. The CSV file at `../data.csv` contains the same demo rows; edit the model DataFolder parameter to switch source mode. Review all business definitions in the project README before using real data.\n\nThis is a generated PBIP source; Power BI Desktop open, refresh, DAX evaluation, and visuals still need acceptance testing.\n')
 print(f'Generated {len(SPECS)} native PBIP sources.')
if __name__=='__main__':main()
