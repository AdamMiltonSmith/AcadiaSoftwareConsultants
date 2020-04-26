import json

x = {
    '738':  '#ff0000',
    '700': 'ff8000',
    '1180': '#ffff00',
    '1142': '#1eff00',
    '235': '#00ff59',
    '197': '#00ffe1',
    '677': '#0084ff',
    '639': '#1900ff',
    '1119': '#9500ff',
    '1081': '#ff00cc',
}

with open('resources/colors.json', 'w') as json_f:
    json.dump(x, json_f, indent=4, sort_keys=True)
