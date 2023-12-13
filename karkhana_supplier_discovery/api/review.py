"""
Add a api that puts a Pre Stage Profile under review
"""
import frappe

from karkhana_supplier_discovery.actions.pre_staging.on_update import calculate_profile_percentage

@frappe.whitelist()
def put_under_review(doc):
	"""
	give method url: /api/method/karkhana_supplier_discovery.api.review.put_under_review
	"""

	# calculate completion percentage

	doc = frappe.get_doc('Pre Stage Profile', doc)

	completion_percentage = calculate_profile_percentage(doc)

	if completion_percentage < 50:
		frappe.throw('Profile is incomplete. Cannot put under review.')

	doc.status = 'Under Review'
	doc.save(ignore_permissions=True)
	frappe.db.commit()

