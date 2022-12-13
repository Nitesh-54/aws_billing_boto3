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
sample = client.get_cost_and_usage(
    TimePeriod={
        "Start": start_date,
        "End": end_date
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[
        {
            "Type": "DIMENSION",
            "Key": "LINKED_ACCOUNT"
        }
    ]
)

accounts = {}

for i in range(len(sample["ResultsByTime"])):
    for j in range(len(sample["ResultsByTime"][i]["Groups"])):
        key = sample["ResultsByTime"][i]["Groups"][j]["Keys"][0]
        value = sample["ResultsByTime"][i]["Groups"][j]["Metrics"]["UnblendedCost"]["Amount"]
        if key not in accounts:
            accounts[key] = float(value)
        else:
            accounts[key] += float(value)
            
for i in range(len(sample["DimensionValueAttributes"])):
    print(sample["DimensionValueAttributes"][i]["Attributes"]["description"],
          " : ", accounts[sample["DimensionValueAttributes"][i]["Value"]])
