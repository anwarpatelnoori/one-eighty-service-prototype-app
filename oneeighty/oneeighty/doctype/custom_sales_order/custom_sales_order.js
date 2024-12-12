// Copyright (c) 2024, ateeq and contributors
// For license information, please see license.txt

frappe.ui.form.on("Custom Sales Order", {
	setup:function (frm) {
        frm.compute_total = (frm) => {
            if (frm.doc.add_multiple_asset.length>=1){
                let amount = 0;
                let days = 0
                frm.doc.add_multiple_asset.forEach(price => {
                    amount += price.cost;
                    days += price.estd_day
                });
                frm.set_value('total_amount', amount);
                frm.set_value('total_estimated_days',days)
            }
            else{
                frm.set_value('total_amount', 0);
                frm.set_value('total_estimated_days',0)
            }
        };
	},
    get_estimated_date:function(frm){
        frappe.call({
            method:'oneeighty.oneeighty.doctype.custom_sales_order.custom_sales_order.get_estimated_date',
            args:{
                'docname':frm.doc.name,
                'doctype':frm.doc.doctype
            },
            callback:function(r){
                if(r.message){
                    frm.set_value('estimate_date',r.message)
                }
            }
        })
    }
});
frappe.ui.form.on('Custom Multiple Asset', {
    asset_service_required: function(frm, cdt, cdn) {
        frm.compute_total(frm);
    },
    cost: function(frm, cdt, cdn) {
        frm.compute_total(frm)
    },
    add_multiple_asset_remove: function (frm, cdt, cdn){
        frm.compute_total(frm)
    }
});
