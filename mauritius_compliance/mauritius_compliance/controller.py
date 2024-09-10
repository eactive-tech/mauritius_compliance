

import frappe

def set_vat_category(doc, method=None):
    if doc.items:
        for item in doc.items:
            if item.custom_vat_category == None:
                item.custom_vat_category = doc.custom_vat_category