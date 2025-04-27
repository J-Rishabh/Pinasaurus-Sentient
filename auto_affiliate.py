from amazon_paapi import AmazonApi

# Your credentials
ACCESS_KEY = "YOUR_ACCESS_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"
ASSOCIATE_TAG = "youraffiliatetag-20"
COUNTRY = "us"  # can be 'us', 'ca', 'uk', 'de', 'fr', etc.

# Initialize API
amazon = AmazonApi(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, COUNTRY)

# Search for a product by keyword
def search_and_generate_affiliate_link(keyword):
    items = amazon.search_items(keywords=keyword, item_count=1)
    
    if not items:
        return "No item found."

    item = items[0]
    title = item.title
    asin = item.asin
    url = item.detail_page_url

    return {
        "title": title,
        "ASIN": asin,
        "affiliate_url": url
    }

# Example usage
if __name__ == "__main__":
    keyword = "wireless earbuds"
    result = search_and_generate_affiliate_link(keyword)
    print(result)

