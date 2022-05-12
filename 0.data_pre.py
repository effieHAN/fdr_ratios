# @effie_han for swsc ffdr and information covariates 
import pandas as pd
import numpy as np
import seaborn
from data_pre import *
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS



seaborn.set_style("darkgrid")
pd.plotting.register_matplotlib_converters()
path="/Users/effiehan/Desktop/term4/swsc/fdr_ratios/"



def get_data_return(fund_list):
    data_return = []
    for i in fund_list:
        data= pd.read_csv(path+"net_value/"+i+".csv",index_col = 0,parse_dates = True)
        data['time'] = pd.to_datetime(data['time'], infer_datetime_format=True)
        data=data.set_index('time')
        mon_return = data['netAssetValue'].pct_change()
        data_return.append( mon_return)
    data_return=pd.concat(data_return,axis=1, ignore_index=False)
    data_return.index = pd.to_datetime(data_return.index, format = '%y/%m/%d').strftime('%Y/%m')
    fund_list=["re"+x for x in fund_list]
    fund_list=[x.replace(".OF","OF") for x in fund_list]
    data_return.columns=fund_list
    return data_return 


def get_scale(fund_list):
    scale=[]
    date_list=["2017-03-01",'2018-03-01','2019-03-01','2020-03-01','2021-03-01','2022-03-01']
    for i in date_list:
        data= pd.read_csv(path+"date_scale/"+i+".csv")
        scale_ind=data['ths_fund_scale_fund']
        scale.append(scale_ind)
    scale=pd.concat(scale,axis=1, ignore_index=False)
    scale=scale.T
    


    fund_list=["re"+x for x in fund_list]
    fund_list=[x.replace(".OF","OF") for x in fund_list]
    scale.columns=fund_list
    scale.index=date_list
    scale=scale.reset_index()
    scale['index'] = pd.to_datetime(scale['index'], infer_datetime_format=True)
    scale.index=scale['index']
    scale.index = pd.to_datetime(scale.index, format = '%y/%m/%d').strftime('%Y/%m')
    scale=scale.drop(columns=['index'])
    return scale




def get_fund_size(scale,date):
    scale["sum"] = scale.sum(axis=1)
    size=np.log(scale.div(scale["sum"].values,axis=0))
    current=size[size.index== date]
    begin=size[size.index=='2017/03']
    fund_size= current.sub(begin.values,axis='columns')
    return fund_size

def get_retrun_gap(data_return,date):
    effective=[i for i in data_return.index if i.startswith(date)]
    gap=data_return.diff()
    return_gap=gap.loc[effective].mean()
    return_gap=pd.DataFrame(return_gap)
    return_gap=return_gap.T
    return_gap.index=[date+"/03"]
    return return_gap 
    
def get_index(i):
    index_data= pd.read_excel(path+"csmar/IDX_Idxtrdmth.xlsx")
    index_data['Month'] = pd.to_datetime(index_data['Month'], infer_datetime_format=True)
    index_data=index_data[index_data["Indexcd"]==i]
    index_data=index_data.set_index('Month')
    index_data.index = pd.to_datetime(index_data.index,format='%y/%m/%d').strftime('%Y/%m')
    index_data=index_data.query("index>'2017/03'" )
    index_data=index_data[["Idxrtn"]]
    return index_data

def get_ff():
    ff= pd.read_csv(path+"csmar/Fama-French.csv")
    ff['time'] = pd.to_datetime(ff['time'], infer_datetime_format=True)
    ff=ff.set_index('time')
    ff.index = pd.to_datetime(ff.index,format='%y/%m/%d').strftime('%Y/%m')
    ff=ff.query("index>'2017/03'" )
    return ff


def get_carhart():
    carhart_1= pd.read_excel(path+"csmar/STK_MKT_CARHARTFOURFACTORS.xlsx")
    carhart=carhart_1[['time', 'MarkettypeID',"RiskPremium1",'SMB1','HML1','UMD1', ]]
    carhart['time'] = pd.to_datetime(carhart['time'], infer_datetime_format=True)
    carhart=carhart[carhart["MarkettypeID"]=="P9706"]
    carhart=carhart[['time', "RiskPremium1",'SMB1','HML1','UMD1', ]]
    carhart=carhart.rename(columns={"RiskPremium1":"RiskPremium",'SMB1':"SMB",'HML1':"HML",'UMD1':"UMD",}, errors="raise")
    carhart=carhart.set_index('time')
    carhart.index = pd.to_datetime(carhart.index,format='%y/%m/%d').strftime('%Y/%m')
    carhart=carhart.query("index>'2017/03'" )
    return carhart


