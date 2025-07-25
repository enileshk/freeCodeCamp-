import pandas as pd

def calculate_demographic_data(print_data=True):
    path = r"adult.data.csv"
    # Read data from file
    df = pd.read_csv(path)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby('race')['race'].count()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == "Male"].age.mean(),1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(len(df[df['education'] == "Bachelors"])*100/len(df),1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    high_list = ["Bachelors", "Masters", "Doctorate"]
    higher_education = len(df[df['education'].isin(high_list)])
    lower_education = len(df[~df['education'].isin(high_list)])
    # percentage with salary >50K
    higher_education_rich = round(len(df[(df['education'].isin(high_list)) & (df.salary == ">50K")])*100/
                                     higher_education,1 )
    lower_education_rich = round(len(df[(~df['education'].isin(high_list)) & (df.salary == ">50K")])*100/
                                     lower_education,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()
    count_min_rich = len(df[df['hours-per-week'] == min_work_hours & (df.salary == ">50K")])

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = (df['hours-per-week'] == min_work_hours).sum()

    #rich_percentage = round(count_min_rich*100/num_min_workers,1)
    rich_percentage = round(count_min_rich*100/num_min_workers,1)

    # What country has the highest percentage of people that earn >50K?
    df["high_salary"] = df["salary"] == ">50K"
    result = df.groupby("native-country").agg(
        total_count=("workclass", "count"),
        high_salary_count=("high_salary", "sum")
    ).reset_index()
    result['percent_high_sal'] = result.high_salary_count * 100 / result.total_count
    max_row = result.loc[result['percent_high_sal'].idxmax()]
    highest_earning_country = max_row['native-country']
    highest_earning_country_percentage = round((max_row.percent_high_sal),1)

    # Identify the most popular occupation for those who earn >50K in India.
    high_income = df[(df['salary'] == ">50K") & (df['native-country'] == "India")]

    high2 = high_income.groupby("occupation").agg(
        count_high=("high_salary", "sum")).reset_index()
    #print(high2.head())
    max_row2 = high2.loc[high2['count_high'].idxmax()]
    #print(max_row2.occupation)
    top_IN_occupation = max_row2.occupation

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
