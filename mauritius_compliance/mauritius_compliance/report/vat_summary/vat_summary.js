// Copyright (c) 2024, Eactive and contributors
// For license information, please see license.txt

frappe.query_reports["VAT Summary"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "fieldtype": "Date",
            "label": "From Date",
            "default": frappe.datetime.month_start()
        },
        {
            "fieldname": "to_date",
            "fieldtype": "Date",
            "label": "To Date",
            "default": frappe.datetime.month_end()
        }
	]
};
