import frappe
import json,requests

def create_supplier_master(doc,method):
    supplier_master_check_test = frappe.db.exists("Supplier Master", doc.name)
    if supplier_master_check_test:
        frappe.throw("Supplier is already present in the Supplier Master")
    new_supplier_master_doc = frappe.new_doc("Supplier Master")
    new_supplier_master_doc.company_name = doc.company_name
    new_supplier_master_doc.website= doc.website
    new_supplier_master_doc.total_employees= doc.total_employees
    new_supplier_master_doc.about_us= doc.about_us
    new_supplier_master_doc.listing_type= doc.listing_type
    new_supplier_master_doc.supplier_type= doc.supplier_type
    new_supplier_master_doc.annual_turnover= doc.annual_turnover
    new_supplier_master_doc.year_of_establishment= doc.year_of_establishment
    new_supplier_master_doc.company_gst= doc.company_gst
    new_supplier_master_doc.export_license_registraton_number= doc.export_license_registraton_number
    new_supplier_master_doc.urn= doc.urn
    new_supplier_master_doc.manufacturing_process= doc.manufacturing_process
    new_supplier_master_doc.material_capabilities= doc.material_capabilities
    new_supplier_master_doc.finishing_capabilities= doc.finishing_capabilities
    new_supplier_master_doc.design_services= doc.design_services
    new_supplier_master_doc.machines= doc.machines
    new_supplier_master_doc.allowed_for_listing= doc.allowed_for_listing
    new_supplier_master_doc.slug= doc.slug
    new_supplier_master_doc.featured= doc.featured
    new_supplier_master_doc.supplier_uuid= doc.supplier_uuid
    for i in doc.address:
        new_supplier_master_doc.append("address",get_address(i))
    
    for i in doc.contact:
        new_supplier_master_doc.append("contact",get_contact(i))
    
    for i in doc.certificates:
        new_supplier_master_doc.append("certificates",get_certificates(i))
    
    for i in doc.customer_served:
        new_supplier_master_doc.append("customer_served",get_customer_served(i))
    
    if doc.industry_served:
        for i in doc.industry_served:
            new_supplier_master_doc.append("industry_served",get_industry_served(i))
    
    new_supplier_master_doc.company_logo = doc.company_logo

    new_supplier_master_doc.save(ignore_permissions=True)
    frappe.db.commit()

    print(doc.as_dict())
    # annual_turnover
    # year_of_establishment
    # address (table)//
    # contact (table)//
    # company_gst
    # export_license_registraton_number
    # urn
    # certificates (table)//
    # customer_served (table)//
    # industry_served (table)
    # manufacturing_process
    # material_capabilities
    # finishing_capabilities
    # design_services
    # machines
    # allowed_for_listing

def get_address(address):
    print("address",address.as_dict())
    return{
        "address_title":address.address_title,
        "address_line_1":address.address_line_1,
        "address_line_2":address.address_line_2,
        "city":address.city,
        "state":address.state,
        "country":address.country,
        "pincode":address.pincode,
        "row_reference":address.name

    }
    # data={}
    # return{

    # }
def get_contact(contact):
    return{
        "contact_name":contact.contact_name,
        "designation":contact.designation,
        "email":contact.email,
        "phone":contact.phone,
        "row_reference":contact.name

    }

def get_certificates(certificates):
    return{
        "certificate_name":certificates.certificate_name,
        "image":certificates.image,
        "reference":certificates.reference,
        "row_reference":certificates.name
    }

def get_customer_served(data):
    return{
        "customer_name":data.customer_name,
        "company_logo":data.company_logo,
        "about_project":data.about_project,
        "reference":data.reference,
        "row_reference":data.name
    }

def get_industry_served(data):
    return{
        "industry":data.industry,
        "reference":data.reference,
        "row_reference":data.name
    }

def create_slug(doc,method):
    slug_name = doc.company_name.strip().replace(" ","-").lower()
    unique_element = str(time.time()) 
    hashed_slug = create_unique_slug_hash(unique_element)

    doc.slug = slug_name+"-"+str(hashed_slug[-5:])
    


import hashlib
import time

def create_unique_slug_hash( unique_element):
    # Combine the slug with the unique element
    combined_input = f"{unique_element}"

    # Convert the combined input to bytes
    combined_bytes = combined_input.encode('utf-8')
    
    hash_object = hashlib.md5()

    # Update the hash object with the slug bytes
    hash_object.update(combined_bytes)


    hash_hex = hash_object.hexdigest()

    return hash_hex

    