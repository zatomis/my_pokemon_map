import folium
import json
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon
from django.utils.timezone import localtime, now

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
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_db in Pokemon.objects.all():
        if localtime(pokemon_db.appeared_at) <= time_now:
            if localtime(pokemon_db.disappeared_at) >= time_now:
                add_pokemon(folium_map, pokemon_db.coordinats.lat, pokemon_db.coordinats.lon, f"{request.build_absolute_uri()}/media/{pokemon_db.photo}")

    pokemons_on_page = []
    for pokemon_db in Pokemon.objects.all():
        pokemons_on_page.append({
               'pokemon_id': f'{pokemon_db.id}',
               'img_url': f'{pokemon_db.photo}',
               'title_ru': f'{pokemon_db.title}',
           })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        current_pokemon = Pokemon.objects.get(id=int(pokemon_id))
        requested_pokemon = {   'pokemon_id': current_pokemon.id,
                                'title_ru': f"{current_pokemon.title}",
                                'title_en': f"{current_pokemon.title_en}",
                                'title_jp': f"{current_pokemon.title_jp}",
                                'description': f"{current_pokemon.description}",
                                'img_url': f"{request.build_absolute_uri('/')[:-1]}/media/{current_pokemon.photo}",
                                'entities': [{'level': f"{current_pokemon.level}", 'lat': f"{current_pokemon.coordinats.lat}", 'lon': f"{current_pokemon.coordinats.lon}",}],}
        print("")
        if current_pokemon.next_evolution is None:
            requested_pokemon['next_evolution'] = { 'title_ru': "Нет потомка",
                                                    'pokemon_id': 0,
                                                    'img_url': ''}
            requested_pokemon['previous_evolution'] = { 'title_ru': f"{current_pokemon.previous_evolution.title}",
                                                        'pokemon_id': current_pokemon.previous_evolution.id,
                                                        'img_url': ''}

        else:
            requested_pokemon['next_evolution'] = {'title_ru': f"{current_pokemon.next_evolution.title}",
                                                   'pokemon_id': current_pokemon.next_evolution.id,
                                                   'img_url': ''}

        if current_pokemon.previous_evolution is None:
            requested_pokemon['previous_evolution'] = { 'title_ru': "Нет предка",
                                                        'pokemon_id': 0,
                                                        'img_url': ''}
            requested_pokemon['next_evolution'] = {'title_ru': f"{current_pokemon.next_evolution.title}",
                                                   'pokemon_id': current_pokemon.next_evolution.id,
                                                   'img_url': ''}

        else:
            requested_pokemon['previous_evolution'] = { 'title_ru': f"{current_pokemon.previous_evolution.title}",
                                                        'pokemon_id': current_pokemon.previous_evolution.id,
                                                        'img_url': ''}

    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon['entities']:
        add_pokemon(
            folium_map, pokemon_entity['lat'], pokemon_entity['lon'],
            requested_pokemon['img_url']
        )


    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
