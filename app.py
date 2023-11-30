from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

from run import batch_run_by_fix_context


app = Flask(__name__)

CSV_FILE = 'cache_result.demo'  # Assuming the CSV file is named 'cache_result.demo'

df = pd.read_csv(CSV_FILE) # Load the CSV file into a Pandas DataFrame

@app.route('/')
def index():
    # Render the main page with the DataFrame displayed in an HTML table
    return render_template('index.html', table=df.to_html(index=False))

@app.route('/update', methods=['POST'])
def update():
    global df
    # Get the updated values from the form
    input_context = request.form['input_context']
    round = int(request.form['round'])

    df = pd.DataFrame(columns=df.columns)
    for row in batch_run_by_fix_context(round, input_context):
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    # Update the DataFrame
    df.to_csv(CSV_FILE, index=False)

    # Redirect back to the main page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6001)
