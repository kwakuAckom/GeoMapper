from django.shortcuts import redirect, render
from .forms import SearchForm
from .models import Search
import folium as fl
import geocoder as gc

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()
    
    searches = Search.objects.all()
    addresses = [search.address for search in searches]
    previous_address = None
    for address in addresses:
        location = gc.osm(address)
        lat = location.lat
        lng = location.lng
        if lat is not None and lng is not None:
            break
        address.delete()    
    if lat is None or lng is None:
        address = previous_address

    m = fl.Map(location=[5.1097, -1.2826], zoom_start=10)
    fl.Marker([lat, lng], tooltip="Marker Tooltip", popup="Marker Popup").add_to(m)

    m = m._repr_html_()
    context = {
        "m": m,
        "form": form,
    }
    return render(request, 'index.html', context)
