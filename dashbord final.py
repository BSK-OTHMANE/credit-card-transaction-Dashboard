import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_csv("E:\S2\data viz\donnnnn.csv")
st.set_page_config(page_title="card transaction",page_icon='bar_chart',layout='wide')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.title(":bar_chart: Transactions électroniques par carte ")
df=pd.read_csv("e:/S2/data viz/donnnnn.csv")

st.sidebar.title('À propos')
st.sidebar.write("""Le tableau de bord de visualisation des transactions bancaires offre un aperçu des comportements 
                 financiers des clients, en utilisant des données telles que l'attrition du client, l'âge, le sexe, etc.
                  Les utilisateurs peuvent explorer les tendances clés, identifier les segments à haut risque et surveiller les performances des cartes.
                  Avec des graphiques interactifs et des filtres, le tableau de bord facilite la prise de décision stratégique et la gestion proactive de la clientèle.""")
st.sidebar.title("Choisir ton filtre:")



# Create for Feature 1
Gender = st.sidebar.multiselect("le Genre", df["Gender"].unique())
if not Gender:
    df2 = df.copy()
else:
    df2 = df[df["Gender"].isin(Gender)]

# Create for Feature 2
Marital_Status = st.sidebar.multiselect("État civil", df2["Marital_Status"].unique())
if not Marital_Status:
    df3 = df2.copy()
else:
    df3 = df2[df2["Marital_Status"].isin(Marital_Status)]

# Create for Feature 3
Attrition_Flag = st.sidebar.multiselect("Attrition_Flag", df3["Attrition_Flag"].unique())
if not Attrition_Flag:
    df4 = df3.copy()
else:
    df4 = df3[df3["Attrition_Flag"].isin(Attrition_Flag)]

# Create for Feature 4
Card_Category = st.sidebar.multiselect("Catégorie_carte", df4["Card_Category"].unique())
if not Card_Category:
    df5 = df4.copy()
else:
    df5 = df4[df4["Card_Category"].isin(Card_Category)]


# Create for Feature 6
Income_Category = st.sidebar.multiselect("Catégorie_de revenu", df5["Income_Category"].unique())
if not Income_Category:
    filtered_df = df5
else:
    filtered_df = df5[df5["Income_Category"].isin(Income_Category)]


col1, col2 , col3 = st.columns((3))
with col1:
    st.subheader("Répartition des transactions selon le sexe")
    dicte = {'M': (sum(filtered_df[filtered_df['Gender'] == 'M']['Total_Trans_Ct']))/(sum(filtered_df['Total_Trans_Ct'])), 'F' : (sum(filtered_df[filtered_df['Gender'] == 'F']['Total_Trans_Ct']))/(sum(filtered_df['Total_Trans_Ct']))}
    fig = px.pie(values=list(dicte.values()), names=list(dicte.keys()),
             color_discrete_sequence=['pink','blue'], 
             labels={'names':'Sexe', 'values':'Pourcentage'})
    st.plotly_chart(fig,use_container_width=True)

with col2:
    st.subheader("""Répartitin du montant du credit""")
    fig = px.histogram(filtered_df, x='Credit_Limit', nbins=10,
                   labels={'Credit_Limit':'Montant du crédit', 'count':'Nombre de clients'},
                   color_discrete_sequence=['skyblue'])

    fig.update_traces(marker=dict(line=dict(color='black', width=1)))
    st.plotly_chart(fig,use_container_width=True)

with col3:
    st.subheader("Distribution des Carte par Types")
    st.subheader("")
    # Count occurrences of each card type
    card_counts = filtered_df['Card_Category'].value_counts()

    # Create a DataFrame from the value counts
    df_counts = card_counts.reset_index()
    df_counts.columns = ['Card_Category', 'Count']

    # Create the pie plot
    fig = px.pie(df_counts, values='Count', names='Card_Category')
    st.plotly_chart(fig,use_container_width=True,height = 200,width=200)

st.subheader('La matrice de corrélation sous forme de heatmap')

df_sta = filtered_df.select_dtypes(exclude=['object'])

    # Calculate correlation matrix
matrice_correlation = df_sta.corr()

    # Convert Seaborn heatmap to Plotly
fig2 = px.imshow(matrice_correlation.values,
                    labels=dict(x="Variables", y="Variables"),
                    x=matrice_correlation.columns,
                    y=matrice_correlation.index)
fig2.update_layout(xaxis=dict(ticks="outside", tickangle=45),
                  yaxis=dict(ticks="outside"),
                  coloraxis_colorbar=dict(title="Corrélation"),
                  width=800, height=600)

st.plotly_chart(fig2,use_container_width=True)

# Create the scatter plot

st.subheader('Total_Trans_Amt  vs Total_Trans_Ct ')

