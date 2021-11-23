import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
ecom_data = pd.read_csv('data.csv',sep=';')
# ecom_data.dropna(inplace=True)

st.set_page_config(page_title='mondelez',layout='wide')
st.header('Mondelez Noviembre 2021')
# st.dataframe(ecom_data)
proveedores=ecom_data['NOM_PRO'].unique().tolist()
mes=ecom_data['MES_DOC'].unique().tolist()

st.sidebar.header("filtrar aqui")
mes_selection=st.sidebar.slider('Mes:',
                        min_value=min(mes),
                        max_value=max(mes),
                        value=(min(mes),max(mes)))

proveedor_selection=st.sidebar.multiselect('proveedor:',
                        proveedores,
                        default=proveedores)  

mask=(ecom_data['NOM_PRO'].isin(proveedor_selection)) & (ecom_data['MES_DOC'].between(*mes_selection))
num_resul=ecom_data[mask].shape[0]  
df_selection= ecom_data[mask]
st.dataframe(df_selection)  
st.markdown(f'*resultado disponibles: {num_resul}*') 
                                       



#df_grouped=ecom_data.groupby(by=['NOM_PRO','COD_MES']).agg({'COB': ['mean']}).reset_index()
#df_grouped.columns=['proveedor','supervisor','promedio']
#df_grouped

# ----plotear bar chart
coverage_by_supervisor=(
    df_selection.groupby(by=['COD_MES']).sum()[['COB']].sort_values(by='COB')
)
fig_coverage_sup=px.bar(
    coverage_by_supervisor,
    x="COB",
    y=coverage_by_supervisor.index,
    orientation="h",
    title="<b>Cobertura por supervisor</b>",
    # color_descrete_sequence=["#008388"] * len(coverage_by_supervisor),
    #template="plotly_whhite",
)
st.plotly_chart(fig_coverage_sup)
# bar_chart=px.bar(df_grouped,
#                x='supervisor',
#                Y='promedio',
#                text='promedio',
#                color_discrete_sequence=['#F63366']*len(df_grouped),
#                template='plotly_white')
# st.bar_chart

pie_chart=px.pie(ecom_data,
                title='proveedores',
                values='VTA',
                names='COD_PLA')

st.plotly_chart(pie_chart)                