from lib.const import WEB_URLS, PRODUCT_CATEGORY, MIN_PRICE, MAX_PRICE
from lib.utils.utils import Utils
from typing import Dict, List

def main():
    """
    Main function of the application that is called when the application is run.
    """
    all_products = {}

    for url in WEB_URLS:
        for category in PRODUCT_CATEGORY:
            while True:
                try:
                    if all_products.get(category) and len(all_products[category]) >= 100:
                        break

                    web_response = Utils.get_products_from_web(url, category)
                    product = Utils.parse_html(web_response)
                    filter_product = Utils.filter_products(product)
                    evaluate_product = Utils.evaluate_products_with_ml(filter_product)
                    if not evaluate_product:
                        continue
                    
                    if category not in all_products:
                        all_products[category] = [
                            evaluate_product
                        ]
                    else:
                        all_products[category].append(evaluate_product)
                except Exception as e:
                    print(f"Error: {e}")
                    continue
 
    for category in all_products:
        products = all_products[category]
        sorted_products = Utils.sort_products(products)

        for product in sorted_products[0:3]:
            Utils.send_telegram_message(product)
            Utils.send_twitter_message(product)



if __name__ == "__main__":
    main()