import pandas as pd
import folium
import requests
from shapely.geometry import shape, Polygon, MultiPolygon

# Country codes dictionary
COUNTRY_CODES = {
    8: 'Albania', 12: 'Algeria', 36: 'Australia', 40: 'Austria', 50: 'Bangladesh', 51: 'Armenia',
    68: 'Bolivia', 76: 'Brazil', 104: 'Myanmar', 124: 'Canada', 156: 'China', 158: 'Taiwan',
    170: 'Colombia', 203: 'Czech Republic', 218: 'Ecuador', 231: 'Ethiopia', 276: 'Germany',
    300: 'Greece', 320: 'Guatemala', 344: 'Hong Kong', 356: 'India', 360: 'Indonesia',
    364: 'Iran', 368: 'Iraq', 392: 'Japan', 398: 'Kazakhstan', 400: 'Jordan', 404: 'Kenya',
    410: 'South Korea', 417: 'Kyrgyzstan', 422: 'Lebanon', 434: 'Libya', 458: 'Malaysia',
    484: 'Mexico', 496: 'Mongolia', 504: 'Morocco', 558: 'Nicaragua', 566: 'Nigeria',
    528: 'Netherlands', 586: 'Pakistan', 604: 'Peru', 608: 'Philippines', 630: 'Puerto Rico',
    642: 'Romania', 643: 'Russia', 702: 'Singapore', 703: 'Slovakia', 704: 'Vietnam',
    716: 'Zimbabwe', 764: 'Thailand', 762: 'Tajikistan', 788: 'Tunisia', 792: 'Turkey',
    804: 'Ukraine', 818: 'Egypt', 826: 'United Kingdom', 840: 'United States', 860: 'Uzbekistan',
    862: 'Venezuela'
}

# Question contents
QUESTION_CONTENT = {
    "Q18": "Drug addicts",
    "Q19": "People of a different race",
    "Q20": "People who have AIDS",
    "Q21": "Immigrants/foreign workers",
    "Q22": "Homosexuals",
    "Q23": "People of a different religion",
    "Q24": "Heavy drinkers",
    "Q25": "Unmarried couples living together",
    "Q26": "People who speak a different language"
}

# Calculate percentages
def count_percentage_by_country(dataframe, question_column):
    results = []
    for country_code, country_name in COUNTRY_CODES.items():
        df_country = dataframe[dataframe['B_COUNTRY'] == country_code]
        count_1 = df_country[question_column].value_counts().get(1, 0)
        count_2 = df_country[question_column].value_counts().get(2, 0)
        total = count_1 + count_2
        percentage = (count_1 / total) * 100 if total > 0 else 0
        if percentage > 0:
            results.append((country_name, percentage))
    return sorted(results, key=lambda x: x[1], reverse=True)

# Get country statistics
def get_country_statistics(dataframe, country_name, question_columns):
    country_code = next((code for code, name in COUNTRY_CODES.items() if name == country_name), None)
    if country_code is None:
        print(f"Country '{country_name}' not found.")
        return None

    results = {}
    for question in question_columns:
        df_country = dataframe[dataframe['B_COUNTRY'] == country_code]
        count_1 = df_country[question].value_counts().get(1, 0)
        count_2 = df_country[question].value_counts().get(2, 0)
        total = count_1 + count_2
        percentage = (count_1 / total) * 100 if total > 0 else 0
        results[QUESTION_CONTENT[question]] = round(percentage, 2)
    return results

# Generate map with question title
def generate_map(results, question_column, geojson_data, output_file):
    world_map = folium.Map(location=[20, 0], zoom_start=2)
    title = QUESTION_CONTENT.get(question_column, "Unknown question")

    folium.Choropleth(
        geo_data=geojson_data,
        data=pd.DataFrame(results, columns=["Country", question_column]),
        columns=["Country", question_column],
        key_on="feature.properties.name",
        fill_color="YlGnBu",
        nan_fill_color="grey",
        legend_name=f"{title} Percentage (%)"
    ).add_to(world_map)

    world_map.save(output_file)
    print(f"Map saved as '{output_file}'")

