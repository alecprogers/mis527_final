import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    # Read in dataframe from Excel document
    df = pd.read_excel('Baby Names Dataset.xlsx')

    # Rename columns
    df.columns = ['year', 'name', 'sex', 'count']

    # Add column containing number of letters in name
    df['letter_count'] = df['name'].apply(lambda x: len(x))

    # print(df)

    # Prints a list of the 50 longest names in descending order -- Alec
    longest_names(df)

    # Generates a graph showing the popularity of our team's names over time -- Alec
    plot_team_names(df)

    # Generates a graph showing the most popular names over time -- Alec
    plot_popular_names(df)

    # Generates a graph showing how average name length has fluctuated over time -- Alec
    plot_letter_count(df)

    # Prints the 50 most popular male and female names since 1880 and a list of names that appear in the data every year
    # -- Alec
    most_popular_name(df)

    # Method to show the count of the top 5 names across different centuries -- Colby
    aggregate_names_by_cent(df)

    # Method to show number of male and female records across centuries -- Colby
    records_by_century(df)

    # Method to plot sustained popularity of names over different centuries --  Colby
    names_by_cent(df)

    # Gets the count of the most popular name in the year 1985 -- Ben
    most_popular_year_1985_names(df)

    # Gets the count of the most popular name in the year 2000 -- Ben
    most_popular_year_2000_names(df)

    # Graphs popular names from 1985 to 2000
    popular_names_1985_2000(df)

    # Graphs popular names from 2000 to 2015 -- Ben
    popular_names_2000_2015(df)

    # Graphs popularity of names from pop culture with relation to major pop culture events -- Maddie
    pop_culture_name(df, "Maverick", 1986, "black")
    pop_culture_name(df, "Khaleesi", 2011, "black")
    pop_culture_name(df, "Daphne", 1969, "black")
    pop_culture_name(df, "Lucy", 1952, "black")
    g_name(df)


# Prints a list of the 50 longest names in descending order -- Alec
def longest_names(df):
    df = df.groupby(['name'])['letter_count'].mean().to_frame()
    df = df.sort_values(['letter_count'], ascending=False)
    df = df.reset_index()
    # print(df[:50])
    print(df)


# Generates a graph showing the popularity of our team's names over time -- Alec
def plot_team_names(df):
    name_df = pd.pivot_table(df, index='year', columns='name', values='count', fill_value=0)

    our_names_df = name_df[['Alec', 'Benjamin', 'Colby', 'Madelyn', 'Ryland']]

    plt.figure()
    our_names_df.plot()
    plt.title('Popularity of Our Names')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.show()


# Generates a graph showing the most popular names over time -- Alec
def plot_popular_names(df):
    # Top male names: James, John, Robert, Michael, William
    # Top female names: Mary, Elizabeth, Patricia, Jennifer, Linda

    name_df = pd.pivot_table(df, index='year', columns='name', values='count', fill_value=0)
    top_names_df = name_df[['James', 'John', 'Robert', 'Michael', 'Mary', 'Elizabeth', 'Patricia',
                            'Jennifer']]

    plt.figure()
    top_names_df.plot()
    plt.title('Popularity of Top 4 Male and Female Names')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.show()


# Generates a graph showing how average name length has fluctuated over time -- Alec
def plot_letter_count(df):
    word_count_df = df.groupby('year')['letter_count'].mean().to_frame(name='avg_letter_count')

    plt.figure()
    word_count_df.plot()
    plt.title('Average Number of Letters Per Name')
    plt.xlabel('Year')
    plt.ylabel('Letters')
    plt.show()


