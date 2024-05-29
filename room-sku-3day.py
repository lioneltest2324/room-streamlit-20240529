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
index_df = output_groupby_df(ads_daily, ['SKU', 'scenes','product_type_1','product_type_2','product_type_3'],['impression'], 'sum').reset_index()
index_df = index_df.drop(columns=['impression'])
index_df = index_df.drop_duplicates()

# with st.sidebar:
#     selected_range = out_date_range_data(ads_daily,'Date',"自选日期范围")

# 选择日期范围内的数据
ads_daily['Date'] = pd.to_datetime(ads_daily['Date'])
# 处理普通选择日期范围内的数据
# ads_daily_filtered_date_range_df = create_date_filtered_df(ads_daily, 'Date', selected_range)
# st.dataframe(ads_daily_filtered_date_range_df,width=1600, height=200)

current_date = datetime.now()
yesterday = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')
three_date = (current_date - timedelta(days=3)).strftime('%Y-%m-%d')

four_date = (current_date - timedelta(days=4)).strftime('%Y-%m-%d')
six_date = (current_date - timedelta(days=6)).strftime('%Y-%m-%d')

seven_date = (current_date - timedelta(days=7)).strftime('%Y-%m-%d')
nine_date = (current_date - timedelta(days=9)).strftime('%Y-%m-%d')

ten_date = (current_date - timedelta(days=10)).strftime('%Y-%m-%d')
twelve_date = (current_date - timedelta(days=12)).strftime('%Y-%m-%d')

thirteen_date = (current_date - timedelta(days=13)).strftime('%Y-%m-%d')
fifteen_date = (current_date - timedelta(days=15)).strftime('%Y-%m-%d')

sixteen_date = (current_date - timedelta(days=16)).strftime('%Y-%m-%d')
eighteen_date = (current_date - timedelta(days=18)).strftime('%Y-%m-%d')

nineteen_date = (current_date - timedelta(days=19)).strftime('%Y-%m-%d')
twentyone_date = (current_date - timedelta(days=21)).strftime('%Y-%m-%d')
column_config = {}
# ---------------------------------------------------------------------第一个7日df---------------------------------------------------------------------------------------------------
startdate = three_date
enddate = yesterday
start_formatted_date = datetime.strptime(startdate, '%Y-%m-%d').strftime('%m-%d')
end_formatted_date = datetime.strptime(enddate, '%Y-%m-%d').strftime('%m-%d')

startdate_date = datetime.strptime(startdate, '%Y-%m-%d').date()
enddate_date = datetime.strptime(enddate, '%Y-%m-%d').date()
fix_selected_range = (startdate_date, enddate_date)
ads_daily_filtered_date_range_1_3_df = create_date_filtered_df(ads_daily, 'Date', fix_selected_range)
merge_1_3_df = output_groupby_df(ads_daily_filtered_date_range_1_3_df, ['SKU'],
['impression', 'click', 'cost', 'ads value', 'conversions', ], 'sum').reset_index()
merge_1_3_df = add_custom_proportion_to_df_x100(merge_1_3_df,'click','impression','CTR')
merge_1_3_df = add_custom_proportion_to_df(merge_1_3_df,'cost','click','CPC')
merge_1_3_df = add_custom_proportion_to_df(merge_1_3_df,'ads value','cost','ads ROI')

merge_1_3_df = merge_1_3_df.rename(columns={
'impression': f'impression({start_formatted_date}-{end_formatted_date})',
'click': f'click({start_formatted_date}-{end_formatted_date})',
'cost': f'cost({start_formatted_date}-{end_formatted_date})',
'ads value': f'ads value({start_formatted_date}-{end_formatted_date})',
'conversions': f'conversions({start_formatted_date}-{end_formatted_date})',
'CTR': f'CTR({start_formatted_date}-{end_formatted_date})',
'ads ROI': f'ads ROI({start_formatted_date}-{end_formatted_date})',
'CPC': f'CPC({start_formatted_date}-{end_formatted_date})'
})
column_config[f'CTR({start_formatted_date}-{end_formatted_date})'] = st.column_config.NumberColumn(
                format='%.2f%%',  # 显示为百分比
                min_value=0,
                max_value=1,
                label=f'CTR({start_formatted_date}-{end_formatted_date})'
            )

