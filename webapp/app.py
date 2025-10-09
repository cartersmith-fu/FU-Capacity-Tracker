from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    df = pd.read_csv('../data/example_data.csv')
    df = df.tail(10)  # show the 10 most recent entries
    return render_template('index.html', data=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
