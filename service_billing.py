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
cost_and_usage = client.get_cost_and_usage(
    TimePeriod={
        "Start": start_date,
        "End": end_date
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[
        {
            "Type": "DIMENSION",
            "Key": "SERVICE"
        }
    ]
)

services = {}

for i in range(len(cost_and_usage["ResultsByTime"])):
    for j in range(len(cost_and_usage["ResultsByTime"][i]["Groups"])):
        key = cost_and_usage["ResultsByTime"][i]["Groups"][j]["Keys"][0]
        value = cost_and_usage["ResultsByTime"][i]["Groups"][j]["Metrics"]["UnblendedCost"]["Amount"]
        if key not in services:
            services[key] = float(value)
        else:
            services[key] += float(value)

for i, j in services.items():
    print(i, " : ", j)

print(sum(services.values()))
