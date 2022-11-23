import os
import warnings
warnings.simplefilter("ignore")

import pandas as pd
import utils


folder_path_base = "C:/Users/admin/Documents/trips/"
folder_downloads = "C:/Users/admin/Documents/trips/downloads/"
# first = folder_path + "EneFeb.xlsx"
# second = folder_path + "MarAbr.xlsx"
# third = folder_path + "MayMay.xlsx"

def tipo_viaje(row):
    if type(row["tipo_de_viaje"]) == float:
        # if row["origen"] == row["destino"]:
        #     return "Urbana"
        # else:
        #     return "Nacional"
        return 'Ultima milla'
    else:
        if row["tipo_de_viaje"] == 'Urbana':
            return 'Ultima milla'
        else:
            return 'Larga milla'

def probar():

    print("\nProcessing...\n")
    
    # Obtener el listado de archivos en la carpeta
    downloads = os.listdir(folder_downloads)
    df_t = pd.read_excel(folder_downloads+downloads[0], engine="openpyxl")
    utils.rename_colum(df_t)
    datafull = pd.DataFrame(columns=df_t.columns)
    
    for f in downloads:

        df = pd.read_excel(folder_downloads+f, engine="openpyxl")
        utils.rename_colum(df)
        datafull = pd.concat([datafull,df],axis=0)
        

    # organizar algunas columnas

    # Array de campos a parametrizar como entero
    to_int = [
        'consecutivo',
        'valor_total_flete',
        'conductor_id',
        'total_flete',
        'total_tarifa',
        'flete',
        'tarifa',
        'descuentos',
        'bonificaciones',
        'bonificaciones_tarifa',
        'valor_calculo_retenciones',
        'reteica',
        'retefuente',
        'anticipo',
        'saldo',
        'pagado',
        'anticipo_cc',
        'saldo_cc',
        'porcentaje_de_valores_integrales',
        'valor_integral',
        'costo_total_de_servicios_adicionales',
        'tarifa_total_de_servicios_adicionales',
    ]

    # convertir a enteros
    for field in to_int:
        datafull[field] = datafull[field].fillna(0)
        datafull[field] = datafull[field].astype(int)

    # array para convertir a bigint
    to_big_int = [
        'conductor_telefono'
    ]

    # convertir a enteros
    for field in to_big_int:
        datafull[field] = datafull[field].fillna(0)
        new = datafull[field].astype(str)
        new = new.str.split(".",n=1,expand=True)
        new = new[0]
        datafull[field] = new.str[-10:]
        # datafull.drop(columns =["conductor_telefono"], inplace = True)

    # datafull['consecutivo'] = datafull['consecutivo'].astype(int)

    # datafull['conductor_id'] = datafull['conductor_id'].fillna(0)
    # datafull['conductor_id'] = datafull['conductor_id'].astype(int)
    
    # datafull['total_flete'] = datafull['total_flete'].fillna(0)
    # datafull['total_flete'] = datafull['total_flete'].astype(int)
    
    # datafull['total_tarifa'] = datafull['total_tarifa'].fillna(0)
    # datafull['total_tarifa'] = datafull['total_tarifa'].astype(int)
    
    viajes_pago_pendiente = datafull[datafull['estado_del_pago']=="Pendiente"]
    viajes_pago_pendiente = viajes_pago_pendiente[viajes_pago_pendiente['placa'] != ()]


    facturaOk_pagoPte = viajes_pago_pendiente[viajes_pago_pendiente['estado_facturacion'] == 'Facturado']


    # Obtener un listado de los viajes de Tev
    viajes_tev = datafull[datafull['nombre_cliente']=="TRANSPORTES TEV SAS"]
    viajes_tev = viajes_tev[["nombre_cliente","fecha","consecutivo","origen","destino","conductor_id","conductor_name","total_flete","total_tarifa","placa","manifiesto","numero_facturacion","tipo_de_viaje"]]
    viajes_tev = viajes_tev.sort_values(by=["consecutivo"])

    viajes_diarios = datafull[datafull['placa']!=""]
    viajes_diarios = viajes_diarios[["consecutivo","origen","destino","nombre_cliente","fecha","placa","tipo_de_viaje","total_flete","total_tarifa"]].sort_values(by=["consecutivo"])
    viajes_diarios['tipo_operacion'] = viajes_diarios.apply(lambda row: tipo_viaje(row), axis=1)
    viajes_diarios["fecha"] = viajes_diarios["fecha"].astype('string')

    fecha = viajes_diarios["fecha"].str.split(pat='/',expand=True)
    viajes_diarios[["dia","mes","anio"]] = fecha
    
    viajes_diarios_sum = viajes_diarios.groupby(by=["anio","mes","dia","fecha"]).sum()
    viajes_diarios_sum.sort_values(by=["anio","mes","dia"])

    driver_phones = datafull[['conductor_name','conductor_telefono','tipo_de_vehiculo']]
    driver_phones2 = driver_phones.drop_duplicates()

    customer_list = datafull[['cliente','nombre_cliente']]
    customer_list2 = customer_list.drop_duplicates()


    driver_phones2.to_excel(folder_path_base + "driver_phones.xlsx")
    customer_list2.to_excel(folder_path_base + "customer_list.xlsx")

    # datafull.to_csv(folder_path_base + "consolidado.csv")
    datafull.to_excel(folder_path_base + "consolidado.xlsx")
    viajes_pago_pendiente.to_excel(folder_path_base + "viajes_pago_pendiente.xlsx")
    viajes_tev.to_excel(folder_path_base + "viajes_tev.xlsx")
    viajes_diarios.to_excel(folder_path_base + "viajes_diarios.xlsx")
    viajes_diarios_sum.to_excel(folder_path_base + "viajes_diarios_sum.xlsx")
    facturaOk_pagoPte.to_excel(folder_path_base + "facturaOk_pagoPte.xlsx")
    
    print("Done 👍✅")

if __name__ == '__main__':
    probar()