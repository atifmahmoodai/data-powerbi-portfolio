"""Validate generated sources and fixtures, without claiming Desktop/DAX execution."""
from __future__ import annotations
import argparse
import base64
import csv
import datetime as dt
import hashlib
import json
import math
import re
import subprocess
import zlib
from pathlib import Path
from catalog import projects, ASOF

ROOT=Path(__file__).resolve().parents[1]
SCHEMA_PIN='24ce2795f9fb15655f61185246b6578536ca43f8'

def require(ok,message):
    if not ok: raise ValueError(message)

def load(folder, spec):
    data={}
    for name,t in spec['tables'].items():
        with (folder/f'data/demo/{name}.csv').open(newline='',encoding='utf-8') as f:
            reader=csv.DictReader(f)
            require(reader.fieldnames==list(t['columns']),f'{name}: CSV header mismatch')
            rows=list(reader)
        for row in rows:
            for c,typ in t['columns'].items():
                require(row[c] is not None,f'{name}.{c}: missing field')
                if typ in ['decimal','double','int64']:
                    row[c]=int(row[c]) if typ=='int64' else float(row[c])
                    require(math.isfinite(row[c]),f'{name}.{c}: nonfinite value')
                elif typ=='dateTime' and row[c]: dt.date.fromisoformat(row[c])
        data[name]=rows
    return data

def unique(rows,cols):
    values=[tuple(r[c] for c in cols) for r in rows]
    require(len(values)==len(set(values)),f'Duplicate natural key: {cols}')

