# eBay Fashion Brands Tracker: Designer vs Streetwear.
* Automated ETL pipeline using 2 eBay APIs to track active and sold listing prices for designer and streetwear brands on eBay GB.

## The Project:
I've created this project because I'm interested in being a sustainable fashion consumer ♻️

One of the main ways to achieve this is by opting to buy second-hand clothes and using marketplaces like:
- eBay,
- Depop,
- and Vinted to do source new clothes, particularly branded items from designer and streetwear labels.

The project itself is informed by a wave of consumers like myself who have contributed to the [UK's pre-loved fashion market](https://www.businessoffashion.com/news/sustainability/uk-second-hand-shopping-to-top-6-billion-this-year/) being valued at **£4.3 billion in 2024**! 

Due to the availability APIs with marketplace data on the eBay Developers Programme, I decided that this was the most appropriate source of raw data that could be used to create a fully functional portfolio project so that I could build an automated ETL pipeline with the snapshots taken used to form an ongoing weekly comparative analysis in Tableau to create visualised dashboards.

### Tech Stack:

| **Category**      | **Technology**    |
| -----------       | -----------       |
| Language          | Python 3.12       |
| Database          | PostgreSQL        |
| Visualisation     | Tableau Public    |
| Scheduling        | Cron              |


| **Python Packages**    |                   |
| API requests           | `requests`        |
| Database connection    | `psycopg2-binary` |
| Data transformation    | `datetime`        |
| Credentials management | `json`            |

| **APIs**        |                                                              |
| Active listings | eBay Browse API v1                                           |
| Sold listings   | eBay Finding API (pending Marketplace Insights API approval) |


| API requests | `requests` |
| Database connection | `psycopg2-binary` |
| Data transformation | `datetime` |
| Credentials management | `json` |
| **APIs** | |
| Active listings | eBay Browse API v1 |
| Sold listings | eBay Finding API (pending Marketplace Insights API approval) |


