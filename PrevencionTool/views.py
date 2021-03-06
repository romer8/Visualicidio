from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from PrevencionTool.models import Victima, Agresor
import os
import json
import csv
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objs as go
# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
def feminicidios_data():
    if not Victima.objects.all():
        print("here")
        Victima.objects.all().delete()
        Agresor.objects.all().delete()
        # array=[]
        count=0
        csv_path="PrevencionTool/static/PrevencionTool/scripts/Bol_Feminicidio 2013-16.csv"
        with open(csv_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
            print('Loading...')
            for row in spamreader:
                count=count+1
                ano_victima=row[0]
                mes_victima = row[1]
                fecha_victima = row[2]
                nombre_victima = row[3]
                edad_victima=row[4]
                lugar_victima=row[5]
                provincia_victima=row[6]
                departamento_victima=row[7]
                geolocalizacion_victima=row[8]
                circunstancias_victima=row[9]
                agresion_previa_victima=row[10]
                causa_muerte_victima=row[11]
                numero_hijos_victima=row[22]

                estado_del_caso=row[17]
                situacion_del_presunto_autor=row[18]

                nombre_acusado=row[12]
                edad_acusado=row[13]
                temperancia=row[14]
                intento_suicidio=row[15]
                relacion_victima=row[16]
                sentencia=row[19]
                fecha_sentencia=row[20]

                victima_row = Victima(
                    ano=ano_victima,
                    mes=mes_victima,
                    fecha=fecha_victima,
                    nombre=nombre_victima,
                    edad=edad_victima,
                    lugar=lugar_victima,
                    provincia=provincia_victima,
                    departamento=departamento_victima,
                    geolocalizacion=geolocalizacion_victima,
                    circunstancias=circunstancias_victima,
                    agresion_previa=agresion_previa_victima,
                    estado_del_caso=estado_del_caso,
                    causa_muerte=causa_muerte_victima,
                    numero_hijos=numero_hijos_victima
                )
                agresor_row=Agresor(
                    ano=ano_victima,
                    mes=mes_victima,
                    fecha=fecha_victima,
                    nombre_victima=nombre_victima,
                    nombre_acusado=nombre_acusado,
                    edad_acusado=edad_acusado,
                    temperancia=temperancia,
                    intento_suicidio=intento_suicidio,
                    relacion_victima=relacion_victima,
                    estado_del_caso=estado_del_caso,
                    situacion_del_presunto_autor=situacion_del_presunto_autor,
                    sentencia=sentencia,
                    fecha_sentencia=fecha_sentencia
                )
                victima_row.save()
                agresor_row.save()
    return

def getTableVictimaData():
    feminicidios_data()
    victimas_array=[]
    agresor_array=[]
    datos1={
        'victimas':victimas_array,
        'agresores':agresor_array
    }
    victimas=Victima.objects.all()
    print(len(victimas))
    agresores=Agresor.objects.all()
    for  i in range(1,(len(victimas)-1)):
        # print("this is the geolocalizacion")
        # print(victimas[i].geolocalizacion)
        # if(victimas[i].geolocalizacion!="No se sabe" and victimas[i].geolocalizacion!="Geolocalización" ):
        if(victimas[i].geolocalizacion!="No se sabe"):
            point=victimas[i].geolocalizacion.split(',')

        elif (victimas[i].geolocalizacion=="No se sabe"):
            point=["No se sabe"," No se sabe"]

        # print("this is the point")
        # print(point)
        datos_victima={
            'ano_muerte': victimas[i].ano,
            'mes_muerte': victimas[i].mes,
            'fecha_muerte':victimas[i].fecha,
            'nombre_victima':victimas[i].nombre,
            'edad_victima':victimas[i].edad,
            'lugar_victima':victimas[i].lugar,
            'provincia':victimas[i].provincia,
            'departmento':victimas[i].departamento,
            'lat': point[0],
            'long':point[1].strip(),
            'circunstancias': victimas[i].circunstancias,
            'agesion_previa':victimas[i].agresion_previa,
            'estado_del_caso':victimas[i].estado_del_caso,
            'situacion_del_presunto_autor':victimas[i].situacion_del_presunto_autor,
            'numero_hijos': victimas[i].numero_hijos
        }
        victimas_array.append(datos_victima)

        datos_agresor={
            'ano_crimen':agresores[i].ano,
            'mes_crimen':agresores[i].mes,
            'fecha_crimen':agresores[i].fecha,
            'nombre_victima':agresores[i].nombre_victima,
            'edad_acusado':agresores[i].edad_acusado,
            'temperancia': agresores[i].temperancia,
            'intento_suicidio':agresores[i].intento_suicidio,
            'relacion_victima':agresores[i].relacion_victima,
            'estado_del_caso':agresores[i].estado_del_caso,
            'situacion_del_presunto_autor':agresores[i].situacion_del_presunto_autor,
            'sentencia':agresores[i].sentencia,
            'fecha_sentencia':agresores[i].fecha_sentencia
        }
        agresor_array.append(datos_agresor)

    return datos1


datos = getTableVictimaData()


def default_map(request):

    file_path_bolivia="PrevencionTool/static/PrevencionTool/scripts/countries.geojson"
    file_path_departments="PrevencionTool/static/PrevencionTool/scripts/departamentosBol.json"
    file_path_municipalities="PrevencionTool/static/PrevencionTool/scripts/MunicipiosBol.json"
    data_dict={}
    with open(file_path_bolivia) as json_data:
        data_dict=json.load(json_data)

    with open(file_path_departments) as json_data:
        depts=json.load(json_data)

    with open(file_path_municipalities) as json_data:
        munipals=json.load(json_data)

    feminicidios_data2=getTableVictimaData()
    # chart_object=getNationalTimeSeries(feminicidios_data2)
    # print(data2)

    context={
        "countries":data_dict,
        "departments":depts,
        "munipalities":munipals,
        "feminicidios_data":feminicidios_data2,
        # "chart_object": chart_object
    }
    return render(request, 'PrevencionTool/index.html', context)

def localGraphs(request):
    # print("THIS IS THE LOCALGRAPHS")
    territory = request.GET['territory']
    # datos = getTableVictimaData(request)
    fechas=[]
    muertes=[]
    departamentos=[]
    for x in datos['victimas']:
        if x['fecha_muerte'] !='No se sabe':
            count=1
            fechas.append(datetime.datetime.strptime(x['fecha_muerte'], '%d-%m-%Y'))
            departamentos.append(x['departmento'])
            muertes.append(count)
    if territory != 'Nacional':
        newFeminicidioObject={
            'fecha_muerte':fechas,
            'departamento': departamentos,
            'muertes':muertes,
        }
        columns=['fecha_muerte','departamento','muertes']
        # columns=['fecha_muerte','muertes']
        df=pd.DataFrame(newFeminicidioObject, columns=columns)
        df.sort_values(by=['fecha_muerte'], inplace = True, ascending=True)
        df['fecha_muerte']= df['fecha_muerte'].dt.strftime('%Y-%m-%d')
        depa_df = df.loc[df['departamento'] == territory]
        # print(type(depa_df))
        # print(depa_df)
        depa_df_group=depa_df.groupby(['fecha_muerte'])['muertes'].sum().reset_index()
        # print(type(depa_df_group))
        depa_df_group2 = depa_df_group[['fecha_muerte','muertes']].copy()

        # print(depa_df_group2)
        depa_df_group2[['Year','Month','Day']]= depa_df_group2['fecha_muerte'].str.split('-', expand=True)
        # print("afeter")
        # print(depa_df_group2)
        depa_df_group3=depa_df_group2.groupby(['Year','Month'])['muertes'].sum().reset_index()
        depa_df_group3['newFecha'] = depa_df_group3[['Year', 'Month']].agg('-'.join, axis=1)

        # print(depa_df_group3)

        depa_json = depa_df_group3.to_json(orient='columns')
        depa_json_ob = json.loads(depa_json)
        # print(depa_json_ob)
        dates = list(depa_json_ob['newFecha'].values())
        deaths = list(depa_json_ob['muertes'].values())

        depa_object={
            'fecha':dates,
            'muertes':deaths
        }
    else:
        newFeminicidioObject={
            'fecha_muerte':fechas,
            'muertes':muertes,
        }
        columns=['fecha_muerte','muertes']
        df=pd.DataFrame(newFeminicidioObject, columns=columns)
        df.sort_values(by=['fecha_muerte'], inplace = True, ascending=True)
        df['fecha_muerte']= df['fecha_muerte'].dt.strftime('%Y-%m-%d')
        national_df=df.groupby(['fecha_muerte'])['muertes'].sum().reset_index()
        depa_df_group2 = national_df[['fecha_muerte','muertes']].copy()

        # print(depa_df_group2)
        depa_df_group2[['Year','Month','Day']]= depa_df_group2['fecha_muerte'].str.split('-', expand=True)
        # print("afeter")
        # print(depa_df_group2)
        depa_df_group3=depa_df_group2.groupby(['Year','Month'])['muertes'].sum().reset_index()
        depa_df_group3['newFecha'] = depa_df_group3[['Year', 'Month']].agg('-'.join, axis=1)

        # print(depa_df_group3)
        national_json = depa_df_group3.to_json(orient='columns')
        # print(national_json)
        national_json_ob = json.loads(national_json)
        dates = list(national_json_ob['newFecha'].values())
        deaths = list(national_json_ob['muertes'].values())

        depa_object={
            'fecha':dates,
            'muertes':deaths
        }

    return JsonResponse(depa_object)
def getNumberOfMonths(df):
    print("localpie vefore")
    # depa_count_df = df.loc[df['departamento'] == "La Paz"]
    depa_count_df = df
    df_count_sum = depa_count_df.groupby(['fecha_muerte'])['muertes'].sum().reset_index()
    df_count_sum[['Year','Month','Day']]= df_count_sum['fecha_muerte'].str.split('-', expand=True)
    df_count_sum['Year-Month']= df_count_sum[['Year', 'Month']].agg('-'.join, axis=1)
    total_meses = df_count_sum['Year-Month'].unique()
    return total_meses.size

def getNumberOfYears(df):
    depa_count_df = df
    df_count_sum = depa_count_df.groupby(['fecha_muerte'])['muertes'].sum().reset_index()
    df_count_sum[['Year','Month','Day']]= df_count_sum['fecha_muerte'].str.split('-', expand=True)
    total_years = df_count_sum['Year'].unique()
    return total_years.size
def getSTDBigArea(df):
    depa_count_df = df
    df_count_sum = depa_count_df.groupby(['fecha_muerte'])['muertes'].sum().reset_index()
    df_count_sum[['Year','Month','Day']]= df_count_sum['fecha_muerte'].str.split('-', expand=True)
    df_sum_year=df_count_sum.groupby(['Year'])['muertes'].sum().reset_index()
    sum_deaths_years = df_sum_year['muertes'].to_numpy()
    standard_dev = np.std(sum_deaths_years)
    print("this is the standard dev")
    print(standard_dev)
    return standard_dev

def getSTDSmallArea(df,areaType):
    list_unique_areas_std=[]
    df_count_sum = df
    df_count_sum[['Year','Month','Day']]= df_count_sum['fecha_muerte'].str.split('-', expand=True)
    df_grouped_depa = df_count_sum.groupby([areaType,'Year'])['muertes'].sum().reset_index()
    areas_list = sorted(df_count_sum[areaType].unique())
    for area in areas_list:
        area_df_one = df_grouped_depa.loc[df_grouped_depa[areaType] == area]
        sum_deaths_years = area_df_one['muertes'].to_numpy()
        area_std = np.std(sum_deaths_years)
        list_unique_areas_std.append(area_std)
    return list_unique_areas_std

def localPieGraphs(request):
    territory = request.GET['territory']
    print(territory)
    # datos = getTableVictimaData(request)
    fechas=[]
    muertes=[]
    departamentos=[]
    provincias = []
    national_object={}
    for x in datos['victimas']:
        if x['fecha_muerte'] !='No se sabe':
            count=1
            # fechas.append(datetime.datetime.strptime(x['fecha_muerte'], '%d-%m-%Y').strftime("%m/%d/%Y"))
            fechas.append(datetime.datetime.strptime(x['fecha_muerte'], '%d-%m-%Y'))
            departamentos.append(x['departmento'])
            muertes.append(count)
            provincias.append(x['provincia'])

    newFeminicidioObject={
        'fecha_muerte':fechas,
        'departamento': departamentos,
        'muertes':muertes,
        'provincia':provincias,
    }
    columns=['fecha_muerte','departamento','provincia','muertes']
    # columns=['fecha_muerte','muertes']
    df=pd.DataFrame(newFeminicidioObject, columns=columns)
    df.sort_values(by=['fecha_muerte'], inplace = True, ascending=True)
    df['fecha_muerte']= df['fecha_muerte'].dt.strftime('%Y-%m-%d')
    total_months=getNumberOfMonths(df)
    total_years = getNumberOfYears(df)

    if territory =='Nacional':
        standard_dev_nacional = getSTDBigArea(df)
        national_df=df.groupby(['departamento'])['muertes'].sum().reset_index()
        new_index = len(national_df)
        total_sum_regions = national_df['muertes'].sum()
        national_df.loc[new_index]=['Nacional',total_sum_regions]
        national_df['average_monthly']= national_df['muertes']/total_months
        national_df['average_years']= national_df['muertes']/total_years
        list_unique_areas_std = getSTDSmallArea(df,'departamento')
        list_unique_areas_std.append(standard_dev_nacional)
        np_unique_areas_std = np.asarray(list_unique_areas_std)
        print(list_unique_areas_std)

        national_df['std_year']=np_unique_areas_std
        # national_df['totalMonths'] = total_months
        print(national_df)
        national_json = national_df.to_json(orient='columns')
        national_json_ob = json.loads(national_json)
        departamento_list = list(national_json_ob['departamento'].values())
        deaths = list(national_json_ob['muertes'].values())
        avg_month_list = list(national_json_ob['average_monthly'].values())
        avg_years_list = list(national_json_ob['average_years'].values())
        variation_year_list = list(national_json_ob['std_year'].values())
        national_object={
            'territory':departamento_list,
            'muertes':deaths,
            'avg_years':avg_years_list,
            'avg_months':avg_month_list,
            'variation':variation_year_list
        }
    else:
        print("we are not in national")
        depa_df = df.loc[df['departamento'] == territory]
        standard_dev_dep = getSTDBigArea(depa_df)
        list_unique_areas_std = getSTDSmallArea(depa_df,'provincia')
        print("first list")
        print(list_unique_areas_std)
        list_unique_areas_std.append(standard_dev_dep)
        np_unique_areas_std = np.asarray(list_unique_areas_std)
        depa_df_group=depa_df.groupby(['provincia'])['muertes'].sum().reset_index()
        new_index = len(depa_df_group)
        total_sum_regions = depa_df_group['muertes'].sum()
        depa_df_group.loc[new_index]=['Nacional',total_sum_regions]
        depa_df_group['average_monthly']= depa_df_group['muertes']/total_months
        depa_df_group['average_years']= depa_df_group['muertes']/total_years
        print("this is the length of the stds in the deps")
        print(len(np_unique_areas_std))
        print(depa_df_group)
        depa_df_group['std_year']=np_unique_areas_std

        # depa_df_group['totalMonths'] = total_months

        # print(type(depa_df_group))
        #
        print(depa_df_group)

        depa_json = depa_df_group.to_json(orient='columns')
        depa_json_ob = json.loads(depa_json)
        # print(depa_json_ob)
        provincias_list = list(depa_json_ob['provincia'].values())
        deaths = list(depa_json_ob['muertes'].values())
        avg_month_list = list(depa_json_ob['average_monthly'].values())
        avg_years_list = list(depa_json_ob['average_years'].values())
        variation_year_list = list(depa_json_ob['std_year'].values())


        national_object={
            'territory':provincias_list,
            'muertes':deaths,
            'avg_years':avg_years_list,
            'avg_months':avg_month_list,
            'variation': variation_year_list
        }

    return JsonResponse(national_object)
