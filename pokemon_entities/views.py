import folium
import json
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon
from django.utils.timezone import localtime, now
from django.shortcuts import get_object_or_404

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


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
    time_now = localtime(now())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=10)
    for pokemon_db in Pokemon.objects.filter(pokemon_entities__appeared_at__lte=time_now, pokemon_entities__disappeared_at__gte=time_now):
        add_pokemon(folium_map, pokemon_db.pokemon_entities.lat, pokemon_db.pokemon_entities.lon, f"{request.build_absolute_uri('/media/')}{pokemon_db.photo}")

    pokemons_on_page = []
    for pokemon_db in Pokemon.objects.all():
        pokemons_on_page.append({
               'pokemon_id': pokemon_db.id,
               'img_url': pokemon_db.photo,
               'title_ru': pokemon_db.title,
           })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    # try:
    current_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))
    requested_pokemon = {'pokemon_id': current_pokemon.id,
                         'title': current_pokemon.title,
                         'title_en': current_pokemon.title_en,
                         'title_jp': current_pokemon.title_jp,
                         'description': current_pokemon.pokemon_entities.description,
                         'img_url': f"{request.build_absolute_uri('/media/')}{current_pokemon.photo}",
                         'entities': [{'level': current_pokemon.pokemon_entities.level, 'lat': current_pokemon.pokemon_entities.lat, 'lon': current_pokemon.pokemon_entities.lon,}],}

    if current_pokemon.evolution is None:
        requested_pokemon['previous_evolution'] = { 'title_ru': "Предок неизвестен",
                                                'pokemon_id': 0,
                                                'img_url': ''}
    else:
        requested_pokemon['previous_evolution'] = { 'title_ru': current_pokemon.evolution.title,
                                                'pokemon_id': current_pokemon.evolution.id,
                                                'img_url': f"{request.build_absolute_uri('/media/')}{current_pokemon.evolution.photo}"}

    if current_pokemon.relative.first() is None:
        requested_pokemon['next_evolution'] = { 'title_ru': "Нет потомков",
                                                    'pokemon_id': 0,
                                                    'img_url': ''}
    else:
        requested_pokemon['next_evolution'] = { 'title_ru': current_pokemon.relative.first().title,
                                                    'pokemon_id': current_pokemon.relative.first().id,
                                                    'img_url': f"{request.build_absolute_uri('/media/')}{current_pokemon.relative.first().photo}"}


    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon['entities']:
        add_pokemon(
            folium_map, pokemon_entity['lat'], pokemon_entity['lon'],
            requested_pokemon['img_url']
        )


    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
