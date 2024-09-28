# Copyright (c) 2024, Eactive and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	selected_vat_category = filters.get("vat_category") 

	columns = [
		{
			"fieldname": "name",
			"label": "Document Name",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": "150 px"
		},
		{
			"fieldname": "posting_date",
			"label": "Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "customer",
			"label": "Party",
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "total_amount",
			"label": "Total Amount",
			"fieldtype": "Float"
		},
		{
			"fieldname": "taxable_amount",
			"label": "Taxable Amount",
			"fieldtype": "Float"
		},
		{
			"fieldname": "tax_amount",
			"label": "Tax Amount",
			"fieldtype": "Float"
		},
	]

	result = []


	result = frappe.db.sql("""
		SELECT
			si.name,
			si.posting_date,
			si.customer,
			si.grand_total AS total_amount,
			stc.tax_amount AS tax_amount,
			sii.amount as taxable_amount
		FROM
			`tabSales Invoice` si
		LEFT JOIN
			`tabSales Invoice Item` AS sii ON sii.parent=si.name
		LEFT JOIN
			`tabSales Taxes and Charges` stc ON stc.parent = si.name
		WHERE
			si.posting_date BETWEEN %s AND %s 
			AND si.custom_vat_category = %s
	""", (from_date, to_date,selected_vat_category), as_dict=True)

	return columns, result
