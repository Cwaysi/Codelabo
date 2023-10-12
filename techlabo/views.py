from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from . forms import *
from django.db.models import Q, Max, F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .SMS import send_message

"""
    managing all project posts, request, and cofounders managament
"""



def login_view(request):
    """
    user login function to check if user is already 
    logged in to be directed to home page
    """
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')  # Replace 'home' with the URL name of your home page
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')  # Replace 'login.html' with the path to your login template


def logout_view(request):
    """
    user logout view function
    """
    logout(request)
    return redirect('login') 


class SignUpView(View):
    """
    class to sign or register user into the system
    """
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Saving the user instance
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('usercomp')
        return render(request, 'registration/signup.html', {'form': form})

# user profile completion
@login_required(login_url="/")
def usercomp (request):
    """
    function to check if user has completed the 
    userprofile, if not the userprofile form will be opened
    to be completed
    """
    try:
        ext = UserProfile.objects.get(user=request.user)
        return redirect('home')
    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user 
                profile.save()
                return redirect('home')
        else:
            form = UserProfileForm()
        context = {
            'form': form
        }
        return render(request, 'usercomp.html', context)
        
        
#Home view
@login_required(login_url="/")
def home(request):
    """ 
    home view to list all projects, and make request as a cofounder
    """
    projects = Project.objects.all().order_by('-date_updated')
    
    #checking if request has been made by current user
    project_requests = ProjectRequest.objects.filter(user=request.user)
    req_made = set(request.project.id for request in project_requests)

    searchquery = request.GET.get('q')
    #search query lookup
    if searchquery:
        # Filter products that contain the search query in their name, description or category
        projects = Project.objects.filter(
            Q(title__icontains=searchquery) |
            Q(description__icontains=searchquery) |
            Q(industry__icontains=searchquery) |
            Q(tech_stack_needed__name__icontains=searchquery)
        ).order_by('-date_updated')
        projects = projects.annotate(
            max_id=Max('id')
        ).filter(
            id=F('max_id')
        )
        
        # request form
    form = RequestForm()
    context= {
        'form': form,
        'projects':projects,
        'req_made': req_made,
    }
    return render (request, 'home.html', context)


#Save request from home
def request (request, id):
    """ 
    saving cofounding requests made
    """
    project = Project.objects.get(pk=id)
    print(project)
    if request.method == 'POST':
        print('posted')
        form = RequestForm(request.POST)
        if form.is_valid():
            print('valid')
            msg = form.cleaned_data.get('message')
            print(msg)
            requestt = ProjectRequest()
            requestt.user = request.user
            requestt.message = msg
            requestt.project = project
            requestt.save()
            return redirect('home')
        else:
            print(form.errors)

#edit profile
@login_required(login_url="/")
def editprofile(request, id):
    """ 
    user editing his/her profile
    """
    try:
        pro = UserProfile.objects.get(user=id)
        form = UserProfileForm(request.POST or None, instance=pro)
        if request.method == 'POST':
            form = UserProfileForm(request.POST or None, instance=pro)
            if form.is_valid():
                form.save()
                return redirect('posted')
            else:
                form = ProjectForm(instance=pro)
        context = {
        'form': form,
        }
        return render(request, 'editprofile.html', context)

    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user 
                profile.save()
                return redirect('home')
        else:
            form = UserProfileForm()
        context = {
            'form': form
        }
        return render(request, 'usercomp.html', context)

# View a founders profile
@login_required(login_url="/")
def fprofile (request, id):
    """ Viewing a user's profile """
    usr = User.objects.get(pk=id)
    try:
        profile = UserProfile.objects.get(user=usr)
        form = MessageForm(request.POST)
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.user = request.user 
                message.to = usr
                message.save()
                msg = str(form.cleaned_data.get('message'))
                sender = str(request.user.first_name + ", " + request.user.last_name)
                send_message(str(profile.phone), msg, sender )
                messages.success(request, 'Message sent successfully!')
                form = MessageForm(request.POST)
                #return redirect('home')
        context= {
            'form':form,
            'profile': profile,
        }
        return render (request, 'founderprofile.html', context)
    except UserProfile.DoesNotExist:
        return redirect('posted')
    
        
#all posted projects of current users
@login_required(login_url="/")
def posted(request):
    """
    get all projects posted by current user
    """
    projects = Project.objects.filter(founder=request.user).order_by('-date_updated')
    current_user = request.user
    print(current_user.first_name)

    # Print cofounders for each project
    projects_with_cofounders = []
    for project in Project.objects.filter(founder=current_user):
        cofounders_instance = Cofounders.objects.filter(project=project).first()
        cofounders = cofounders_instance.co_founders.all() if cofounders_instance else []
        projects_with_cofounders.append({'project': project, 'cofounders': cofounders})

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.founder = request.user  # Setting the founder user to the current user
            project.save()
            return redirect('posted')
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'projects': projects,
        'projects_with_cofounders': projects_with_cofounders,
    }
    return render(request, 'posted.html', context)

#edit profile
@login_required(login_url="/")
def editproject(request, id):
    """ 
    making changes to a posted project
    """
    pro = get_object_or_404(Project, id=id)
    form = ProjectForm(request.POST or None, instance=pro)
    if request.method == 'POST':
        form = ProjectForm(request.POST or None, instance=pro)
        if form.is_valid():
            form.save()
            return redirect('posted')
        else:
            form = ProjectForm(instance=pro)
    context = {
        'form': form,
    }
    return render(request, 'editproject.html', context)


@login_required(login_url="/")
def deleteproject(request, id):
    """ 
    delete a posted project
    """
    project = get_object_or_404(Project, id=id)
    project.delete()
    return redirect('posted')


@login_required(login_url="/")
def requestreceive (request):
    """
    get all request to current user's projects
    """
    req = ProjectRequest.objects.filter(project__founder=request.user).order_by('-date_updated')
    context = {
        'req': req,
    }
    return render(request, 'requestreceive.html', context)


@login_required(login_url="/")
def accept(request, id):
    """
    function to accept a cofounder to be a part of a project
    """
    req = get_object_or_404(ProjectRequest, pk=id)
    if req.is_accepted:
        return redirect('requestreceive')
    req.is_accepted = True
    req.save()

    # Adding the user to co_founders
    cofounders, created = Cofounders.objects.get_or_create(project=req.project)
    cofounders.co_founders.add(req.user)

    return redirect('requestreceive')

@login_required(login_url="/")
def withdraw(request, id):
    """
    function to redraw a cofounder from a project
    """
    req = get_object_or_404(ProjectRequest, pk=id)

    if not req.is_accepted:
        # Request is not accepted
        return redirect('requestreceive')

    req.is_accepted = False
    req.save()

    # Removing the user from co_founders
    cofounders = Cofounders.objects.get(project=req.project)
    cofounders.co_founders.remove(req.user)

    return redirect('requestreceive')

@login_required(login_url="/") 
def cofounding(request):
    """
    Retrieve all projects where the current user is a co-founder by
    using the values('project') to retrieve the project ids
    """ 
    cofounding_projects = Cofounders.objects.filter(co_founders=request.user).values('project')
    projects = Project.objects.filter(id__in=cofounding_projects)

    context = {
        'projects': projects,
    }

    return render(request, 'cofounding.html', context)

@login_required(login_url="/") 
def messag(request):
    """ 
    get all the current user's messages
    """
    usr = request.user
    msg = Message.objects.filter(to = usr).order_by('-date_created')
    context = {
        'msg': msg
    }
    return render (request, 'message.html', context)