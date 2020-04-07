from flask import Flask, render_template
import glob
import re
import csv
import json
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', data=get_all_data_sources())


@app.route('/data/<file>')
def flash_cards(file):
    data = get_data_source_by_name(file)
    print(data)
    if data == None:
        return 404

    return render_template('flash_cards.html', name=file, cards=json.dumps(data))


def get_all_data_sources():
    files = glob.glob('data/*.csv')
    data = []

    for f in files:
        try:
            data.append(re.search(r'data[\/\\](.+?).csv', f).group(1))
        except AttributeError:
            pass

    return data


def get_data_source_by_name(name):
    try:
        data = {}
        with open('data/{}.csv'.format(name)) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                data[row[0]] = row[1]

            return data

    except IOError:
        print('IOError')
        return None


if __name__ == '__main__':
    debug = os.environ.get("DEBUG")
    app.run(debug=debug != "False", host='0.0.0.0')
