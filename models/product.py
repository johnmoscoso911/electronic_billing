from openerp.osv import expression
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, _

########## ########## ########## ########## ##########
# Product
########## ########## ########## ########## ##########
class Product(models.Model):
	_name = 'sri.product'
	_description = 'Product'

	name = fields.Char(string='Name', size=120, required=True)
	code = fields.Char(string='Code', size=20, required=True)
	ancillary_code = fields.Char(string='Ancillary Code', size=20)
	unit_price = fields.Float(string='Unit Price', digits=(20, 6), required=True)
	discount = fields.Float(string='Discount (%)', digits=(3, 2), required=True, default=0, help='For percent enter a ratio between 0-100')
	iva = fields.Selection([
		('0', '0%'),
		('2', '12%'),
		('6', 'No subject to tax'),
		('7', 'Tax exempt'),
	], string='Fare of I.V.A.', required=True, default='2')
	discount_amount = fields.Float(string='Discount', compute='_compute_amount')
	iva_amount = fields.Float(string='I.V.A.', compute='_compute_amount')
	total = fields.Float(string='Total', compute='_compute_amount')
	#tax_ids = fields.One2many('sri.product.tax', 'product_id', string='Taxes', copy=False)
	additional_ids = fields.One2many('sri.product.additional', 'product_id', string='Additional Fields', copy=False)

	_sql_constraints = [
		('unit_price_check', 'check(unit_price > 0)', 'The unit price must be greater than 0'),
		('discount_check', 'check(discount between 0 and 100)', 'Must be entered a value between 0-100'),
	]

	#@api.multi
	@api.one
	@api.depends('unit_price', 'discount', 'iva')
	def _compute_amount(self):
		#for product in self:
		#	product.discount_amount = unit_price
		self.discount_amount = self.unit_price * self.discount / 100
		percentage = 0
		if self.iva == '2':
			percentage = 0.12
		self.iva_amount = (self.unit_price - self.discount_amount) * percentage
		self.total = (self.unit_price - self.discount_amount) + self.iva_amount
		#sum(line.child_field for line in self.unit_price)

########## ########## ########## ########## ##########
# Additional Fields to Product
########## ########## ########## ########## ##########
class ProductAdditional(models.Model):
	_name = 'sri.product.additional'
	_description = 'Additional Fields to Product'

	name = fields.Char(string='Name', size=80, required=True)
	value = fields.Char(string='Value', size=300, required=True)
	product_id = fields.Many2one('sri.product', string='Product', required=True)

########## ########## ########## ########## ##########
# Taxes and Rates to Product
########## ########## ########## ########## ##########
class ProductTax(models.Model):
	_name = 'sri.product.tax'
	_description = 'Taxes and Rates to Product'
	_rec_name = 'tax'

	tax = fields.Selection([
		('2', 'IVA'),
		('3', 'ICE'),
		('5', 'IRBPNR'),
	], string='Tax', required=True, default='2')
	# tax_code = fields.Integer(string='Tax Code', required=True, help="Use:\n"\
	# 	" '0' 0%% IVA\n"\
	# 	" '2' 12%% IVA\n"\
	# 	" '6' No subject to tax\n"\
	# 	" '7' Tax exempt")
	#tax_rate = fields.Float(string='Tax Rate', digits=(3, 2), help='For percent enter a ratio between 0-100')
	product_id = fields.Many2one('sri.product', string='Product', required=True)

	#_sql_constraints = [
	#	('tax_rate_check', 'check(tax_rate between 0 and 100)', 'Must be entered a value between 0-100'),
	#	('tax_unique', 'unique(tax, product_id)', 'Tax must be unique for Product'),
	#]