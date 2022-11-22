# Docket Scraper

Spiders Implemented

- https://www.uniqlo.com/


## Tech Stack

1. python 3.10
1. scrapy 2.7.1
1. playwright 1.28.0


## How To Setup

#### Pre-requisites

You need to install:

1. Create a Python 3.10 virtual environment
    - `python3 -m venv /path/to/new/virtual/environment`
1. Activate the virtual environment
   - `source /path/to/new/virtual/environment/bin/activate`
1. Install requirements in the virtual environment
    - `pip install -r requirments.txt`
1. Install web drivers for Playwright
    - `playwright install`

#### How To Run Crawler
1. `scrapy crawl uniqlo -a profile_information -a product_url`
   
1. `product_url`: required argument. e.g 
   - `https://www.uniqlo.com/us/en/products/E450181-000/00?colorDisplayCode=03&sizeDisplayCode=003&pldDisplayCode=000`
   
1. `profile_information`: required argument. It contains the personal information of a user ordering the product. This information will be consumed in `checkout delivery page`.
```
For example
profile_information = {
  "first_name": "Maggie",
  "last_name": "Schultz",
  "street": "31100 Bainbridge Rd",
  "city": "Solon",
  "state_code": "OH",
  "zip_code": "44139",
  "phone": "4402489400"
}
```


### Example Command to Run the Crawler 
- `scrapy crawl uniqlo -a profile_information='{"first_name": "Maggie", "last_name": "Schultz", "street": "31100 Bainbridge Rd", "city": "Solon", "state_code": "OH", "zip_code": "44139", "phone": "4402489400"}' -a product_url='https://www.uniqlo.com/us/en/products/E450181-000/00?colorDisplayCode=03&sizeDisplayCode=003&pldDisplayCode=000'`

## Unqilo Spider Crawling Logic

- Open `Login Page` and sign in
- Open `Cart Page` and remove already added items
- Open `Product Page`
- Add the product to `cart`
- Parse and save product related information
- Open `Checkout Payment Page` and click change delivery option
- Update `Customer Delivery Details` in `Checkout Delivery Page`
- Open `Checkout Payment Page` and parse product cost, shipping and tax related information
- Merge `Product` and `Checkout Payment` information and return it

## Item Schema

```
{
  "url": string,
  "color": string,
  "size": string,
  "name": string,
  "subtotal": string,
  "shipping_cost": string,
  "estimated_tax": string,
  "total": string,
  "shipping_option": string,
  "estimated_shipping_date": string
}
```

## Challenges
- The information required to extract depends upon multiple inputs from a user
- The information required exists on different pages
- The websites are designed to prevent bots they make use of session id to prevent crawling.
  
    ---- That's why I have to make use of `Playwright` to extract data
  
- [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright) is the official plugin for Playwright integration with scrapy
    
    ---- Due to `scrapy-playwright` plugin bug I was unable to login in Uniqlo. The site was keeping me `redirecting the login page` even after getting `status code 200`
    
    ---- I found that avoiding `scrapy-playwright` plugin and using `playwright` web drivers directly solved the Login issue.
  
    ---- Here is the stackoverflow link [scrapy-playwright and playwright works differently](https://stackoverflow.com/questions/72375388/websites-using-scrapy-playwright-and-only-playwright-work-differently). The link indicates that developers are facing the similar issue I was facing using the `scrapy-playwright` plugin.
  
    ---- At the moment the crawler works only with `headless=False` option. The Uniqlo website is somehow detecting `headless=True` mode and this results in scraping failure.