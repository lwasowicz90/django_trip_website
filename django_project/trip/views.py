from django.shortcuts import render
# Create your views here.

offers = [
    {
        'country': 'Polska',
        'detailed_location': 'Wrocław',
        'from_date': 'August 10, 2020',
        'to_date': 'August 20, 2020',
        'price': '1200',
        'hotel_stars': 4
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1800',
        'hotel_stars': 3
    }
]

def home(request):
    context = {
        'offers': offers,
    }
    return render(request,'trip/home.html', context)

def about(request):
    return render(request,'trip/about.html', {'title': 'About'})