# Prints the 50 most popular male and female names since 1880 and a list of names that appear in the data every year
# -- Alec
def most_popular_name(df):
    # Dataframe showing which names have appeared on the list the most times
    name_appearances_df = df.groupby(['name', 'sex'])['count'].count().to_frame()
    name_appearances_df = name_appearances_df.reset_index()
    name_appearances_df = name_appearances_df.sort_values(by=['count', 'name'], ascending=True)

    # Male name listed the most times
    male_apps_df = name_appearances_df[name_appearances_df['sex'] == 'M']

    male_136_df = male_apps_df[male_apps_df['count'] == 136]    # 136 is the total number of years recorded
    print('\nMale names appearing every year (total: {}):'.format(male_136_df['name'].count()))
    print(male_136_df['name'].tolist())

    # Female name listed the most times
    female_apps_df = name_appearances_df[name_appearances_df['sex'] == 'F']

    female_136_df = female_apps_df[female_apps_df['count'] == 136]  # 136 is the total number of years recorded
    print('\nFemale names appearing every year (total: {}):'.format(female_136_df['name'].count()))
    print(female_136_df['name'].tolist())

    # Dataframe showing the total number of people given each name
    name_count_df = df.groupby(['name', 'sex'])['count'].sum().to_frame()
    name_count_df = name_count_df.reset_index()

    print('\n')

    # Male name with highest count
    male_totals_df = name_count_df[name_count_df['sex'] == 'M']
    male_totals_df = male_totals_df.sort_values(['count'], ascending=False)
    male_totals_df = male_totals_df.reset_index()
    male_totals_df.index = male_totals_df.index + 1
    male_totals_df = male_totals_df.drop(columns=['index', 'sex'])
    print('Top 50 male names:')
    print(male_totals_df[:50])

    print()

    # Female name with highest count
    female_totals_df = name_count_df[name_count_df['sex'] == 'F']
    female_totals_df = female_totals_df.sort_values(['count'], ascending=False)
    female_totals_df = female_totals_df.reset_index()
    female_totals_df.index = female_totals_df.index + 1
    female_totals_df = female_totals_df.drop(columns=['index', 'sex'])
    print('Top 50 female names:')
    print(female_totals_df[:50])


# Method to show the count of the top 5 names across different centuries -- Colby
def aggregate_names_by_cent(df):
    df["century"] = df["year"].apply(get_century)
    cent_df = df.groupby(["century", "name"])["count"].sum().to_frame(name="count")
    cent_df = cent_df.reset_index()

    print("Distribution of the Top 5 most popular names across centuries\n\n")

    print(cent_df[cent_df["name"] == "Mary"])
    print(cent_df[cent_df["name"] == "Elizabeth"])
    print(cent_df[cent_df["name"] == "Patricia"])
    print(cent_df[cent_df["name"] == "Jennifer"])
    print(cent_df[cent_df["name"] == "Linda"])

    print(cent_df[cent_df["name"] == "James"])
    print(cent_df[cent_df["name"] == "John"])
    print(cent_df[cent_df["name"] == "Robert"])
    print(cent_df[cent_df["name"] == "Michael"])
    print(cent_df[cent_df["name"] == "William"])

    #  print(cent_df)

    return


# Method to show number of male and female records across centuries -- Colby
def records_by_century(df):
    df["century"] = df["year"].apply(get_century)
    cent_df = df.groupby(["century", "sex"])["count"].sum().to_frame(name="count")
    cent_df = cent_df.reset_index()

    print("Number of male and female records across each century/n/n")

    print(cent_df)

    return


# Method to get century column -- Colby
def get_century(year):
    if year < 1900:
        return "19th"
    elif year < 2000:
        return "20th"
    else:
        return "21st"


# Method to plot sustained popularity of names over different centuries --  Colby
def names_by_cent(df):
    df["century"] = df["year"].apply(get_century)
    cent_df = df.groupby("century")["name"].value_counts().to_frame(name="count")
    cent_df["count"] = cent_df["count"].apply(division)
    cent_df = cent_df.reset_index()

    top10_19th_df = cent_df[:10]
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    labels = top10_19th_df["name"]
    plt.figure()
    top10_19th_df.plot(kind="bar")
    plt.title("Top 10 Names That Sustained Popularity in the 19th Century")
    plt.xticks(x, labels, rotation=90)
    plt.xlabel("Name")
    plt.ylabel("Count of years over 100")
    plt.show()

    top10_20th_df = cent_df[527:537]
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    labels = top10_20th_df["name"]
    plt.figure()
    top10_20th_df.plot(kind="bar")
    plt.title("Top 10 Names That Sustained Popularity in the 20th Century")
    plt.xticks(x, labels, rotation=90)
    plt.xlabel("Name")
    plt.ylabel("Count of years over 100")
    plt.show()

    top10_21st_df = cent_df[5633:5643]
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    labels = top10_21st_df["name"]
    plt.figure()
    top10_21st_df.plot(kind="bar")
    plt.title("Top 10 Names That Sustained Popularity in the 21st Century")
    plt.xticks(x, labels, rotation=90)
    plt.xlabel("name")
    plt.ylabel("Count of years over 100")
    plt.show()

    print(top10_19th_df)
    print(top10_20th_df)
    print(top10_21st_df)


# Method to divide value counts to avoid double counts -- Colby
def division(score):
    return score / 2


