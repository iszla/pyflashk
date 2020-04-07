import csv
import glob
import json
import re

from flask import Flask, abort, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', data=get_all_data_sources())


@app.route('/data/<file>')
def flash_cards(file):
    data = get_data_source_by_name(file)

    if data is None:
        return abort(404)

    return render_template(
        'flash_cards.html',
        name=file,
        cards=json.dumps(data)
    )


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
        return None


if __name__ == '__main__':
    app.run(host='0.0.0.0')