# ---------------------------------------------------------------------第一个3日df---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------第二个3日df---------------------------------------------------------------------------------------------------
startdate = six_date
enddate = four_date
start_formatted_date = datetime.strptime(startdate, '%Y-%m-%d').strftime('%m-%d')
end_formatted_date = datetime.strptime(enddate, '%Y-%m-%d').strftime('%m-%d')

startdate_date = datetime.strptime(startdate, '%Y-%m-%d').date()
enddate_date = datetime.strptime(enddate, '%Y-%m-%d').date()
fix_selected_range = (startdate_date, enddate_date)
ads_daily_filtered_date_range_4_6_df = create_date_filtered_df(ads_daily, 'Date', fix_selected_range)
merge_4_6_df = output_groupby_df(ads_daily_filtered_date_range_4_6_df, ['SKU'],
['impression', 'click', 'cost', 'ads value', 'conversions', ], 'sum').reset_index()
merge_4_6_df = add_custom_proportion_to_df_x100(merge_4_6_df,'click','impression','CTR')
merge_4_6_df = add_custom_proportion_to_df(merge_4_6_df,'ads value','cost','ads ROI')
merge_4_6_df = add_custom_proportion_to_df(merge_4_6_df,'cost','click','CPC')

merge_4_6_df = merge_4_6_df.rename(columns={
'impression': f'impression({start_formatted_date}-{end_formatted_date})',
'click': f'click({start_formatted_date}-{end_formatted_date})',
'cost': f'cost({start_formatted_date}-{end_formatted_date})',
'ads value': f'ads value({start_formatted_date}-{end_formatted_date})',
'conversions': f'conversions({start_formatted_date}-{end_formatted_date})',
'CTR': f'CTR({start_formatted_date}-{end_formatted_date})',
'ads ROI': f'ads ROI({start_formatted_date}-{end_formatted_date})',
'CPC': f'CPC({start_formatted_date}-{end_formatted_date})'
})
column_config[f'CTR({start_formatted_date}-{end_formatted_date})'] = st.column_config.NumberColumn(
                format='%.2f%%',  # 显示为百分比
                min_value=0,
                max_value=1,
                label=f'CTR({start_formatted_date}-{end_formatted_date})'
            )
# ---------------------------------------------------------------------第二个3日df---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------第三个3日df---------------------------------------------------------------------------------------------------
startdate = nine_date
enddate = seven_date
start_formatted_date = datetime.strptime(startdate, '%Y-%m-%d').strftime('%m-%d')
end_formatted_date = datetime.strptime(enddate, '%Y-%m-%d').strftime('%m-%d')

startdate_date = datetime.strptime(startdate, '%Y-%m-%d').date()
enddate_date = datetime.strptime(enddate, '%Y-%m-%d').date()
fix_selected_range = (startdate_date, enddate_date)
ads_daily_filtered_date_range_7_9_df = create_date_filtered_df(ads_daily, 'Date', fix_selected_range)
merge_7_9_df = output_groupby_df(ads_daily_filtered_date_range_7_9_df, ['SKU'],
['impression', 'click', 'cost', 'ads value', 'conversions', ], 'sum').reset_index()
merge_7_9_df = add_custom_proportion_to_df_x100(merge_7_9_df,'click','impression','CTR')
merge_7_9_df = add_custom_proportion_to_df(merge_7_9_df,'ads value','cost','ads ROI')
merge_7_9_df = add_custom_proportion_to_df(merge_7_9_df,'cost','click','CPC')


merge_7_9_df = merge_7_9_df.rename(columns={
'impression': f'impression({start_formatted_date}-{end_formatted_date})',
'click': f'click({start_formatted_date}-{end_formatted_date})',
'cost': f'cost({start_formatted_date}-{end_formatted_date})',
'ads value': f'ads value({start_formatted_date}-{end_formatted_date})',
'conversions': f'conversions({start_formatted_date}-{end_formatted_date})',
'CTR': f'CTR({start_formatted_date}-{end_formatted_date})',
'ads ROI': f'ads ROI({start_formatted_date}-{end_formatted_date})',
'CPC': f'CPC({start_formatted_date}-{end_formatted_date})'
})
column_config[f'CTR({start_formatted_date}-{end_formatted_date})'] = st.column_config.NumberColumn(
                format='%.2f%%',  # 显示为百分比
                min_value=0,
                max_value=1,
                label=f'CTR({start_formatted_date}-{end_formatted_date})'
            )
# ---------------------------------------------------------------------第三个3日df---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------第四个3日df---------------------------------------------------------------------------------------------------

