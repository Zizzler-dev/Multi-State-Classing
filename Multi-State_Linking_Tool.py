from multiprocessing.resource_sharer import stop
from operator import index
import streamlit as st
import pandas as pd
from itertools import chain


st.image('zizzl health logo 22.png')
st.title("Multi-State Classing Tool")


st.subheader("Upload Census Here:")

census = st.file_uploader("Upload Census:")

def convert_df(df):
    return df.to_csv(index=False)


if census is not None:
    censusdf = pd.read_csv(census, encoding_errors='replace')

    count = censusdf.count(axis=0)[1]

    for i in censusdf.index:
        if(i > 0 and i <(count-1) and censusdf['Relationship'][i] != 'Employee' and censusdf['Zip Code'][i] != censusdf['Zip Code'][i-1]):
            check = True
            index = i
            while (check == True):
                censusdf['Zip Code'][i] = censusdf['Zip Code'][i-1]
                if(censusdf['Relationship'][i+1] != 'Employee'):
                    i += 1
                else: 
                    i = index
                    check = False

    st.subheader("Upload Classed File Here:")


    classed_file_df = pd.read_csv('National classing matrix.csv')
    zip_to_fips_df = pd.read_csv('CSA zip.csv')


    join = pd.merge(classed_file_df[['FIPS','Class']], zip_to_fips_df, on = 'FIPS', how = 'inner')

    

    list = join[['Class','Zip Code', 'rating_area_id']].set_index('Zip Code').to_dict()
    list = list['Class']
    
    censusdf['Class'] = censusdf['Zip Code'].map(list)

    check = False

    

    classes = censusdf['Class'].unique()

    
    for i in classes:
        st.write('Class ', str(i))
        format = censusdf[ censusdf['Class'] == i]
        st.write(format[['First Name','Last Name', 'DOB', 'Zip Code', 'Relationship', 'Notes']])
        csv = convert_df(format[['First Name','Last Name', 'DOB', 'Zip Code', 'Relationship', 'Notes']]) 

        st.download_button(
            label = 'Download above data as CSV',
            data = csv,
            file_name = 'Class '+ str(i) +'.csv',
            mime='text/csv'
        )  
