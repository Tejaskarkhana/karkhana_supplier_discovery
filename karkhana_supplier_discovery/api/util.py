

def generate_response(status, msg, data=None):
	# frappe.errprint(data)
	# response = Response()
	data = {
		"status"  : status,
		"message" : msg,
		"data"    : data
	}
	# response.mimetype = 'application/json'
	# response.charset = 'utf-8'
	# response.data = json.dumps(data, default=json_handler,separators=(',',':'))
	return data