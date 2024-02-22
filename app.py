from thefuzz import fuzz
from pandas import DataFrame
import pandas as pd
import numpy as np
import time

def mide_tiempo(funcion):
    def funcion_medida(*args, **kwargs):
        inicio = time.time()
        c = funcion(*args, **kwargs)
        print(time.time() - inicio)
        return c
    return funcion_medida

data_odoo = pd.read_excel("data/odoo.xlsx")
data_chint = pd.read_excel("data/chint.xlsx")

codigos_odoo_df = data_odoo["default_code"]
codigos_chint_df = data_chint[["MODELO", "CODIGO DE\nARTICULO"]]

@mide_tiempo
def compare_str(df1: DataFrame, df2: DataFrame) -> DataFrame:
    df_return = pd.DataFrame(columns=["CodigoOdoo", "CodigoChint", "Codigo", "Porcentaje de Precisión"])
    df_return_less_100 = pd.DataFrame(columns=["CodigoOdoo", "CodigoChint", "Codigo", "Porcentaje de Precisión"])
    cont = 0
    
    for odoo_product in df1:
        for chint_product, chint_code in zip(df2["MODELO"], df2["CODIGO DE\nARTICULO"]):
            percent_str = fuzz.ratio(str(chint_product).strip(), str(odoo_product).strip())
            
            if percent_str == 100:
                df_temporary = pd.DataFrame(data=np.array([[odoo_product, chint_product, chint_code, str(percent_str)],], dtype=str),columns=df_return.columns)
                print(df_temporary)
                df_return = pd.concat([df_return, df_temporary])
            
            if percent_str > 70: ...
                # df_temporary = pd.DataFrame(data=np.array([[odoo_product, chint_product, chint_code, str(percent_str)],], dtype=str),columns=df_return.columns)
                # print(df_temporary)
                # df_return_less_100 = pd.concat([df_return_less_100, df_temporary])
            
    return df_return, df_return_less_100
    
df_result, df_less_100 = compare_str(codigos_odoo_df, codigos_chint_df)

df_result.to_excel("df_result.xlsx")
df_less_100.to_excel("df_result_less_100.xlsx")
