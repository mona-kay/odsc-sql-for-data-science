# All Activities

## Getting Started
### At the Command Line
After setting up SQLite3, you can access the global power plants database by changing directory into the folder where you downloaded the file. For example:
```
> cd Documents/odsc-sql-for-data-science
```

Then, start SQLite3 and open the database file.
```
> sqlite3
> .open global_powerplants.db
```

From there, you can query information from the tables in the database.
```
SELECT *
FROM countries
LIMIT 10;
```

## Activity 1
The `global_powerplants.db` database file contains data on the characteristics and output of thousands of power plants around the world.

1. Select the first few records from the `countries` and `power_plants` tables.
Do you see any information shared between the two tables? Note this down, as this will be necessary for the next section.

2. Identify the other tables available in this database by querying the `sqlite_master` schema.


## Activity 2

1. Determine how many records are in the `power_plants` table.

2. How many unique types of `primary_fuel` exist in the `power_plants` table?

3. Which type of `primary_fuel` has the highest average `capacity_mw`?

4. Which `country_id` has the highest total `generation_gwh` in the `power_generation` table?


## Activity 3

1. What type of join do you need if you want the number of power plants per country, _including_ countries with no records in the `power_plants` table?

2. Select all information from the `countries` and `power_plants` tables using a left join. Limit your results to 100.


## Activity 4

1. How many power plants are in each country? Join the `power_plants` table to the `countries` table to get the country name.

2. Which country has the most power plants in the database? You can use `DESC` to sort your results in descending order.

3. Which country has the most unique sources in the `data_sources` table?


## Activity 5

1. What is the oldest power plant in the `power_plants` table? Use the `commissioning_year` column to find out.

2. Create a new column called `fuels` that combines the `primary_fuel` and `other_fuel` columns.

3. Trim down the `url` column in the `data_sources` table using the `REPLACE()` function to remove `http://`. You can read about how it works here: https://www.sqlitetutorial.net/sqlite-replace-function/


## Activity 6

1. How many power plants in the database have a primary fuel that is a form of renewable energy -- `IN ('Hydro', 'Wind', 'Solar', 'Geothermal', 'Wave and Tidal')`?

2. There are a lot of missing values in the `year_of_capacity_data` column. Replace all missing values with the year `'2018'` using a `CASE` statement.


## Activity 7

1. Prepare a “pivot table” of countries’ average `capacity_mw` by whether or not the power plant’s primary fuel is a renewable `('Hydro', 'Wind', 'Solar', 'Geothermal', 'Wave and Tidal')`. Each renewable type should be a separate column.

2. Determine the average `capacity_mw` across all power plants. Then, calculate the average `capacity_mw` by `primary_fuel`. What % higher or lower is each fuel type capacity compared to your benchmark average?
