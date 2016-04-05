import re

from openerp.osv import expression
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, _

########## ########## ########## ########## ##########
# Issuing
########## ########## ########## ########## ##########
class Issuing(models.Model):
	_name = 'sri.issuing'
	_description = 'Issuing'

	name = fields.Char(string='Name', size=300, required=True)
	ruc = fields.Char(string='R.U.C.', size=13, required=True)
	tradename = fields.Char(string='Trade Name', size=300)
	parent_establishment_address = fields.Char(string='Address of Parent Establishment', size=300, required=True)
	establishment_address = fields.Char(string='Address of Establishment', size=300)
	establishment_code = fields.Char(string='Address of Establishment', size=3, required=True)
	issue_point_code = fields.Char(string='Issue Point Code', size=3, required=True)
	resolution_number = fields.Char(string='Resolution Number (Special Contributor)', size=5)
	obliged_accounting = fields.Selection([
		('SI', 'Yes'),
		('NO', 'No'),
	], string='', required=True)
	emission_type_id = fields.Many2one('sri.emission.type', string='Type of Emission', required=True)
	environment = fields.Selection([
		('1', 'Test'),
		('2', 'Production'),
	], string='', required=True, default='2')

	_sql_constraints = [
		('ruc_unique', 'unique(ruc)', 'The R.U.C. must be unique'),
	]

	@api.one
	@api.constrains('ruc', 'resolution_number')
	def _check_ruc(self):
		pattern = re.compile('\d{13}')
		for issue in self:
			match = pattern.match(issue.ruc)
			if match == None:
				#raise ValueError(_('Number of R.U.C. must contain 13 digits') % issue.name)
				raise ValidationError(_('Number of R.U.C. must contain 13 digits'))
				#raise UserError(_('Number of R.U.C. must contain 13 digits'))
			if issue.resolution_number:
				match = re.compile('\d{3,5}').match(issue.resolution_number)
				if match == None:
					raise ValidationError(_('Number of resolution must contain between 3 and 5 digits'))

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		domain = []
		if name:
			domain = ['|', ('ruc', operator, name), ('name', operator, name), ('tradename', operator, name)]
			if operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = ['&'] + domain
		item = self.search(expression.AND([domain, args]), limit=limit)
		return item.name_get()

	@api.one
	def copy(self, default=None):
		default = dict(default or {})
		default.update(
			ruc = _('%s999') % (self.ruc[0:10] or '')
		)
		return super(Issuing, self).copy(default)
