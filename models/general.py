from openerp.osv import expression
from openerp import api, fields, models, _

########## ########## ########## ########## ##########
# Type of Emission
########## ########## ########## ########## ##########
class EmissionType(models.Model):
	_name = 'sri.emission.type'
	_description = 'Type of Emission'

	name = fields.Char(string='Type of Emission', size=120, required=True)
	code = fields.Char(size=2, required=True)

	_sql_constraints = [
		('code_unique', 'unique(code)', 'The code must be unique'),
	]

	@api.multi
	@api.depends('name', 'code')
	def name_get(self):
		result = []
		for item in self:
			name = '%s [%s]' % (item.name, item.code)
			result.append((item.id, name))
		return result

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		domain = []
		if name:
			domain = ['|', ('code', '=', name), ('name', operator, name)]
			if operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = ['&'] + domain
		item = self.search(expression.AND([domain, args]), limit=limit)
		return item.name_get()

	@api.one
	def copy(self, default=None):
		default = dict(default or {})
		default.update(
			name=_('%s (copy)') % (self.name or ''),
			code=_('%s (copy)') % (self.code or '')
		)
		return super(EmissionType, self).copy(default)

########## ########## ########## ########## ##########
# Type of Voucher
########## ########## ########## ########## ##########
class VoucherType(models.Model):
	_name = 'sri.voucher.type'
	_description = 'Type of Voucher'

	name = fields.Char(string='Type of Voucher', size=80, required=True)
	code = fields.Char(size=2, required=True)

	_sql_constraints = [
		('code_unique', 'unique(code)', 'The code must be unique'),
	]

	@api.multi
	@api.depends('name', 'code')
	def name_get(self):
		result = []
		for item in self:
			name = '%s [%s]' % (item.name, item.code)
			result.append((item.id, name))
		return result

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		domain = []
		if name:
			domain = ['|', ('code', '=', name), ('name', operator, name)]
			if operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = ['&'] + domain
		item = self.search(expression.AND([domain, args]), limit=limit)
		return item.name_get()

	@api.one
	def copy(self, default=None):
		default = dict(default or {})
		default.update(
			name=_('%s (copy)') % (self.name or ''),
			code=_('%s (copy)') % (self.code or '')
		)
		return super(VoucherType, self).copy(default)

########## ########## ########## ########## ##########
# Type of Identification
########## ########## ########## ########## ##########
class IdentificationType(models.Model):
	_name = 'sri.id.type'
	_description = 'Type of Identification'

	name = fields.Char(string='Type of Identification', size=92, required=True)
	code = fields.Char(size=2, required=True)

	_sql_constraints = [
		('code_unique', 'unique(code)', 'The code must be unique'),
	]

	@api.multi
	@api.depends('name', 'code')
	def name_get(self):
		result = []
		for item in self:
			name = '%s [%s]' % (item.name, item.code)
			result.append((item.id, name))
		return result

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		domain = []
		if name:
			domain = ['|', ('code', '=', name), ('name', operator, name)]
			if operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = ['&'] + domain
		item = self.search(expression.AND([domain, args]), limit=limit)
		return item.name_get()

	@api.one
	def copy(self, default=None):
		default = dict(default or {})
		default.update(
			name=_('%s (copy)') % (self.name or ''),
			code=_('%s (copy)') % (self.code or '')
		)
		return super(IdentificationType, self).copy(default)