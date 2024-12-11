// Copyright (c) 2024, ateeq and contributors
// For license information, please see license.txt

frappe.ui.form.on("Custom Sales Order", {
	setup:function (frm) {
        frm.compute_total = (frm) => {
            if (frm.doc.service_details.length>=1){
                let amount = 0;
                let days = 0
                frm.doc.service_details.forEach(price => {
                    amount += price.amount;
                    days += price.standard_leadtime_in_days
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
});
frappe.ui.form.on('Custom Activity', {
    service_price: function(frm, cdt, cdn) {
        calculate_total(frm, cdt, cdn);
    },
    quantity: function(frm, cdt, cdn) {
        calculate_total(frm, cdt, cdn);
    },
    service: function(frm,cdt,cdn){
        calculate_total(frm, cdt, cdn);
    },
    service_details_remove: function (frm, cdt, cdn){
        frm.compute_total(frm)
    }
});

function calculate_total(frm, cdt, cdn) {
    let child = locals[cdt][cdn];
    let total_price = child.quantity * child.service_price;
    frappe.model.set_value(cdt, cdn, 'amount', total_price);
    frm.compute_total(frm);
}

