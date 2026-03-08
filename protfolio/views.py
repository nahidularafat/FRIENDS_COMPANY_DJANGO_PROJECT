from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CustomUserCreationForm, ReviewForm, DeveloperForm,
    ServiceForm, BlogPostForm, ClientForm, ContactInfoForm
)
from .forms import (
    CustomUserCreationForm, ReviewForm, DeveloperForm,
    ServiceForm, BlogPostForm, ClientForm
)
from .models import Service, BlogPost, Developer, Review, Profile, Client
from .models import ContactInfo, ContactMessage
from django.contrib.auth.models import User
from .forms import ContactInfoForm
from .models import ContactInfo
# --- Decorators ---
def superadmin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'SUPERADMIN':
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap

# --- Authentication Views ---
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# --- Page Views ---
def home(request):
    services = Service.objects.all()
    clients = Client.objects.all()
    try:
        from .models import HeroSection
        hero_section = HeroSection.objects.filter(is_active=True).first()
    except ImportError:
        hero_section = None
    
    context = {
        'services': services,
        'clients': clients,
        'hero_section': hero_section,
    }
    return render(request, 'index.html', context)


def services_page(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def blog_page(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog.html', {'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_detail.html', {'post': post})

def about_us_page(request):
    developers = Developer.objects.all()
    return render(request, 'about_us.html', {'developers': developers})

def review_page(request):
    reviews = Review.objects.all().order_by('-created_at')
    form = ReviewForm()
    return render(request, 'review.html', {'reviews': reviews, 'form': form})

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_page')
    return redirect('review_page')

# --- Generic CRUD for models WITHOUT author field ---
@login_required
@superadmin_required
def create_item(request, model_form, template_name, redirect_url, item_name):
    if request.method == 'POST':
        form = model_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        form = model_form()
    return render(request, template_name, {'form': form, 'title': f'Add New {item_name}'})

@login_required
@superadmin_required
def update_item(request, pk, model_class, model_form, template_name, redirect_url):
    item = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        form = model_form(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        form = model_form(instance=item)
    item_name_display = getattr(item, 'title', getattr(item, 'name', 'Item'))
    return render(request, template_name, {'form': form, 'title': f'Edit {item_name_display}'})

@login_required
@superadmin_required
def delete_item(request, pk, model_class, template_name, cancel_url):
    item = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect(cancel_url)
    return render(request, template_name, {'object': item, 'cancel_url': cancel_url})

# --- Service CRUD ---
def service_create(request):
    return create_item(request, ServiceForm, 'generic_form.html', 'services', 'Service')

def service_update(request, pk):
    return update_item(request, pk, Service, ServiceForm, 'generic_form.html', 'services')

def service_delete(request, pk):
    return delete_item(request, pk, Service, 'confirm_delete.html', 'services')

# --- BlogPost CRUD (Special Handling for Author) ---
@login_required
@superadmin_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = BlogPostForm()
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add New Blog Post'})

def blog_update(request, pk):
    return update_item(request, pk, BlogPost, BlogPostForm, 'generic_form.html', 'blog')

def blog_delete(request, pk):
    return delete_item(request, pk, BlogPost, 'confirm_delete.html', 'blog')

# --- Developer CRUD ---
def developer_create(request):
    return create_item(request, DeveloperForm, 'generic_form.html', 'about_us', 'Developer')

def developer_update(request, pk):
    return update_item(request, pk, Developer, DeveloperForm, 'generic_form.html', 'about_us')

def developer_delete(request, pk):
    return delete_item(request, pk, Developer, 'confirm_delete.html', 'about_us')

# --- Client CRUD ---
@login_required
@superadmin_required
def client_create(request):
    return create_item(request, ClientForm, 'generic_form.html', 'home', 'Client')

@login_required
@superadmin_required
def client_update(request, pk):
    return update_item(request, pk, Client, ClientForm, 'generic_form.html', 'home')

@login_required
@superadmin_required
def client_delete(request, pk):
    return delete_item(request, pk, Client, 'confirm_delete.html', 'home')

# --- Superadmin Dashboard ---
@login_required
@superadmin_required
def dashboard(request):
    try:
        from .views import hero_section_update
    except ImportError:
        pass
    return render(request, 'dashboard/dashboard.html')

@login_required
@superadmin_required
def user_management(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        user_to_change = get_object_or_404(User, id=user_id)
        if hasattr(user_to_change, 'profile'):
            user_to_change.profile.role = new_role
            user_to_change.profile.save()
        return redirect('user_management')

    users = User.objects.all().select_related('profile')
    return render(request, 'dashboard/user_management.html', {'users': users})

# --- Hero Section Update ---
try:
    from .forms import HeroSectionForm
    from .models import HeroSection
    @login_required
    @superadmin_required
    def hero_section_update(request):
        hero_section, created = HeroSection.objects.get_or_create(is_active=True)
        return update_item(request, hero_section.pk, HeroSection, HeroSectionForm, 'generic_form.html', 'dashboard')
except (ImportError, NameError):
    pass

# --- Contact Page ---
def contact(request):
    contacts = ContactInfo.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save the message
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        # Show success message
        messages.success(request, "Your message has been sent successfully!")

        # Redirect back to contact page
        return redirect('contact')

    return render(request, 'contact.html', {'contacts': contacts})

# --- ContactInfo CRUD ---

@login_required
@superadmin_required
def contactinfo_create(request):
    return create_item(request, ContactInfoForm, 'generic_form.html', 'contact', 'Contact Info')

@login_required
@superadmin_required
def contactinfo_update(request, pk):
    return update_item(request, pk, ContactInfo, ContactInfoForm, 'generic_form.html', 'contact')

@login_required
@superadmin_required
def contactinfo_delete(request, pk):
    return delete_item(request, pk, ContactInfo, 'confirm_delete.html', 'contact')