def get_rf():
    risk_free= pd.read_excel(path+"csmar/BND_Exchange.xlsx")
    risk_free["Nrrmtdt"]=risk_free["Nrrmtdt"]/100
    risk_free=risk_free.rename(columns={"Nrrmtdt": "Rf",}, errors="raise")
    risk_free['time'] = pd.to_datetime(risk_free['time'])
    risk_free=risk_free.set_index('time')
    risk_free= risk_free.resample('M').agg({'Rf':'last'})
    risk_free.index = pd.to_datetime(risk_free.index, format = '%y/%m/%d').strftime('%Y/%m')
    risk_free=risk_free.query("index>'2017/03'" )
    return risk_free


def cal_capm(data_return,ff,risk_free,date):
    data_return=data_return.sub(risk_free['Rf'], axis=0)
    beta=[]
    for i in data_return.columns:
        endog = data_return[i]
        exog = sm.add_constant(ff[["MKT"]])
        rols = RollingOLS(endog, exog, window=36)
        rres = rols.fit()
        beta_ind = rres.params["MKT"].copy()
        a_ind = rres.params["const"].copy()
        beta_ind=pd.DataFrame(beta_ind)
        a_ind=pd.DataFrame(a_ind)
        beta.append(beta_ind)
    beta = pd.concat(beta,axis=1, ignore_index=False)
    beta.columns=data_return.columns
    beta=beta[beta.index==date]
    treynor=data_return[data_return.index==date].div(beta)
    return beta, treynor





def get_fund_flow(scale,data_return,date):
    date=int(date)
    date=str(date-1)
    scale=scale.T
    effective=[i for i in data_return.index if i.startswith(date)]
    re=data_return.loc[effective].mean()
    re=pd.DataFrame(re)
    re["scale"]=scale[date+"/03"]
    re=re.rename(columns={0:"return"})
    re["flow"]=(re.scale - (1+re["return"]*re.scale.shift(1)))/(1+re["return"]*re.scale.shift(1))
    re=re[["flow"]]
    re=re.T
    return re
    
    
    
def cal_sharp(ExcessR):
    return ExcessR.mean()/np.sqrt(ExcessR.var())
def get_sharp(data_return,risk_free,date):
    data_return=data_return.sub(risk_free['Rf'], axis=0)
    sharp=data_return.rolling(window=36).apply(lambda x: cal_sharp(x))
    sharp=sharp[sharp.index==date]
    return sharp

def cal_carhart(data_return,carhart,risk_free,date):
    data_return=data_return.sub(risk_free['Rf'], axis=0)
    rsquare=[]
    alpha=[]
    vol=[]
    p_values=[]
    for i in data_return.columns:
        endog = data_return[i]
        exog = sm.add_constant(carhart[["RiskPremium","SMB","HML","UMD"]])
        rols = RollingOLS(endog, exog, window=36)
        rres = rols.fit()
        alpha_ind = rres.params["const"].copy()
        rsquare_ind = rres.rsquared.copy()
        vol_ind=rres.ssr.copy()
        vol_ind=pd.DataFrame(vol_ind)
        rsquare_ind=pd.DataFrame(rsquare_ind)
        rsquare.append(rsquare_ind)
        alpha.append(alpha_ind)
        p=rres.pvalues
        p=pd.DataFrame(p)
        p=p[[0]]
        # p=pd.DataFrame(p)
        p_values.append(p)
        vol.append(vol_ind)
    rsquare = pd.concat(rsquare,axis=1, ignore_index=False)
    p_values=pd.concat(p_values,axis=1, ignore_index=False)
    p_values.columns=data_return.columns
    rsquare.columns=data_return.columns
    alpha = pd.concat(alpha,axis=1, ignore_index=False)
    alpha.columns=data_return.columns
    vol = pd.concat(vol,axis=1, ignore_index=False)
    vol.columns=data_return.columns
    p_values.index=data_return.index
    rsquare=rsquare[rsquare.index==date]
    alpha=alpha[alpha.index==date]
    p_values=p_values[p_values.index==date]
    vol=vol[vol.index==date]
    return rsquare,alpha,vol,p_values


def get_port(inf):
    fund= pd.read_csv(path+"date_scale/2017-03-01.csv",index_col = 0,parse_dates = True)
    fund_list=fund["thscode"].values.tolist()
    data_return=get_data_return(fund_list)
    combo=pd.read_csv(path+"cov/combo.csv",index_col = 0,parse_dates = True)
    combo=combo.reset_index()
    select=pd.read_csv(path+"ffdr/"+inf+".csv",parse_dates = True)
    select_r=select["x"].values.tolist()
    fund_name=combo[combo.index.isin(select_r)]
    names=fund_name["index"].values.tolist()
    port=data_return[data_return.columns.intersection(names)]
    return port



def get_portfolio_return(port,name):
    return_port=port.mean(axis=1)
    return_port=pd.DataFrame(return_port)
    return_port=return_port.rename(columns={0: name,}, errors="raise")
    return return_port
    


