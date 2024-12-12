# Copyright (c) 2024, ateeq and contributors
# For license information, please see license.txt
# print('\n\n\n\n\n\n\n\n')
import frappe
from frappe.model.document import Document
import ast

class CustomSalesOrder(Document):
    def before_save(self):
        # print('\n\n\n\n\n\n\n\n')
        # print(type(self.add_multiple_asset[0]))
        # print(self.add_multiple_asset[0])
        # print('\n\n\n\n\n\n\n\n')
        all_service = []
        for asset in self.add_multiple_asset:
            all_service.append(asset.asset_service_required)        
        # FCR
        fcr = ['FCR  Bags Small','FCR  Footwear Any Size']
        if any(service in all_service for service in fcr):
            self.fcr = 1
        else:
            self.fcr = 0
        # Cleaning
        cleaning = ['Cleaning Bags Small','Cleaning Footwear Any Size']
        if any(service in all_service for service in cleaning):
            self.cleaning = 1
        else:
            self.cleaning = 0
        
		# Stiching - Small Any Small
        if 'Stiching - Small Any Small' in all_service:
            self.stiching = 1
        else:
            self.stiching = 0
        
		# Glue Any Small
        if 'Glue Any Small' in all_service:
            self.glue = 1
        else:
            self.glue = 0

		# Resize - Machine    
        if 'Resize - Machine Footwear Any Size' in all_service:
            self.resize = 1
        else:
            self.resize = 0

		# Spot    
        if 'Spot Footwear Any Size' in all_service:
            self.spot = 1
        else:
            self.spot = 0        

@frappe.whitelist()
def get_estimated_date(doctype,docname):
	get_user_assinged = frappe.db.get_value(doctype,docname,'_assign')
	get_user_assigned_list = ast.literal_eval(get_user_assinged)
	get_assigned_task = frappe.get_list('ToDo',filters={'reference_type':doctype,'allocated_to':get_user_assigned_list[0],'status':'Open'},fields=['custom_standard_leadtime_in_days'])
	day = 0
	for i in get_assigned_task:
		day+=(i['custom_standard_leadtime_in_days'])	
	return frappe.utils.add_days(frappe.utils.today(),day)



def before_save(self):
    # Loop through all assets in the add_multiple_asset list
    for asset in self.add_multiple_asset:
        # Print asset service for debugging purposes
        print('\n\n\n\n\n\n\n\n')
        print(asset.asset_service_required)
        print('\n\n\n\n\n\n\n\n')

        # Initialize/reset flags
        self.cleaning = 0
        self.stiching = 0
        self.glue = 0
        self.resize = 0
        self.spot = 0

        # Check for cleaning services
        if asset.asset_service_required in ['Cleaning Footwear Any Size', 'Cleaning Bags Small', 
                                            'FCR  Bags Small', 'FCR  Footwear Any Size', 'FCR Footwear Any Size']:
            self.cleaning = 1
        
        # Check for stiching service
        if asset.asset_service_required == 'Stiching - Small Any Small':
            self.stiching = 1
        
        # Check for glue service
        if asset.asset_service_required == 'Glue Any Small':
            self.glue = 1
        
        # Check for resize service
        if asset.asset_service_required == 'Resize - Machine Footwear Any Size':
            self.resize = 1
        
        # Check for spot service
        if asset.asset_service_required == 'Spot Footwear Any Size':
            self.spot = 1
