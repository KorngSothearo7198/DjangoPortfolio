

from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import ChatMessage, ContactInfo, Profile, Project, ProjectCategory, TechStack, SkillCategory, Skill, ToolCategory
from .forms import ContactForm
from django.contrib import messages


def index(request):
    # Active profile
    profile = Profile.objects.filter(is_active=True).first()
    contact_info = ContactInfo.objects.filter(is_active=True).first()


    # Tech stacks
    tech_stacks = profile.tech_stacks.all().order_by('order') if profile else []

    # Skills grouped by category (technical, professional, etc.)
    skill_categories = SkillCategory.objects.all().order_by('order')
    skills_by_category = {}
    if profile:
        for category in skill_categories:
            skills = profile.skills.filter(category=category).order_by('order')
            skills_by_category[category.slug] = skills

    # Tools grouped by category
    tool_categories = ToolCategory.objects.all().order_by('order')
    tools_by_category = {}
    if profile:
        for category in tool_categories:
            tools = profile.tools.filter(category=category)
            tools_by_category[category.name] = tools

    # Convert dict to items for template iteration
    tools_by_category_items = tools_by_category.items()


    tool_categories = ToolCategory.objects.all().order_by('order')
    tools_by_category_list = []
    if profile:
        for category in tool_categories:
            tools = profile.tools.filter(category=category)
            tools_by_category_list.append((category, tools))



    # Projects grouped by categories
    project_categories = ProjectCategory.objects.all().order_by('id')  # for filter buttons
    projects = Project.objects.filter(profile=profile, is_active=True).order_by('order')

    # Optional: Prepare a dict mapping project categories to projects
    projects_by_category = {}
    for category in project_categories:
        # Get projects in this category
        projects_in_category = projects.filter(category=category)
        projects_by_category[category.slug] = projects_in_category



    # Contact form
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            obj = form.save()
            print("SAVED:", obj)
            messages.success(request, "Your message has been sent successfully!")
            return redirect('index')
        else:
            print(form.errors)




    context = {
        'profile': profile,
        'tech_stacks': tech_stacks,
        'skill_categories': skill_categories,
        # 'skills_by_category': skills_by_category,
        'skills_by_category': skills_by_category.items(),  # pass items()

        'tool_categories': tool_categories,
        'tools_by_category': tools_by_category,
        'tools_by_category_items': tools_by_category_items,  # use items

        'tools_by_category_list': tools_by_category_list,



        'projects': projects,  # all projects
        'project_categories': project_categories,  # for filter buttons
        'projects_by_category': projects_by_category,  # optional dict


        'form': form,
        'contact_info': contact_info,
    }
    return render(request, 'portfolio/base.html', context)




# views.py - Enhanced Chatbot View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import ChatMessage
import json
from datetime import datetime

def chatbot_view(request):
    if request.method == "POST":
        try:
            user_msg = request.POST.get('message', '').strip()
            
            if not user_msg:
                return JsonResponse({'message': 'Please type a message.', 'type': 'error'})
            
            # Save user message
            ChatMessage.objects.create(sender='user', message=user_msg)
            
            # Process user message and generate bot reply
            bot_reply = process_user_message(user_msg)
            
            # Save bot message
            ChatMessage.objects.create(sender='bot', message=bot_reply)
            
            return JsonResponse({
                'message': bot_reply,
                'type': 'text',
                'timestamp': timezone.now().strftime('%I:%M %p')
            })
            
        except Exception as e:
            return JsonResponse({
                'message': 'Sorry, I encountered an error. Please try again.',
                'type': 'error'
            })
    
    # GET request → load page with history
    chat_history = ChatMessage.objects.all().order_by('created_at')[:50]
    return render(request, 'portfolio/chatbot.html', {'chat_history': chat_history})

