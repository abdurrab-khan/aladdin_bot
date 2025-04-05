from .lib import Websites, COMMON_URLS
from .utils import Utils, get_daily_category


def main(all_website, all_category):
    """
    Main function of the application that is called when the application is run.
    """
    all_products = {}

    for web in all_website:
        for category in all_category:
            url = COMMON_URLS[web].format(category=category.value)
            print(f"URLS:: {url}")
            try:
                search_result = Utils.get_products_from_web(
                    url, web, category)

                all_products[category] = search_result
            except Exception as e:
                print(f"Error: {e}")
                continue

    print(all_products)

    for category in all_products:
        products = all_products[category]
        final_products = Utils.sort_products(products)

        for product in final_products:
            if product is None:
                return

            image_path = product['product_image']

            Utils.send_telegram_message(product, image_path)
            Utils.send_twitter_message(product, image_path)


if __name__ == "__main__":
    all_category = get_daily_category()
    # all_website = [web for web in Websites]

    # if all_category is None:
    #     exit(1)

    # main(all_website, all_category)
    print("hello world")
    print(all_category)
