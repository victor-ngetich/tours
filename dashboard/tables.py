from __future__ import absolute_import ,unicode_literals
from dashboard.models import booking,payment
import django_tables2 as tables


# class CheckBoxColumnWithName(tables.CheckBoxColumn):
#     @property
#     def header(self):
#         return self.verbose_name

class PaymentsTable(tables.Table):
	# amend = CheckBoxColumnWithName(verbose_name="Select", accessor="pk")
	class Meta:
		model = payment
		fields = ("booking", "amountpaid", "transaction_id", "hotel", "adults", "kids", 'start_date', 'end_date', 'days', "date_paid")
		# attrs = {'class': 'mytable'}

# class servicesTable(tables.Table):
# 	# amend = CheckBoxColumnWithName(verbose_name="Select", accessor="pk")
# 	class Meta:
# 		model = services
# 		fields = ('Title','company_name','email','cellphone','attachment','user_id','created_at','location','payment_info','description','amend')