def process_user_message(user_msg):
    """
    Process user message and return appropriate bot response
    """
    message = user_msg.lower().strip()
    
    # Greetings and introductions
    greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    if any(greet in message for greet in greetings):
        return get_greeting_response()
    
    # Identity questions
    identity_patterns = {
        'who are you': "I'm an AI assistant created to help you with various tasks. You can think of me as your virtual helper! 🤖",
        'what is your name': "I don't have a specific name, but you can call me Assistant or AI Helper! What would you like to call me?",
        'what are you': "I'm an artificial intelligence chatbot designed to assist users like you with questions, information, and conversation.",
        'what about you': "I'm here to help! I can answer questions, provide information, and have conversations. What would you like to know about me?",
        'your name': "You can call me Assistant! I'm your AI helper. 😊",
        'what should i call you': "You can call me Assistant, ChatBot, or whatever name you prefer! I'm here to help.",
        'introduce yourself': "Hello! I'm an AI assistant designed to help users with information, answer questions, and provide assistance. Nice to meet you! 👋",
        'are you human': "No, I'm not human. I'm an artificial intelligence program created to assist users like you! 🤖",
        'are you real': "I'm a real AI assistant, though I exist as software rather than a physical being. I'm here to genuinely help you!",
        'what can you do': "I can help you with many things! Here are some examples:\n• Answer questions\n• Provide information\n• Have conversations\n• Help with tasks\n• Give suggestions\n\nWhat would you like help with?",
    }
    
    for pattern, response in identity_patterns.items():
        if pattern in message:
            return response
    
    # Common questions and conversation
    if 'how are you' in message:
        return "I'm doing great, thank you for asking! How about you? 😊"
    
    if 'thank you' in message or 'thanks' in message:
        return "You're welcome! Is there anything else I can help you with? 😊"
    
    if 'goodbye' in message or 'bye' in message or 'see you' in message:
        return "Goodbye! Feel free to come back anytime if you need help. Have a great day! 👋"
    
    if 'help' in message:
        return "Sure, I'd be happy to help! What do you need assistance with? You can ask me about:\n• General information\n• Explanations\n• Suggestions\n• Or just chat with me!"
    
    if 'what time' in message or 'what is the time' in message:
        current_time = datetime.now().strftime('%I:%M %p')
        return f"The current time is {current_time}. What else can I help you with?"
    
    if 'what date' in message or 'what is today' in message:
        current_date = datetime.now().strftime('%B %d, %Y')
        return f"Today is {current_date}. Is there anything specific you'd like to know?"
    
    if 'how old are you' in message:
        return "As an AI, I don't have an age in the human sense. I exist to help you whenever you need! 💫"
    
    if 'where are you from' in message:
        return "I exist in the digital world! I was created to be accessible from anywhere to help users like you. 🌐"
    
    if 'do you have feelings' in message:
        return "I don't have feelings like humans do, but I'm designed to understand and respond to emotions in a helpful way. How are you feeling today?"
    
    if 'can you learn' in message:
        return "I can process and remember information from our conversation, but I don't learn in the same way humans do. Each conversation helps me assist you better though!"
    
    # Knowledge questions
    knowledge_responses = {
        'what is ai': "Artificial Intelligence (AI) refers to computer systems designed to perform tasks that normally require human intelligence, like understanding language or recognizing patterns.",
        'what is machine learning': "Machine Learning is a subset of AI where computers learn from data without being explicitly programmed for each task.",
        'tell me about yourself': "I'm an AI assistant with the goal of being helpful, harmless, and honest. I'm here to answer questions, provide information, and assist you with various tasks!",
        'what is your purpose': "My purpose is to assist users by providing helpful information, answering questions, and making tasks easier through conversation.",
        'who created you': "I was created by developers using artificial intelligence technologies to build helpful assistant tools.",
        'what is chatgpt': "ChatGPT is an AI language model developed by OpenAI that can understand and generate human-like text based on the input it receives.",
        'how do you work': "I work by processing your input, understanding the context, and generating relevant responses based on patterns and information I've been trained on.",
    }
    
    for pattern, response in knowledge_responses.items():
        if pattern in message:
            return response
    
    # Small talk and casual conversation
    small_talk = {
        'nice to meet you': "Nice to meet you too! How can I assist you today? 😊",
        'i am fine': "That's great to hear! What can I help you with today?",
        'i am good': "Awesome! I'm here if you need anything. Just let me know!",
        'what is up': "Not much! Just here and ready to help. What's up with you? 😄",
        'how is your day': "My day is always good when I get to help users like you! How's your day going?",
        'i need help': "I'm here to help! Please tell me what you need assistance with, and I'll do my best. 🤗",
        'i have a question': "I'd be happy to answer your question! What would you like to know?",
        'tell me a joke': "Why don't scientists trust atoms? Because they make up everything! 😄 Want to hear another?",
        'tell me something interesting': "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat!",
        'what is the meaning of life': "That's a deep question! Many people believe life's meaning comes from relationships, experiences, growth, or helping others. What do you think gives life meaning?",
    }
    
    for pattern, response in small_talk.items():
        if pattern in message:
            return response
    
    # Questions about capabilities
    if 'can you' in message:
        capabilities = [
            "Can I answer questions? Yes, I can!",
            "Can I help with information? Absolutely!",
            "Can I provide suggestions? Sure thing!",
            "Can I have conversations? Definitely!",
            "Can I assist with tasks? I'll do my best!",
        ]
        
        for capability in capabilities:
            if capability.lower() in message:
                return "Yes, I can! What specifically would you like me to help with?"
        
        return "Yes, I can help with many things! What specifically would you like me to do? I can answer questions, provide information, help with tasks, or just chat!"
    
    # Default responses for unknown queries
    default_responses = [
        "That's an interesting question! Could you rephrase it or ask me something else?",
        "I'm not sure I understand. Could you try asking in a different way?",
        "I'm still learning! Could you ask me something else or rephrase your question?",
        "That's beyond my current capabilities, but I'd be happy to help with other questions!",
        "I don't have enough information about that. Could you ask me something else?",
        "Let me think about that... Actually, could you try asking something different? I'm better at answering specific questions!",
    ]
    
    # Check if it's a question (ends with ? or starts with question words)
    is_question = message.endswith('?') or any(
        message.startswith(word) for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'do', 'does', 'is', 'are']
    )
    
    if is_question:
        return "That's a good question! I'm still learning and might not have all the answers, but I'll do my best to help with what I know. Could you try asking something else?"
    
    # For statements or unclear input
    return "I see! Could you tell me more about what you're looking for, or ask me a specific question?"

