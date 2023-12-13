import frappe
import requests
import json
from frappe.auth import LoginManager
import os
from karkhana_logging import log
from karkhana_supplier_discovery.api.util import generate_response


@frappe.whitelist()
@log
def get_featured_suppliers(*args, **kwargs):
    try:
        # featured_suppliers_list = frappe.db.get_list('Supplier Master',filters={'featured': 1},fields=['*'],page_length=0)
        featured_suppliers_list = [frappe.get_doc("Supplier Master", item.name).as_dict() for item in frappe.get_list("Supplier Master",filters={'featured': 1})]
        print(featured_suppliers_list)
        


        return generate_response('green','featured suppliers returned',featured_suppliers_list)
    except Exception as e:
        return generate_response('red','Error in returing featured suppliers',e)

@frappe.whitelist()
@log
def get_verified_suppliers(*args, **kwargs):
    try:
        # verified_suppliers_list = frappe.db.get_list('Supplier Master',filters={'listing_type': "Verified"},fields=['company_name'],page_length=0)
        verified_suppliers_list = [frappe.get_doc("Supplier Master", item.name).as_dict() for item in frappe.get_list("Supplier Master",filters={'listing_type': "Verified"})]
        # print(Verified_suppliers_list)
        return generate_response('green','verified suppliers returned',verified_suppliers_list)
    except Exception as e:
        return generate_response('red','Error in returing verified suppliers',e)

@frappe.whitelist()
@log
def get_audited_suppliers(*args, **kwargs):
    try:
        audited_suppliers_list = frappe.db.get_list('Supplier Master',filters={'listing_type': "Audited"},fields=['company_name'],page_length=0)
        # print(Verified_suppliers_list)
        return generate_response('green','Audited suppliers returned',audited_suppliers_list)
    except Exception as e:
        return generate_response('red','Error in returing Audited suppliers',e)

@frappe.whitelist()
@log
def get_supplier_detail(slug,*args, **kwargs):
    try:
        supplier_master_doc_check = frappe.db.exists("Supplier Master",{"slug":slug} )
        if not supplier_master_doc_check:
            return generate_response('red','Supplier Does Not Exist')
        
        supplier_master_doc = frappe.get_doc("Supplier Master",supplier_master_doc_check)
        return generate_response('green','Supplier data returned',supplier_master_doc)
    except Exception as e:
        return generate_response('red','Error in returing Audited suppliers',e)


@frappe.whitelist()
@log
def get_supplier_address(supplier_uuid,*args, **kwargs):
    try:
        supplier_master_doc_check = frappe.db.exists("Supplier Master",{"uuid":supplier_uuid} )
        if not supplier_master_doc_check:
            return generate_response('red','Supplier Does Not Exist')
        
        supplier_master_doc = frappe.get_doc("Supplier Master",supplier_master_doc_check)
        address = []
        contact = []
        for add in supplier_master_doc.address:
            address.append({
                "name": add.name,
                "address_title": add.address_title,
                "address_line_1": add.address_line_1,
                "address_line_2": add.address_line_2,
                "city": add.city,
                "state": add.state,
                "country": add.country,
                "pincode": add.pincode
            })

        for cont in supplier_master_doc.contact:
            contact.append({
                "name": cont.name,
                "contact_name": cont.contact_name,
                "designation": cont.designation,
                "email": cont.email,
                "phone": cont.phone
            })
        return generate_response('green','Supplier data returned',{"address":address,"contact":contact})
    except Exception as e:
        return generate_response('red','Error in returing Address & contact suppliers',e)

