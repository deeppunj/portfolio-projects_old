
# ## Webscraping using requests and BeautifulSoup
# Get the list of top 15 books every year for the last 10 years from Goodreads page

import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
##################
# Title 
##################
 
st.title("Goodreads Top 15 Books for the last 10 years")

st.write("""
### Top 15 books every year from 2012 to 2021: Choose the year from the sidebar.
""")

##################
# SideBar
##################
year = st.sidebar.selectbox("Which year from the range 2012-2021", np.arange(2012, 2022))

plot_type = st.sidebar.radio("Plot Type", ("Average Rating", "Rating Count", "Shelvings", "Top Authors", "All in One"))

# # get the data set:

# Get the path of the folder where this script is running
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'gr_booklist_df.csv')

# Load the dataframe using the correct path
book_df = pd.read_csv(csv_path)


book_df = pd.read_csv('gr_booklist_df.csv')
book_df_trim = book_df[book_df["Year"]==year]

st.write(book_df_trim.drop(columns="Review").reset_index(drop=True))

############################################### work of data ###############
# convert Avg rating column to numerical format
book_df["Avg rating"] = book_df["Avg rating"].astype(float)

# check the ratings count column
book_df["Rating Count"] = book_df["Rating Count"].str.split(' ').str[0]


# check the shelvings column
book_df["Shelvings"] = book_df["Shelvings"].str.split(' ').str[0]

#now we need to remove the commas in the numbers OTHERWISE they will create problem when we will convert them to numbers """

book_df['Shelvings'] = book_df['Shelvings'].str.replace(',', '')

# now we have m and k in the values in Rating count and Shelvings columns. we need to change that to m = 1000000 and k = 1000

book_df["Rating Count"] = book_df["Rating Count"].replace(
    {'k': '*1e3', 'm': '*1e6'}, regex=True).map(pd.eval).astype(int)
book_df['Shelvings'] = book_df['Shelvings'].replace(
    {'k': '*1e3', 'm': '*1e6'}, regex=True).map(pd.eval).astype(int)

book_df_mean = book_df.copy()

book_df_mean.groupby(pd.Grouper(key="Year")).mean()


book_df_sorted = book_df.groupby(
    ['Author'], as_index=False).mean().sort_values('Avg rating', ascending=False)
# here as_index is very important to use otherwise the column Author will be used as index and we don't want that here.

##################
# Plots
##################
st.markdown("## **Plots**")

# paramter 

def param(plot_type):
    if plot_type == "Top Authors":
        num = st.sidebar.slider('Number of Authors',
                            min_value=5, max_value=20, value=10, step=5)
    return num


def plot_figure(plot_type):
    if plot_type == "Average Rating":
        fig = plt.figure(figsize=(19, 12))
        plt.style.use('ggplot')
        sns.set(font_scale=1.5)


        ax1 = plt.subplot(2, 2, 1)
        sns.boxplot(data=book_df_mean, x='Year', y=('Avg rating'))
        plt.ylabel("Average Ratings per year")
        st.pyplot(fig)
    
    elif plot_type== "Rating Count":
        fig = plt.figure(figsize=(19, 12))
        plt.style.use('ggplot')
        sns.set(font_scale=1.5)

        ax2 = plt.subplot(2, 2, 2)
        sns.lineplot(data=book_df_mean, x='Year', y=('Rating Count'))
        st.pyplot(fig)
    elif plot_type == "Shelvings":
        fig = plt.figure(figsize=(19, 12))
        plt.style.use('ggplot')
        sns.set(font_scale=1.5)

        ax3 = plt.subplot(2, 2, 3)
        sns.barplot(data=book_df_mean, x='Year', y="Shelvings")
        st.pyplot(fig)
    elif plot_type == "Top Authors":
        num = param(plot_type)    
       
        fig = plt.figure(figsize=(19, 12))
        plt.style.use('ggplot')
        sns.set(font_scale=1)

        ax4 = plt.subplot(2, 2, 4)
        sns.barplot(data=book_df_sorted[:int(num)], x='Author', y='Avg rating')
        plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
        for patch in ax4.patches:
            ax4.annotate("{:.2f}".format(patch.get_height()),  # this is the text/label
                        # (x, y) these are the coordinates to position the label
                        (patch.get_x()+patch.get_width()/2, patch.get_height()),
                        # horizontal and vertical alignment, can be left, right, center.
                        ha='center', va='center',
                        xytext=(0, 10),  # distance from text to points (x,y)
                        textcoords='offset points')  # how to position the label
        st.pyplot(fig)

    else:
        fig = plt.figure(figsize=(19, 12))


        plt.style.use('ggplot')
        sns.set(font_scale=1.5)

        ax1 = plt.subplot(2, 2, 1)
        sns.boxplot(data=book_df_mean, x='Year', y=('Avg rating'))
        plt.ylabel("Average Ratings per year")

        ax2 = plt.subplot(2, 2, 2)
        sns.lineplot(data=book_df_mean, x='Year', y=('Rating Count'))

        ax3 = plt.subplot(2, 2, 3)
        sns.barplot(data=book_df_mean, x='Year', y="Shelvings")

        ax4 = plt.subplot(2, 2, 4)
        sns.barplot(data=book_df_sorted[:10], x='Author', y='Avg rating')
        plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
        for patch in ax4.patches:
            ax4.annotate("{:.2f}".format(patch.get_height()),  # this is the text/label
                        # (x, y) these are the coordinates to position the label
                        (patch.get_x()+patch.get_width()/2, patch.get_height()),
                        # horizontal and vertical alignment, can be left, right, center.
                        ha='center', va='center',
                        xytext=(0, 10),  # distance from text to points (x,y)
                        textcoords='offset points')  # how to position the label

        plt.tight_layout()
        st.pyplot(fig)

## run this function
plot_figure(plot_type)
