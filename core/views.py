from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Item
from users.models import Conversation
from users.forms import ConversationMessageForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about.html")

def search_bar(request):
     if request.method == 'GET':
          items = Item.objects.filter(is_sold=False)
          query = request.GET.get('query')
        
          if query:
               items = items.filter(Q(name__icontains=query))

     return render(request, 'core/search.html',{'items':items, 'query':query})

def item_list(request):
     if request.method == 'GET':
        items = Item.objects.filter(is_sold=False)
        categories = Category.objects.all()  
        category_id = request.GET.get('category',0)
        if category_id: 
             items=items.filter(category_id=category_id)
       
        return render(request, "core/item_list.html", {'category':categories, 'items':items, 'category_id':int(category_id)})

def detail(request, pk):
     item=get_object_or_404(Item,pk=pk)
     return render(request, "core/detail.html", {'item':item })

@login_required
def dashboard(request):
     items = Item.objects.filter(created_by=request.user)
     return render(request, "core/dashboard.html",{
          
          "items":items
     })
    
@login_required
def delete(request, pk):
     item = get_object_or_404(Item, pk=pk, created_by=request.user)
     item.delete()

     return redirect("dashboard")

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id]) 

    return render(request, 'core/inbox.html', {'conversations':conversations})

@login_required
def inbox_convo(request,pk):
     conversation= Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
     if request.method == 'POST':
          form = ConversationMessageForm(request.POST)

          if form.is_valid():
               conversation_message = form.save(commit=False)
               conversation_message.conversation = conversation
               conversation_message.created_by = request.user
               conversation_message.save()
               conversation.save()

               return redirect('inbox_convo', pk=pk)
     else:
          form = ConversationMessageForm()

     return render(request, 'core/inbox_convo.html', {'conversation':conversation,
                                                      'form':form})