def business_checks(slug,data):
    n=int(slug[:2])
    if n==1:
        for r in data['Vehicles']:
            require(r['Status'] in ['Sold','In Stock'],'Invalid vehicle status')
            end=r['SaleDate'] or ASOF.isoformat()
            require((dt.date.fromisoformat(end)-dt.date.fromisoformat(r['PurchaseDate'])).days==r['DaysHeld'],'Vehicle days held mismatch')
            require((r['Status']=='Sold')==bool(r['SaleDate']),'Vehicle sale/status mismatch')
            require((r['SalePrice']>0)==(r['Status']=='Sold'),'Sale amount/status mismatch')
            expected_band='0–30' if r['DaysHeld']<=30 else '31–60' if r['DaysHeld']<=60 else '61–90' if r['DaysHeld']<=90 else '91+'
            require(r['AgeBand']==expected_band,'Age-band label/boundary mismatch')
    elif n==2:
        unique(data['Targets'],['AccountID','Date'])
        require(all(r['Units']>0 and r['Revenue']>=0 and r['Cost']>=0 for r in data['Sales']),'Invalid sale')
        require(all(r['TargetRevenue']>=0 for r in data['Targets']),'Negative account target')
        account_ids={r['AccountID'] for r in data['Accounts']}
        target_dates={r['Date'] for r in data['Targets']}
        first=dt.date.fromisoformat(min(target_dates)); last=dt.date.fromisoformat(max(target_dates))
        expected_dates={(first+dt.timedelta(days=i)).isoformat() for i in range((last-first).days+1)}
        require(target_dates==expected_dates,'Target dates must cover a continuous daily period')
        expected_pairs={(account_id,date) for account_id in account_ids for date in target_dates}
        actual_pairs={(r['AccountID'],r['Date']) for r in data['Targets']}
        require(actual_pairs==expected_pairs,'Each account must have exactly one target for every target date')
    elif n==3:
        for r in data['Stock']:
            require(0<=r['Reserved']<=r['OnHand'] and r['UnitCost']>=0,'Invalid stock')
            require(r['SnapshotDate']==ASOF.isoformat(),'Mixed snapshots')
            require((ASOF-dt.date.fromisoformat(r['ReceiptDate'])).days==r['AgeDays'],'Invalid lot age')
            require(r['AgeDays']>=0,'Stock receipt date is after snapshot')
            expected_band='0–30' if r['AgeDays']<=30 else '31–60' if r['AgeDays']<=60 else '61–90' if r['AgeDays']<=90 else '91+'
            require(r['AgeBand']==expected_band,'Stock age-band label/boundary mismatch')
    elif n==4:
        unique(data['PnL'],['DepartmentID','Date','Category'])
        require(all(r['Category'] in ['Revenue','COGS','Operating Expense'] and r['Actual']>=0 and r['Budget']>=0 for r in data['PnL']),'Invalid P&L category/sign')
    elif n==5:
        unique(data['Trading'],['StoreID','Date'])
        require(all(0<=r['Transactions']<=r['Visitors'] and 0<=r['Refunds']<=r['GrossSales'] for r in data['Trading']),'Invalid retail conversion/refunds')
        require(all(r['Target']>=0 and r['Units']>=0 and r['NetCOGS']>=0 for r in data['Trading']),'Invalid retail target, units or net cost')
        store_ids={r['StoreID'] for r in data['Stores']}
        trading_dates={r['Date'] for r in data['Trading']}
        first=dt.date.fromisoformat(min(trading_dates)); last=dt.date.fromisoformat(max(trading_dates))
        expected_dates={(first+dt.timedelta(days=i)).isoformat() for i in range((last-first).days+1)}
        require(trading_dates==expected_dates,'Retail trading dates must cover a continuous daily period')
        expected_pairs={(store_id,date) for store_id in store_ids for date in trading_dates}
        actual_pairs={(r['StoreID'],r['Date']) for r in data['Trading']}
        require(actual_pairs==expected_pairs,'Each store must have exactly one record for every trading date')
    elif n==6:
        unique(data['Advertising'],['ChannelID','Date'])
        require(all(r['GrossSales']>=0 and r['Discount']>=0 and 0<=r['Refund']<=r['GrossSales']-r['Discount']+.001 and r['NetCOGS']>=0 and r['ShippingCost']>=0 and r['PaymentFee']>=0 and r['FulfilmentCost']>=0 for r in data['Orders']),'Invalid order revenue, refund or cost')
        require(all(r['AdSpend']>=0 for r in data['Advertising']),'Negative ad spend')
        channel_ids={r['ChannelID'] for r in data['Channels']}
        ad_dates={r['Date'] for r in data['Advertising']}
        first=dt.date.fromisoformat(min(ad_dates)); last=dt.date.fromisoformat(max(ad_dates))
        expected_dates={(first+dt.timedelta(days=i)).isoformat() for i in range((last-first).days+1)}
        require(ad_dates==expected_dates,'Advertising dates must cover a continuous daily period')
        expected_pairs={(channel_id,date) for channel_id in channel_ids for date in ad_dates}
        actual_pairs={(r['ChannelID'],r['Date']) for r in data['Advertising']}
        require(actual_pairs==expected_pairs,'Each channel must have one ad-spend record for every advertising date')
    elif n==7:
        for r in data['Opportunities']:
            require(0<=r['Probability']<=1,'Invalid stage probability')
            require(bool(r['ClosedDate'])==(r['Stage'] in ['Won','Lost']),'Opportunity close mismatch')
            if r['ClosedDate']: require(r['CreatedDate']<=r['ClosedDate']<=ASOF.isoformat(),'Invalid opportunity dates')
    elif n==8:
        unique(data['Workforce'],['DepartmentID','Date'])
        prev={}; coverage={}
        for r in sorted(data['Workforce'],key=lambda x:(x['DepartmentID'],x['Date'])):
            key=r['DepartmentID']; coverage.setdefault(key,set()).add(r['Date'])
            require(r['ClosingHeadcount']==r['OpeningHeadcount']+r['Hires']-r['Leavers'],'Headcount rollforward failed')
            require(0<=r['AbsentHours']<=r['ScheduledHours'],'Invalid absence hours')
            if key in prev: require(prev[key]==r['OpeningHeadcount'],'Monthly headcount discontinuity')
            prev[key]=r['ClosingHeadcount']
        require(len({tuple(sorted(x)) for x in coverage.values()})==1,'Inconsistent department periods')
    elif n==9:
        unique(data['Performance'],['ProjectID','Date'])
        require(all(r['ActualHours']>=0 and r['CostBudget']>=0 for r in data['Performance']),'Invalid project hours/budget')
    else:
        for r in data['Jobs']:
            complete=r['Status']=='Completed'
            require(bool(r['CompletedDate'])==complete,'Job completion/status mismatch')
            if complete:
                require(r['CycleDays']==(dt.date.fromisoformat(r['CompletedDate'])-dt.date.fromisoformat(r['CreatedDate'])).days,'Cycle time mismatch')
                require(r['OnTime']==int(r['CompletedDate']<=r['DueDate']),'On-time flag mismatch')
            else: require(r['OnTime']==r['Rework']==0,'Open job marked completed KPI')

