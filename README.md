

Workflow of the eBay API Data:

'single responsibility principle'

api.py — only fetches raw data, knows nothing about transformation
transform.py — only shapes data, knows nothing about the API or database
load.py — only inserts data, knows nothing about eBay or transformations
main.py — orchestrates all three in sequence

