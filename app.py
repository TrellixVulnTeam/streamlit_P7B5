import pandas as pd
import streamlit as st
import plotly.express as px
ecom_data = pd.read_csv('norte1.csv',sep=';')
# ecom_data.dropna(inplace=True)

st.set_page_config(page_title='mondelez',layout='wide')
st.header('Mondelez Diciembre 2021')

proveedores=ecom_data['COD_MES'].unique().tolist()
mes=ecom_data[' MES '].unique().tolist()
mes_selection=st.sidebar.slider('Mes:',
                        min_value=min(mes),
                        max_value=max(mes),
                        value=(min(mes),max(mes))
                        )

proveedor_selection=st.sidebar.multiselect('Proveedor:',
                        proveedores,
                        default=proveedores)  

mask=(ecom_data['COD_MES'].isin(proveedor_selection)) & (ecom_data[' MES '].between(*mes_selection))
num_resul=ecom_data[mask].shape[0]  
df_selection= ecom_data[mask]
# st.dataframe(df_selection)  
st.markdown(f'*resultado disponibles: {num_resul}*') 
                                       



#df_grouped=ecom_data.groupby(by=['NOM_PRO','COD_MES']).agg({'COB': ['mean']}).reset_index()
#df_grouped.columns=['proveedor','supervisor','promedio']
#df_grouped

# ----plotear bar chart
coverage_by_supervisor=(
    df_selection.groupby(by=[' MES ']).sum()[[' COB ']].sort_values(by=' COB ')
)
fig_coverage_sup=px.bar(
    coverage_by_supervisor,
    x=" COB ",
    y=coverage_by_supervisor.index,
    orientation="h",
    title="<b>Coberturas en el mes</b>",
    # color_descrete_sequence=["#008388"] * len(coverage_by_supervisor),
    #template="plotly_whhite",
)
st.plotly_chart(fig_coverage_sup)


pie_chart=px.pie(df_selection,
                title='Frecuencia de compras',
                values=' COB ',
                names='EFE_MON')

st.plotly_chart(pie_chart) 

pie_chart1=px.pie(df_selection,
                title='Compras Mensual',
                values=' DROP_MON ',
                names='EFE_MON')

st.plotly_chart(pie_chart1) 