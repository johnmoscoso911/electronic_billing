# -*- coding: 850 -*-
{
	'name': 'Facturaci\xF3n Electr\xF3nica',
	'version': '0.1',
	'summary': 'Facturaci\xF3n electr\xF3nica para Ecuador',
	'sequence': 99,
	'description': u"""
Emisión de Comprobantes Electrónicos
====================================
 * Factura
 * Nota de Crédito
 * Nota de Débito
 * Guía de Remisión
 * Comprobante de Retención
	""",
	'category': 'Custom',
	'author': 'John Moscoso',
	#'website': 'http://wwww.google.com',
	'depends': ['website'],
	'data': [
		#'security/electronic_billing.xml',
		'security/ir.model.access.csv',
		'data/data.xml',
		'views/menuitem.xml',
		'views/emission_type_view.xml',
		'views/voucher_type_view.xml',
		'views/id_type_view.xml',
		'views/customer_view.xml',
		'views/product_view.xml',
	],
	'demo': [
		#'demo/.xml',
	],
	'qweb': [
		#'static/src/xml/.xml',
	],
	'application': True,
	'auto_install': False,
}