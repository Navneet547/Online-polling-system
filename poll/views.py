from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from poll.models import *
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
class Poll_list(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self,request):
        all_polls = Poll.objects.all()
        search_term = ''
        if 'name' in request.GET:
            all_polls = all_polls.order_by('text')

        if 'date' in request.GET:
            all_polls = all_polls.order_by('-pub_date')

        if 'vote' in request.GET:
            all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

        if 'search' in request.GET:
            search_term = request.GET['search']
            all_polls = all_polls.filter(text__icontains=search_term)

        paginator = Paginator(all_polls, 4) 
        page = request.GET.get('page')
        polls = paginator.get_page(page)

        get_dict_copy = request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

        context = {
            'polls': polls,
            'params': params,
            'search_term': search_term,
        }
        print(polls)
        return render(request,'poll-list.html',context)
    
class Add_poll(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self,request):
        return render(request,'add-poll.html')
    def post(self, request):
        owner = request.user
        text = request.POST.get('text')
        poll = Poll(owner=owner, text=text)
        poll.save()
        choice1 = request.POST.get('choice1')
        choice2 = request.POST.get('choice2')
        choice3 = request.POST.get('choice3')
        choice4 = request.POST.get('choice4')
        Choice(poll=poll, choice_text=choice1).save()
        Choice(poll=poll, choice_text=choice2).save()
        Choice(poll=poll, choice_text=choice3).save()
        Choice(poll=poll, choice_text=choice4).save()
        return redirect("poll:poll-list")

    
class Poll_Details(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self, request, poll_id, *args, **kwargs):
        poll = get_object_or_404(Poll, id=poll_id)
        if not poll.active:
          return redirect('poll:poll-result', poll_id=poll.id)

        loop_count = poll.choice_set.count()
        context = {
            'poll': poll,   
            'loop_time': range(0, loop_count),
        }
        return render(request, 'poll-details.html', context)
    
    def post(self, request,poll_id,*args,**kwargs):
        poll = get_object_or_404(Poll, pk=poll_id)
        choice_id = request.POST.get('choice')
        if not poll.user_can_vote(request.user):
            messages.error( request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
            return redirect("poll:poll-list")

        if choice_id:
            choice = Choice.objects.get(id=choice_id)
            vote = Vote(user=request.user, poll=poll, choice=choice)
            vote.save()
            print(vote)
            return render(request, 'poll-result.html', {'poll': poll})
        else:
            messages.error(request, "No choice selected!", extra_tags='alert alert-warning alert-dismissible fade show')
            return redirect("poll:poll-details", poll_id)
    
class End_Poll(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self, request, poll_id, *args, **kwargs):
        poll = get_object_or_404(Poll, id=poll_id)
        if request.user != poll.owner:
            return redirect('home')

        if poll.active is True:
            poll.active = False
            poll.save()
            return redirect('poll:poll-list')
        else:
            return render(request, 'poll-list.html', {'poll': poll})
        
class Poll_Edit(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self, request,poll_id,*args,**kwargs):
        poll=get_object_or_404(Poll,id=poll_id)
        return render(request,'poll-edit.html',{'poll':poll})
    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        poll.text = request.POST.get('text')
        poll.active = request.POST.get('active', False) == 'on'
        poll.save()
        return redirect('poll:poll-list')
    
class Poll_delete(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self, request,poll_id,*args,**kwargs):
        poll=get_object_or_404(Poll,id=poll_id)
        poll.delete()
        messages.success(request, f"Poll \"{poll.text}\" is deleted successfully.",extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('poll:poll-list')
    
class Choice_edit(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self, request,choice_id,*args,**kwargs):
        choice = get_object_or_404(Choice, pk=choice_id)
        poll = get_object_or_404(Poll, pk=choice.poll.id)
        if request.user != poll.owner:
            return redirect('home')
        return render(request,'choice-edit.html',{'choice':choice})

    def post(self, request, choice_id, *args, **kwargs):
        choice = get_object_or_404(Choice, pk=choice_id)
        poll = get_object_or_404(Poll, pk=choice.poll.id)
        
        # Check if the logged-in user is the owner of the poll
        if request.user != poll.owner:
            return redirect('home')

        # Update the choice with the new data from the POST request
        choice_text = request.POST.get('choice1')
        choice.choice_text = choice_text
        choice.save()

        # Redirect to a success page or display a success message
        messages.success(request, "Choice updated successfully.", extra_tags='alert alert-success alert-dismissible fade show')
        return redirect('poll:poll-edit', poll_id=poll.id)


class Poll_result(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self, request,poll_id,*args,**kwargs):
        # Retrieve the poll object based on the poll_id
        poll = get_object_or_404(Poll, id=poll_id)

        # Retrieve the votes for the poll
        votes = Vote.objects.filter(poll=poll)

        return render(request, 'poll-result.html', {'poll': poll, 'votes': votes})