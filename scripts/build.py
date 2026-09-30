"""Build all ten independent PBIP projects. Python 3.10+, standard library only.

Generated folders are owned by this builder. Preserve Desktop edits before rebuilding.
"""
from __future__ import annotations
import base64
import csv
import hashlib
import io
import json
import uuid
import zlib
from pathlib import Path
from catalog import projects

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 'https://developer.microsoft.com/json-schemas/fabric/item/'
M_TYPES = {'string':'type text', 'int64':'Int64.Type', 'decimal':'Currency.Type', 'double':'type number', 'dateTime':'type date'}

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def js(path, data):
    write(path, json.dumps(data, indent=2, ensure_ascii=False)+'\n')

def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'astra-power-bi/'+value))

def lit(v):
    s = str(v).lower() if isinstance(v, bool) else "'"+v.replace("'", "''")+"'" if isinstance(v,str) else str(v)+'D'
    return {'expr':{'Literal':{'Value':s}}}

def color(v): return {'solid':{'color':lit(v)}}

def field(ref):
    table, name = ref.split('.', 1) if '.' in ref else ('Metrics', ref)
    return {('Measure' if table=='Metrics' else 'Column'):{'Expression':{'SourceRef':{'Entity':table}},'Property':name}}

def projection(ref):
    return {'field':field(ref), 'queryRef':ref if '.' in ref else 'Metrics.'+ref, 'nativeQueryRef':ref.split('.')[-1]}

def build_model(p, folder):
    tables=[]
    contract=[]
    hashes={}
    for name,t in p['tables'].items():
        buf=io.StringIO(newline='')
        w=csv.DictWriter(buf, fieldnames=list(t['columns']), lineterminator='\n')
        w.writeheader(); w.writerows(t['rows'])
        text=buf.getvalue()
        write(folder/f'data/demo/{name}.csv',text)
        write(folder/f'data/import-template/{name}.csv',text if name=='Metrics' else ','.join(t['columns'])+'\n')
        hashes[name]=hashlib.sha256(text.encode()).hexdigest()
        zipobj=zlib.compressobj(wbits=-15)
        payload=base64.b64encode(zipobj.compress(text.encode())+zipobj.flush()).decode()
        typed=', '.join('{"'+c+'", '+M_TYPES[typ]+'}' for c,typ in t['columns'].items())
        m=['let',f'    Demo = Binary.Decompress(Binary.FromText("{payload}", BinaryEncoding.Base64), Compression.Deflate),',
           f'    Source = if DataMode = "Demo" then Demo else if DataMode = "Folder" then File.Contents(DataFolder & "/{name}.csv") else error "DataMode must be Demo or Folder",',
           '    Parsed = Csv.Document(Source, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
           '    Headers = Table.PromoteHeaders(Parsed, [PromoteAllScalars=true]),',
           f'    Typed = Table.TransformColumnTypes(Headers, {{{typed}}}, "en-US")','in','    Typed']
        write(folder/f'queries/{name}.m','\n'.join(m)+'\n')
        cols=[]
        for c,typ in t['columns'].items():
            col={'name':c,'dataType':typ,'sourceColumn':c,'summarizeBy':'none','lineageTag':uid(p['slug']+'/'+name+'/'+c)}
            if c.endswith('ID'): col['isHidden']=True
            if typ=='dateTime': col['formatString']='dd MMM yyyy'
            if name=='Calendar' and c=='Date': col['isKey']=True
            cols.append(col)
        table={'name':name,'lineageTag':uid(p['slug']+'/'+name),'columns':cols,
               'partitions':[{'name':name,'mode':'import','source':{'type':'m','expression':m}}]}
        if name=='Calendar': table['dataCategory']='Time'
        if name=='Metrics':
            table['columns'][0]['isHidden']=True
            table['measures']=[dict(name=m['name'],expression=m['dax'],formatString=m['format'],description=m['description'],displayFolder='Business metrics',lineageTag=uid(p['slug']+'/measure/'+m['name'])) for m in p['measures']]
        tables.append(table)
        contract.append(f"## {name}\n\nGrain: {t['grain']}. Unique key: `{t['key']}`.\n\n| Column | Type |\n|---|---|\n"+'\n'.join(f'| {c} | {typ} |' for c,typ in t['columns'].items()))
    rels=[]
    for ft,fc,tt,tc in p['relationships']:
        rels.append(dict(name=uid(p['slug']+'/'+ft+'/'+fc),fromTable=ft,fromColumn=fc,toTable=tt,toColumn=tc,crossFilteringBehavior='oneDirection',fromCardinality='many',toCardinality='one'))
    model={'name':'Model','compatibilityLevel':1567,'model':{'culture':'en-US','defaultPowerBIDataSourceVersion':'powerBI_V3','sourceQueryCulture':'en-US',
           'tables':tables,'relationships':rels,'expressions':[
               {'name':'DataMode','kind':'m','expression':'"Demo" meta [IsParameterQuery=true, List={"Demo", "Folder"}, DefaultValue="Demo", Type="Text", IsParameterQueryRequired=true]'},
               {'name':'DataFolder','kind':'m','expression':f'"C:/PowerBI/Astra/power-bi/{p["slug"]}/data/demo" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'}],
           'annotations':[{'name':'__PBI_TimeIntelligenceEnabled','value':'0'}]}}
    js(folder/'Model.SemanticModel/model.bim',model)
    js(folder/'Model.SemanticModel/definition.pbism',{'$schema':SCHEMA+'semanticModel/definitionProperties/1.0.0/schema.json','version':'1.0','settings':{}})
    js(folder/'Dashboard.pbip',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json','version':'1.0','artifacts':[{'report':{'path':'Dashboard.Report'}}],'settings':{'enableAutoRecovery':True}})
    js(folder/'Dashboard.Report/definition.pbir',{'$schema':SCHEMA+'report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../Model.SemanticModel'}}})
    js(folder/'data/manifest.json',{'label':'SYNTHETIC DEMO — no real clients','asOf':'2026-09-30','currency':'PKR','sha256':hashes})
    write(folder/'DATA-CONTRACT.md','# Data contract\n\nUTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.\n\n'+p['rules']+'\n\n'+'\n\n'.join(contract))
    write(folder/'measures.dax','\n\n'.join('// '+m['description']+'\n'+m['name']+' =\n'+m['dax'] for m in p['measures'])+'\n')
    js(folder/'validation/expected-demo.json',{'method':'Independent Python reference totals; NOT evaluated by the DAX engine','scope':'All filters cleared; entire supplied period or snapshot','metrics':p['expected']})
    query='EVALUATE\nROW(\n'+',\n'.join('    "'+n+'", ['+n+']' for n in p['expected'])+'\n)\n'
    write(folder/'Model.SemanticModel/DAXQueries/Reconcile.dax',query)