startdate = twelve_date
enddate = ten_date
start_formatted_date = datetime.strptime(startdate, '%Y-%m-%d').strftime('%m-%d')
end_formatted_date = datetime.strptime(enddate, '%Y-%m-%d').strftime('%m-%d')

startdate_date = datetime.strptime(startdate, '%Y-%m-%d').date()
enddate_date = datetime.strptime(enddate, '%Y-%m-%d').date()
fix_selected_range = (startdate_date, enddate_date)
ads_daily_filtered_date_range_10_12_df = create_date_filtered_df(ads_daily, 'Date', fix_selected_range)
merge_10_12_df = output_groupby_df(ads_daily_filtered_date_range_10_12_df, ['SKU'],
['impression', 'click', 'cost', 'ads value', 'conversions', ], 'sum').reset_index()
merge_10_12_df = add_custom_proportion_to_df_x100(merge_10_12_df,'click','impression','CTR')
merge_10_12_df = add_custom_proportion_to_df(merge_10_12_df,'ads value','cost','ads ROI')
merge_10_12_df = add_custom_proportion_to_df(merge_10_12_df,'cost','click','CPC')

merge_10_12_df = merge_10_12_df.rename(columns={
'impression': f'impression({start_formatted_date}-{end_formatted_date})',
'click': f'click({start_formatted_date}-{end_formatted_date})',
'cost': f'cost({start_formatted_date}-{end_formatted_date})',
'ads value': f'ads value({start_formatted_date}-{end_formatted_date})',
'conversions': f'conversions({start_formatted_date}-{end_formatted_date})',
'CTR': f'CTR({start_formatted_date}-{end_formatted_date})',
'ads ROI': f'ads ROI({start_formatted_date}-{end_formatted_date})',
'CPC': f'CPC({start_formatted_date}-{end_formatted_date})'
})
column_config[f'CTR({start_formatted_date}-{end_formatted_date})'] = st.column_config.NumberColumn(
                format='%.2f%%',  # 显示为百分比
                min_value=0,
                max_value=1,
                label=f'CTR({start_formatted_date}-{end_formatted_date})'
            )

# ---------------------------------------------------------------------第四个3日df---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------第五个3日df---------------------------------------------------------------------------------------------------
startdate = fifteen_date
enddate = thirteen_date
start_formatted_date = datetime.strptime(startdate, '%Y-%m-%d').strftime('%m-%d')
end_formatted_date = datetime.strptime(enddate, '%Y-%m-%d').strftime('%m-%d')

startdate_date = datetime.strptime(startdate, '%Y-%m-%d').date()
enddate_date = datetime.strptime(enddate, '%Y-%m-%d').date()
fix_selected_range = (startdate_date, enddate_date)
ads_daily_filtered_date_range_13_15_df = create_date_filtered_df(ads_daily, 'Date', fix_selected_range)
merge_13_15_df = output_groupby_df(ads_daily_filtered_date_range_13_15_df, ['SKU'],
['impression', 'click', 'cost', 'ads value', 'conversions', ], 'sum').reset_index()
merge_13_15_df = add_custom_proportion_to_df_x100(merge_13_15_df,'click','impression','CTR')
merge_13_15_df = add_custom_proportion_to_df(merge_13_15_df,'ads value','cost','ads ROI')
merge_13_15_df = add_custom_proportion_to_df(merge_13_15_df,'cost','click','CPC')

merge_13_15_df = merge_13_15_df.rename(columns={
'impression': f'impression({start_formatted_date}-{end_formatted_date})',
'click': f'click({start_formatted_date}-{end_formatted_date})',
'cost': f'cost({start_formatted_date}-{end_formatted_date})',
'ads value': f'ads value({start_formatted_date}-{end_formatted_date})',
'conversions': f'conversions({start_formatted_date}-{end_formatted_date})',
'CTR': f'CTR({start_formatted_date}-{end_formatted_date})',
'ads ROI': f'ads ROI({start_formatted_date}-{end_formatted_date})',
'CPC': f'CPC({start_formatted_date}-{end_formatted_date})'
})
column_config[f'CTR({start_formatted_date}-{end_formatted_date})'] = st.column_config.NumberColumn(
                format='%.2f%%',  # 显示为百分比
                min_value=0,
                max_value=1,
                label=f'CTR({start_formatted_date}-{end_formatted_date})'
            )
