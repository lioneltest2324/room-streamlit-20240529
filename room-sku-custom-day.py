import streamlit as st
import pandas as pd
from datetime import datetime,timedelta
from universal_component_for_campaign import load_and_process_data,process_usfeed_and_hmfeed_sku_on_ads_data,process_hk_cost_and_value_on_ads_data,\
    process_old_new_sku_2022_and_2023_on_ads_data,merged_spu_to_sku_on_ads_data,merged_imagelink_to_sku_on_ads_data,create_date_filtered_df,\
    output_groupby_df,out_date_range_data,add_groupby_sum_columns_to_list_df,create_dynamic_column_setting,add_custom_proportion_to_df,\
    add_custom_proportion_to_df_x100,format_first_two_rows,format_comparison,colorize_comparison,create_compare_summary_df,\
    create_sensor_gmv_filter_input,create_sensor_campaign_filter_input_df
st.set_page_config(layout="wide")
# ---------------------------------------------------------------------基础数据处理区开始---------------------------------------------------------------------------------------------------
all_url = 'https://docs.google.com/spreadsheets/d/15UcirhRx_gTzmcC4aaTJ1OWfNForcACQ96vul_mw6f0/edit#gid=949961835'
spu_index_url = "https://docs.google.com/spreadsheets/d/1bQTrtNC-o9etJ3xUwMeyD8m383xRRq9U7a3Y-gxjP-U/edit#gid=0"

ads_daily = load_and_process_data(all_url,501000108)
sensor_daily = load_and_process_data(all_url,949961835)
scenes = load_and_process_data(spu_index_url,2136048739)
spu_index = load_and_process_data(spu_index_url,455883801)
image_index = load_and_process_data(spu_index_url,666585210)
image_index  = image_index.rename(columns={'SKU ID':'SKU'})

ads_daily['product'] = ads_daily['product'].str.strip().str.replace('\n', '').replace('\t', '').str.upper()

scenes['三级类目'] = scenes['三级类目'].str.lower()
ads_daily  = ads_daily.rename(columns={'product':'SKU'})
scenes  = scenes.rename(columns={'三级类目':'product_type_3','所属场景':'scenes'})
spu_index = spu_index.drop_duplicates()
ads_daily = merged_spu_to_sku_on_ads_data(ads_daily,spu_index,'SKU', 'SPU')
ads_daily = merged_spu_to_sku_on_ads_data(ads_daily,scenes,'product_type_3', 'scenes')
ads_daily= merged_imagelink_to_sku_on_ads_data(ads_daily,image_index,'SKU', 'imagelink')

index_df = output_groupby_df(ads_daily, ['SKU', 'scenes','product_type_1','product_type_2','product_type_3'],['impression'], 'sum').reset_index()
index_df = index_df.drop(columns=['impression'])
index_df = index_df.drop_duplicates()

with st.sidebar:
    selected_range = out_date_range_data(ads_daily,'Date',"自选日期范围")

# 选择日期范围内的数据
ads_daily['Date'] = pd.to_datetime(ads_daily['Date'])

# 处理普通选择日期范围内的数据
ads_daily_filtered_date_range_df = create_date_filtered_df(ads_daily, 'Date', selected_range)

merge_summary_df = output_groupby_df(ads_daily_filtered_date_range_df, ['SKU', 'SPU','product_type_1','product_type_2','product_type_3','scenes','imagelink'],
['impression', 'click', 'cost', 'ads value', 'conversions', ], 'sum').reset_index()
merge_summary_df = add_custom_proportion_to_df_x100(merge_summary_df,'click','impression','CTR')
merge_summary_df = add_custom_proportion_to_df(merge_summary_df,'cost','click','CPC')
merge_summary_df = add_custom_proportion_to_df(merge_summary_df,'ads value','cost','ads ROI')


column_config = {}
column_config['imagelink'] = st.column_config.ImageColumn(
    width="small"
            )

merged_df_left = merge_summary_df.filter(regex='SKU|SPU|scenes|imagelink|product_type_1|product_type_2|product_type_3|impression|click|cost|ads value|conversions|CPC|CTR|ads ROI')

unique_scenes = scenes['scenes'].unique()

scenes_options = st.multiselect(
    '选择场景',
    unique_scenes
)
scenes_select_df = merged_df_left[merged_df_left['scenes'].isin(scenes_options)]
unique_cate1 = scenes_select_df['product_type_1'].unique()
unique_cate2 = scenes_select_df['product_type_2'].unique()
unique_cate3 = scenes_select_df['product_type_3'].unique()
cate1_options = st.multiselect(
    '选择一级类目',
    unique_cate1
)
cate2_options = st.multiselect(
    '选择二级类目',
    unique_cate2
)
if cate2_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_2'].isin(cate2_options)]
    unique_cate3 = scenes_select_df['product_type_3'].unique()
    cate3_options = st.multiselect(
        '选择三级类目',
        unique_cate3
    )
else:
    cate3_options = st.multiselect(
        '选择三级类目',
        unique_cate3
    )


if scenes_options and cate1_options and cate2_options and cate3_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_2'].isin(cate2_options)]
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_3'].isin(cate3_options)]
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[9], ascending=False), column_config=column_config, width=2000, height=800)

elif scenes_options and cate1_options and cate2_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_2'].isin(cate2_options)]
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[9], ascending=False), column_config=column_config, width=2000, height=800)
elif scenes_options and cate1_options and cate3_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_3'].isin(cate3_options)]
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[9], ascending=False), column_config=column_config, width=2000, height=800)
elif scenes_options and cate1_options:
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[9], ascending=False), column_config=column_config, width=2000, height=800)
elif scenes_options and cate2_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_2'].isin(cate2_options)]
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[9], ascending=False), column_config=column_config, width=2000, height=800)
elif scenes_options and cate3_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_3'].isin(cate3_options)]
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[9], ascending=False), column_config=column_config, width=2000, height=800)
else:
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[9], ascending=False), column_config=column_config, width=2000, height=800)
