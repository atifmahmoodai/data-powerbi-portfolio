"""Regression checks for costly grain/sign/cohort errors and invalid source data."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from catalog import projects
from validate import business_checks, reference

class BusinessRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.specs=projects()

    def data(self,n): return {name:copy.deepcopy(t['rows']) for name,t in self.specs[n-1]['tables'].items()}

    def test_all_fixtures_obey_contract(self):
        for p in self.specs:
            with self.subTest(p=p['slug']): business_checks(p['slug'],{k:v['rows'] for k,v in p['tables'].items()})

    def test_headcount_is_latest_not_period_sum(self):
        d=self.data(8); expected=sum(r['ClosingHeadcount'] for r in d['Workforce'] if r['Date']=='2026-09-30')
        self.assertEqual(reference('08',d)['Headcount'],expected)
        self.assertLess(expected,sum(r['ClosingHeadcount'] for r in d['Workforce']))

    def test_ecommerce_ads_are_not_joined_per_order(self):
        d=self.data(6); before=reference('06',d)
        d['Orders']*=2
        after=reference('06',d)
        self.assertEqual(before['Ad Spend'],after['Ad Spend'])
        self.assertAlmostEqual(after['Contribution after Ads'],before['Contribution before Ads']*2-before['Ad Spend'])

    def test_crm_open_deals_do_not_dilute_win_rate(self):
        d=self.data(7); before=reference('07',d)['Win Rate']
        d['Opportunities'].extend(copy.deepcopy([r for r in d['Opportunities'] if r['IsOpen']]))
        self.assertEqual(reference('07',d)['Win Rate'],before)

    def test_profit_does_not_change_when_cash_changes(self):
        d=self.data(4); before=reference('04',d)
        d['Cash'][0]['CashMovement']+=100000
        after=reference('04',d)
        self.assertEqual(before['Operating Profit'],after['Operating Profit'])
        self.assertEqual(after['Net Cash Movement']-before['Net Cash Movement'],100000)

    def test_unsold_vehicle_does_not_increase_sold_profit(self):
        d=self.data(1); before=reference('01',d)
        stock=next(r for r in d['Vehicles'] if r['Status']=='In Stock'); stock['PurchaseCost']+=100000
        after=reference('01',d)
        self.assertEqual(before['Gross Profit'],after['Gross Profit'])
        self.assertEqual(after['Stock Value']-before['Stock Value'],100000)

    def test_dealership_age_bands_match_the_90_day_cutoff(self):
        rows=self.data(1)['Vehicles']
        for row in rows:
            expected='0–30' if row['DaysHeld']<=30 else '31–60' if row['DaysHeld']<=60 else '61–90' if row['DaysHeld']<=90 else '91+'
            self.assertEqual(row['AgeBand'],expected)

    def test_sales_targets_cover_every_account_on_every_target_date(self):
        d=self.data(2)
        d['Targets'].pop()
        with self.assertRaisesRegex(ValueError,'every target date'):
            business_checks('02',d)

    def test_inventory_age_bands_match_the_90_day_cutoff(self):
        d=self.data(3)
        business_checks('03',d)
        self.assertTrue(any(r['AgeDays']>90 and r['AgeBand']=='91+' for r in d['Stock']))
        d['Stock'][0]['AgeBand']='91+'
        with self.assertRaisesRegex(ValueError,'age-band label/boundary'):
            business_checks('03',d)

    def test_inventory_ageing_detail_shows_exact_lot_age(self):
        page=self.specs[2]['pages'][1]
        self.assertIn('Stock.AgeDays',page['table'])

    def test_financial_comparison_charts_name_the_compared_series(self):
        pnl, budget, cash=self.specs[3]['pages']
        self.assertIn('Revenue and operating profit',pnl['charts'][1][0])
        self.assertIn('vs budget',budget['charts'][0][0])
        self.assertIn('vs budget',budget['charts'][1][0])
        self.assertIn('inflow vs outflow',cash['charts'][1][0])

    def test_retail_daily_records_cover_every_store(self):
        d=self.data(5)
        d['Trading'].pop()
        with self.assertRaisesRegex(ValueError,'every trading date'):
            business_checks('05',d)

    def test_retail_conversion_definition_is_visible(self):
        page=self.specs[4]['pages'][1]
        self.assertIn('not unique customers',page['note'])

    def test_stock_ageing_detail_supports_actionable_stock_filtering(self):
        page=self.specs[0]['pages'][1]
        self.assertIn('Vehicles.Status',page['slicers'])
        self.assertTrue({'Vehicles.Status','Vehicles.PurchaseDate','Vehicles.DaysHeld'}.issubset(page['table']))

    def test_invalid_source_rows_are_rejected(self):
        cases=[(1,'Vehicles','DaysHeld',-1),(2,'Sales','Units',-1),(3,'Stock','Reserved',999999),(4,'PnL','Category','Unknown'),(5,'Trading','Transactions',999999),(6,'Orders','Refund',99999999),(7,'Opportunities','Probability',1.2),(8,'Workforce','ClosingHeadcount',-1),(9,'Performance','ActualHours',-1),(10,'Jobs','CompletedDate','2099-01-01')]
        for n,t,col,value in cases:
            with self.subTest(n=n):
                d=self.data(n); d[t][0][col]=value
                with self.assertRaises(ValueError): business_checks(f'{n:02d}',d)

if __name__=='__main__': unittest.main()
