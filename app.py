import pandas as pd
import streamlit as st
import plotly.express as px
#import geemap.foliumap as geemap
import sys
import geemap
import folium
#import ee
#ee.Initialize()
import os
ecom_data = pd.read_csv('norte1.csv',sep=';')
# ecom_data.dropna(inplace=True)
st.set_page_config(page_title='mondelez',layout='wide')
st.markdown("""
<style>
.big-font {
    font-size:40px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Mondelez Diciembre 2021</p>', unsafe_allow_html=True)
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
          df_cob=df_selection.loc[df_selection['MES']==12]
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
     dia=ecom_data['DIA_VIS'].unique().tolist()
     dia_selection=st.sidebar.selectbox("Elije dia de visita",
                        dia,
                        index=0)  
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
          
          if st.checkbox("Mostrar Plano"):
               mask=(ecom_data['COD_VEN']==vendedor_selection) & (ecom_data['DIA_VIS']==dia_selection)
               num_resul=ecom_data[mask]  
               resul=ecom_data[mask].shape[0] 
               df_cob=num_resul.loc[num_resul['MES']<12]
               resul_cob=df_cob.shape[0]
               st.markdown(resul)
               st.markdown(resul_cob)
               df_sel=df_cob.loc[:,['COD_CLI','DIA_VIS','NOM_CLI','DIR_CLI','LONGITUD','LATITUD']] 
               import ee
               import geemap.foliumap as geemap
               from streamlit_folium import folium_static
               from folium import plugins
               from folium.plugins import HeatMap
               from folium.plugins import MarkerCluster
               
               # Create an interactive map
                  
               try:
                    ee.Initialize()
               except Exception as e:
                    ee.Authenticate()
                    ee.Initialize()

               mapa=geemap.Map()
               #mapa = folium.Map(location=[-11.9021, -77.0686], tiles="OpenStreetMap",max_zoom=25, zoom_start=20)
               #Map = geemap.Map(plugin_Draw=True, Draw_export=False)
               # Add a basemap
               #Map.add_basemap("TERRAIN")
               fc = geemap.pandas_to_ee(df_sel, latitude="LATITUD", longitude="LONGITUD")
               mapa.addLayer(fc, {'color':'red'}, "CLIENTES")
               mapa.centerObject(fc,zoom=15)
               
               #cartera=folium.FeatureGroup(name='clientes')
               #for i in df_sel.itertuples():
               #     folium.Marker(location=[i.LATITUD,i.LONGITUD],
               #                    popup=i.NOM_CLI).add_to(cartera)
               #     mapa.add_child(cartera)
               #     latitud=i.LATITUD
               #     longitud=i.LONGITUD
                    
               import pandas as pd

               d=num_resul.loc[:,['COD_CLI','NOM_CLI','DIR_CLI','LATITUD','LONGITUD']] 
               df=num_resul.loc[:,['COD_CLI','NOM_CLI','DIR_CLI']] 
               col_names=df.columns.values.tolist()
               x="LONGITUD"
               y="LATITUD"
               marker_cluster = plugins.MarkerCluster(name="cluster").add_to(mapa)
               mapa.add_child(marker_cluster)

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
                    
               # Render the map using streamlit
               mapa.add_child(folium.map.LayerControl())
               #mapa=folium.Map(location=[latitud,longitud],zoom_start=15)
               #mapa.centerObject(marker_cluster,zoom=35)
               folium_static(mapa)
               #folium_static(mapa.add_child(folium.map.LayerControl())) 
               st.table(d)
               st.download_button(label='Download CSV',data=d.to_csv(),mime='text/csv')