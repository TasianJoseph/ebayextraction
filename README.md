# eBay Fashion Brands Tracker: Designer vs Streetwear.
* Automated ETL pipeline using 2 eBay APIs to track active and sold listing prices for designer and streetwear brands on eBay GB.

## The Project:
I've created this project because I'm interested in fashion and especially the resale behaviours for designer and streetwear brands given the [UK's pre-loved fashion market] (https://www.businessoffashion.com/news/sustainability/uk-second-hand-shopping-to-top-6-billion-this-year/) was valued at £4.3 billion in 2024! 

Workflow of the eBay API Data:

'single responsibility principle'

api.py — only fetches raw data, knows nothing about transformation
transform.py — only shapes data, knows nothing about the API or database
load.py — only inserts data, knows nothing about eBay or transformations
main.py — orchestrates all three in sequence

