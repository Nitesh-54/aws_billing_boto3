import boto3
from datetime import datetime, timedelta, date
import time
from dateutil.relativedelta import relativedelta

end_date = datetime.strptime(
    (datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d')
end_date1 = str(end_date)
end_date1 = end_date1.split(' ')
end = end_date1[0]

print(end)

start_date = end_date - relativedelta(months=5)
start_date = str(start_date)
start_date = start_date.split(' ')
start = start_date[0]

print(start)

client = boto3.client('ce', region_name='us-east-1')
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': start,
        'End': end
    },
    Granularity='MONTHLY',
    Metrics=[
        'AmortizedCost',
    ]
)
bill = 0
for i in range(len(response["ResultsByTime"])):
    int_bill = response["ResultsByTime"][i]["Total"]["AmortizedCost"]["Amount"]
    bill = bill + float(int_bill)
print(bill)
