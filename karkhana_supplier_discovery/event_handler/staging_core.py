import frappe
import json,requests
import ast

def on_staging_core_update(doc,method):
    prev_doc = doc.get_doc_before_save()
    if prev_doc and doc.status and doc.status == "Approved" and prev_doc.status == "Pending":
        print("approve")
        approve_changes(doc)
    if prev_doc and doc.status and doc.status == "Rejected" and prev_doc.status == "Pending":
        reject_changes(doc)
        print("reject")
    print(doc)

def approve_changes(doc):
    print("inside approve_changes")
    supplier_master_check_test = frappe.db.exists("Supplier Master", doc.docname)
    if not supplier_master_check_test:
        return
    supplier_master = frappe.get_doc("Supplier Master",supplier_master_check_test)

    if doc.action == "changed":
        # supplier_master. = doc.new
        if doc.field == "year_of_establishment":
            # a= "16-11-2023"
            b = doc.new.split("-")
            # print(b)
            stri = ""
            for i in range(len(b)-1,-1,-1):
                print(b[i])
                stri+=b[i] +"-"
            doc.new = stri[0:-1]

        setattr(supplier_master, doc.field, doc.new)
        supplier_master.save(ignore_permissions=True)
        frappe.db.commit()
    elif doc.action == "row_changed":
        if  doc.previous:
            edit_row(doc)



             


def reject_changes(doc):
    pre_stage_doc = frappe.get_doc("Pre Stage",doc.docname)

    if doc.action == "changed":
        if doc.field == "year_of_establishment":
            # a= "16-11-2023"
            b = doc.previous.split("-")
            # print(b)
            stri = ""
            for i in range(len(b)-1,-1,-1):
                print(b[i])
                stri+=b[i] +"-"
            doc.previous = stri[0:-1]
        
        setattr(pre_stage_doc, doc.field, doc.previous)
        pre_stage_doc.save(ignore_permissions=True)
        frappe.db.commit()


    print(doc)

def edit_row(doc):
    print("inside rdit row")
    child_table_json={
        "address":"Supplier Master Address",
        "contact":"Supplier Master Contact",
        "certificates":"Supplier Master Ceritificate",
        "customer_served":"Supplier Master Customer",
        "industry_served":"Supplier Master Industry Served"
    }
    child_table_check  = frappe.db.exists(child_table_json[doc.field],{"row_reference":doc.row_reference})
    print("child_table_check",child_table_check)
    if not child_table_check:
        return 
    child_table = frappe.get_doc(child_table_json[doc.field],child_table_check)
    try:
        child_row = eval(doc.new)
    except Exception as e:
        return 
    # print(eval(doc.new))
    for i in child_row:
        print(i)
        setattr(child_table, i[0], i[1])
    child_table.save(ignore_permissions=True)
    frappe.db.commit()
    

    

    


