# [dashboard of a kaggle dataset](https://inika1.pythonanywhere.com/) 
creating a data visualisation dashboard of a [kaggle dataset](https://www.kaggle.com/datasets/antaresnyc/human-metagenomics?resource=download) - named demo_data1.csv in this repository  


### plots made
dropdown box option where you can update the data by specifying the disease using @app.callback

1. age histogram 

2. scatter plot of age against bmi

3. histogram showing the count of each disease (can specify the gender)

4. map displaying the geographical distribution of data subjects

# [data visualizer:](https://inika2.pythonanywhere.com/) 

web app that creates interactive plots (scatter, histogram, and map) of a csv file

**refresh website after uploading a CSV file / selecting a demo dataset

**file must be less than 10mb, and contain columns with numerical(eg age or bmi) and geographical data (countries or USA states) to use all the plotting functions

### scatter plot:

takes in two numerical values, both dropdowns(value 1 & 2) will only show numerical values

### group by dropdown:

the histogram and scatter plot values can be grouped and colored differently depending on the value in the groupby dropdown, if nothing is selected the values will not be grouped

to use the group by dropdown for the map, you must also select a value in the select map condition dropdown, and the map will only show locations for the subjects that have that value as well. you can select multiple values in the select map condition dropdown.

### map:

if the data column has country locations, they must be either country names or ISO-3 country codes
if the data column has USA state locations, they must be the state names or the two letter abbreviations of the names

there are two demo datasets(named demo_data1 and demo_data2 in this repository) 

**link to webapp: https://inika2.pythonanywhere.com/ 



# libraries required

dash plotly pandas numpy statsmodels pycountry dash_bootstrap_components