@frappe.whitelist()
@log
def supplier_search(*args, **kwargs):
    if frappe.local.request.method == "POST" and frappe.local.request.data:
        kwargs = json.loads(frappe.local.request.data)
    conditions = []
    values = []
    child_table_filters={
        "ha":"child table",
        "city":"child1"
    }
    temp = {}
    # return kwargs

    for field, value in kwargs.items():
        if value:
            # Check if the field belongs to the child table, prefix appropriately
            
            if field == "cmd":
                break
            if value == "null":
                continue
            if field in child_table_filters.keys():  # Replace with actual child table fields
                field = f'{child_table_filters[field]}.`' + field + '`'
            elif field == "search_term":
                search_condition = f"(parent.`manufacturing_process` LIKE '%{value}%'  OR parent.`material_capabilities` LIKE '%{value}%' OR parent.`finishing_capabilities` LIKE '%{value}%' OR parent.`design_services` LIKE '%{value}%' OR parent.`machines` LIKE '%{value}%')"
                conditions.append(search_condition)
                break
            else:
                if field == "services_options":
                    search_service_condition = []
                    temp=[]
                    for i in value:
                        temp.append(i)
                        search_condition = f"(parent.`manufacturing_process` LIKE '%{i}%'  OR parent.`material_capabilities` LIKE '%{i}%' OR parent.`finishing_capabilities` LIKE '%{i}%' OR parent.`design_services` LIKE '%{i}%' OR parent.`machines` LIKE '%{i}%')"
                        search_service_condition.append(search_condition)
                    
                    total_search_condition = "  OR ".join(search_service_condition) if search_service_condition else "1 = 1"
                    conditions.append(total_search_condition)
                    # return temp
                    continue
                field = 'parent.`' + field + '`'

            conditions.append(f"{field} = '{value}'")
            values.append(value)
            temp[field] = value
    query_conditions = " AND ".join(conditions) if conditions else "1 = 1"
    query = """SELECT parent.`name`, parent.`email`, parent.`about_us`,parent.`annual_turnover`,parent.`year_of_establishment`,parent.`total_employees`,parent.`company_gst` FROM `tabSupplier Master` AS parent LEFT JOIN `tabSupplier Master Address` AS child1 ON parent.`name` = child1.`parent` LEFT JOIN `tabSupplier Master Ceritificate` AS child2 ON parent.`name` = child2.`parent` WHERE {}""".format(query_conditions)
    # return query
    result = frappe.db.sql(query, debug = 1,as_dict=True)
    return generate_response('green','Supplier list returned',result )

@frappe.whitelist()
@log
def supplier_type_options(*args, **kwargs):
    try:
        supplier_master_doctype = frappe.get_doc("DocType","Supplier Master")
        
        for i in supplier_master_doctype.fields:
            if i.fieldname == "company_type":
                return generate_response('green','Returing Supplier Type Options',i.options.split("\n"))
        # return supplier_master_doctype.fields.options
    except Exception as e:
        return generate_response('red','Error in returing Supplier Type Options',e)


@frappe.whitelist()
@log
def service_options(*args, **kwargs):
    try:
        service_json={
            "Sheet Metal":["Laser Cutting & Bending","Laser Cutting"],
            "Vacuum Casting":"",
            "3D Printing":["SLS","SLA","MJF","FDM","DMLS","DLP"],
            "Injection Molding":"",
            "Help me Choose":"",
            "Forging":"",
            "Fabrication":"",
            "Extrusion":"",
            "CNC Machining":["CNC Milling","CNC Turning"],
            "Casting":"",
            "As per Technical Drawings":""
        }
        op_list=[]
        for i in service_json.keys():
            op_list.append(i)
            if service_json[i] != "":
                op_list.append(service_json[i])

        return generate_response('green','Returing service Options',op_list)
        # return supplier_master_doctype.fields.options
    except Exception as e:
        return generate_response('red','Error in returing Supplier Type Options',e)