def reference(slug,d):
    """Recompute selected acceptance metrics from written CSVs, independent of DAX."""
    def s(rows,c): return sum(r[c] for r in rows)
    n=int(slug[:2])
    if n==1:
        sold=[r for r in d['Vehicles'] if r['Status']=='Sold']; stock=[r for r in d['Vehicles'] if r['Status']=='In Stock']
        rev=s(sold,'SalePrice'); profit=rev-s(sold,'PurchaseCost')-s(sold,'Reconditioning')
        return {'Units Sold':len(sold),'Sales Revenue':rev,'Gross Profit':profit,'Gross Margin':profit/rev,'Stock Units':len(stock),'Stock Value':s(stock,'PurchaseCost')+s(stock,'Reconditioning'),'Aged Stock Units':sum(r['DaysHeld']>90 for r in stock)}
    if n==2:
        rev=s(d['Sales'],'Revenue'); target=s(d['Targets'],'TargetRevenue')
        return {'Revenue':rev,'Gross Profit':rev-s(d['Sales'],'Cost'),'Revenue Target':target,'Target Attainment':rev/target,'Sales Transactions':len(d['Sales']),'Active Customers':len({r['AccountID'] for r in d['Sales']})}
    if n==3:
        r=d['Stock']; units=s(r,'OnHand'); val=sum(x['OnHand']*x['UnitCost'] for x in r); aged=sum(x['OnHand']*x['UnitCost'] for x in r if x['AgeDays']>90)
        return {'On Hand Units':units,'Available Units':units-s(r,'Reserved'),'Stock Value':val,'Aged Value':aged,'Aged Value Share':aged/val,'Weighted Stock Age':sum(x['AgeDays']*x['OnHand'] for x in r)/units}
    if n==4:
        rev=s([r for r in d['PnL'] if r['Category']=='Revenue'],'Actual'); profit=rev-s([r for r in d['PnL'] if r['Category']!='Revenue'],'Actual'); cash=d['Cash']
        return {'Revenue':rev,'Operating Profit':profit,'Operating Margin':profit/rev,'Net Cash Movement':s(cash,'CashMovement'),'Cash Inflow':s([r for r in cash if r['CashMovement']>0],'CashMovement'),'Cash Outflow':-s([r for r in cash if r['CashMovement']<0],'CashMovement')}
    if n==5:
        r=d['Trading']; net=s(r,'GrossSales')-s(r,'Refunds'); tx=s(r,'Transactions'); vis=s(r,'Visitors')
        return {'Net Sales':net,'Gross Profit':net-s(r,'NetCOGS'),'Visitors':vis,'Transactions':tx,'Store Conversion':tx/vis,'Average Basket':net/tx}
    if n==6:
        r=d['Orders']; net=s(r,'GrossSales')-s(r,'Discount')-s(r,'Refund'); pre=net-s(r,'NetCOGS')-s(r,'ShippingCost')-s(r,'PaymentFee')-s(r,'FulfilmentCost'); spend=s(d['Advertising'],'AdSpend')
        return {'Net Revenue':net,'Ad Spend':spend,'Contribution before Ads':pre,'Contribution after Ads':pre-spend,'Order Count':len(r),'Revenue to Ad Spend':net/spend}
    if n==7:
        r=d['Opportunities']; op=[x for x in r if x['IsOpen']]; won=[x for x in r if x['Stage']=='Won']; closed=[x for x in r if not x['IsOpen']]
        return {'Open Opportunities':len(op),'Open Pipeline':s(op,'Amount'),'Weighted Pipeline':sum(x['Amount']*x['Probability'] for x in op),'Won Deals':len(won),'Win Rate':len(won)/len(closed),'Stale Open Deals':sum(x['LastActivityDate']<(ASOF-dt.timedelta(days=14)).isoformat() for x in op)}
    if n==8:
        r=d['Workforce']; last=max(x['Date'] for x in r); months=len({x['Date'] for x in r})
        return {'Headcount':s([x for x in r if x['Date']==last],'ClosingHeadcount'),'Hires':s(r,'Hires'),'Leavers':s(r,'Leavers'),'Period Attrition':s(r,'Leavers')/(s(r,'OpeningHeadcount')/months),'Absence Rate':s(r,'AbsentHours')/s(r,'ScheduledHours'),'Payroll':s(r,'Payroll')}
    if n==9:
        r=d['Performance']; rev=s(r,'RecognizedRevenue'); cost=s(r,'LaborCost')+s(r,'SubcontractCost')+s(r,'Expenses')
        return {'Recognized Revenue':rev,'Delivery Cost':cost,'Project Profit':rev-cost,'Project Margin':(rev-cost)/rev,'Budget Remaining':s(r,'CostBudget')-cost,'Invoice Cash Gap':s(r,'Invoiced')-s(r,'Collected')}
    r=d['Jobs']; done=[x for x in r if x['Status']=='Completed']; op=[x for x in r if x['Status']=='Open']
    return {'Jobs Created':len(r),'Completed Jobs':len(done),'Open Jobs':len(op),'On Time Rate':s(done,'OnTime')/len(done),'Overdue Open Jobs':sum(x['DueDate']<ASOF.isoformat() for x in op),'First Pass Yield':(len(done)-s(done,'Rework'))/len(done),'Recorded Cost':s(r,'Cost')}

