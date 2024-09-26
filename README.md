# CDC Data Analysis Dashboard

This project is a dashboard that analyzes data from the Centers for Disease Control and Prevention (CDC) in the United States. The dashboard was built using the **Streamlit** library, which allows for creating interactive web applications in Python. The data provides insights into chronic disease indicators across the United States.

## Features

- Interactive dashboard created using Streamlit.
- Data visualization and filtering options based on various chronic disease indicators.
- Displays data from different U.S. states, organized by chronic disease topics and other key factors.

## Dataset Description

The dataset used in this project contains several columns that represent various aspects of chronic disease reporting. Below is a description of each column:

| Column Name                  | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `Year_Start`                  | Identifies the year when reporting started.                                 |
| `Year_End`                    | Identifies the year when reporting ends.                                    |
| `State_Abbreviation`          | Two-character postal abbreviation for the state name.                       |
| `State_Name`                  | Name of U.S. state or District of Columbia.                                 |
| `Data_Source`                 | Identifies the source from where the data is collected.                     |
| `Topic`                       | Identifies the chronic disease topic.                                       |
| `Question`                    | Identifies the chronic disease indicator.                                   |
| `Data_Value_Unit`             | Identifies the unit of the data value.                                      |
| `Data_Value_Type`             | Identifies the type of data value.                                          |
| `Data_Value`                  | Identifies the actual value of the data.                                    |
| `Data_Value_Alt`              | Identifies the alternate data value (non-numeric values are eliminated).    |
| `Data_Value_Footnote`         | Provides footnotes for data values.                                         |
| `Low_Confidence_Limit`        | Lower confidence interval of the data.                                      |
| `High_Confidence_Limit`       | Higher confidence interval of the data.                                     |
| `Stratification_Category_1`   | Identifies the sampling category of the population.                         |
| `Stratification1`             | Identifies the sampling sub-category of the population.                     |
| `Latitude`                    | Latitude of the geographical location.                                      |
| `Longitude`                   | Longitude of the geographical location.                                     |
| `Location_ID`                 | Location identifier.                                                       |
| `Topic_ID`                    | Short form of the chronic disease category.                                 |
| `Question_ID`                 | Short form of the chronic disease indicator.                                |
| `Data_Value_Type_ID`          | Short form representing the data value type.                                |
| `Stratification_Category_ID1` | Short form of the sampling category.                                        |
| `Stratification_ID1`          | Short form of the sampling sub-category.                                    |

## Technologies Used

- **Streamlit**: A Python library for building interactive web apps quickly.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For data visualization.

## How to Run

1. Clone the repository.
2. Install the required dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt



