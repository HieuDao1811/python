from django.shortcuts import render
from .models import ChatHistory
from .services import ask_ai


def chat_view(request):
    answer = None
    question = None
    products = []

    if request.method == "POST":
        question = request.POST.get("question")
        answer, products = ask_ai(question)

        ChatHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            question=question,
            answer=answer
        )

    return render(request, "ai_chat/chat.html", {
        "question": question,
        "answer": answer,
        "products": products,
    })