#!/usr/bin/env python

"""
http://datasets.wri.org/dataset/globalpowerplantdatabase
"""

import pandas as pd
from sqlalchemy import create_engine

pplants = pd.read_csv('globalpowerplantdatabasev120/global_power_plant_database.csv')

# Create database
engine = create_engine('sqlite:///global_powerplants.db', echo=False)
pplants.to_sql('pplants_all', con = engine)

engine.execute("SELECT * FROM pplants_all LIMIT 5;").fetchall()

# Create and check unique country records
engine.execute("""
               CREATE TABLE countries_test AS
               SELECT DISTINCT country, country_long
               FROM pplants_all;
               """)

engine.execute("SELECT * FROM countries_test LIMIT 5;").fetchall()

# Create and check the countries table
engine.execute("""
               CREATE TABLE countries AS
               SELECT DISTINCT
                   RANK() over(ORDER BY country) as id,
                   country AS country_short,
                   country_long AS country
               FROM countries_test;
               """)

engine.execute("SELECT * FROM countries LIMIT 5;").fetchall()

# Create and check unique source records
engine.execute("""
               CREATE TABLE sources_test AS
               SELECT DISTINCT source, geolocation_source, url
               FROM pplants_all;
               """)

engine.execute("SELECT * FROM sources_test LIMIT 5;").fetchall()

# Create and check the sources table
engine.execute("""
               CREATE TABLE data_sources AS
               SELECT RANK() over(ORDER BY source) as id, source, geolocation_source, url
               FROM sources_test WHERE source IS NOT NULL ORDER BY source;
               """)

engine.execute("SELECT * FROM data_sources LIMIT 5;").fetchall()

# Get generation data by year
engine.execute("""
               CREATE TABLE power_generation AS
               SELECT
                   c.id AS country_id,
                   p.gppd_idnr,
                   '2013' as year,
                   p.generation_gwh_2013 AS generation_gwh
               FROM pplants_all p
               JOIN countries c
               ON p.country = c.country_short
               WHERE p.generation_gwh_2013 IS NOT NULL

               UNION ALL

               SELECT
                   c.id AS country_id,
                   p.gppd_idnr,
                   '2014' as year,
                   p.generation_gwh_2014 AS generation_gwh
               FROM pplants_all p
               JOIN countries c
               ON p.country = c.country_short
               WHERE p.generation_gwh_2014 IS NOT NULL

               UNION ALL

               SELECT
                   c.id AS country_id,
                   p.gppd_idnr,
                   '2015' as year,
                   p.generation_gwh_2013 AS generation_gwh
               FROM pplants_all p
               JOIN countries c
               ON p.country = c.country_short
               WHERE p.generation_gwh_2015 IS NOT NULL

               UNION ALL

               SELECT
                   c.id AS country_id,
                   p.gppd_idnr,
                   '2016' as year,
                   p.generation_gwh_2013 AS generation_gwh
               FROM pplants_all p
               JOIN countries c
               ON p.country = c.country_short
               WHERE p.generation_gwh_2016 IS NOT NULL

               UNION ALL

               SELECT
                   c.id AS country_id,
                   p.gppd_idnr,
                   '2017' as year,
                   p.generation_gwh_2013 AS generation_gwh
               FROM pplants_all p
               JOIN countries c
               ON p.country = c.country_short
               WHERE p.generation_gwh_2017 IS NOT NULL;
               """)

engine.execute("SELECT * FROM power_generation LIMIT 5;").fetchall()

# Create the main table
engine.execute("""
               CREATE TABLE power_plants AS
               SELECT DISTINCT
                   p.wepp_id,
                   p.name,
                   c.id AS country_id,
                   p.gppd_idnr,
                   p.capacity_mw,
                   p.latitude,
                   p.longitude,
                   p.primary_fuel,
                   p.other_fuel1 AS other_fuel,
                   p.commissioning_year,
                   p.owner,
                   p.source,
                   s.id AS source_id,
                   p.year_of_capacity_data,
                   p.estimated_generation_gwh
               FROM pplants_all p
               JOIN countries c
               ON p.country = c.country_short
               LEFT JOIN data_sources s
               ON s.source = p.source;
               """)

# Drop unneeded tables
engine.execute("DROP TABLE pplants_all;")
engine.execute("DROP TABLE countries_test;")
engine.execute("DROP TABLE sources_test;")
