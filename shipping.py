import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt 
from dataprep.clean.clean_country import validate_country


ships = pd.read_csv("/home/user/Downloads/ships/US_MerchantFleet_ST202010011334_v4.csv")
print(ships.info())
print(ships["Economy Label"].unique())

# Drop empty columns
ships = ships.dropna(axis="columns")
print(ships.info())
print(ships.head(10))                
ships = ships.replace("Korea, Republic of", "South Korea")
    

''' Q1)world shipping growth over the years 
'''

world_ships = ships[ships["Percentage of total world"] == 100]
print(world_ships.to_string())
x= world_ships[world_ships["ShipType Label"] == "Total fleet"]
print(x)

# plot the world's ships 1980-2020
plt.figure(figsize=(15,8))
sns.lineplot(x="Year", y="Dead weight tons in thousands", data=x)
plt.title("Total World Ship Fleet 1980-2020")


# Drop regional Economies
ships["remove_region"] = validate_country(ships["Economy Label"])
ships = ships[ships["remove_region"] == True]
print(ships)

''' q2)what countries own the biggest fleets ?
'''

# sum the total cargo tonnes per country across all the years and get the top 10
flag = ships[ships["ShipType Label"].str.contains("Total fleet")]
print(flag)
country_tonnage = flag.groupby("Economy Label")["Dead weight tons in thousands"].sum().sort_values(ascending=False).reset_index()
world_ships_ten = country_tonnage.head(10)
print(world_ships_ten)


# a bar plot of the top ten world ships 
sns.set(font_scale=3, context="paper", color_codes=False)

fig, axes = plt.subplots(1, 1, figsize=(35, 15))
sns.barplot(data=world_ships_ten, x="Economy Label", y="Dead weight tons in thousands").set(title="world_ships Ten Fleet Owners")
plt.tight_layout()
plt.yscale('log')
plt.show()

# A GeoDataframe
df_geo = gpd.GeoDataFrame(country_tonnage)
print(df_geo.head(3))
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world_ships = country_tonnage.rename(columns = {'Economy Label':'name'})
merge = pd.merge(world, world_ships, on="name")
print(merge.head())

# world map ships distribution
ax = world["geometry"].boundary.plot(figsize=(20,16))
merge.plot( column="Dead weight tons in thousands", ax=ax, cmap='OrRd', 
                     legend=True, legend_kwds={"label": "Dead weight tons in thousands", "orientation":"horizontal"})


''' q3) under what flag are most ships registered?
''' 

oil_tankers = ships[ships["ShipType Label"].isin(["Oil tankers"])]["Dead weight tons in thousands"].sum()
print("Tonnes in Thousands for oil tankers:", oil_tankers)
Bulk_carriers = ships[ships["ShipType Label"].isin(["Bulk carriers"])]["Dead weight tons in thousands"].sum()
print("Tonnes in Thousands for bulk carriers:", Bulk_carriers)
General_cargo = ships[ships["ShipType Label"].isin(["General cargo"])]["Dead weight tons in thousands"].sum()
print("Tonnes in Thousands for general cargo ships:", General_cargo)
Container_ships = ships[ships["ShipType Label"].isin(["Container ships"])]["Dead weight tons in thousands"].sum()
print("Tonnes in Thousands for container ships:", Container_ships)
Other_types_of_ships = ships[ships["ShipType Label"].isin(["Other types of ships"])]["Dead weight tons in thousands"].sum()
print("Tonnes in Thousands for other types of ships:", Other_types_of_ships)

# plot out the types of ships
data = [oil_tankers, Bulk_carriers, General_cargo, Container_ships, Other_types_of_ships]
keys = ["oil tankers", "Bulk carriers", "General cargo", "Container ships", "Other types of ships"]
fig, axes = plt.subplots(1, 1, figsize=(35, 15))
palette_color = sns.color_palette('bright')
plt.pie(data, labels=keys, colors=palette_color, autopct='%.0f%%')
plt.title("Types Of Ships Ferrying Worldwide")

''' q4) Where are most ships built ?
'''
ship_building = pd.read_csv("/home/user/Downloads/ships/US_ShipBuilding_ST202010131356_v1.csv")
ship_building = ship_building.replace("Korea, Republic of", "South Korea")
print(ship_building.info())
 
# drop the two columns
ship_building = ship_building.drop(columns=["Percentage of total all economies Footnote", "Gross Tonnage Footnote"])
print(ship_building.info())

# Drop regional Economies
ship_building["remove_region"] = validate_country(ship_building["Country Label"])
ship_building = ship_building[ship_building["remove_region"] == True]
print(ship_building)

# Total Sum Of Ships Built Over the Entire Duration 
total_build = ship_building.groupby("Country Label")["Gross Tonnage"].sum().sort_values(ascending=False).reset_index()
print(total_build)

# Plot The world_ships 10 Ship Building Countries
upper_builders = total_build.head(10)
print(upper_builders)
fig, axes = plt.subplots(1, 1, figsize=(35, 15))
sns.barplot(data=upper_builders, x="Country Label", y="Gross Tonnage")
sns.despine(left=True, bottom=True)
plt.yscale('log')
plt.xticks(rotation=45)
plt.title("world_ships 10 Ship Builders Worldwide", fontsize=40)

''' q5) Where are most ships scrapped? 
'''
ship_scrapping = pd.read_csv("/home/user/Downloads/ships/US_ShipScrapping_ST202010121509_v1.csv")
print(ship_scrapping.info())

# drop two empty columns
ship_scrapping = ship_scrapping.drop(columns=["Percentage of total all economies Footnote", "Gross Tonnage Footnote"])
print(ship_scrapping.info())

#drop regional economies
ship_scrapping = ship_scrapping.replace("Korea, Republic of", "South Korea")
ship_scrapping["remove_region"] = validate_country(ship_scrapping["Country Label"])
ship_scrapping = ship_scrapping[ship_scrapping["remove_region"] == True]
print(ship_scrapping)

# sort by 10 highest gross tonnage
ship_scrapping = ship_scrapping.groupby("Country Label")["Gross Tonnage"].sum().sort_values(ascending=False).reset_index()
ship_scrapping = ship_scrapping.head(10)

# plot the 10 highest scrappers
fig, axes = plt.subplots(1, 1, figsize=(45, 15))
#sns.set(font_scale=5)
sns.barplot(data=ship_scrapping, x="Country Label", y="Gross Tonnage")
sns.despine(left=True, bottom=True)
plt.yscale('log')
plt.xticks(rotation=45)
plt.title("world_ships 10 Ship Scrappers Worldwide", fontsize=40)