# Graphs popular names from 1985 to 2000 -- Ben
def popular_names_1985_2000(df):
    # Getting yearly name counts for name Michael
    mike_df = df[df['name'] == "Michael"]
    mike_count_df = mike_df.groupby('year')['count'].sum()
    mike_count_df = mike_count_df.reset_index()
    mike_year_df = mike_count_df[(mike_count_df['year'] >= 1985) & (mike_count_df['year'] <= 2000)]
    mike_year_df = mike_year_df.set_index("year")

    # Getting yearly name counts for name Christopher
    chris_df = df[df['name'] == "Christopher"]
    chris_count_df = chris_df.groupby('year')['count'].sum()
    chris_count_df = chris_count_df.reset_index()
    chris_year_df = chris_count_df[(chris_count_df['year'] >= 1985) & (chris_count_df['year'] <= 2000)]
    chris_year_df = chris_year_df.set_index("year")

    # Getting yearly name counts for name Jessica
    jess_df = df[df['name'] == "Jessica"]
    jess_count_df = jess_df.groupby('year')['count'].sum()
    jess_count_df = jess_count_df.reset_index()
    jess_year_df = jess_count_df[(jess_count_df['year'] >= 1985) & (jess_count_df['year'] <= 2000)]
    jess_year_df = jess_year_df.set_index("year")

    # Getting yearly name counts for name Ashley
    ashley_df = df[df['name'] == "Ashley"]
    ashley_count_df = ashley_df.groupby('year')['count'].sum()
    ashley_count_df = ashley_count_df.reset_index()
    ashley_year_df = ashley_count_df[
        (ashley_count_df['year'] >= 1985) & (ashley_count_df['year'] <= 2000)]
    ashley_year_df = ashley_year_df.set_index("year")

    # Getting yearly name counts for name Matthew
    matthew_df = df[df['name'] == "Matthew"]
    matthew_count_df = matthew_df.groupby('year')['count'].sum()
    matthew_count_df = matthew_count_df.reset_index()
    matthew_year_df = matthew_count_df[
        (matthew_count_df['year'] >= 1985) & (matthew_count_df['year'] <= 2000)]
    matthew_year_df = matthew_year_df.set_index("year")

    # Getting yearly name counts for name Jennifer
    jen_df = df[df['name'] == "Jennifer"]
    jen_count_df = jen_df.groupby('year')['count'].sum()
    jen_count_df = jen_count_df.reset_index()
    jen_year_df = jen_count_df[(jen_count_df['year'] >= 1985) & (jen_count_df['year'] <= 2000)]
    jen_year_df = jen_year_df.set_index("year")

    # Getting yearly name counts for name Joshua
    josh_df = df[df['name'] == "Joshua"]
    josh_count_df = josh_df.groupby('year')['count'].sum()
    josh_count_df = josh_count_df.reset_index()
    josh_year_df = josh_count_df[(josh_count_df['year'] >= 1985) & (josh_count_df['year'] <= 2000)]
    josh_year_df = josh_year_df.set_index("year")

    # Getting yearly name counts for name Amanda
    amanda_df = df[df['name'] == "Amanda"]
    amanda_count_df = amanda_df.groupby('year')['count'].sum()
    amanda_count_df = amanda_count_df.reset_index()
    amanda_year_df = amanda_count_df[
        (amanda_count_df['year'] >= 1985) & (amanda_count_df['year'] <= 2000)]
    amanda_year_df = amanda_year_df.set_index("year")

    # Getting yearly name counts for name Daniel
    dan_df = df[df['name'] == "Daniel"]
    dan_count_df = dan_df.groupby('year')['count'].sum()
    dan_count_df = dan_count_df.reset_index()
    dan_year_df = dan_count_df[(dan_count_df['year'] >= 1985) & (dan_count_df['year'] <= 2000)]
    dan_year_df = dan_year_df.set_index("year")

    # Getting yearly name counts for name David
    david_df = df[df['name'] == "David"]
    david_count_df = david_df.groupby('year')['count'].sum()
    david_count_df = david_count_df.reset_index()
    david_year_df = david_count_df[(david_count_df['year'] >= 1985) & (david_count_df['year'] <= 2000)]
    david_year_df = david_year_df.set_index("year")

    # Plotting all yearly counts with labels for each name
    plt.figure()
    plt.title("Most Popular Year 1985 Names over 15 Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Names")
    plt.plot(mike_year_df, label='Michael')
    plt.plot(chris_year_df, label="Christopher")
    plt.plot(jess_year_df, label="Jessica")
    plt.plot(ashley_year_df, label="Ashley")
    plt.plot(matthew_year_df, label="Matthew")
    plt.plot(jen_year_df, label="Jennifer")
    plt.plot(josh_year_df, label='Joshua')
    plt.plot(amanda_year_df, label='Andrew')
    plt.plot(dan_year_df, label='Hannah')
    plt.plot(david_year_df, label='Joseph')
    plt.legend(fontsize=7.5)
    plt.show()

    return


