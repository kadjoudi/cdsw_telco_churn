## Part 5: Model Serving for Viz Apps

from collections import ChainMap
import cdsw, numpy
from churnexplainer import ExplainedModel

#Load the model save earlier.
em = ExplainedModel(model_name='telco_linear',data_dir='/home/cdsw')

cased_cols = ["StreamingTV","MonthlyCharges","PhoneService","PaperlessBilling","Partner","OnlineBackup","gender","Contract","TotalCharges","StreamingMovies","DeviceProtection","PaymentMethod","tenure","Dependents","OnlineSecurity","MultipleLines","InternetService","SeniorCitizen","TechSupport"]

# This is the main function used for serving the model. It will take in the JSON formatted arguments , calculate the probablity of 
# churn and create a LIME explainer explained instance and return that as JSON.

def explain_viz(args):
  rows = args.get("data").get("rows")
  result = {
    "colnames": ['probability'],
    "coltypes": ['REAL']
  }
  outRows = []
  for row in rows:
    print(row)
    if (row[17] == '0') or (row[17] == 0):
      row[17] = "No"
    elif (row[17] == '1') or (row[17] == 1):
      row[17] = "Yes"
    print("row1")
    print(row[1])
    row[1] = float(row[1])
    row[8] = float(row[8])
    row[12] = int(float(row[12]))
    data = dict(zip(cased_cols,row))
    data = dict(ChainMap(data, em.default_data))
    data = em.cast_dct(data)
    print(data)
    probability, explanation = em.explain_dct(data)
    #probability = 0.763245
    outRows.append([probability])
  result['rows'] = outRows
  return {
    "version": "1.0",
    "data": result
  }
x= {
  "data": {
    "colnames": [
      "streamingtv",
      "monthlycharges",
      "phoneservice",
      "paperlessbilling",
      "partner",
      "onlinebackup",
      "gender",
      "contract",
      "totalcharges",
      "streamingmovies",
      "deviceprotection",
      "paymentmethod",
      "tenure",
      "dependents",
      "dnlinesecurity",
      "multiplelines",
      "internetservice",
      "seniorcitizen",
      "techsupport"
    ],
    "coltypes": [
      "STRING",
      "REAL",
      "STRING",
      "STRING",
      "STRING",
      "STRING",
      "STRING",
      "STRING",
      "REAL",
      "STRING",
      "STRING",
      "STRING",
      "INT",
      "STRING",
      "STRING",
      "STRING",
      "STRING",
      "STRING",
      "STRING"
    ],
    "rows": [
      [
        "No",
        70.35,
        "No",
        "No",
        "No",
        "No",
        "Female",
        "Month-to-month",
        1397.475,
        "No",
        "No",
        "Bank transfer (automatic)",
        29,
        "No",
        "No",
        "No",
        "DSL",
        0,
        "No"
      ],
      [
        "No",
        10.35,
        "No",
        "No",
        "No",
        "No",
        "Male",
        "Month-to-month",
        1397.475,
        "No",
        "No",
        "Bank transfer (automatic)",
        9,
        "No",
        "No",
        "No",
        "DSL",
        1,
        "No"
      ]
    ]
  }
}
explain_viz(x)