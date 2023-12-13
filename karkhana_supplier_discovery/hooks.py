from . import __version__ as app_version

app_name = "karkhana_supplier_discovery"
app_title = "Supplier Discovery"
app_publisher = "karkhana.io"
app_description = "Supplier Discovery"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "weadmin@karkhana.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/karkhana_supplier_discovery/css/karkhana_supplier_discovery.css"
# app_include_js = "/assets/karkhana_supplier_discovery/js/karkhana_supplier_discovery.js"

# include js, css files in header of web template
# web_include_css = "/assets/karkhana_supplier_discovery/css/karkhana_supplier_discovery.css"
# web_include_js = "/assets/karkhana_supplier_discovery/js/karkhana_supplier_discovery.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "karkhana_supplier_discovery/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "karkhana_supplier_discovery.install.before_install"
# after_install = "karkhana_supplier_discovery.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "karkhana_supplier_discovery.uninstall.before_uninstall"
# after_uninstall = "karkhana_supplier_discovery.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "karkhana_supplier_discovery.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Version": {
		"after_insert": "karkhana_supplier_discovery.actions.pre_staging.on_update.post_to_staging"
	},
	"Pre Stage":{
		"before_insert" : "karkhana_supplier_discovery.event_handler.pre_stage.create_slug",
		"on_update": "karkhana_supplier_discovery.actions.pre_staging.on_update.update_supplier_stage",
		"after_insert":"karkhana_supplier_discovery.event_handler.pre_stage.create_supplier_master"
	},
	"Staging Core":{
		"on_update":["karkhana_supplier_discovery.event_handler.staging_core.on_staging_core_update"
			]
			
		

	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"karkhana_supplier_discovery.tasks.all"
#	],
#	"daily": [
#		"karkhana_supplier_discovery.tasks.daily"
#	],
#	"hourly": [
#		"karkhana_supplier_discovery.tasks.hourly"
#	],
#	"weekly": [
#		"karkhana_supplier_discovery.tasks.weekly"
#	]
#	"monthly": [
#		"karkhana_supplier_discovery.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "karkhana_supplier_discovery.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "karkhana_supplier_discovery.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "karkhana_supplier_discovery.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["karkhana_supplier_discovery.utils.before_request"]
# after_request = ["karkhana_supplier_discovery.utils.after_request"]

# Job Events
# ----------
# before_job = ["karkhana_supplier_discovery.utils.before_job"]
# after_job = ["karkhana_supplier_discovery.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"karkhana_supplier_discovery.auth.validate"
# ]

