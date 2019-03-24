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
		fields = ("booking", "agencyname", "agencycontact", "transaction_id", "amountpaid", "hotel", "adults", "kids", 'start_date', 'end_date', 'days', "date_paid")
		attrs = {'class': 'table-bordered table-striped table-hover'}
		# template = 'django_tables2/bootstrap.html'

class AgencyPaymentsTable(tables.Table):
	# amend = CheckBoxColumnWithName(verbose_name="Select", accessor="pk")
	class Meta:
		model = payment
		fields = ("user_full", "clientemail", "booking", "agencyname", "transaction_id", "amountpaid", "hotel", "adults", "kids", 'start_date', 'end_date', 'days', "date_paid")
		attrs = {'class': 'table-bordered table-striped table-hover'}


class ApprovedBookingsTable(tables.Table):
	# amend = CheckBoxColumnWithName(verbose_name="Select", accessor="pk")
	class Meta:
		model = booking
		fields = ("user_full", "p_name2", "clientemail", "hotel", "adults", "kids", 'start_date', 'end_date', 'days', "date_added", "approved")
		attrs = {'class': 'table-bordered table-striped table-hover'}
