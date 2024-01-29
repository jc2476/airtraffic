from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('static/airtraffic.csv')

@app.route('/monthly-stats', methods=['GET'])
def monthly_stats():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    data = df[(df['Year'] == year) & (df['Month'] == month)]
    return jsonify(data.to_dict(orient='records'))

@app.route('/yearly-summary', methods=['GET'])
def yearly_summary():
    year = request.args.get('year', type=int)
    data = df[df['Year'] == year]
    return jsonify(data.to_dict(orient='records'))

@app.route('/date-range', methods=['GET'])
def date_range():
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    range_data = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    return jsonify(range_data.to_dict(orient='records'))


@app.route('/top-busiest-months', methods=['GET'])
def top_busiest_months():
    limit = request.args.get('limit', default=10, type=int)
    sorted_data = df.sort_values(by=['Pax'], ascending=False)
    top_data = sorted_data.head(limit)
    return jsonify(top_data.to_dict(orient='records'))


@app.route('/average-load-factor', methods=['GET'])
def average_load_factor():
    result = df.groupby('Year')['LF'].mean()
    return jsonify(result.to_dict())


@app.route('/domestic-vs-international', methods=['GET'])
def domestic_vs_international():
    year = request.args.get('year', type=int)
    comparison_data = df[df['Year'] == year][['Dom_Pax', 'Int_Pax', 'Dom_Flt', 'Int_Flt']]
    return jsonify(comparison_data.to_dict(orient='records'))


@app.route('/yearly-growth', methods=['GET'])
def yearly_growth():
    metric = request.args.get('metric', default='Pax')  # Or 'Flt' for flights
    df['Previous_Year'] = df[metric].shift(1)
    df['Growth'] = ((df[metric] - df['Previous_Year']) / df['Previous_Year']) * 100
    growth_data = df[['Year', 'Growth']].dropna()
    return jsonify(growth_data.to_dict(orient='records'))


@app.route('/extreme-travel-months', methods=['GET'])
def extreme_travel_months():
    highest = df.groupby('Month')['Pax'].sum().idxmax()
    lowest = df.groupby('Month')['Pax'].sum().idxmin()
    return jsonify({'highest_travel_month': highest, 'lowest_travel_month': lowest})


@app.route('/seasonal-trends', methods=['GET'])
def seasonal_trends():
    # Simple approach: Average traffic per month across all years
    trends = df.groupby('Month')['Pax'].mean()
    return jsonify(trends.to_dict())


@app.route('/health', methods=['GET'])
def health_check():
    # You can add custom logic to check the health of your application here.
    # For a basic health check, you can simply return a success message.
    return jsonify({'status': 'healthy'})

#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)