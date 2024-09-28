# Copyright (c) 2024, Eactive and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	columns = [
		{
			"fieldname": "vat_category",
			"label": "Vat Category",
			"fieldtype": "Link",
			"options": "VAT Category",
			"width": "500 px"
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

	vat_categories = frappe.db.sql("""
		SELECT
			vc.name as vat_category,
			vc.lft, vc.rgt,
			vc.parent_vat_category as parent,
			(COUNT(parent.name) - 1) AS indent
		FROM
			`tabVAT Category` AS vc,
			`tabVAT Category` AS parent
		WHERE
			vc.lft BETWEEN parent.lft AND parent.rgt
		GROUP BY 
			vc.name
		ORDER BY 
			vc.lft
	""", as_dict=True)

	for category in vat_categories:
		invoices = frappe.db.sql("""
			SELECT
				SUM(sii.amount) AS amount,
				SUM(stc.tax_amount) as tax_amount
			FROM
				`tabSales Invoice Item` sii
			LEFT JOIN
				`tabSales Invoice` AS si ON sii.parent = si.name
			LEFT JOIN 
				`tabVAT Category` vc ON vc.name = sii.custom_vat_category
			LEFT JOIN
				`tabSales Taxes and Charges` stc ON stc.parent = si.name
			WHERE
				vc.lft >= %s AND vc.rgt <= %s 
				AND si.posting_date BETWEEN %s AND %s
		""", (category.get("lft"), category.get("rgt"), from_date, to_date), as_dict=True)
    
		#frappe.log_error('invoice',invoices)

		# Directly assign the taxable amount after the query
		taxable_amount = invoices[0].get("amount") if invoices and invoices[0].get("amount") else 0
		category["taxable_amount"] = taxable_amount
		tax_amount = invoices[0].get("tax_amount") if invoices and invoices[0].get("tax_amount") else 0
		category["tax_amount"] = tax_amount
		
		result.append(category)

	return columns, result
