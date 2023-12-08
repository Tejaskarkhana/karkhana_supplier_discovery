import frappe
import json


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