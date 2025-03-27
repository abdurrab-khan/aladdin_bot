from .lib import WEB_URLS, PRODUCT_CATEGORY, MAX_PRODUCTS, ProductSearchResult, Utils


def main():
    """
    Main function of the application that is called when the application is run.
    """
    all_products = {}

    for url in WEB_URLS:
        for category in PRODUCT_CATEGORY:
            page = 1

            while True:
                try:
                    if all_products.get(category) and len(all_products[category]) >= MAX_PRODUCTS:
                        break

                    search_result: ProductSearchResult = Utils.get_products_from_web(
                        url.format(page_number=page, category=category))

                    if search_result.is_last_page or not search_result.products or not search_result:
                        break

                    if not all_products.get(category):
                        all_products[category] = search_result.products
                    else:
                        all_products[category].extend(search_result.products)

                    page += 1
                except Exception as e:
                    print(f"Error: {e}")
                    continue

    for category in all_products:
        products = all_products[category]
        sorted_products = Utils.sort_products(products)
        filtered_products = Utils.filter_products(sorted_products)

        for product in filtered_products:
            if product is None:
                return

            image_path = Utils.download_images(product)

            if not image_path or not image_path[0]:
                continue

            Utils.send_telegram_message(product, image_path)
            Utils.send_twitter_message(product, image_path)


if __name__ == "__main__":
    main()
