from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from .models import Message
from django.views.decorators.csrf import csrf_exempt


@require_http_methods(["GET"])
def hello_world(request):
    """
    Simple Hello World endpoint that demonstrates database connectivity
    """
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_connected = True
        db_message = "Database is connected!"
    except Exception as e:
        db_connected = False
        db_message = f"Database connection error: {str(e)}"
    
    # Get message count from database
    try:
        message_count = Message.objects.count()
    except Exception:
        message_count = 0
    
    return JsonResponse({
        'message': 'Hello World from Django Backend!',
        'database_connected': db_connected,
        'database_message': db_message,
        'total_messages': message_count,
    })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def messages_view(request):
    """
    View to list all messages (GET) or create a new message (POST)
    """
    if request.method == "GET":
        messages = Message.objects.all()
        return JsonResponse({
            'count': messages.count(),
            'messages': [
                {
                    'id': msg.id,
                    'content': msg.content,
                    'created_at': msg.created_at.isoformat()
                }
                for msg in messages
            ]
        })
    
    elif request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
            content = data.get('content', '')
            
            if not content:
                return JsonResponse({'error': 'Content is required'}, status=400)
            
            message = Message.objects.create(content=content)
            return JsonResponse({
                'id': message.id,
                'content': message.content,
                'created_at': message.created_at.isoformat()
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
