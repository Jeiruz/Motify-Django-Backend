from .models import Comment

def comment_list_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    object_id = request.GET.get('id')
    return Comment.objects.filter(object_id=object_id, parent=None)[int(offset): int(offset) + int(limit)]

def is_there_more_comments(request):
    offset = request.GET.get('offset')
    object_id = request.GET.get('id')   
    if int(offset) > Comment.objects.filter(object_id=object_id, parent=None).count():
        return False
    return True


def comment_reply_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    parent_id = request.GET.get('id')
    return Comment.objects.filter(parent=parent_id)[int(offset): int(offset) + int(limit)]

def is_there_more_replies(request):
    offset = request.GET.get('offset')
    parent_id = request.GET.get('id') 
    if int(offset) > Comment.objects.filter(parent=parent_id).count():
        return False
    return True