def build_report(p,folder):
    report=folder/'Dashboard.Report'; d=report/'definition'
    js(d/'version.json',{'$schema':SCHEMA+'report/definition/versionMetadata/1.0.0/schema.json','version':'2.0.0'})
    js(report/'StaticResources/RegisteredResources/AstraTheme.json',{'name':'Astra Analytics','dataColors':['#137C82','#BE9154','#5064A1','#CF6558','#759C91','#7F6D92'],'background':'#F3F5F7','foreground':'#182A3A','tableAccent':'#137C82','textClasses':{'label':{'fontFace':'Segoe UI','fontSize':11},'title':{'fontFace':'Segoe UI Semibold','fontSize':14},'callout':{'fontFace':'Segoe UI Semibold','fontSize':28}}})
    js(d/'report.json',{'$schema':SCHEMA+'report/definition/report/3.1.0/schema.json','themeCollection':{'customTheme':{'name':'AstraTheme','type':'RegisteredResources','reportVersionAtImport':{'visual':'2.1.0','page':'2.0.0','report':'3.1.0'}}},'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'AstraTheme','path':'AstraTheme.json','type':'CustomTheme'}]}]})
    pageids=[f'page{i+1:02d}' for i in range(len(p['pages']))]
    js(d/'pages/pages.json',{'$schema':SCHEMA+'report/definition/pagesMetadata/1.0.0/schema.json','pageOrder':pageids,'activePageName':pageids[0]})
    for pageid,page in zip(pageids,p['pages']):
        base=d/'pages'/pageid
        js(base/'page.json',{'$schema':SCHEMA+'report/definition/page/2.0.0/schema.json','name':pageid,'displayName':page['title'],'displayOption':'FitToPage','width':1280,'height':800,'objects':{'background':[{'properties':{'color':color('#F3F5F7'),'transparency':lit(0)}}]}})
        count=0
        def visual(kind,title,x,y,w,h,roles=None,objects=None):
            nonlocal count
            count+=1; name=f'{pageid}_v{count:02d}'
            v={'visualType':kind,'drillFilterOtherVisuals':True,'visualContainerObjects':{'title':[{'properties':{'show':lit(bool(title)),'text':lit(title),'fontColor':color('#182A3A'),'fontSize':lit(12)}}],'background':[{'properties':{'show':lit(True),'color':color('#FFFFFF'),'transparency':lit(0)}}],'border':[{'properties':{'show':lit(True),'color':color('#DDE4E9'),'radius':lit(6)}}]}}
            if roles: v['query']={'queryState':{k:{'projections':[projection(r) for r in refs]} for k,refs in roles.items()}}
            if objects: v['objects']=objects
            js(base/f'visuals/{name}/visual.json',{'$schema':SCHEMA+'report/definition/visualContainer/2.1.0/schema.json','name':name,'position':{'x':x,'y':y,'width':w,'height':h,'z':count,'tabOrder':count},'visual':v})
        visual('textbox','',24,12,1232,48,objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':p['short'].upper()+'  /  '+page['title'],'textStyle':{'fontFamily':'Segoe UI Semibold','fontSize':'22pt','color':'#182A3A'}}]}]}}]})
        visual('textbox','',24,66,1232,36,objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':'SYNTHETIC DEMO  |  PKR  |  '+page.get('note',p['scope']),'textStyle':{'fontSize':'10pt','color':'#526674'}}]}]}}]})
        for i,ref in enumerate(page['slicers']):
            visual('slicer',ref.split('.')[-1],24+i*416,112,400,66,{'Values':[ref]},{'data':[{'properties':{'mode':lit('Dropdown')}}]})
        for i,m in enumerate(page['cards']):
            visual('card',m,24+i*312,194,296,102,{'Values':[m]},{'labels':[{'properties':{'color':color('#137C82'),'fontSize':lit(27)}}]})
        for i,chart in enumerate(page['charts']):
            title,kind,cat,vals=chart
            visual(kind,title,24+i*624,312,608,236,{'Category':[cat],'Y':vals})
        visual('tableEx',page.get('tableTitle','Management detail'),24,564,1232,212,{'Values':page['table']},{'grid':[{'properties':{'rowPadding':lit(7)}}],'columnHeaders':[{'properties':{'fontColor':color('#182A3A'),'backColor':color('#E8EFF2')}}]})

def build_docs(p,folder):
    links='\n'.join(f'- **{page["title"]}:** '+', '.join(page['cards']) for page in p['pages'])
    notes='\n'.join(f'- **{page["title"]}:** {page["note"]}' for page in p['pages'] if page.get('note'))
    metrics='\n'.join(f'| {m["name"]} | {m["description"]} |' for m in p['measures'])
    write(folder/'README.md',f'''# {p['title']}

{p['purpose']}

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

{links}

{('### Page guidance\n\n'+notes) if notes else ''}

## Business scope

{p['scope']}

{p['rules']}

## KPI definitions

| Metric | Definition |
|---|---|
{metrics}

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
''')

def main():
    items=projects()
    for p in items:
        folder=ROOT/p['slug']
        build_model(p,folder); build_report(p,folder); build_docs(p,folder)
    js(ROOT/'catalog.json',[{'folder':p['slug'],'title':p['title'],'entrypoint':p['slug']+'/Dashboard.pbip','tables':len(p['tables']),'measures':len(p['measures']),'pages':len(p['pages']),'status':'source-built; Desktop acceptance pending'} for p in items])
    print(f'Built {len(items)} projects, {sum(len(p["pages"]) for p in items)} report pages.')

if __name__=='__main__': main()
