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

**refresh website after uploading a CSV file / selecting a demo dataset**

**file must be less than 10mb, and contain columns with numerical(eg age or bmi), time(years) and geographical data (countries or USA states) to use all the plotting functions**

### histogram:
    takes in one data coloumn(variable 1) - columns will not show up in the dropdown if there is only one unique value 

### scatter plot:

    takes in two numerical data columns(variable 1 & 2), both dropdowns will only show numerical values
    
    if the groupby dropdown is selected, and has only two unique values(eg male and female), an unpaired t test will be calculated and the results will be shown (using statsmodels)

### group by dropdown:

    the histogram and scatter plot values can be grouped and colored differently depending on the data column selected in the groupby dropdown, if nothing is selected the values will not be grouped

    to use the group by dropdown for the map, you must also select a value in the select map condition dropdown, and the map will only show locations for the subjects that have that value as well. you can select multiple values in the select map condition dropdown.

### map:

    if the data column has country locations, they must be either country names or ISO-3 country codes

    if the data column has USA state locations, they must be the state names or the two letter abbreviations of the names
 

### time slider:

    if the csv file contains a column for time(years only), the values will be shown on the time slider
    
    when a year is selected data only from that year will be shown


there are two demo datasets(named demo_data1 and demo_data2 in this repository) 



# libraries required

dash plotly pandas numpy statsmodels pycountry dash_bootstrap_components




