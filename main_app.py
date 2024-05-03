import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def outliers_by_detail_name():  
    st.title("Outliers by Detail Name")
    outlier_by_detail_name = pd.read_csv('outlier_by_detail_name.csv')
    outlet_filter = list(st.sidebar.multiselect('Select Outlet', list(outlier_by_detail_name['outlet'].unique())))
    if 'All' in outlet_filter or len(outlet_filter)==0:
        outlet_filter = ['All']
    detail_name_filter = list(st.sidebar.multiselect('Select Detail Name', list(outlier_by_detail_name['detail_name'].unique())))
    if 'All' in detail_name_filter or len(detail_name_filter)==0:
        detail_name_filter = ['All']
    filtered_df = outlier_by_detail_name.copy()
    print("OUTLET FILTER - ",outlet_filter)
    print("DETAIL NAME FILTER - ",detail_name_filter)
    if outlet_filter==['All'] and detail_name_filter==['All']:
        pass
    elif outlet_filter!=["All"] and detail_name_filter!=["All"]:
        filtered_df = filtered_df[(filtered_df['outlet'].isin(outlet_filter)) & (filtered_df['detail_name'].isin(detail_name_filter))]
    elif outlet_filter!=["All"] and detail_name_filter==["All"]:
        filtered_df = filtered_df[(filtered_df['outlet'].isin(outlet_filter))]
    elif outlet_filter==["All"] and detail_name_filter!=["All"]:
        filtered_df = filtered_df[(filtered_df['detail_name'].isin(detail_name_filter))]
    if filtered_df.shape == (0,6):
        st.title("NO DATA FOUND FOR APPLIED FILTERS")
    else:
        st.dataframe(filtered_df, width=800, height=800)



def outliers_by_units():
    st.title("Outliers by Units")
    outlier_by_unit = pd.read_csv('outlier_unit_wise.csv')
    outlet_filter = list(st.sidebar.multiselect('Select Outlet', list(outlier_by_unit['Unit_Number'].unique())))
    if 'All' in outlet_filter or len(outlet_filter)==0:
        outlet_filter = ['All']
    month_filter = list(st.sidebar.multiselect('Select Transaction Month', list(outlier_by_unit['Transaction_Month'].unique())))
    if 'All' in month_filter or len(month_filter)==0:
        month_filter = ['All']
    filtered_df = outlier_by_unit.copy()
    print("OUTLET FILTER - ",outlet_filter)
    print("MONTH FILTER - ",month_filter)
    if outlet_filter==['All'] and month_filter==['All']:
        pass
    elif outlet_filter!=["All"] and month_filter!=["All"]:
        filtered_df = filtered_df[(filtered_df['Unit_Number'].isin(outlet_filter)) & (filtered_df['Transaction_Month'].isin(month_filter))]
    elif outlet_filter!=["All"] and month_filter==["All"]:
        filtered_df = filtered_df[(filtered_df['Unit_Number'].isin(outlet_filter))]
    elif outlet_filter==["All"] and month_filter!=["All"]:
        filtered_df = filtered_df[(filtered_df['Transaction_Month'].isin(month_filter))]
    if filtered_df.shape == (0,4):
        st.title("NO DATA FOUND FOR APPLIED FILTERS")
    else:
        st.dataframe(filtered_df, width=800, height=800)
    

    

def non_drillable_items():
    st.title("Non-Drillable Items")
    non_drillables = pd.read_excel('non-drillable items.xlsx')
    fig, ax1 = plt.subplots(figsize=(8, 6))

    ax1.bar(list(non_drillables['detail_name']), list(non_drillables['total_gross']), color='b', alpha=0.5)
    ax1.set_ylabel('Sum of Total Gross', color='b')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
    ax2 = ax1.twinx()

    ax2.plot(list(non_drillables['detail_name']), list(non_drillables['Average of total_gross']), color='r')
    ax2.set_ylabel('Average of Total Gross', color='r')

    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    # Add title and labels
    plt.xlabel('Detail Name')

    st.pyplot(fig)
    st.dataframe(non_drillables, width=800, height=800)

def heatmap():
    final_output = pd.read_excel('final_output_with_contracts.xlsx')

    outlet_filter = list(st.sidebar.multiselect('Select Outlet', list(final_output['outlet'].unique())))
    if len(outlet_filter)==0:
        outlet_filter = ['All']
    contract_filter = list(st.sidebar.multiselect('Select Contract Type', list(final_output['contract_types'].unique())))
    if len(contract_filter)==0:
        contract_filter = ['All']
    month_filter = list(st.sidebar.multiselect('Select Month', list(final_output['month'].unique())))
    if len(month_filter)==0:
        month_filter = ['All']

    filtered_df = final_output.copy()

    if outlet_filter==['All'] and contract_filter==['All'] and month_filter == ['All']:
        pass
    elif outlet_filter==['All'] and contract_filter==['All'] and month_filter != ['All']:
        filtered_df = filtered_df[(filtered_df['month'].isin(month_filter))]
    elif outlet_filter==['All'] and contract_filter!=['All'] and month_filter == ['All']:
        filtered_df = filtered_df[(filtered_df['contract_types'].isin(contract_filter))]
    elif outlet_filter!=['All'] and contract_filter==['All'] and month_filter == ['All']:
        filtered_df = filtered_df[(filtered_df['outlet'].isin(outlet_filter))]
    elif outlet_filter!=['All'] and contract_filter!=['All'] and month_filter == ['All']:
        filtered_df = filtered_df[(filtered_df['outlet'].isin(outlet_filter)) & (filtered_df['contract_types'].isin(contract_filter))]
    elif outlet_filter!=['All'] and contract_filter==['All'] and month_filter != ['All']:
        filtered_df = filtered_df[(filtered_df['month'].isin(month_filter)) & (filtered_df['outlet'].isin(outlet_filter))]
    elif outlet_filter==['All'] and contract_filter!=['All'] and month_filter != ['All']:
        filtered_df = filtered_df[(filtered_df['contract_types'].isin(contract_filter)) & (filtered_df['month'].isin(month_filter))]
    elif outlet_filter!=['All'] and contract_filter!=['All'] and month_filter != ['All']:
        filtered_df = filtered_df[(filtered_df['outlet'].isin(outlet_filter)) & (filtered_df['month'].isin(month_filter)) & (filtered_df['contract_types'].isin(contract_filter))]

    cols = ['hour','day','count_of_transactions']
    heatmap_data = filtered_df[cols]

    try:

        pivot_table = heatmap_data.pivot_table(values='count_of_transactions', index='day', columns='hour', aggfunc = 'sum')

        sns.heatmap(pivot_table, cmap='YlGnBu') 

        plt.xlabel('Hour')
        plt.ylabel('Day of the Week')
        plt.title('Weekly Trends of Labour Forecast')
        st.pyplot(plt)
    except:
        st.title("No Data to Display")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Outliers by Detail Name", "Outliers by Units","Weekly Trends for Labour Forecast","Non-Drillable Items"])

if page == "Outliers by Detail Name":
    outliers_by_detail_name()
elif page == "Outliers by Units":
    outliers_by_units()
elif page == "Weekly Trends for Labour Forecast":
    heatmap()
elif page=="Non-Drillable Items":
    non_drillable_items()


