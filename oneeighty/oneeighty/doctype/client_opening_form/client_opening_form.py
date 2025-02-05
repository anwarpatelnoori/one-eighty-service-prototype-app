# Copyright (c) 2025, ateeq and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.password import update_password
from frappe.utils import get_url

class ClientOpeningForm(Document):
    """Custom DocType for client onboarding."""
    pass

def create_user(self, event=None):
    """Creates a website user when a client submits the form."""
    
    if not self.email:
        frappe.throw("Email is required to create an account.")

    # Check if a user with this email already exists
    if frappe.db.exists("User", self.email):
        frappe.throw(f"A user with this email ({self.email}) already exists.")

    # Create a new Website User
    user = frappe.get_doc({
        "doctype": "User",
        "email": self.email,
        "first_name": self.customer_name or "",
        "send_welcome_email": 0,  # We will send a manual reset password email
        "user_type": "Website User",
        "enabled": 1
    })
    user.insert(ignore_permissions=True)

    # Generate a random password and enforce reset
    new_password = frappe.generate_hash(length=10)
    update_password(user.name, new_password)

    # Send Reset Password Email
    send_password_reset_email(self.email)

    # frappe.msgprint(f"Website User created successfully for {self.email}")

def send_password_reset_email(email):
    """Send password reset email to the customer"""
    
    reset_link = get_url(f"/update-password?key={frappe.generate_hash(email, 10)}")
    
    subject = "Reset Your Password"
    message = f"""
        <p>Dear User,</p>
        <p>Your account has been created successfully.</p>
        <p><b>Click the link below to set your password:</b></p>
        <p><a href="{reset_link}" target="_blank">{reset_link}</a></p>
        <p>Thank you.</p>
    """

    frappe.sendmail(
        recipients=email,
        subject=subject,
        message=message
    )