def get_greeting_response():
    """Return time-appropriate greeting"""
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "Good morning! ☀️ I'm your AI assistant. How can I help you today?"
    elif 12 <= current_hour < 17:
        return "Good afternoon! 🌤️ I'm here to assist you. What can I do for you?"
    elif 17 <= current_hour < 22:
        return "Good evening! 🌙 Welcome! How may I assist you today?"
    else:
        return "Hello! 🌜 I'm available to help you. What can I do for you?"




# views.py
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import ChatMessage

# def chatbot_view(request):
#     if request.method == "POST":
#         user_msg = request.POST.get('message')
#         if user_msg:
#             # Save user message
#             ChatMessage.objects.create(sender='user', message=user_msg)

#             # Bot logic (សាមញ្ញសម្រាប់ example)
#             if 'hello' in user_msg.lower():
#                 bot_reply = "Hello! How can I help you?"
#             elif 'help' in user_msg.lower():
#                 bot_reply = "Sure! Ask me anything."
#             else:
#                 bot_reply = "I'm a bot 🤖, I can't understand that."

#             # Save bot message
#             ChatMessage.objects.create(sender='bot', message=bot_reply)

#             return JsonResponse({'message': bot_reply})

#     # GET request → load page with history
#     chat_history = ChatMessage.objects.all().order_by('created_at')
#     return render(request, 'portfolio/chatbot.html', {'chat_history': chat_history})
