from ..lib.types import SendMessageTo

TELEGRAM_MESSAGE_TEMPLATE = """
<b>{product_name}</b>\n\n⭐ Reviews: {stars} ({product_rating} Stars)\n\n💰 Price: <s>❎ ₹{product_price}</s> ➡️ <b>₹{product_discount}</b>\n🔥 Discount: Save ➡️ {product_discount_percentage}%!!\n\n
{product_url}
"""

X_MESSAGE_TEMPLATE = """
{product_name}
{product_price}
{product_discount}
{product_rating}
{product_discount_percentage}
{product_url}
"""

MESSAGE_TEMPLATES = {
    SendMessageTo.TELEGRAM: TELEGRAM_MESSAGE_TEMPLATE,
    SendMessageTo.X: X_MESSAGE_TEMPLATE,
}
