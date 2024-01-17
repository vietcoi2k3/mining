# from fastapi import FastAPI,status,HTTPException,Path,UploadFile
# from fastapi.responses import JSONResponse
# from fastapi.responses import FileResponse, PlainTextResponse
# import numpy as np
# import pandas as pd
# import io
# app=FastAPI()
# columns_to_check=['V1', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V10', 'V11', 'V12', 'V13','V14', 'V18', 'V21']
# data = pd.DataFrame(columns=["Id", "Name_Of_Parking", "Location_Parking", "Sum_Parking", "Sum_Parking_Used", "Amount_Empty"])
# @app.post('/upfile',status_code=status.HTTP_201_CREATED)
# async def upload_file(file: UploadFile):
#     df=pd.read_csv(file.file)
#     intercept=np.array([-4.28548786])
#     if (set(columns_to_check).issubset(df.columns)):
#         df['Class']=1 / (1 + np.exp(-(intercept+0.0354467*df['V1']+ 0.07953281*df['V3']+ 0.73125973*df['V4']+ 0.04843018*df['V5']-0.16346112*df['V6']+0.00876506*df['V7']-0.25582466*df['V8']-0.46524737*df['V10']+0.40093164*df['V11']-0.52889934*df['V12']-0.37117827*df['V13']-0.6333818*df['V14']+-0.04860106*df['V18']+0.13294069*df['V21'])))
#         threshold = 0.9
#         df['Class'] = np.where(df['Class'] >= threshold, 1, 0)
#         global data
#         data = df.copy()
#     else:
#         raise HTTPException(status_code=400, detail= 'sai định dạng')
#     return "done"
# @app.get('/get',status_code=status.HTTP_201_CREATED)
# async def hello():
#     data.to_csv('1.csv')
#     return 'done'
from fastapi import FastAPI, status, HTTPException, UploadFile, HTMLResponse
from fastapi.responses import HTMLResponse
import numpy as np
import pandas as pd
import io

app = FastAPI()
columns_to_check = ['V1', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V10', 'V11', 'V12', 'V13', 'V14', 'V18', 'V21']
data = pd.DataFrame(columns=["Id", "Name_Of_Parking", "Location_Parking", "Sum_Parking", "Sum_Parking_Used", "Amount_Empty"])

@app.post('/upfile', status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile):
    df = pd.read_csv(file.file)
    intercept = np.array([-4.28548786])
    if set(columns_to_check).issubset(df.columns):
        df['Class'] = 1 / (1 + np.exp(-(intercept + 0.0354467*df['V1'] + 0.07953281*df['V3'] + 0.73125973*df['V4'] +
                                       0.04843018*df['V5'] - 0.16346112*df['V6'] + 0.00876506*df['V7'] - 0.25582466*df['V8'] -
                                       0.46524737*df['V10'] + 0.40093164*df['V11'] - 0.52889934*df['V12'] - 0.37117827*df['V13'] -
                                       0.6333818*df['V14'] - 0.04860106*df['V18'] + 0.13294069*df['V21'])))

        threshold = 0.9
        df['Class'] = np.where(df['Class'] >= threshold, 1, 0)

        global data
        data = df.copy()
    else:
        raise HTTPException(status_code=400, detail='Sai định dạng')
    return "done"

@app.get('/get', response_class=HTMLResponse)
async def get_data():
    data.to_csv('1.csv', index=False)
    return '''
        <html>
            <body>
                <h2>Download CSV</h2>
                <p><a href="/download">Click here to download the CSV file</a></p>
            </body>
        </html>
    '''

@app.get('/download', status_code=status.HTTP_200_OK)
async def download_data():
    return FileResponse('1.csv', media_type="text/csv", headers={'Content-Disposition': 'attachment; filename=test.csv'})
