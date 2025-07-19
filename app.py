from flask import Flask, request, render_template
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Define the full file path
FILE_PATH = os.path.join(os.path.dirname(__file__), "sis_inscris.xlsx")

# Load or create the Excel file
try:
    df = pd.read_excel(FILE_PATH, sheet_name=None)
    if 'All Members' not in df:
        df['All Members'] = pd.DataFrame(columns=['Nom Complet', 'Date de Naissance', 'Ville', 'Date Inscription'])
except FileNotFoundError:
    df = {
        '2021': pd.DataFrame(columns=['Nom Complet', 'Date de Naissance', 'Ville', 'Date Inscription']),
        '2022': pd.DataFrame(columns=['Nom Complet', 'Date de Naissance', 'Ville', 'Date Inscription']),
        '2023': pd.DataFrame(columns=['Nom Complet', 'Date de Naissance', 'Ville', 'Date Inscription']),
        '2024': pd.DataFrame(columns=['Nom Complet', 'Date de Naissance', 'Ville', 'Date Inscription']),
        '2025': pd.DataFrame(columns=['Nom Complet', 'Date de Naissance', 'Ville', 'Date Inscription']),
        'All Members': pd.DataFrame(columns=['Nom Complet', 'Date de Naissance', 'Ville', 'Date Inscription'])
    }
    with pd.ExcelWriter(FILE_PATH) as writer:
        for sheet, frame in df.items():
            frame.to_excel(writer, sheet_name=sheet, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            nom = request.form['nom']
            naissance = request.form['naissance']
            ville = request.form['ville']
            inscription = request.form['inscription']
            year = datetime.strptime(inscription, '%Y-%m-%d').year

            new_data = pd.DataFrame({
                'Nom Complet': [nom],
                'Date de Naissance': [naissance],
                'Ville': [ville],
                'Date Inscription': [inscription]
            })

            # Save to the year-specific sheet
            with pd.ExcelWriter(FILE_PATH, mode='a', if_sheet_exists='overlay') as writer:
                if str(year) in df:
                    new_data.to_excel(writer, sheet_name=str(year), startrow=df[str(year)].shape[0] + 1, index=False, header=False)
                    df[str(year)] = pd.concat([df[str(year)], new_data], ignore_index=True)
                else:
                    new_data.to_excel(writer, sheet_name=str(year), index=False)
                    df[str(year)] = new_data

            # Save to the All Members sheet
            with pd.ExcelWriter(FILE_PATH, mode='a', if_sheet_exists='overlay') as writer:
                if 'All Members' in df:
                    new_data.to_excel(writer, sheet_name='All Members', startrow=df['All Members'].shape[0] + 1, index=False, header=False)
                    df['All Members'] = pd.concat([df['All Members'], new_data], ignore_index=True)
                else:
                    new_data.to_excel(writer, sheet_name='All Members', index=False)
                    df['All Members'] = new_data

            return 'success'
        except Exception as e:
            return 'error'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)