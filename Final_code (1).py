#importing all necessary libraries
import pandas as pd #for for data handling
import matplotlib.pyplot as plt  #for visualisation

df = pd.read_csv(r"\Users\Indumathi\OneDrive\Desktop\Programming buisness\Assignment 2\cleanedDF3.csv") #reading the csv file
print(df.head()) #print first five rows
print(df.isnull().sum()) #checking for null values

#data cleaning
unique_locations = df['location'].unique()  #for checking all unique values of locations
print(unique_locations) #for viewing
locations = [
    'Africa', 'Asia', 'Europe', 'European Union', 
    'High income', 'Low income', 'Lower middle income', 
    'North America', 'Oceania', 'South America', 
    'Upper middle income', 'World']  #found these unnecessary locations for our analysis
df_cleaned = df[~df['location'].isin(locations)]  #removing those unnecessary locations from above list
print(df_cleaned) #now this contains only the country names which will be use full for analysis
df_cleaned.rename(columns={'location': 'country'}, inplace=True) # renaming the column name; location to country for better understanding
print(df_cleaned.head()) # for checking cleaned data ie first 5 rows

#task 1
df_cleaned['date'] = pd.to_datetime(df_cleaned['date']) #converting the date to datetime format, where py code can read these date objects
df_filter = df_cleaned[df_cleaned['date'].isin(['2021-12-31', '2022-12-31'])] # checking the required dates whether they are in the columns
df_filter = df_filter.dropna(subset=['people_fully_vaccinated_per_hundred']) # it will check for null values and drops them

def function(year):      #function block
    df_year = df_filter[df_filter['date'] == year]  #checking the specified date
    df_sort = df_year.sort_values(by='people_fully_vaccinated_per_hundred', ascending=False) #this will sort values from largest to smallest
    
    top_5 = df_sort[['country', 'people_fully_vaccinated_per_hundred']].head(5).round(0) #for getting the top 5 countries
    bottom_5 = df_sort[['country', 'people_fully_vaccinated_per_hundred']].tail(5).round(0) #for getting the bottom 5 countries
    
    return top_5, bottom_5 #returning the function

top_2021, bottom_2021 = function('2021-12-31') #applies the function block to the date mentioned
top_2022, bottom_2022 = function('2022-12-31')
#outputs the values and index=False indicates that it will not show index values of the output since we dont require that
print("Top 5 Countries in 2021:\n", top_2021.to_string(index=False))
print()
print("Bottom 5 Countries in 2021:\n", bottom_2021.to_string(index=False))
print()
print("Top 5 Countries in 2022:\n", top_2022.to_string(index=False))
print()
print("Bottom 5 Countries in 2022:\n", bottom_2022.to_string(index=False))


#task 2
df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])  
df_cleaned = df_cleaned.sort_values(by='date') 

daily_totals = df_cleaned.groupby('date')['daily_vaccinations'].sum() #adds the values of same date

max_date = daily_totals.idxmax().date()  #for getting the date where vaccinations is max
max_vaccinations = daily_totals.max()   #for getting the total count 
#outputs the max vaccinations with the date
print("The date with the highest number of vaccinations given worldwide is:", max_date , "and number of vacinations given is:",max_vaccinations)

#task 3
df_max_vaccinations = df_cleaned[df_cleaned['date'] == '2021-06-27'] #now checking the data on 27 june 2021
#sorting values by total vaccinations from max to min value which helps to get top values
top_5 = df_max_vaccinations.sort_values(by='total_vaccinations', ascending=False).head(5)[['country', 'total_vaccinations']].round(0)
#sorting values by total vaccinations from min to max value which helps to get bottom values
bottom_5 = df_max_vaccinations.sort_values(by='total_vaccinations', ascending=True).head(5)[['country', 'total_vaccinations']].round(0)
#outputing the top 5 and bottom 5 countries on 27 june 2021
print("Top 5 Countries on 2021-06-27 with the most vaccinations:")
print(top_5.to_string(index=False))
print()
print("Bottom 5 Countries on 2021-06-27 with the least vaccinations:")
print(bottom_5.to_string(index=False))

#task 4
#creating visualisation for top and bottom countries from task 1
#using line chart is the best visualisation for time series data
#the below lists are the top and bottom countries from task 1
top_countries = ['Brunei', 'Cuba', 'Chile', 'Portugal', 'Singapore', 'Hong Kong', 'Malta', 'South Korea']
bottom_countries = ['Nigeria', 'Malawi', 'Zambia', 'Guinea', "Cote d'Ivoire", 'Kyrgyzstan', 'Russia', 'Croatia', 'Poland', 'Timor']

df_cleaned['date'] = pd.to_datetime(df_cleaned['date']) #converting date to datetime format
df_cleaned['month'] = df_cleaned['date'].dt.to_period('M') #for representing month with yearly level ie it adds month and year in output like Jan 2020
#checking the avg data of full vaccination per 100 by grouping months and country
monthly_vaccination = df_cleaned.groupby(['month', 'country'])['people_fully_vaccinated_per_hundred'].mean().reset_index() 
#creating the range of months based upon our data
monthly_vaccination = monthly_vaccination[(monthly_vaccination['month'] >= '2020-10') & (monthly_vaccination['month'] <= '2022-10')]
#creating function for line chart
def plot(countries, title):
    #checking data whether it is availabe with the montly_vaccination for those countries
    country_data = monthly_vaccination[monthly_vaccination['country'].isin(countries)]
    #its creates a table with month corresponding to country and vaccinations data per 100 people
    pivot_data = country_data.pivot(index='month', columns='country', values='people_fully_vaccinated_per_hundred')
    #labeling 
    ax = pivot_data.plot(figsize=(12, 8), title=title) #line chart title
    ax.set_xlabel("Month") #labeling x axis
    ax.set_ylabel("Fully Vaccinated People Per 100") #labelling y axis
    ax.set_xticks(pivot_data.index)  #sets tick marks on axis with pivot data
    ax.set_xticklabels(pivot_data.index.strftime('%b %Y'))  #sets month labels ie jan feb....
    plt.xticks(rotation=45) #sets rotation of month labels for avoiding overlapping
    plt.grid(False) #removes grid lines in the background for clear graph
    plt.tight_layout() #creating the layout for above data
    plt.show() #displays the line chart
#these below uses the above function and plots graph for top and bottom countries of task 1 over the period of 2 years
plot(top_countries, 'Top Countries by Fully Vaccinated People (Per 100) Over Time (Oct 2020 - Oct 2022)')
plot(bottom_countries, 'Bottom Countries by Fully Vaccinated People (Per 100) Over Time (Oct 2020 - Oct 2022)')