@frappe.whitelist()
def test(*args, **kwargs):
    if frappe.local.request.method == "POST" and frappe.local.request.data:
        kwargs = json.loads(frappe.local.request.data)
        # return kwargs
    conditions = []
    values = []
    child_table_filters={
        "ha":"child table",
        "city":"child1"
    }
    temp = {}
    # return kwargs

    for field, value in kwargs.items():
        if value:
            # Check if the field belongs to the child table, prefix appropriately
            
            if field == "cmd":
                break
            if value == "null":
                continue
            if field in child_table_filters.keys():  # Replace with actual child table fields
                field = f'{child_table_filters[field]}.`' + field + '`'
            elif field == "search_term":
                search_condition = f"(parent.`manufacturing_process` LIKE '%{value}%'  OR parent.`material_capabilities` LIKE '%{value}%' OR parent.`finishing_capabilities` LIKE '%{value}%' OR parent.`design_services` LIKE '%{value}%' OR parent.`machines` LIKE '%{value}%')"
                conditions.append(search_condition)
                continue
            else:
                if field == "services_options":
                    search_service_condition = []
                    temp=[]
                    for i in value:
                        temp.append(i)
                        search_condition = f"(parent.`manufacturing_process` LIKE '%{i}%'  OR parent.`material_capabilities` LIKE '%{i}%' OR parent.`finishing_capabilities` LIKE '%{i}%' OR parent.`design_services` LIKE '%{i}%' OR parent.`machines` LIKE '%{i}%')"
                        search_service_condition.append(search_condition)
                    
                    total_search_condition = "  OR ".join(search_service_condition) if search_service_condition else "1 = 1"
                    conditions.append(total_search_condition)
                    # return temp
                    continue

                field = 'parent.`' + field + '`'

            conditions.append(f"{field} = '{value}'")
            values.append(value)
            # temp[field] = value
    # return temp
    query_conditions = " AND ".join(conditions) if conditions else "1 = 1"
    query = """SELECT parent.`name`, parent.`about_us`,parent.`annual_turnover`,parent.`year_of_establishment`,parent.`total_employees`,parent.`company_gst` FROM `tabSupplier Master` AS parent LEFT JOIN `tabSupplier Master Address` AS child1 ON parent.`name` = child1.`parent` LEFT JOIN `tabSupplier Master Ceritificate` AS child2 ON parent.`name` = child2.`parent` WHERE {}""".format(query_conditions)
    # return query
    result = frappe.db.sql(query, debug = 1,as_dict=True)
    return generate_response('green','Supplier list returned',result)




@frappe.whitelist()
@log
def supplier_search2(*args, **kwargs):
    parent_filter = {}
    parent_or_filter = {}
    result = []        
    json_data = kwargs
    city = json_data.get("city")
    address_filter = {}
    if city:
        address_filter["city"] = city
    parent_doc_list = frappe.get_all("Supplier Master Address",filters=address_filter,fields=["parent"])

    if len(parent_doc_list) > 0:
        parent_filter["name"] = ["in",[i["parent"] for i in parent_doc_list]]
    
    if json_data.get("search_term"):
        parent_or_filter["manufacturing_process"] = ["like",f"%{json_data.get('search_term')}%"]
        parent_or_filter["material_capabilities"] = ["like", f"%{json_data.get('search_term')}%"]
        parent_or_filter["finishing_capabilities"] = ["like", f"%{json_data.get('search_term')}%"]
        parent_or_filter["design_services"] = ["like", f"%{json_data.get('search_term')}%"]
        parent_or_filter["machines"] = ["like", f"%{json_data.get('search_term')}%"]
    
    if json_data.get("services_options"):
        parent_or_filter["manufacturing_process"] = ["like"] + [f"%{i}%" for i in json_data.get("services_options",[])]
        parent_or_filter["material_capabilities"] = ["like"] + [f"%{i}%" for i in json_data.get("services_options",[])]
        parent_or_filter["finishing_capabilities"] = ["like"] + [f"%{i}%" for i in json_data.get("services_options",[])]
        parent_or_filter["design_services"] = ["like"] + [f"%{i}%" for i in json_data.get("services_options",[])]
        parent_or_filter["machines"] = ["like"] + [f"%{i}%" for i in json_data.get("services_options",[])]
    result = frappe.get_all("Supplier Master",filters=parent_filter,or_filters=parent_or_filter,fields=["name","about_us",
                                                                    "annual_turnover",
                                                                    "total_employees",
                                                                    "year_of_establishment",
                                                                    "company_gst"])
    return generate_response('green','Supplier list returned',result )
