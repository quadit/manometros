# Copyright 2022 - QUADIT, SA DE CV (https://www.quadit.mx)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': "Restrict Supplier Creation",
    'summary': "Restrict supplier creation",
    'category': "Extra Rights",
    'version': '14.0.0.0.1',
    'author': "QUADIT",
    'website': "https://www.quadit.mx",
    'license': "LGPL-3",
    'sequence': 4,
    'depends': ["base"],
    'data': [
        "security/groups.xml",
        "security/account_rules.xml",
    ],
    'development_status': "Beta",
    'maintainers': [
        'kuro088',
    ],
    'installable': True,
    'auto_install': False

}
