# WVS Research Project

**A project for analyzing and visualizing World Values Survey (WVS) data**  
This project enables the following functionalities:
- **Maps** visualizing survey results for questions in **Show Card 3**.
- **Text statistics** identifying the Top-5 and Bottom-5 countries for rejection rates.
- **Statistics for a single country** across all questions.
- **Comparison** between two countries with a **bar chart** highlighting the differences.

---

## Project Structure

```plaintext
WVS_research/
│
├── data/
│   └── WVS_Cross-National_Wave_7_csv_v6_0.csv        # Input data file
│
├── documentation/                                   # WVS Documentation
│   ├── F00010738-WVS-7_Master_Questionnaire.pdf
│   ├── F00010762-List_of_countries_WVS7.pdf
│   └── ...
│
├── output_results/                                  # Analysis results
│   ├── Germany_vs_United_States_comparison.png      # Comparison chart
│   ├── map_Q18.html                                 # Map for Q18
│   ├── map_Q19.html                                 # Map for Q19
│   ├── ...                                          # Maps for all questions
│   ├── question_statistics.txt                      # Text statistics
│   └── United_States_statistics.png                 # Single-country chart
│
├── LICENSE                                          # License file
├── main.py                                          # Main script
├── show_card_3_analysis.py                          # Analysis functions
└── README.md                                        # Project documentation
```

---

## Dependencies

Ensure you have **Python >=3.8** installed. Install the required libraries using `pip`:

```bash
pip install pandas folium matplotlib requests shapely
```

---

## How to Run the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/WVS_research.git
   cd WVS_research
   ```

2. **Run the script:**
   ```bash
   python main.py
   ```

3. **Choose an option:**
   - **1**: Generate maps and text statistics for all survey questions.
   - **2**: Get statistics for a specific country.
   - **3**: Compare statistics for two countries.

---

## Questions in Show Card 3

| Question | Description                               |
|----------|-------------------------------------------|
| Q18      | Drug addicts                              |
| Q19      | People of a different race                |
| Q20      | People who have AIDS                      |
| Q21      | Immigrants/foreign workers                |
| Q22      | Homosexuals                               |
| Q23      | People of a different religion            |
| Q24      | Heavy drinkers                            |
| Q25      | Unmarried couples living together         |
| Q26      | People who speak a different language     |

---

## License

This project is licensed under the **MIT License**. See the file **LICENSE** for details.

---

## Authors and Acknowledgements

**Author**: Nikita Manaenkov  
**Data Source**: [World Values Survey](https://www.worldvaluessurvey.org/).  

