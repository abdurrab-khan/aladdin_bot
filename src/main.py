from .lib import WEB_URLS, ProductSearchResult, Utils


def main():
    """
    Main function of the application that is called when the application is run.
    """
    all_products = {}
    product_category = ""

    for url in WEB_URLS:
        for category in product_category:
            try:
                search_result: ProductSearchResult = Utils.get_products_from_web(
                    url.format(category=category))

                all_products[category] = search_result.products
            except Exception as e:
                print(f"Error: {e}")
                continue

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
    main()