fig5 = px.scatter(filtered_df,x='Total_Trans_Amt',y='Total_Trans_Ct',  
                 labels={ 'Total_Trans_Amt': 'Total_Trans_Amt','Total_Trans_Ct': 'Total_Trans_Ct'},
                 color='Total_Trans_Amt',  # Color points by Credit Limit
                 color_continuous_scale='viridis',  # Choose a color scale
                 size='Total_Trans_Amt',  # Size points by Credit Limit
                 size_max=15,  # Set the maximum size of points
                 opacity=0.7,  # Set the opacity of points
                 hover_name='Total_Trans_Amt',  # Display Customer Age on hover
                 hover_data={'Months_on_book': True, 'Credit_Limit': True}  # Additional data to display on hover
                )

# Customize the layout
fig5.update_layout(
    yaxis_title_font_size=16,  # Set y-axis title font size
    legend_title='Credit Limit',  # Set legend title
    legend_font_size=12,  # Set legend font size
    legend_font_color='black',  # Set legend font color
    legend_title_font_size=14,  # Set legend title font size
    legend_bgcolor='lightgrey',  # Set legend background color
    legend_bordercolor='darkgrey',  # Set legend border color
    margin=dict(l=50, r=50, t=50, b=50),  # Set margin
)

st.plotly_chart(fig5,use_container_width=True)

    
st.subheader("Credit Limit vs. Taux d'utilisation moyen du carte")

    # Create the scatter plot
fig3 = px.scatter(filtered_df, x='Credit_Limit', y='Avg_Utilization_Ratio',
                    labels={'Credit_Limit': 'Credit Limit', 'Avg_Utilization_Ratio': 'Average Utilization Ratio'},
                    color='Avg_Utilization_Ratio',  # Color points by Average Utilization Ratio
                    color_continuous_scale='plasma',  # Choose a color scale
                    size='Avg_Utilization_Ratio',  # Size points by Average Utilization Ratio
                    size_max=10,  # Set the maximum size of points
                    opacity=0.7,  # Set the opacity of points
                    hover_name='Customer_Age',  # Display Customer Age on hover
                    hover_data={'Credit_Limit': True, 'Avg_Utilization_Ratio': True}  # Additional data to display on hover
                    )

    # Customize the layout
fig3.update_layout(
        xaxis_title_font_size=16,  # Set x-axis title font size
        yaxis_title_font_size=16,  # Set y-axis title font size
        margin=dict(l=50, r=50, t=50, b=50),  # Set margin
    )

st.plotly_chart(fig3,use_container_width=True)

col21,col22=st.columns((2))
with col21:
    st.subheader("Credit Limit vs. Mois d'inactivité (12 months)")
        # Create the scatter plot
    fig4 = px.scatter(filtered_df, x='Credit_Limit', y='Months_Inactive_12_mon',
                        labels={'Credit_Limit': 'Credit Limit', 'Months_Inactive_12_mon': 'Months Inactive (12 months)'},
                        color='Credit_Limit',  # Color points by Months Inactive (12 months)
                        color_continuous_scale='viridis',  # Choose a color scale
                        size_max=10,  # Set the maximum size of points
                        opacity=0.7,  # Set the opacity of points
                        hover_name='Customer_Age',  # Display Customer Age on hover
                        hover_data={'Credit_Limit': True, 'Months_Inactive_12_mon': True}  # Additional data to display on hover
                        )



        # Customize the layout
    fig4.update_layout(
            xaxis_title_font_size=16,  # Set x-axis title font size
            yaxis_title_font_size=16,  # Set y-axis title font size
            margin=dict(l=50, r=50, t=50, b=50),  # Set margin
        )
    st.plotly_chart(fig4,use_container_width=True)

with col22:
    st.subheader('Âge du client vs Months on Book')
    linedata=filtered_df.groupby('Months_on_book')['Customer_Age'].mean().reset_index()
    # Create the line plot with customized parameters
    fig6 = px.line(linedata, x='Customer_Age', y='Months_on_book',
                labels={'Customer_Age': 'Customer Age', 'Months_on_book': 'Months on Book'},  # Custom axis labels
                line_shape='spline',  # Smooth line
                color_discrete_sequence=['#636EFA'],  # Custom line color
                template='plotly_dark',  # Dark theme
                )

    # Fill area under the line with a transparent color
    fig6.update_traces(fill='tozeroy', fillcolor='rgba(99, 110, 250, 0.3)', line=dict(width=2))

    # Update layout for better aesthetics
    fig6.update_layout(
        xaxis=dict(tickmode='linear'),  # Adjust x-axis ticks
        yaxis=dict(title='Months on Book'),  # Customize y-axis title
    )

    st.plotly_chart(fig6,use_container_width=True)

# Display filtered data
st.header('Filtred data')
st.write(filtered_df)
csv = filtered_df.to_csv(index = False)
st.download_button("Telecharger Filtred Data", data = csv, file_name = "Filtred_data.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')




