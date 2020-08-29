
import datetime as dt
import pandas as pd



def calc_irr(guess):
	date_entry = input("Please key in your regular investment start date (YYYY-MM-DD): ")
	regular_premium= float(input("Please key in your monthly regular premium amount: $"))
	current_account_value= float(input("Please key in your current account value: $"))
	
	year, month, day = map(int, date_entry.split('-'))
	start = dt.date(year, month, day)
	end=dt.date.today()
	num_months_invested= (end.year - start.year) * 12 + (end.month - start.month)
	
	sum_npv=300 #random number to start with to kickstart iteration
	itercount=0
	print("Iterating...showing iteration count, interest rate and net present value")

	while abs(sum_npv)>=0.5:

		month_index=[i for i in range(1,num_months_invested+2)] #last element is index for total account value
		cashflow=[]
		net_present_value=[]

		for i in month_index:
			if i<num_months_invested+1:
				cashflow.append(-regular_premium)
				npv=(-regular_premium)/((1+guess/100)**(i-1))
				net_present_value.append(npv)

			else:
				cashflow.append(current_account_value)
				net_present_value.append(current_account_value/((1+guess/100)**(i-1)))

		sum_npv=sum(net_present_value)

		if sum_npv>0.5:
			guess+=0.005
		elif sum_npv<-0.5:
			guess-=0.005

		###debugging section in case went past iterations 
		itercount+=1


		if itercount%1000==0:
			print(itercount, guess, sum_npv)

		if itercount%49999==0:
			print(itercount, guess, sum_npv)

		if itercount>50000:
			print("\nExceeded 50000 iterations...")
			#print(net_present_value)
			print("Exited when monthly IRR is {}, and Net Present Value is {}".format(guess,sum_npv))
			return


	

	table=pd.DataFrame()
	table['Month']=month_index
	table['Cashflow']=cashflow
	table['Present Value at IRR']=net_present_value
	print("\nIterations completed! Showing results..\n")
	print(table, itercount)
	print("\nThe monthly IRR is {}%".format(guess))



calc_irr(10)
