from django.shortcuts import render
# Create your views here.

offers = [
    {
        'country': 'Polska',
        'detailed_location': 'Wrocław',
        'from_date': 'August 10, 2020',
        'to_date': 'August 20, 2020',
        'price': '1200',
        'hotel_stars': 4,
        'img_url': 'http://localhost:8000/static/trip/img/services/service-1.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-1.png',
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1803',
        'hotel_stars': 3,
        'img_url': 'https://i.content4travel.com/cms/img/u/desktop/seres/tcpweka_0.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-3.png',
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1800',
        'hotel_stars': 3,
        'img_url': 'http://localhost:8000/static/trip/img/services/service-4.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-4.png',
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1800',
        'hotel_stars': 3,
        'img_url': 'http://localhost:8000/static/trip/img/services/service-3.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-3.png',
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1800',
        'hotel_stars': 3,
        'img_url': 'http://localhost:8000/static/trip/img/services/service-8.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-8.png',
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1800',
        'hotel_stars': 3,
        'img_url': 'http://localhost:8000/static/trip/img/services/service-1.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-1.png',
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1800',
        'hotel_stars': 3,
        'img_url': 'http://localhost:8000/static/trip/img/services/service-6.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-6.png',
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1800',
        'hotel_stars': 3,
        'img_url': 'http://localhost:8000/static/trip/img/services/service-4.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-4.png',
    },
    {
        'country': 'Włochy',
        'detailed_location': 'Rzym',
        'from_date': 'May 10, 2020',
        'to_date': 'May 20, 2020',
        'price': '1800',
        'hotel_stars': 3,
        'img_url': 'http://localhost:8000/static/trip/img/services/service-4.jpg',
        'img_icon_url': 'http://localhost:8000/static/trip/img/services/service-icon-4.png',
    }
]

def home(request):
    context = {
        'offers': offers,
    }
    return render(request,'trip/home.html', context)

def about(request):
    return render(request,'trip/about.html', {'title': 'About'})