from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, NewItemForm, EditItemForm, ConversationMessageForm
from core.views import Item
from .models import Conversation

# Create your views here.

def register(request):
    if request.method == "POST":
     form = UserRegisterForm(request.POST)
     if form.is_valid():
        form.save()
        username = form.cleaned_data.get("username")
        messages.success(request, f"Your Account has been created, you can now Log-in")
        return redirect("login")
    else:
     form = UserRegisterForm()
    return render(request, "users/register.html", {"form":form})

@login_required
def new(request):
  page_title= "Create A New Item"
  if request.method == "POST":
     form = NewItemForm(request.POST, request.FILES)
     if form.is_valid():
      item = form.save(commit=False)
      item.created_by = request.user
      item.save()
      messages.success(request, f"You Have Successfuly Created a New Item!")
      return redirect("new")
  else:
    form = NewItemForm()
    return render(request, 'users/form.html',{
    
    'form':form,
    'page_title':page_title,

    })
  
@login_required
def edit(request,pk):
  page_title= "Edit Item"
  item= get_object_or_404(Item,pk=pk,created_by=request.user)
  if request.method == "POST":
     form = EditItemForm(request.POST, request.FILES, instance=item)
     if form.is_valid():
      form.save()
      messages.success(request, f"You Have Successfuly Edited This Item!")
      return redirect("item")
  else:
    form = EditItemForm(instance=item)
    return render(request, 'users/form.html',{
    
    'form':form,
    'page_title':page_title,
    
    })
  
@login_required
def new_conversation(request, item_pk):
  page_title = 'Start Conversation'
  item = get_object_or_404(Item, pk=item_pk)
  if item.created_by == request.user:
    return redirect('core/dashboard.html')
  conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id]) 

  if conversations:
    return redirect('inbox_convo', pk=conversations.first().id)
  if request.method == 'POST':
    form = ConversationMessageForm(request.POST)
    if form.is_valid():
      conversation = Conversation.objects.create(item=item)
      conversation.members.add(request.user)
      conversation.members.add(item.created_by)
      conversation.save()

      conversation_message = form.save(commit=False)
      conversation_message.conversation = conversation
      conversation_message.created_by = (item.created_by)
      conversation_message.save()

      return redirect('detail',pk = item_pk)
  else:
    form = ConversationMessageForm()

  return render(request, 'users/messages.html',{'form':form,
                                        'page_title':page_title,
              })

