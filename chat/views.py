from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage

def chatbot_page(request):
    """Render the page with chatbot"""
    print("Chatbot page accessed")  # Log when page is loaded
    return render(request, 'portfolio/includes/chatbot.html')  # Your main page

def send_chat_message(request):
    """Handle AJAX POST messages"""
    if request.method == "POST":
        name = request.POST.get('name', 'Guest')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        print(f"Received message from {name} ({email}): {message}")  # Log incoming message

        if message:
            chat = ChatMessage.objects.create(name=name, email=email, message=message)

            print(f"Saved message to DB: {chat}")  # Log saved message

            response = {
                'status': 'success',
                'message': chat.message,
                'created_at': chat.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'name': chat.name
            }

            print(f"Sending response: {response}")  # Log outgoing response
            return JsonResponse(response)

    print("Invalid request received")  # Log if request is not POST or message empty
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
