import os
import pandas as pd
import requests
import matplotlib.pyplot as plt
from show_card_3_analysis import (
    count_percentage_by_country,
    get_country_statistics,
    generate_map,
    QUESTION_CONTENT
)

# File paths and configurations
INPUT_FILE = "./data/WVS_Cross-National_Wave_7_csv_v6_0.csv"
OUTPUT_DIR = "./output_results"
QUESTION_COLUMNS = [f"Q{i}" for i in range(18, 27)]
GEOJSON_URL = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"

# Load data and GeoJSON
data = pd.read_csv(INPUT_FILE, low_memory=False)
response = requests.get(GEOJSON_URL)
geojson_data = response.json()


# Option 1: Generate maps and text statistics
def analyze_all_questions():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    text_output_file = os.path.join(OUTPUT_DIR, "question_statistics.txt")

    # Clear the text output file if it exists
    if os.path.exists(text_output_file):
        os.remove(text_output_file)

    # Process all questions
    for question in QUESTION_COLUMNS:
        print(f"Processing {question}...")

        # Calculate percentages
        results = count_percentage_by_country(data, question)

        # Generate map
        map_file = os.path.join(OUTPUT_DIR, f"map_{question}.html")
        generate_map(results, question, geojson_data, map_file)

        # Generate text report
        top_5 = results[:5]
        bottom_5 = sorted(results[-5:], key=lambda x: x[1])
        question_title = QUESTION_CONTENT.get(question, "Unknown question")

        with open(text_output_file, 'a', encoding='utf-8') as file:
            file.write(f"\nStatistics for {question} - {question_title}:\n")
            file.write("\nTop-5 countries with highest rejection:\n")
            for country, perc in top_5:
                file.write(f"{country}: {perc:.2f}%\n")
            file.write("\nBottom-5 countries with lowest rejection:\n")
            for country, perc in bottom_5:
                file.write(f"{country}: {perc:.2f}%\n")

        print(f"Map saved: {map_file}")
    print(f"Textual statistics saved to: {text_output_file}")


# Option 2: Get statistics for a single country and save bar chart
def analyze_single_country():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    country = input("Enter country name: ")
    results = get_country_statistics(data, country, QUESTION_COLUMNS)

    if results:
        print(f"\nStatistics for '{country}':")
        for question, percentage in results.items():
            print(f"{question}: {percentage}%")

        # Create bar chart
        plt.figure(figsize=(10, 6))
        questions = list(results.keys())
        percentages = list(results.values())

        plt.bar(questions, percentages, color='skyblue')
        plt.title(f"Rejection Percentages for '{country}'")
        plt.xlabel("Questions")
        plt.ylabel("Percentage (%)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Save chart as image
        chart_path = os.path.join(OUTPUT_DIR, f"{country.replace(' ', '_')}_statistics.png")
        plt.savefig(chart_path)
        plt.close()
        print(f"Bar chart saved as '{chart_path}'")
    else:
        print("No data available for the selected country.")


# Option 3: Compare statistics for two countries
def compare_two_countries():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    country1 = input("Enter the first country name: ")
    country2 = input("Enter the second country name: ")

    results1 = get_country_statistics(data, country1, QUESTION_COLUMNS)
    results2 = get_country_statistics(data, country2, QUESTION_COLUMNS)

    if results1 and results2:
        print(f"\nStatistics for '{country1}':")
        for question, percentage in results1.items():
            print(f"{question}: {percentage}%")
        print(f"\nStatistics for '{country2}':")
        for question, percentage in results2.items():
            print(f"{question}: {percentage}%")

        # Calculate differences
        differences = {
            question: round(results1[question] - results2[question], 2)
            for question in results1.keys()
        }

        print("\nDifferences between the two countries:")
        for question, diff in differences.items():
            print(f"{question}: {diff}%")

        # Create bar chart
        plt.figure(figsize=(12, 6))
        questions = list(results1.keys())
        percentages1 = list(results1.values())
        percentages2 = list(results2.values())

        bar_width = 0.35
        x = range(len(questions))

        plt.bar(x, percentages1, width=bar_width, color='skyblue', label=country1)
        plt.bar([p + bar_width for p in x], percentages2, width=bar_width, color='orange', label=country2)
        plt.title(f"Comparison of Rejection Percentages: {country1} vs {country2}")
        plt.xlabel("Questions")
        plt.ylabel("Percentage (%)")
        plt.xticks([p + bar_width / 2 for p in x], questions, rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()

        # Save chart as image
        chart_path = os.path.join(OUTPUT_DIR, f"{country1.replace(' ', '_')}_vs_{country2.replace(' ', '_')}_comparison.png")
        plt.savefig(chart_path)
        plt.close()

        print(f"Comparison bar chart saved as '{chart_path}'")
    else:
        print("No data available for one or both selected countries.")

# Run options
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("1. Generate maps and text statistics for all questions")
    print("2. Get statistics for a specific country")
    print("3. Compare statistics for two countries")

    choice = input("Choose an option (1/2/3): ")
    if choice == "1":
        analyze_all_questions()
    elif choice == "2":
        analyze_single_country()
    elif choice == "3":
        compare_two_countries()
    else:
        print("Invalid choice.")
