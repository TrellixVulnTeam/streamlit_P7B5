import pandas as pd
import streamlit as st
import plotly.express as px
import sys
import folium
import os
import geopandas as gpd
from pyproj import CRS
from streamlit_folium import folium_static
from folium import plugins
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import os
#st.set_page_config(page_title='mondelez',Layout="wide")
crs=CRS('epsg:3857')
ecom_data = pd.read_csv('norte1.csv',sep=';')
dejavo_data=pd.read_csv('dejavo1.csv',sep=';')
polygonos=gpd.read_file("shape/RUTAS_BAT_2022_region.shp")
geopath=polygonos.geometry.to_json()
#zonas=folium.features.GeoJson(geopath)
polygon=folium.FeatureGroup(name='rutas_bat')
polygon.add_child(folium.features.GeoJson(geopath))
#mapa.add_to(zonas)


# ecom_data.dropna(inplace=True)
st.set_page_config(page_title='mondelez',layout='wide')
st.markdown("""
<style>
.big-font {
    font-size:40px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Mondelez 2022</p>', unsafe_allow_html=True)
nav=st.sidebar.radio("Menu",["KPI's","Cobertura","Volumen","Vendedor","Ubicacion"],index=0)
if nav == "Cobertura":
     proveedores=ecom_data['COD_MES'].unique().tolist()
     mes=ecom_data['MES'].unique().tolist()
     mes_selection=st.sidebar.slider('Mes:',
                        min_value=min(mes),
                        max_value=max(mes),
                        value=(min(mes),max(mes))
                        )
     proveedor_selection=st.sidebar.multiselect('Supervisor:',
                        proveedores,
                        default=proveedores)  
     
     mask=(ecom_data['COD_MES'].isin(proveedor_selection)) & (ecom_data['MES'].between(*mes_selection))
     num_resul=ecom_data[mask].shape[0] 
     df_selection= ecom_data[mask]
     bins=[0, 25, 50 , 100, sys.maxsize]
     labels=[' <25','25-50','50-100','>100']
     ticket_group=pd.cut(df_selection['DROP_MON'],bins=bins,labels=labels)
     df_selection['CATEGORIA']=ticket_group
     figheatmap=px.density_heatmap(df_selection,x='EFE_MON',y='CATEGORIA',
                                   z='COB',
                                   #color_continuous_scale="Viridis",
                                   marginal_x='histogram',
                                   marginal_y='histogram',
                                   labels={'CATEGORIA':'Categoría','EFE_MON':'Frecuencia de compra'},
                                   title="Analisis por rango de compras")
                                  
     st.markdown("## Coverage Dashboard")
     df_col=df_selection["DROP_MON"]
     compra_min=df_col.min(skipna=True)
     compra_max=int(df_col.max(skipna=True))
     compra_pro=int(df_col.mean(skipna=True)) 
     col1, col2, col3, col4, col5=st.columns(5) 
     with col1:
          df_cob=df_selection.loc[df_selection['COB']==1]
          cli_cor=df_cob.shape[0]
          st.markdown("**Cobertura:**")
          st.markdown(f"<h2 style='text-align: left; color: red;'>{cli_cor:,}</h2)", unsafe_allow_html=True)                                   
     with col2:
          st.markdown("**Cartera:**")
          st.markdown(f"<h2 style='text-align: left; color: red;'>{num_resul:,}</h2)", unsafe_allow_html=True)
     with col3:
          st.markdown("Compra mín:")
          st.markdown(f"<h2 style='text-align: left; color: red;'>{compra_min:,}</h2)", unsafe_allow_html=True)
     with col4:
          st.markdown("Compra máx:")
          st.markdown(f"<h2 style='text-align: left; color: red;'>{compra_max:,}</h2)", unsafe_allow_html=True)
     with col5:
          st.markdown("Compra prom:")
          st.markdown(f"<h2 style='text-align: left; color: red;'>{compra_pro:,}</h2)", unsafe_allow_html=True)       
     st.markdown("---")
     #st.markdown("<hr/>", unsafe_allow_html=True)
     # ----plotear bar chart
     coverage_by_supervisor=(
          df_selection.groupby(by=['MES']).sum()[['COB']].sort_values(by='COB')
          )
     fig_coverage_sup=px.bar(
          coverage_by_supervisor,
          x="COB",
          y=coverage_by_supervisor.index,
          labels={'COB':'registro de última compra'},
          orientation="h",
          title="Clientes con registro de compras",
          )
     colchart1, colchart2=st.columns(2)  
     with colchart1:
               colchart1.plotly_chart(fig_coverage_sup,use_container_width = True)
     with colchart2:
               colchart2.plotly_chart(figheatmap,use_container_width = True)

     pie_chart=px.pie(df_selection,
                title='Frecuencia de compras',
                values='COB',
                names='EFE_MON')
     pie_chart1=px.pie(df_selection,
                title='Compras Mensual',
                values='DROP_MON',
                names='EFE_MON')

     col_pie1, col_pie2=st.columns(2)
     with col_pie1:
          col_pie1.plotly_chart(pie_chart, use_container_width = True)
     with col_pie2:
          col_pie2.plotly_chart(pie_chart1, use_container_width = True) 

if nav == "Vendedor":
     supervisores=ecom_data['COD_MES'].unique().tolist()
     proveedor_selection=st.sidebar.selectbox("Elije un Supervisor",
                        supervisores,
                        index=0)  
     if proveedor_selection :
          vend_list=ecom_data.loc[ecom_data['COD_MES']==proveedor_selection]
          vendedores=vend_list['COD_VEN'].unique().tolist()
          vendedor_selection=st.sidebar.selectbox("Elije un Vendedor",
                        vendedores,
                        index=0) 
          mask=(ecom_data['COD_VEN']==vendedor_selection) 
          st.markdown(vendedor_selection)     
          num_resul=ecom_data[mask].shape[0]  
          num_resul=ecom_data[mask].shape[0] 
          df_selection= ecom_data[mask]          
          #st.title("KPI's del vendedor") 
     st.markdown("## KPI's del vendedor")
     df_col=pd.to_numeric(df_selection["DROP_MON"])
     compra_min=df_col.min(skipna=True)
     compra_max=int(df_col.max(skipna=True))
     compra_pro=int(df_col.mean(skipna=True)) 
     col1, col2, col3, col4,col5=st.columns(5)                                    
     with col1:
          df_cob=df_selection.loc[df_selection['MES']==12]
          cli_cor=df_cob.shape[0]
          st.markdown("**Cobertura:**")
          st.markdown(f"<h2 style='text-align: left; color: yellow;'>{cli_cor:,}</h2)", unsafe_allow_html=True)
     with col2:
          st.markdown("**Cartera:**")
          st.markdown(f"<h2 style='text-align: left; color: yellow;'>{num_resul:,}</h2)", unsafe_allow_html=True)
     with col3:
          st.markdown("Compra mín:")
          st.markdown(f"<h2 style='text-align: left; color: yellow;'>{compra_min:,}</h2)", unsafe_allow_html=True)
     with col4:
          st.markdown("Compra máx:")
          st.markdown(f"<h2 style='text-align: left; color: yellow;'>{compra_max:,}</h2)", unsafe_allow_html=True)
     with col5:
          st.markdown("Compra prom:")
          st.markdown(f"<h2 style='text-align: left; color: yellow;'>{compra_pro:,}</h2)", unsafe_allow_html=True)       
     st.markdown("---")
     if st.checkbox("Mostrar clientes no coberturdos"):
          df_sel=df_selection.loc[df_selection['MES']<12]
          df_sel=df_sel.loc[:,['COD_CLI','DIA_VIS','NOM_CLI','DIR_CLI','ULT_FEC','ULT_COM']]
          num_cob=df_sel.shape[0]
          st.success(f'Clientes no coberturados {num_cob:,}')
          st.table(df_sel)
          st.download_button(label='Download CSV',data=df_sel.to_csv(),mime='text/csv')
if nav == "Ubicacion":
     dia=dejavo_data['DIA_VIS'].unique().tolist()
     dia_selection=st.sidebar.selectbox("Elije dia de visita",
                        dia,
                        index=0)  
     supervisores=dejavo_data['COD_MES'].unique().tolist()
     proveedor_selection=st.sidebar.selectbox("Elije un Supervisor",
                        supervisores,
                        index=0)  
     if proveedor_selection :
          vend_list=dejavo_data.loc[dejavo_data['COD_MES']==proveedor_selection]
          vendedores=vend_list['COD_VEN'].unique().tolist()
          vendedor_selection=st.sidebar.selectbox("Elije un Vendedor",
                        vendedores,
                        index=0) 
          
          if st.checkbox("Mostrar Plano"):
               mask=(dejavo_data['COD_VEN']==vendedor_selection) & (dejavo_data['DIA_VIS']==dia_selection)
               num_resul=dejavo_data[mask]  
               resul=dejavo_data[mask].shape[0] 
               df_cob=num_resul.loc[num_resul['AVA']==0]
               resul_cob=df_cob.shape[0]
               #st.markdown(resul)
               st.markdown(resul_cob)
               df_sel=num_resul.loc[:,['COD_CLI','DIA_VIS','NOM_CLI','DIR_CLI','LONGITUD','LATITUD','REC_CLI']] 
               
               for i in df_sel.itertuples():
                    lat=i.LATITUD
                    lon=i.LONGITUD
               mapa = folium.Map(location=[lat, lon], tiles="OpenStreetMap", zoom_start=15)
               mapa.add_child(polygon)
              
               # Add a basemap
               #Map.add_basemap("TERRAIN")
                             
               cartera=folium.FeatureGroup(name='clientes_folium')
               for i in df_sel.itertuples():
                    folium.Marker(location=[i.LATITUD,i.LONGITUD],
                                   popup=i.NOM_CLI,
                                   icon=plugins.BeautifyIcon(
                                        icon='circle',
                                        number=i.REC_CLI,
                                        border_color='blue',
                                        border_widht=2,
                                        text_color='black',
                                        text_size=10,
                                        text_align='center',
                                        inner_icon_style='font-size:18px;padding-top:-5px;')).add_to(cartera)
                    mapa.add_child(cartera)
               
               rec_log=folium.FeatureGroup(name='recorrido')
               points=[]
               for i in df_sel.itertuples():
                    points.append([i.LATITUD,i.LONGITUD])
                                      
               folium.PolyLine(points,
                              color='red',
                              dash_array='10').add_to(rec_log)
               mapa.add_child(rec_log)
               #folium.Marker(location=[0.LATITUD,0.LATITUD], popup='Inicio',icon='cloud').add_to(mapa)
               d=df_cob.loc[:,['COD_CLI','NOM_CLI','DIR_CLI','LATITUD','LONGITUD']] 
               df=df_cob.loc[:,['COD_CLI','NOM_CLI','DIR_CLI']] 
               col_names=df.columns.values.tolist()
               x="LONGITUD"
               y="LATITUD"
               marker_cluster=folium.FeatureGroup(name='clientes_cluster')  
               marker_cluster=MarkerCluster()
               for row in d.itertuples():
                    html = ""
                    for p in col_names:
                                html = (
                                  html
                                    + "<b>"
                                    + p
                                    + "</b>"
                                    + ": "
                                    + str(eval(str("row." + p)))
                                    + "<br>"
                                   )
                    popup_html = folium.Popup(html, min_width=100, max_width=200)
                    folium.Marker(
                                   location=[eval(f"row.{y}"), eval(f"row.{x}")],
                                   popup=popup_html
                    ).add_to(marker_cluster)
               #marker_cluster.add_child(MarkerCluster(marker_cluster))
              
               mapa.add_child(marker_cluster)   
               # Render the map using streamlit
               mapa.add_child(folium.map.LayerControl())
               #mapa=folium.Map(location=[latitud,longitud],zoom_start=15)
               #mapa.centerObject(marker_cluster,zoom=35)
               folium_static(mapa,width=1200, height=600)
               #folium_static(mapa)
               #folium_static(mapa.add_child(folium.map.LayerControl())) 
               #st.table(df)
               st.download_button(label='Download CSV',data=df.to_csv(),mime='text/csv')