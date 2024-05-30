# Project Name

This python program allows for the collection and analysis of media and survey data related to arms control agreements to contribute to a research study on the analysis of the successors and failures of such agreements.

## Installation

1. Clone the repository:
git clone https://github.com/EthanMasters23/ArmsControlProject.git

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate

python3 setup.py install
```

## Usage


## Dependencies

Dependencies can found in the requirements.txt


## Project Structure

```css
Arms Control Project/
├── Procfile
├── README.md
├── api_method
│   ├── __init__.py
│   ├── __pycache__
│   │   └── api_data_fetcher.cpython-311.pyc
│   ├── api_data_fetcher.py
│   ├── api_method_driver.py
│   └── api_method_pipeline_log.log
├── arms_control_app
│   ├── __init__.py
│   ├── arms_control_app.py
│   └── article_count.py
├── assets
│   ├── Article_Data_ApiMethod_Raw_(1945-1946).json
│   ├── Article_Data_Cleaned_Df_(1945-1946).json
│   ├── Article_Data_RegexMethod_Raw_(1945-1946).json
│   ├── PollingData.csv
│   └── roper-folder-toplines-asof-20230127.csv
├── lib
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── data_cleaner.cpython-311.pyc
│   │   └── data_visualization.cpython-311.pyc
│   ├── data_cleaner.py
│   └── data_visualization.py
├── polling_data
│   ├── __init__.py
│   └── polling_data_compiler.py
├── regex_method
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── article_stats_fetcher.cpython-311.pyc
│   │   └── regex_data_fetcher.cpython-311.pyc
│   ├── article_stats_fetcher.py
│   ├── regex_data_fetcher.py
│   └── regex_method_driver.py
├── requirements.txt
├── setup.py
└── testing.py
```

## Arms Control Dash Application

This application analyzes public opinion research data and provides interactive visualizations to explore the trends.

## Dash App Showcase

### Description
This Dash app allows users to search for public opinion research data by year and month. It provides interactive graphs and charts to visualize the data dynamically.

### Resources
- [Screenshots](screenshots/)
- [Demo GIF](demo.gif)
- [Demo Scripts](demo_scripts/)
- [Documentation](docs/)

Feel free to explore the app and provide feedback!


## Contributing


## License