def schema_registry(root):
    from referencing import Registry,Resource
    from referencing.jsonschema import DRAFT7
    require(subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==SCHEMA_PIN,'Wrong Microsoft schema revision')
    resources={}
    for f in root.rglob('*.json'):
        try: d=json.loads(f.read_text())
        except (ValueError,UnicodeError): continue
        if not isinstance(d,dict): continue
        url='https://developer.microsoft.com/json-schemas/'+f.relative_to(root).as_posix()
        resources[url]=Resource(contents=d,specification=DRAFT7)
        if '$id' in d: resources[d['$id']]=resources[url]
    return resources,Registry().with_resources(resources.items())

def validate_project(p,resources=None,registry=None):
    folder=ROOT/p['slug']; data=load(folder,p); schema_count=0
    for name,t in p['tables'].items():
        unique(data[name],[t['key']])
        require(all(r[t['key']]!='' for r in data[name]),'Blank primary key')
    business_checks(p['slug'],data)
    model=json.loads((folder/'Model.SemanticModel/model.bim').read_text())['model']; tables={t['name']:t for t in model['tables']}
    for rel in model['relationships']:
        target={r[rel['toColumn']] for r in data[rel['toTable']]}
        require(all(r[rel['fromColumn']]=='' or r[rel['fromColumn']] in target for r in data[rel['fromTable']]),f'Orphan foreign key: {rel}')
    manifest=json.loads((folder/'data/manifest.json').read_text())
    for name,t in tables.items():
        source='\n'.join(t['partitions'][0]['source']['expression'])
        payload=re.search(r'Binary.FromText\("([^"]+)"',source).group(1)
        raw=(folder/f'data/demo/{name}.csv').read_bytes()
        require(zlib.decompress(base64.b64decode(payload),wbits=-15)==raw,'Embedded demo mismatch')
        require(hashlib.sha256(raw).hexdigest()==manifest['sha256'][name],'Demo hash mismatch')
    measures={m['name'] for m in tables['Metrics']['measures']}
    for m in tables['Metrics']['measures']:
        # Check qualified model references and unqualified measure dependencies.
        dax=m['expression']
        for table,col in re.findall(r"'?([A-Za-z][A-Za-z0-9_]*)'?\[([^\]]+)\]",dax):
            require(table in tables and col in {c['name'] for c in tables[table]['columns']},f'Unknown DAX column: {table}.{col}')
        unqualified=re.sub(r"'?([A-Za-z][A-Za-z0-9_]*)'?\[[^\]]+\]",'',dax)
        for name in re.findall(r'\[([^\]]+)\]',unqualified): require(name in measures,f'Unknown DAX measure {name}')
    def bindings(obj):
        if isinstance(obj,dict):
            for typ in ['Column','Measure']:
                ref=obj.get(typ)
                if isinstance(ref,dict) and 'Property' in ref:
                    table=ref['Expression']['SourceRef'].get('Entity')
                    if table:
                        require(table in tables,'Unknown visual table')
                        fields={x['name'] for x in tables[table].get('columns' if typ=='Column' else 'measures',[])}
                        require(ref['Property'] in fields,'Unknown visual binding')
            for val in obj.values(): bindings(val)
        elif isinstance(obj,list):
            for val in obj: bindings(val)
    visuals=0
    pages=folder/'Dashboard.Report/definition/pages'
    for pagefile in pages.glob('*/page.json'):
        page=json.loads(pagefile.read_text()); positions=[]
        for vf in pagefile.parent.glob('visuals/*/visual.json'):
            v=json.loads(vf.read_text()); bindings(v); pos=v['position']; x,y,w,h=(pos[k] for k in ['x','y','width','height']); visuals+=1
            require(0<=x and 0<=y and x+w<=page['width'] and y+h<=page['height'],'Visual outside canvas')
            require(all(not(x<a+c and x+w>a and y<b+d and y+h>b) for a,b,c,d in positions),'Overlapping visuals')
            positions.append((x,y,w,h))
    require(len(list(pages.glob('*/page.json')))==3 and visuals==36,'Unexpected report size')
    for f in folder.rglob('*'):
        if f.suffix not in ['.json','.pbip','.pbir','.pbism','.bim']: continue
        d=json.loads(f.read_text())
        if resources and isinstance(d,dict) and '$schema' in d:
            from jsonschema import Draft7Validator
            require(d['$schema'] in resources,'Unknown schema URL')
            errors=list(Draft7Validator(resources[d['$schema']].contents,registry=registry).iter_errors(d))
            require(not errors,f'{f}: '+str(errors[:1]))
            schema_count+=1
    expected=json.loads((folder/'validation/expected-demo.json').read_text())['metrics']; actual=reference(p['slug'],data)
    require(set(actual)==set(expected),'Reference metric mismatch')
    for name,value in expected.items():
        require(name in measures,'Expected metric missing from DAX')
        require(math.isclose(actual[name],value,rel_tol=1e-10,abs_tol=.0001),f'Reconciliation failed: {name}')
    return dict(project=p['slug'],pages=3,visuals=visuals,measures=len(measures),tables=len(tables),rows=sum(len(r) for r in data.values()),schemaFiles=schema_count,reconciledMetrics=len(expected))

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--schemas',type=Path); args=parser.parse_args()
    resources,registry=schema_registry(args.schemas) if args.schemas else (None,None)
    results=[validate_project(p,resources,registry) for p in projects()]
    report={'status':'PASS','schemaValidation':bool(resources),'schemaRevision':SCHEMA_PIN if resources else None,'projects':results,'checks':['CSV headers and types','primary/foreign keys','business invariants','embedded demo parity','fixture hashes','DAX reference names (not execution)','visual bindings','canvas bounds and overlap','CSV reconciliation totals'],'notExecuted':['Power BI Desktop open','Power Query refresh','DAX engine evaluation','Native visual rendering','Service deployment or refresh']}
    if resources: report['checks'].append('Microsoft PBIP/PBIR/PBISM JSON schemas')
    (ROOT/'validation').mkdir(exist_ok=True)
    (ROOT/'validation/results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
