from data.xdeals_products import XDEALS_PRODUCTS

def get_products_by_category(category):
    return [p for p in XDEALS_PRODUCTS if p["category"] == category]

def get_product_by_code(code):
    for p in XDEALS_PRODUCTS:
        if p["code"] == code:
            return p
    return None
