import os
from google import genai
from google.genai import types
from pgvector.django import CosineDistance

from products.models import Product


EMBEDDING_MODEL = "gemini-embedding-2"
CHAT_MODEL = "gemini-2.5-flash"
EMBEDDING_DIM = 768


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Chưa tìm thấy GEMINI_API_KEY trong file .env")

    print("GEMINI_API_KEY:", api_key[:10], "...")

    return genai.Client(api_key=api_key)


def embed_text(text):
    client = get_client()

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIM
        )
    )

    return result.embeddings[0].values


def search_products_by_ai(question, top_k=5):
    query_embedding = embed_text(question)

    products = (
        Product.objects
        .exclude(embedding__isnull=True)
        .annotate(distance=CosineDistance("embedding", query_embedding))
        .order_by("distance")[:top_k]
    )

    return list(products)


def ask_ai(question):
    products = search_products_by_ai(question)

    if not products:
        return "Hiện tại chưa có dữ liệu sản phẩm phù hợp. Vui lòng thử lại sau.", []

    context = ""

    for index, product in enumerate(products, start=1):
        context += f"""
        Sản phẩm {index}:
        Tên: {product.name}
        Loại: {product.category.name}
        Mô tả: {product.description}
        Thành phần: {product.ingredients}
        Hương vị: {product.taste}
        Công dụng: {product.benefit}
        Giá: {product.price} VND
        """

    prompt = f"""
    Bạn là nhân viên tư vấn của website bán trà.

    Chỉ được tư vấn dựa trên danh sách sản phẩm bên dưới.
    Không bịa sản phẩm không có trong danh sách.
    Trả lời bằng tiếng Việt, thân thiện, dễ hiểu.
    Nếu người dùng hỏi về sức khỏe, chỉ nói ở mức hỗ trợ tham khảo, không khẳng định chữa bệnh.

    Câu hỏi khách hàng:
    {question}

    Danh sách sản phẩm phù hợp:
    {context}

    Hãy tư vấn sản phẩm phù hợp nhất, giải thích lý do, và nhắc giá sản phẩm.
    """

    client = get_client()

    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=prompt
    )

    return response.text, products