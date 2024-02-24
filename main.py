from flask import Flask, render_template, jsonify
import requests
from datetime import datetime


# Define the datetime_format
def datetime_format(value, format='%Y-%m-%d %H:%M:%S'):
    if value:
        return datetime.fromtimestamp(value / 1000.0).strftime(format)
    return "N/A"

API_KEY = ""
app = Flask(__name__)
app.jinja_env.filters['datetime_format'] = datetime_format

current_balance = 160000000  # Set your current balance here

# Read item IDs from the file
with open('item_ids.txt') as file:
    item_ids = [line.strip() for line in file]

# Store prices data and last updated timestamp globally
prices_data = {}
last_updated = None


@app.template_filter('format_number')
def format_number(value, decimals=2):
    try:
        if decimals == 0:
            return "{:,.0f}".format(value)  # Format as an integer
        return "{:,.2f}".format(value)  # Format with two decimal places
    except (ValueError, TypeError):
        return value


def format_item_name(item_name):
    return item_name.replace('_', ' ').title()


def calculate_max_min_prices(prices_data):
    for item_id, product in prices_data.items():
        if item_id in item_ids:
            buy_prices = [buy['pricePerUnit'] for buy in product['buy_summary']]
            sell_prices = [sell['pricePerUnit'] for sell in product['sell_summary']]

            max_buy_price = max(buy_prices) if buy_prices else 0
            min_sell_price = min(sell_prices) if sell_prices else 0

            product['max_buy_price'] = max_buy_price
            product['min_sell_price'] = min_sell_price


# Modify the calculate_points function to use the first buy and sell prices
def calculate_points(product, current_balance):
    try:
        item_id = product['product_id']
        if item_id not in item_ids:
            return 0.0

        buy_summary = product['buy_summary']
        sell_summary = product['sell_summary']

        if not buy_summary or not sell_summary:
            return 0.0

        first_buy_price = buy_summary[0]['pricePerUnit']
        first_sell_price = sell_summary[0]['pricePerUnit']
        price_difference = first_buy_price - first_sell_price

        if price_difference <= 0 or first_buy_price > current_balance:
            return 0.0

        buy_volume = product['quick_status']['buyMovingWeek']
        sell_volume = product['quick_status']['sellMovingWeek']

        max_affordable_quantity = min(current_balance // first_buy_price, min(buy_volume, sell_volume) / 168)
        if max_affordable_quantity == 0:
            return 0.0

        profit_margin = price_difference * max_affordable_quantity
        points = max(profit_margin, 0)

        max_points = 100
        points = (points / max_points) * 100

        return round(points, 1)
    except KeyError:
        return 0

# In the update_prices function, update the first buy and sell prices
def update_prices():
    global prices_data, last_updated
    try:
        response = requests.get(f"https://api.hypixel.net/skyblock/bazaar?key={API_KEY}").json()
        if response["success"]:
            last_updated = response["lastUpdated"]
            products = response["products"]
            max_points = 0

            for product_id, product in products.items():
                points = calculate_points(product, current_balance)
                max_points = max(max_points, points)
                product['points'] = points

                product['product_id'] = format_item_name(product['product_id'])

                # Update the first buy and sell prices
                if 'buy_summary' in product and len(product['buy_summary']) > 0:
                    product['first_buy_price'] = product['buy_summary'][0]['pricePerUnit']
                else:
                    product['first_buy_price'] = 0

                if 'sell_summary' in product and len(product['sell_summary']) > 0:
                    product['first_sell_price'] = product['sell_summary'][0]['pricePerUnit']
                else:
                    product['first_sell_price'] = 0

                # Filter out items where the buy difference is more than double the sell price
                if 'first_buy_price' in product and 'first_sell_price' in product:
                    if product['first_sell_price'] != 0:
                        buy_sell_ratio = product['first_buy_price'] / product['first_sell_price']
                        if buy_sell_ratio > 2:
                            product['points'] = 0
                    else:
                        product['points'] = 0

            if max_points > 0:
                for product in products.values():
                    product['points'] = (product['points'] / max_points) * 100

            prices_data = products
        else:
            print("Failed to fetch prices data from the server.")
    except Exception as e:
        print("An error occurred:", e)



# Initial update on server start
update_prices()


@app.route('/')
def index():
    filtered_prices_data = {item_id: product for item_id, product in prices_data.items() if item_id in item_ids}
    return render_template('index.html', item_ids=item_ids, prices_data=filtered_prices_data, last_updated=last_updated)


@app.route('/get_prices/<item_id>')
def get_prices_route(item_id):
    prices = prices_data.get(item_id, {})
    return jsonify(prices)


@app.route('/get_all_prices')
def get_all_prices():
    return jsonify(prices_data)


@app.route('/refresh_prices')
def refresh_prices():
    update_prices()

    # Reapply the filter to the updated data
    filtered_prices_data = {item_id: product for item_id, product in prices_data.items() if item_id in item_ids}

    # Format the last_updated timestamp using the datetime_format filter
    formatted_last_updated = datetime_format(last_updated, format='%Y-%m-%d %H:%M:%S')

    return jsonify({
        'success': True,
        'prices_data': filtered_prices_data,
        'last_updated': formatted_last_updated  # Use the formatted timestamp
    })


if __name__ == '__main__':
    app.run(port=5001, debug=True)
