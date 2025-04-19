from ..lib.types import SendMessageTo

# Message templates for different platforms
# These templates are used to format the product information for sending messages.
TELEGRAM_MESSAGE_TEMPLATE = """
✨ <b>{product_name}</b> ✨

⭐ Reviews: {stars} ({product_rating})

💰 <s>₹{product_price}</s>   ➡️ <b>₹{product_discount}</b>
🔥 Save   ➡️ {product_discount_percentage}%!

<b>🛒 Grab yours now!</b>
{product_url}

{tags}
"""

MESSAGE_TEMPLATE = """✨ {product_name} ✨

💰 Price: ₹{product_price}
🔥 You save: ₹{product_discount}  ({product_discount_percentage}% OFF)
⭐ Rated {stars} ★ ({product_rating} reviews)

🛒 Ready to shop?
{product_url}

{tags}"""

MESSAGE_TEMPLATES = {
    SendMessageTo.TELEGRAM: TELEGRAM_MESSAGE_TEMPLATE,
    SendMessageTo.X: MESSAGE_TEMPLATE,
    SendMessageTo.META: MESSAGE_TEMPLATE,
}
