# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.views.generic import View
import datetime
import requests

# Create your views here.
API_BASE = 'https://api.sbif.cl/api-sbifv3/recursos_api/'
API_KEY = '551dd58d90fca467536cde1c80dc3728d7030876'
FORMAT = 'json'

class ConsultarSebif(View):

    def dispatch(self, request, *args, **kwargs):
        return super(ConsultarSebif, self).dispatch(request, *args, **kwargs)
    
    def get_context(self, request):
        context = {}
        response = requests.get('http://api.sbif.cl/api-sbifv3/recursos_api/uf/?apikey=551dd58d90fca467536cde1c80dc3728d7030876&formato=json')
        data = response.json()
        context['uf'] = data['UFs']
        context['dolares'] = {}
        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'consultas/detail.html', self.get_context(request))

    def post(self, request, *args, **kwargs):
        context=self.get_context(request)
        response = {}
        ufs = {}
        data = request.POST
        print(data)
        #errors = self.validate(data)
        filter_ = request.POST.get('filter',None)
        desde = request.POST.get('desde',None)
        desde_ = datetime.datetime.strptime(desde, "%Y-%m-%d") if desde else None
        hasta = request.POST.get('hasta',None)
        hasta_ = datetime.datetime.strptime(hasta, "%Y-%m-%d") if hasta else None

        if filter_ == 'uf':
            if desde and hasta:
                self.get_uf_in_range(desde_, hasta_, context, filter_)
                
            elif desde:
                print('desde_', desde)
                self.get_uf_desde(filter_,desde_, context)

            elif hasta:
                print('hasta_', hasta)
                self.get_uf_desde(filter_,desde_, context)
            
    
        return render(request, 'consultas/detail.html', context)

    def max_value_from_period(self,uf_list):
        max_val = max(uf_list,key=lambda item:item['Valor'])
        return max_val
    
    def min_value_from_period(self,uf_list):
        min_val = min(uf_list,key=lambda item:item['Valor'])
        return min_val

    def promedio_from_period(self,uf_list):
        valores_uf_list = [x['Valor'].replace(".", '').replace(',','.') for x in uf_list]
        float_lst_sum = sum([float(x) for x in valores_uf_list])
        media = (float_lst_sum/len(valores_uf_list))
        return "{0:.2f}".format(media)

    def get_dolar_for_day(self, fecha):
        fecha_ = datetime.datetime.strptime(fecha, "%Y-%m-%d") if fecha else None
        if fecha_:
            try:
                response = requests.get(API_BASE+'dolar/'+str(fecha_.year)+"/"+str(fecha_.month)+"/dias/"+str(fecha_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT)
                if response:
                    dolar =response.json()
                    return dolar['Dolares'][0]
                else:
                    return {'Valor':'No Disponible', 'Fecha': 'No Disponible'}
            except Exception as e:
                print(e)


    def get_uf_hasta(self,filter_, hasta_, context):
        try:
            response = requests.get(API_BASE+filter_+"/anteriores/"+str(hasta_.year)+"/"+str(hasta_.month)+"/dias/"+str(hasta_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT)
            if response:
                if response:
                    uf_list =response.json()
                    max_val = self.max_value_from_period(uf_list['UFs'])
                    context['max_val'] = max_val
                    min_val = self.min_value_from_period(uf_list['UFs'])
                    context['min_val'] = min_val
                    dolares = [self.get_dolar_for_day(x['Fecha']) for x in uf_list['UFs']]
                    context['dolares'] = dolares if dolares else {}
            context['ufs'] = response.json()
        except Exception as e:
            print(e)
        
    def get_uf_desde(self,filter_,desde_, context):
        try:
            response = requests.get(API_BASE+filter_+"/posteriores/"+str(desde_.year)+"/"+str(desde_.month)+"/dias/"+str(desde_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT)
            if response:
                uf_list =response.json()
                max_val = self.max_value_from_period(uf_list['UFs'])
                context['max_val'] = max_val
                min_val = self.min_value_from_period(uf_list['UFs'])
                context['min_val'] = min_val
                dolares = [self.get_dolar_for_day(x['Fecha']) for x in uf_list['UFs']]
                context['dolares'] = dolares if dolares else {}
            context['ufs'] = response.json()
        except Exception as e:
            print(e)

    def get_uf_in_range(self, desde_, hasta_, context, filter_):
        try:
            response = requests.get(API_BASE+filter_+"/periodo/"+str(desde_.year)+"/"+str(desde_.month)+"/"+str(hasta_.year)+"/"+str(hasta_.month)+"?apikey="+API_KEY+"&formato="+ FORMAT)
            if response:
                uf_list =response.json()
                max_val = self.max_value_from_period(uf_list['UFs'])
                context['max_val'] = max_val
                min_val = self.min_value_from_period(uf_list['UFs'])
                context['min_val'] = min_val
                media = self.promedio_from_period(uf_list['UFs'])
                context['media'] = media
                dolares = [self.get_dolar_for_day(x['Fecha']) for x in uf_list['UFs']]
                context['dolares'] = dolares if dolares else {}
            context['ufs'] = response.json()
        except Exception as e:
            print(e)
        