# ---------------------------------------------------------------------第五个3日df---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------第六个3日df---------------------------------------------------------------------------------------------------
startdate = eighteen_date
enddate = sixteen_date
start_formatted_date = datetime.strptime(startdate, '%Y-%m-%d').strftime('%m-%d')
end_formatted_date = datetime.strptime(enddate, '%Y-%m-%d').strftime('%m-%d')

startdate_date = datetime.strptime(startdate, '%Y-%m-%d').date()
enddate_date = datetime.strptime(enddate, '%Y-%m-%d').date()
fix_selected_range = (startdate_date, enddate_date)
ads_daily_filtered_date_range_16_18_df = create_date_filtered_df(ads_daily, 'Date', fix_selected_range)
merge_16_18_df = output_groupby_df(ads_daily_filtered_date_range_16_18_df, ['SKU'],
['impression', 'click', 'cost', 'ads value', 'conversions', ], 'sum').reset_index()
merge_16_18_df = add_custom_proportion_to_df_x100(merge_16_18_df,'click','impression','CTR')
merge_16_18_df = add_custom_proportion_to_df(merge_16_18_df,'ads value','cost','ads ROI')
merge_16_18_df = add_custom_proportion_to_df(merge_16_18_df,'cost','click','CPC')

merge_16_18_df = merge_16_18_df.rename(columns={
'impression': f'impression({start_formatted_date}-{end_formatted_date})',
'click': f'click({start_formatted_date}-{end_formatted_date})',
'cost': f'cost({start_formatted_date}-{end_formatted_date})',
'ads value': f'ads value({start_formatted_date}-{end_formatted_date})',
'conversions': f'conversions({start_formatted_date}-{end_formatted_date})',
'CTR': f'CTR({start_formatted_date}-{end_formatted_date})',
'ads ROI': f'ads ROI({start_formatted_date}-{end_formatted_date})',
'CPC': f'CPC({start_formatted_date}-{end_formatted_date})'
})
column_config[f'CTR({start_formatted_date}-{end_formatted_date})'] = st.column_config.NumberColumn(
                format='%.2f%%',  # 显示为百分比
                min_value=0,
                max_value=1,
                label=f'CTR({start_formatted_date}-{end_formatted_date})'
            )
# ---------------------------------------------------------------------第六个3日df---------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------第七个3日df---------------------------------------------------------------------------------------------------
startdate = twentyone_date
enddate = nineteen_date
start_formatted_date = datetime.strptime(startdate, '%Y-%m-%d').strftime('%m-%d')
end_formatted_date = datetime.strptime(enddate, '%Y-%m-%d').strftime('%m-%d')

startdate_date = datetime.strptime(startdate, '%Y-%m-%d').date()
enddate_date = datetime.strptime(enddate, '%Y-%m-%d').date()
fix_selected_range = (startdate_date, enddate_date)
ads_daily_filtered_date_range_19_21_df = create_date_filtered_df(ads_daily, 'Date', fix_selected_range)
merge_19_21_df = output_groupby_df(ads_daily_filtered_date_range_19_21_df, ['SKU'],
['impression', 'click', 'cost', 'ads value', 'conversions', ], 'sum').reset_index()
merge_19_21_df = add_custom_proportion_to_df_x100(merge_19_21_df,'click','impression','CTR')
merge_19_21_df = add_custom_proportion_to_df(merge_19_21_df,'ads value','cost','ads ROI')
merge_19_21_df = add_custom_proportion_to_df(merge_19_21_df,'cost','click','CPC')

merge_19_21_df = merge_19_21_df.rename(columns={
'impression': f'impression({start_formatted_date}-{end_formatted_date})',
'click': f'click({start_formatted_date}-{end_formatted_date})',
'cost': f'cost({start_formatted_date}-{end_formatted_date})',
'ads value': f'ads value({start_formatted_date}-{end_formatted_date})',
'conversions': f'conversions({start_formatted_date}-{end_formatted_date})',
'CTR': f'CTR({start_formatted_date}-{end_formatted_date})',
'ads ROI': f'ads ROI({start_formatted_date}-{end_formatted_date})',
'CPC': f'CPC({start_formatted_date}-{end_formatted_date})'
})
column_config[f'CTR({start_formatted_date}-{end_formatted_date})'] = st.column_config.NumberColumn(
                format='%.2f%%',  # 显示为百分比
                min_value=0,
                max_value=1,
                label=f'CTR({start_formatted_date}-{end_formatted_date})'
            )