# Graphs popular names from 2000 to 2015 -- Ben
def popular_names_2000_2015(df):
    # Getting yearly name counts for name Jacob
    jacob_df = df[df['name'] == "Jacob"]
    jacob_count_df = jacob_df.groupby('year')['count'].sum()
    jacob_count_df = jacob_count_df.reset_index()
    jacob_year_df = jacob_count_df[jacob_count_df['year'] >= 2001]
    jacob_year_df = jacob_year_df.set_index("year")
    jacob_year_df.columns = ["Yearly_Count"]

    # Getting yearly name counts for name Michael
    mike_df = df[df['name'] == "Michael"]
    mike_count_df = mike_df.groupby('year')['count'].sum()
    mike_count_df = mike_count_df.reset_index()
    mike_year_df = mike_count_df[mike_count_df['year'] >= 2001]
    mike_year_df = mike_year_df.set_index("year")

    # Getting yearly name counts for name Matthew
    matthew_df = df[df['name'] == "Matthew"]
    matthew_count_df = matthew_df.groupby('year')['count'].sum()
    matthew_count_df = matthew_count_df.reset_index()
    matthew_year_df = matthew_count_df[matthew_count_df['year'] >= 2001]
    matthew_year_df = matthew_year_df.set_index("year")

    # Getting yearly name counts for name Joshua
    josh_df = df[df['name'] == "Joshua"]
    josh_count_df = josh_df.groupby('year')['count'].sum()
    josh_count_df = josh_count_df.reset_index()
    josh_year_df = josh_count_df[josh_count_df['year'] >= 2001]
    josh_year_df = josh_year_df.set_index("year")

    # Getting yearly name counts for name Emily
    emily_df = df[df['name'] == "Emily"]
    emily_count_df = emily_df.groupby('year')['count'].sum()
    emily_count_df = emily_count_df.reset_index()
    emily_year_df = emily_count_df[emily_count_df['year'] >= 2001]
    emily_year_df = emily_year_df.set_index("year")

    # Getting yearly name counts for name Christopher
    chris_df = df[df['name'] == "Christopher"]
    chris_count_df = chris_df.groupby('year')['count'].sum()
    chris_count_df = chris_count_df.reset_index()
    chris_year_df = chris_count_df[chris_count_df['year'] >= 2001]
    chris_year_df = chris_year_df.set_index("year")

    # Getting yearly name counts for name Nicholas
    nick_df = df[df['name'] == "Nicholas"]
    nick_count_df = nick_df.groupby('year')['count'].sum()
    nick_count_df = nick_count_df.reset_index()
    nick_year_df = nick_count_df[nick_count_df['year'] >= 2001]
    nick_year_df = nick_year_df.set_index("year")

    # Getting yearly name counts for name Andrew
    andrew_df = df[df['name'] == "Andrew"]
    andrew_count_df = andrew_df.groupby('year')['count'].sum()
    andrew_count_df = andrew_count_df.reset_index()
    andrew_year_df = andrew_count_df[andrew_count_df['year'] >= 2001]
    andrew_year_df = andrew_year_df.set_index("year")

    hannah_df = df[df['name'] == "Hannah"]
    hannah_count_df = hannah_df.groupby('year')['count'].sum()
    hannah_count_df = hannah_count_df.reset_index()
    hannah_year_df = hannah_count_df[hannah_count_df['year'] >= 2001]
    hannah_year_df = hannah_year_df.set_index("year")

    # Getting yearly name counts for name Joseph
    joe_df = df[df['name'] == "Joseph"]
    joe_count_df = joe_df.groupby('year')['count'].sum()
    joe_count_df = joe_count_df.reset_index()
    joe_year_df = joe_count_df[joe_count_df['year'] >= 2001]
    joe_year_df = joe_year_df.set_index("year")

    # Plotting all yearly counts with labels for each name
    plt.figure()
    plt.plot(jacob_year_df, label='Jacob')  # Plots Jacobs change using a line
    plt.plot(mike_year_df, label='Michael')  # Plots Mikes
    plt.plot(matthew_year_df, label="Matthew")  # Plots Matthew
    plt.plot(josh_year_df, label="Joshua")  # Plots Josh
    plt.plot(emily_year_df, label="Emily")  # Plots Emily
    plt.plot(chris_year_df, label="Christopher")  # plots chris
    plt.plot(nick_year_df, label='Nicholas')  # plots nick
    plt.plot(andrew_year_df, label='Andrew')  # plots andrew
    plt.plot(hannah_year_df, label='Hannah')  # plots hannah
    plt.plot(joe_year_df, label='Joseph')  # plots joe
    plt.title("Most Popular Year 2000 Names over 15 Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Names")
    plt.legend(fontsize=7.5)
    plt.show()

    return


