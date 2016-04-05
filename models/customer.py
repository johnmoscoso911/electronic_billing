import re
# sudo apt-get install python-lepl
import lepl.apps.rfc3696

from openerp.osv import expression
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, _

########## ########## ########## ########## ##########
# Customer
########## ########## ########## ########## ##########
class Customer(models.Model):
	_name = 'sri.customer'
	_description = 'Customer'

	name = fields.Char(string='Name', size=92, required=True)
	identification = fields.Char(string='Number of Identification', size=20, required=True)
	email = fields.Char(string='Email Address', size=200, required=True)
	plate = fields.Char(string='License Plate', size=10, help='In the case of remission guides')
	phone = fields.Char(string='Phone', size=20)
	address = fields.Char(string='Address', size=300)

	_sql_constraints = [
		('identification_unique', 'unique(identification)', 'The number of identification must be unique'),
	]

	@api.one
	@api.constrains('email')
	def _check_email(self):
		email_validator = lepl.apps.rfc3696.Email()
		for customer in self:
			if not email_validator(customer.email):
				#raise ValueError(_('Email address is not valid') % customer.name)
				raise ValidationError(_('Email address is not valid'))
				#raise UserError(_('Email address is not valid'))

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		domain = []
		if name:
			domain = ['|', ('identification', operator, name), ('name', operator, name)]
			if operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = ['&'] + domain
		customer = self.search(expression.AND([domain, args]), limit=limit)
		return customer.name_get()

	@api.one
	def copy(self, default=None):
		default = dict(default or {})
		default.update(
			identification = _('%s (copy)') % (self.identification or '')
		)
		return super(Customer, self).copy(default)