import frappe
import json


def calculate_profile_percentage(doc):
	field_weightages = {
		"company_logo": 5,
		"company_name": 10,
		"website": 5,
		"email": 10,
		"total_employees": 5,
		"about_us": 10,
		"listing_type": 5,
		"supplier_type": 5,
		"company_type": 5,
		"annual_turnover": 5,
		"year_of_establishment": 5,
		"address": 5,
		"contact": 5,
		"company_gst": 5,
		"export_license_registraton_number": 5,
		"certificates": 5,
		"customer_served": 5,
		"industry_served": 5,
		"industries": 5,
		"manufacturing_process": 5,
		"material_capabilities": 5,
		"finishing_capabilities": 5,
		"design_services": 5,
		"machines": 5
	}

	# List of compulsory fields
	compulsory_fields = ["company_name", "email", "contact", "address", "company_type"]

	# Check for completion and calculate weighted sum
	weighted_sum = 0
	total_weightage = sum(field_weightages.values())
	for field, weight in field_weightages.items():
			if doc.get(field):
					weighted_sum += weight

	# Check for compulsory fields
	all_compulsory_filled = all(doc.get(field) for field in compulsory_fields)

	# Calculate completion percentage
	completion_percentage = int((weighted_sum / total_weightage) * 100)\
	
	return completion_percentage



def update_supplier_stage(doc, method=None):
	# Weightage for each field
	
	completion_percentage = calculate_profile_percentage(doc)

	# do when profile is incomplete only
	# if under review or approved, don't do anything
	if doc.status in ['Under Review', 'Approved']:
		return

	status = None

	if completion_percentage < 50:
		status = 'Profile Incomplete'
	elif completion_percentage >= 50 and completion_percentage < 100:
		status = 'Open For Listing'
	
	frappe.db.set_value('Pre Stage', doc.name, 'status', status)
	frappe.db.set_value('Pre Stage', doc.name, 'profile_percentage', completion_percentage)

	frappe.db.commit()

	

def add_changed(doc):
	json_payload = json.loads(doc.data)
	for changes in json_payload.get('changed'):
		staging_core = frappe.get_doc({
			'doctype': 'Staging Core',
			'doc': doc.ref_doctype,
			'docname': doc.docname,
			'action': 'changed',
			'field': changes[0],
			'previous': changes[1],
			'new': changes[2],
		})
	
		staging_core.save(ignore_permissions=True)
	
	frappe.db.commit()


def row_added(doc):
	json_payload = json.loads(doc.data)
	for changes in json_payload.get('added'):
		row_added = frappe.get_doc({
			'doctype': 'Staging Core',
			'doc': doc.ref_doctype,
			'docname': doc.docname,
			'action': 'row_changed',
			'field': changes[0],
			'row_reference':  changes[1].get('name'),
			'row_index': changes[1].get('idx'),
			'new': json.dumps(changes[1]),
			'previous': '',
		})
	
		row_added.save(ignore_permissions=True)
	
	frappe.db.commit()



def row_changed(doc):
	json_payload = json.loads(doc.data)
	for changes in json_payload.get('row_changed'):
		change = changes[3]
		new = list(map(lambda x: [x[0], x[2]], change))
		previous = list(map(lambda x: [x[0], x[1]], change))

		print(new)
		row_changed = frappe.get_doc({
			'doctype': 'Staging Core',
			'doc': doc.ref_doctype,
			'docname': doc.docname,
			'action': 'row_changed',
			'field': changes[0],
			'row_reference':  changes[2],
			'row_index': changes[1],
			'new': json.dumps(new),
			'previous': json.dumps(previous),
		})
	
		row_changed.save(ignore_permissions=True)
	
	frappe.db.commit()

def post_to_staging(doc, method=None):
	row_added(doc)
	row_changed(doc)
	add_changed(doc)