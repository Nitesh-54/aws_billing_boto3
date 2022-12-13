import boto3
from datetime import date
from dateutil.relativedelta import relativedelta

end_date = date.today()
end_date = str(end_date)

updated_date = date.today().replace(day=1)

start_date = updated_date - relativedelta(months=3)
start_date = str(start_date)

print(start_date)
print(end_date)

client = boto3.client('ce', region_name='us-east-1')
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date,
        'End': end_date
    },
    Granularity='MONTHLY',
    Metrics=[
        'UnblendedCost',
    ]
)

bill = 0
for i in range(len(response["ResultsByTime"])):
    int_bill = response["ResultsByTime"][i]["Total"]["UnblendedCost"]["Amount"]
    print("Bill from ", response["ResultsByTime"][i]["TimePeriod"]["Start"],
          "-", response["ResultsByTime"][i]["TimePeriod"]["End"], ":", int_bill)
    bill = bill + float(int_bill)

print("Total bill:", bill)
