# internal_jobs = ['GenerateNNSale_ProductIDs_Lumens', 'GenerateNNSale_ProductIDs_YLighting', 'Custom_NN_Sale_Lumens1',
#                  'Custom_NN_Sale_Lumens2', 'Custom_NN_Sale_Lumens3', 'Custom_NN_Sale_Lumens4',
#                  'Custom_NN_Sale_YLighting1', 'Custom_NN_Sale_YLighting2', 'Custom_NN_Sale_YLighting3']
#
# Imports = ['Import Inventory Only to Demandware', 'Import PriceBooks to Demandware From Lumens FTP Site',
#            'WorkFlowCatalog-Pricebook-MinMax-Index(Catalog Import) New',
#            'WorkFlowWeekend-MinMax-Index New', 'partial_publish', 'Bazaarvoice Inline Rating Import'
#            ]
#
# feed_exports = ['pla_lu', 'pla_yl_0', 'pla_yl_1', 'pla_yl_2',
#                 'pla_yl_3', 'Bazaarvoice Product Feed']
#
# other_exports = ['Export Orders To NetSuite',
#                  'Export Promotions',
#                  'Export and Upload Adobe']
#
# operational_jobs = ['replication_to_prod', 'replication_to_prod_pricebooks', 'Search Index Full Lumens',
#                     'Search Index Full Ylighting']
#
# prod_jobs = ['Export ActiveData MarginSale Calculation', 'Export Catalog',
#              'Export Orders To NetSuite Lumens(OMS)',
#              'Export Orders To NetSuite YLighting(OMS)', 'Export PriceBooks', 'Export Trade Customers To NetSuite',
#              'Export Trade Customers To NetSuite for YL/YV']


from datetime import datetime
from pytz import timezone
import pytz

date_format='%m/%d/%Y %H:%M:%S %Z'
date = datetime.now(tz=pytz.utc)
print(date)
#
print('Current date & time is:'+ date.strftime(date_format))
#
# date = date.astimezone(timezone('US/Pacific'))
#
# print('Local date & time is  :'+ date.strftime(date_format))