# ---------------------------------------------------------------------第七个3日df---------------------------------------------------------------------------------------------------
merged_df_left = pd.merge(merge_19_21_df, merge_16_18_df, on='SKU', how='left')
merged_df_left = pd.merge(merged_df_left, merge_13_15_df, on='SKU', how='left')
merged_df_left = pd.merge(merged_df_left, merge_10_12_df, on='SKU', how='left')
merged_df_left = pd.merge(merged_df_left, merge_7_9_df, on='SKU', how='left')
merged_df_left = pd.merge(merged_df_left, merge_4_6_df, on='SKU', how='left')
merged_df_left = pd.merge(merged_df_left, merge_1_3_df, on='SKU', how='left')

merged_df_left = merged_spu_to_sku_on_ads_data(merged_df_left,spu_index,'SKU', 'SPU')
merged_df_left = merged_spu_to_sku_on_ads_data(merged_df_left,index_df,'SKU', 'scenes')
merged_df_left = merged_spu_to_sku_on_ads_data(merged_df_left,index_df,'SKU', 'product_type_1')
merged_df_left = merged_spu_to_sku_on_ads_data(merged_df_left,index_df,'SKU', 'product_type_2')
merged_df_left = merged_spu_to_sku_on_ads_data(merged_df_left,index_df,'SKU', 'product_type_3')
merged_df_left= merged_imagelink_to_sku_on_ads_data(merged_df_left,image_index,'SKU', 'imagelink')
column_config['imagelink'] = st.column_config.ImageColumn(
    width="small"
            )

merged_df_left = merged_df_left.filter(regex='SKU|SPU|scenes|imagelink|product_type_1|product_type_2|product_type_3|impression|click|cost|ads value|conversions|CPC|CTR|ads ROI')

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
param_options = st.multiselect(
    '选择数据维度',
    ['impression','click','cost','ads value','conversions','CPC','CTR','ads ROI']
)
result_string = '|'.join(param_options)


if scenes_options and cate1_options and cate2_options and cate3_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_2'].isin(cate2_options)]
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_3'].isin(cate3_options)]
    scenes_select_df = scenes_select_df.filter(regex=f'SKU|SPU|imagelink|{result_string}')
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[5], ascending=False), column_config=column_config, width=2000, height=800)

elif scenes_options and cate1_options and cate2_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_2'].isin(cate2_options)]
    scenes_select_df = scenes_select_df.filter(regex=f'SKU|SPU|imagelink|{result_string}')
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[5], ascending=False), column_config=column_config, width=2000, height=800)
elif scenes_options and cate1_options and cate3_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_3'].isin(cate3_options)]
    scenes_select_df = scenes_select_df.filter(regex=f'SKU|SPU|imagelink|{result_string}')
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[5], ascending=False), column_config=column_config, width=2000, height=800)
elif scenes_options and cate1_options:
    scenes_select_df = scenes_select_df.filter(regex=f'SKU|SPU|imagelink|{result_string}')
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[5], ascending=False), column_config=column_config, width=2000, height=800)
elif scenes_options and cate2_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_2'].isin(cate2_options)]
    scenes_select_df = scenes_select_df.filter(regex=f'SKU|SPU|imagelink|{result_string}')
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[5], ascending=False), column_config=column_config, width=2000, height=800)
elif scenes_options and cate3_options:
    scenes_select_df = scenes_select_df[scenes_select_df['product_type_3'].isin(cate3_options)]
    scenes_select_df = scenes_select_df.filter(regex=f'SKU|SPU|imagelink|{result_string}')
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[5], ascending=False), column_config=column_config, width=2000, height=800)
else:
    scenes_select_df = scenes_select_df.filter(regex=f'SKU|SPU|imagelink|{result_string}')
    columns_string = '|'.join(scenes_select_df.columns)
    for remove_string in ['SKU|', 'SPU|', '|imagelink']:
        columns_string = columns_string.replace(remove_string, '')
    dynamic_columns = columns_string.split('|')
    fixed_columns = ['SKU', 'SPU', 'imagelink']
    column_order = fixed_columns + dynamic_columns
    scenes_select_df = scenes_select_df[column_order]
    st.dataframe(scenes_select_df.set_index('SKU').sort_values(by=scenes_select_df.columns[5], ascending=False), column_config=column_config, width=2000, height=800)
