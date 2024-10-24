# Auction Site

This project is a fully functional auction site built with Django, featuring user authentication, bidding, commenting, and watchlist management.

## Features

1. **Create Listings**: Users can create auction listings with a title, description, starting bid, image, and category.
  
2. **Active Listings**: Browse all active auctions with title, description, and current bid displayed.
   
3. **Listing Details**: View a detailed page for each listing. Users can bid, comment, and add items to their watchlist.
   
4. **Bid on Listings**: Users can place bids; the highest bidder wins when the auction closes.
   
5. **Watchlist**: Signed-in users can manage their watchlists and easily access saved auctions.
   
6. **Categories**: Browse auctions by category.
   
7. **Admin Panel**: Full control over listings, comments, and bids via Django’s admin interface.

8. **Fake Store API**: You can add dummy products using that API

## Installation

1. **Clone the Repository**:
```bash
git clone https://github.com/aegis945/e-commerce
cd e-commerce
```
2. **Create a Virtual Environment**
```bash
python -m venv venv
```
3. **Activate the Virtual Environment**:
   
  - On macOS/Linux:
```bash
source venv/bin/activate
```
  - On Windows: 
```bash
venv\Scripts\activate
```
4. **Install dependencies**:
```bash
pip install -r requirements.txt
```
5. **Run the following to create dummy data**:
```bash
python manage.py create_dummy_data
```
6. **Run dev server**:
```bash
python manage.py runserver
```
7. **Open your web browser and go to http://127.0.0.1:8000**
