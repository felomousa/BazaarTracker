# Hypixel Bazaar Tracker Application Overview

This document provides a comprehensive overview of the Flask web application designed to track and display price information for items from the Hypixel Bazaar in a game. The application combines Python for backend processing with an HTML template integrated with JavaScript for the frontend, aimed at enhancing user experience through intuitive data presentation and interaction.

## Application Setup and Functionality

### Flask Configuration and Custom Filters
- 🐍 Python Flask app setup with routes and Jinja2 template filters.
- 📅 Custom function `datetime_format` to format timestamps, enhancing user readability.

### API Integration and Data Processing
- 🔑 Placeholder for an API key to fetch real-time data from the Hypixel Bazaar API.
- 💰 Global variable to hold the current balance, allowing for personalized data interaction.
- 📖 Item IDs are read from a local file `item_ids.txt`, ensuring dynamic data usage.

### Data Calculation and Formatting
- 📈 Functions to calculate and format item prices, including finding maximum buy prices and minimum sell prices. Items are normalized and ranked out of 100 based on profitability and market dynamics.
- 🔄 `update_prices` function fetches the latest prices from the Hypixel API, filters items based on price ratios, and dynamically updates item rankings.

## Web Interface and User Interaction

### Flask Routes
- 🌐 Flask routes provide access to the main page, individual item prices, all item prices, and functionality for refreshing data, ensuring a comprehensive user experience.

### HTML Template and Styling
- 🖼️ The HTML template (`index.html`) features Bootstrap and custom CSS styling for a visually appealing layout.
- The interface includes buttons to toggle visibility of price information columns and a DataTable to display item prices with refresh functionality.

### JavaScript Functionality
- Dynamic DataTable initialization, column toggle, and refresh button actions allow for real-time data interaction.
- JavaScript enhances the search input styling and ensures responsive user input handling.

### External Libraries Integration
- 📚 Integration with jQuery, DataTables, and Bootstrap for frontend interactivity and enhanced user interface styling.

## Enhanced User Experience

The Hypixel Bazaar Tracker stands out by providing users with a tool that simplifies complex market data into an easily digestible format. By ranking items based on their profitability and offering a dynamic, responsive interface, it allows users to make informed trading decisions quickly. The application's tailored approach, combined with real-time data updates and customizable views, positions it as a strategic asset for gamers and traders within the Hypixel server ecosystem.
