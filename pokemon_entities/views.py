import folium
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)

now = timezone.localtime()

def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.select_related('subject').filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    )
    for entity in pokemon_entities:
        if entity.subject.image:
            img_url = request.build_absolute_uri(entity.subject.image.url)
        else:
            img_url = DEFAULT_IMAGE_URL

        add_pokemon(
            folium_map, 
            entity.lat,
            entity.lon,
            img_url
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else None,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    now = timezone.localtime()
    active_entities = PokemonEntity.objects.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in active_entities:
        image_url = (
            request.build_absolute_uri(pokemon.image.url) 
            if pokemon.image 
            else DEFAULT_IMAGE_URL
        )
        add_pokemon(folium_map, entity.lat, entity.lon, image_url)
    
    context = {
        'map': folium_map._repr_html_(),
        'pokemon': {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
        }
    }

    return render(request, 'pokemon.html', context)