# Gets the count of the most popular name in the year 1985 -- Ben
def most_popular_year_1985_names(df):
    df_1985 = df[df['year'] == 1985]
    top10_name_df = df_1985.groupby('name')['count'].sum()
    top10_name_df = top10_name_df.reset_index()
    top10_name_df.sort_values(by=["count"], inplace=True, ascending=False)
    top10_name_df = top10_name_df[:10]

    # Plots each one of the names on basis of their count with color determinants for gender
    plt.figure()
    plt.bar(top10_name_df['name'], top10_name_df['count'],
            color=['blue', 'blue', 'pink', 'pink', 'blue', 'pink', 'blue', 'pink', 'blue', 'blue'])
    plt.title("Most Popular Names in the Year 1985")
    plt.xlabel("Name")
    plt.ylabel("Number of Names")
    plt.xticks(rotation=90)
    plt.show()

    return


# Gets the count of the most popular name in the year 2000 -- Ben
def most_popular_year_2000_names(df):
    df_2000 = df[df['year'] == 2000]
    top10_name_df = df_2000.groupby('name')['count'].sum()
    top10_name_df = top10_name_df.reset_index()
    top10_name_df.sort_values(by=["count"], inplace=True, ascending=False)
    top10_name_df = top10_name_df[:10]

    # Plots each one of the names on basis of their count with color determinants for gender
    plt.figure()
    plt.bar(top10_name_df['name'], top10_name_df['count'],
            color=['blue', 'blue', 'blue', 'blue', 'pink', 'blue', 'blue', 'blue', 'pink', 'blue'])
    plt.title("Most Popular Names in the Year 2000")
    plt.xlabel("Name")
    plt.ylabel("Number of Names")
    plt.xticks(rotation=90)
    plt.show()

    return


# -- Maddie
# Takes in the dataframe, desired name, and desired line color
# Finds index of name, puts all indexes into a list
# Loops through list, adds birth year and number of names for that year
# Plots all names in a pivot table
def name_over_years(df, name, c):
    index_list = np.where(df["name"] == name)

    name_df = pd.DataFrame()

    for index in index_list:
        name_df = df[["year", "count"]].iloc[index].reset_index()

    plt.figure()
    plt.plot(name_df["year"], name_df["count"], color=c)
    plt.title("Popularity of {0}".format(name))
    plt.xlabel("Year")
    plt.ylabel("Number of Babies")
    plt.show()

    # print(name_df.to_string())


# -- Maddie
# Takes in the dataframe, desired name, desired year and desired line color
# Desired year is the release year of whatever movie or tv show corresponds to the name
# Finds index of name, puts all indexes into a list
# Loops through list, adds birth year and number of names for that year
# Plots all names in a pivot table
def pop_culture_name(df, name, year, c):
    index_list = np.where(df["name"] == name)

    name_df = pd.DataFrame()

    for index in index_list:
        name_df = df[["year", "count"]].iloc[index].reset_index()

    plt.figure()
    plt.plot(name_df["year"], name_df["count"], color=c)
    plt.axvline(x=year, color="red")
    plt.title("Popularity of {0}".format(name))
    plt.xlabel("Year")
    plt.ylabel("Number of Babies")
    plt.show()


# -- Maddie
# Plots popularity of "Giselle" from 1880-2015
# Marks x axis at 1996, 2007, and 2009 to signify special events
def g_name(df):
    index_list = np.where(df["name"] == "Giselle")

    name_df = pd.DataFrame()

    for index in index_list:
        name_df = df[["year", "count"]].iloc[index].reset_index()

    plt.figure()
    plt.plot(name_df["year"], name_df["count"], color="black")
    plt.axvline(x=1996, color="red")
    plt.axvline(x=2006, color="gold")
    plt.axvline(x=2009, color="dodgerblue")
    plt.title("Popularity of Giselle")
    plt.xlabel("Year")
    plt.ylabel("Number of Babies")
    plt.show()


main()
