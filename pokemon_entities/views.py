import folium
from django.shortcuts import render
from .models import PokemonEntity, Pokemon
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
        # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_on_page = []
    time_now = localtime(now())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=10)
    for pokemon_db in PokemonEntity.objects.filter(appeared_at__lte=time_now, disappeared_at__gte=time_now):
        if pokemon_db.main_pokemon:
            add_pokemon(folium_map, pokemon_db.lat, pokemon_db.lon, request.build_absolute_uri(pokemon_db.main_pokemon.photo.url))
            pokemons_on_page.append({'pokemon_id': pokemon_db.main_pokemon.id,
                                     'img_url': request.build_absolute_uri(pokemon_db.main_pokemon.photo.url),
                                     'title_ru': pokemon_db.main_pokemon.title, })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    current_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))
    requested_pokemon = {'pokemon_id': current_pokemon.id,
                         'title': current_pokemon.title,
                         'title_en': current_pokemon.title_en,
                         'title_jp': current_pokemon.title_jp,
                         'img_url': request.build_absolute_uri(current_pokemon.photo.url),
                         }
    if current_pokemon.evolution:
        requested_pokemon['previous_evolution'] = {'title_ru': current_pokemon.evolution.title,
                                                   'pokemon_id': current_pokemon.evolution.id,
                                                   'img_url': request.build_absolute_uri(current_pokemon.evolution.photo.url)}

    if current_pokemon.next_evolutions.first():
        requested_pokemon['next_evolution'] = {'title_ru': current_pokemon.next_evolutions.first().title,
                                               'pokemon_id': current_pokemon.next_evolutions.first().id,
                                               'img_url': request.build_absolute_uri(current_pokemon.next_evolutions.first().photo.url)}

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(main_pokemon=current_pokemon)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            request.build_absolute_uri(current_pokemon.photo.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
