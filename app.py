import pandas as pd
import streamlit as st
import plotly.express as px
ecom_data = pd.read_csv('norte1.csv',sep=';')
# ecom_data.dropna(inplace=True)

st.set_page_config(page_title='mondelez',layout='wide')

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Mondelez Diciembre 2021</p>', unsafe_allow_html=True)
#st.header('Mondelez Diciembre 2021')

proveedores=ecom_data['COD_MES'].unique().tolist()
mes=ecom_data['MES'].unique().tolist()
mes_selection=st.sidebar.slider('Mes:',
                        min_value=min(mes),
                        max_value=max(mes),
                        value=(min(mes),max(mes))
                        )

proveedor_selection=st.sidebar.multiselect('Proveedor:',
                        proveedores,
                        default=proveedores)  

mask=(ecom_data['COD_MES'].isin(proveedor_selection)) & (ecom_data['MES'].between(*mes_selection))
num_resul=ecom_data[mask].shape[0]  
num_resul=ecom_data[mask].shape[0] 
df_selection= ecom_data[mask]
# st.dataframe(df_selection) 
st.title("Coverage Dashboard") 
st.markdown("##")
df_col=pd.to_numeric(df_selection["DROP_MON"])
compra_min=df_col.min(skipna=True)
compra_max=int(df_col.max(skipna=True))
compra_pro=int(df_col.mean(skipna=True)) 
col1, col2, col3, col4=st.columns(4)                                    
with col1:
     st.subheader("Cartera activa:")
     st.subheader(f'{num_resul:,}')
with col2:
     st.subheader("Compra mínima:")
     st.subheader(f'S/ {compra_min:,}')
with col3:
     st.subheader("Compra máxima:")
     st.subheader(f'S/ {compra_max:,}') 
with col4:
     st.subheader("Compra promedio:")
     st.subheader(f'S/ {compra_pro:,}')       
st.markdown("---")

# ----plotear bar chart
coverage_by_supervisor=(
    df_selection.groupby(by=['MES']).sum()[['COB']].sort_values(by='COB')
)
fig_coverage_sup=px.bar(
    coverage_by_supervisor,
    x="COB",
    y=coverage_by_supervisor.index,
    orientation="h",
    title="<b>Coberturas en el mes</b>",
    # color_descrete_sequence=["#008388"] * len(coverage_by_supervisor),
    #template="plotly_whhite",
)
st.plotly_chart(fig_coverage_sup)
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