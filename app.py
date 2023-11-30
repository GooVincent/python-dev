from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import time
import shutil
import os

from run import batch_run_by_fix_context


app = Flask(__name__)

demo = 'cache_result.demo'
CSV_FILE = f'{demo}.{time.time()}'   # Assuming the CSV file is named 'cache_result.demo'
print(f'cache file:{CSV_FILE}')

# rm cache files
files = os.listdir('./')
for file in files:
    if file.startswith(f'{demo}.'):
        os.remove(file)
shutil.copyfile(demo, CSV_FILE)

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
    round = int(request.form['round']) if len(request.form['round']) > 0 else 1
    seed = int(request.form['seed']) if len(request.form['seed']) > 0 else -1

    df = pd.DataFrame(columns=df.columns)
    answers = batch_run_by_fix_context(round, input_context, seed=seed)
    for row in answers:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    # Update the DataFrame
    df.to_csv(CSV_FILE, index=False)

    # Redirect back to the main page
    return redirect(url_for('index'))

if __name__ == '__main__':
    import sys

    listen_port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=listen_port)
