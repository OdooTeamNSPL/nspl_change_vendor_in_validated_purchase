{
    'name': 'Change Vendor in Validated Purchase',
    'version': '17.0',
    'summary': 'Allow changing vendor in validated purchase orders with group access',
    'description': """
    Allows changing the vendor in validated purchase orders with proper access control. 
    Automatically updates linked receipts, bills, and payments to reflect the new vendor.
    """,

    'category': 'Purchase/accountant',
    'sequence': 5,
    'author': 'Namah Softech Private Limited',
    'contributors': 'Mohit Nare',
    'website': 'http://namahsoftech.com/',
    'support': 'support@namahsoftech.com',
    'price': 14.99,
    'currency': 'USD',
    'license': 'OPL-1',
    'depends': ['base', 'purchase', 'stock','account_accountant'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'views/change_vendor_wizard.xml'
    ],
    'images': ['static/description/img/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
