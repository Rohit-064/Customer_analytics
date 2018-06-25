from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Account, Account_Risk
from .mock import Account_risk, account
from django.db.models import Sum

def index(request):
	template = loader.get_template('userdata/analytics.html')
	if request.method == 'GET':
		context = {
					'user_data': Account_Risk.objects.filter().values()
				  }
	if request.method == 'POST':
		account_name = request.POST['customer_name']
		account_risk_data = Account_Risk.objects.filter(customer_name=account_name).values()
		account_id = account_risk_data[0].get('account_id')
		child_account = Account.objects.filter(account_id=account_id).aggregate(Sum('account_child'))
		stage_won = len(Account.objects.filter(account_id=account_id, stage='Won').values())
		high_pot_account = len(Account.objects.filter(account_id=account_id, potential='HP').values())
		high_pipe_account = len(Account.objects.filter(account_id=account_id, pipeline='HP').values())
		child_account_sum = child_account.get('account_child__sum')
		risk = account_risk_data[0].get('account_risk').split("@")
		context = {
				'account_risk_data': account_risk_data[0],
				'risk': risk,
				'stage_won': stage_won,
				'high_pot_account': high_pot_account,
				'high_pipe_account': high_pipe_account,
				'child_account_sum':child_account_sum
			  }
	return HttpResponse(template.render(context, request))
    
def update_table(dtype,request):
	try:
		if dtype == 'Account_risk':
			for each in request:
				account_id = each.get('account_id')
				account_name = each.get('account_name')
				customer_name = each.get('customer_name')
				risk = each.get('account_risk')
				m = Account_Risk(account_id=account_id, account_name=account_name,
								customer_name=customer_name, account_risk=risk)
				m.save()

		elif dtype == "Account":
			for each in request:
				m = Account(**each)
				m.save()
		else:
			print("Not available")
	except Exception as e:
		print(e)
	    
db_update = False
if db_update:
	#db_type = 'Account'
	#db_type = Account_risk / Account
	db_type = 'Account' 
	db_req = account
	db_add = update_table(db_type, db_req)
else:
	acnt_risk = Account_Risk.objects.filter().values()
	print(acnt_risk[0])	
	print("**********************************************************************************************")
	acnt =Account.objects.filter().values()
	print(type(acnt))
