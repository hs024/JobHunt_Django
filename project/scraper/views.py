from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from .models import JobListing
from .scrapers import run_scrapers
from django.contrib.auth.hashers import check_password ,make_password
from .models import userModel  

def job_list(request):
    INDIAN_PLATFORMS = [
        'Naukri', 
        'Indeed India', 
        'LinkedIn India',
        'Internshala'
    ]
    
    # Always show some jobs (last 100 active ones)
    jobs = JobListing.objects.filter(
        is_active=True,
        source__in=INDIAN_PLATFORMS
    ).order_by('-posted_date')[:100]  # Limit to 100 most recent
    
    if request.method == 'POST':
        search_term = request.POST.get('search_term', '').strip()
        location = request.POST.get('location', 'India').strip()
        
        if search_term:
            try:
                # Run scrapers
                scraped_jobs = run_scrapers(search_term, location)
                messages.success(request, f"Scraped {len(scraped_jobs)} new jobs!")
                
                # Update queryset with filtered results
                jobs = JobListing.objects.filter(
                    is_active=True,
                    source__in=INDIAN_PLATFORMS,
                    title__icontains=search_term,
                    location__icontains=location
                ).order_by('-posted_date')
                
                if not jobs.exists():
                    messages.info(request, "No matching jobs found. Showing recent jobs instead.")
                    jobs = JobListing.objects.filter(
                        is_active=True,
                        source__in=INDIAN_PLATFORMS
                    ).order_by('-posted_date')[:100]
                    
            except Exception as e:
                messages.error(request, f"Scraping failed: {str(e)}")
    
    return render(request, 'scraper/job_list.html', {
        'jobs': jobs,
        'platforms': INDIAN_PLATFORMS
    })

# Add this missing view function
def job_detail(request, pk):
    job = get_object_or_404(JobListing, pk=pk)
    return render(request, 'scraper/job_detail.html', {'job': job})

def userlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = userModel.objects.get(username=username)
        except userModel.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("login")  

        if check_password(password, user.password):
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            messages.success(request, "Login successful!")
            return redirect("job_list") 
        else:
            messages.error(request, "Invalid password.")
            return redirect("login")

    return render(request, 'scraper/userLogin.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))

        userModel.objects.create(username=username, email=email, password=password)
        messages.success(request, "Registration successful!")
        return redirect("login")
    
    return render(request, 'scraper/register.html')