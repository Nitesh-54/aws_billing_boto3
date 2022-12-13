import boto3

from datetime import date

from dateutil.relativedelta import relativedelta



end_date = date.today()

end_date = str(end_date)
print(end_date)



from_date = date.today().replace(day=1)


start_date = from_date - relativedelta(months=3)

start_date = str(start_date)
print(start_date)

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

#print(cost_and_usage)

#print(len(cost_and_usage["ResultsByTime"]))

services = {}

for i in range(len(cost_and_usage["ResultsByTime"])):
    #print(cost_and_usage["ResultsByTime"][i]["Groups"])
    #print(len(cost_and_usage["ResultsByTime"][i]["Groups"]))
    for j in range(len(cost_and_usage["ResultsByTime"][i]["Groups"])):
        key = cost_and_usage["ResultsByTime"][i]["Groups"][j]["Keys"][0]
        value = cost_and_usage["ResultsByTime"][i]["Groups"][j]["Metrics"]["UnblendedCost"]["Amount"]
        if key not in services:
            services[key] = float(value)
        else:
            services[key] += float(value)
        # print(cost_and_usage["ResultsByTime"][i]["Groups"][j]["Keys"][0])
        # print(cost_and_usage["ResultsByTime"][i]["Groups"][j]["Metrics"]["UnblendedCost"]["Amount"])

for i,j in services.items():
    print(i," : ",j)
#print(cost_and_usage["ResultsByTime"][0]["Groups"][0]["Keys"])

print(sum(services.values()))