import requests
from lostark_api_token import Token
from urllib import parse
import json
from LoaJWTMaker import *


headers = {
    'accept': 'application/json',
    'authorization': makeKeyFromStr(Token)
}


def get_profiles(name):
    url = 'https://developer-lostark.game.onstove.com/armories/characters/'+str(name)+'/profiles'
    response = requests.get(url, headers=headers)
    json_obj = response.json()

    # OpenAPI 에서 값을 잘 불러왔는지 확인
    print('get_profile status: '+str(response.status_code))

    if json_obj is None:
        return None

    profile = dict()
    profile['image_url'] = json_obj['CharacterImage']
    profile['status'] = dict()
    profile['tendency'] = dict()

    for d in json_obj['Stats']:
        if d['Type'] == '치명':
            profile['status']['crt'] = d['Value']
        elif d['Type'] == '특화':
            profile['status']['spc'] = d['Value']
        elif d['Type'] == '신속':
            profile['status']['swf'] = d['Value']
        elif d['Type'] == '제압':
            profile['status']['dom'] = d['Value']
        elif d['Type'] == '인내':
            profile['status']['end'] = d['Value']
        elif d['Type'] == '숙련':
            profile['status']['exp'] = d['Value']
        elif d['Type'] == '최대 생명력':
            profile['status']['hp'] = d['Value']
        elif d['Type'] == '공격력':
            profile['status']['atk'] = d['Value']

    for d in json_obj['Tendencies']:
        if d['Type'] == '지성':
            profile['tendency']['kind'] = d['Point']
        elif d['Type'] == '담력':
            profile['tendency']['cour'] = d['Point']
        elif d['Type'] == '매력':
            profile['tendency']['charm'] = d['Point']
        elif d['Type'] == '친절':
            profile['tendency']['intel'] = d['Point']

    return profile


def get_equipment(name):
    url = 'https://developer-lostark.game.onstove.com/armories/characters/'+str(name)+'/equipment'
    response = requests.get(url, headers=headers)
    json_obj = response.json()

    if json_obj is None:
        return

    # OpenAPI 에서 값을 잘 불러왔는지 확인
    print('get_equipment status: '+str(response.status_code))

    # 투구, 어깨, 상의, 하의, 장갑, 무기 순서로 list 에 저장
    temp = dict()
    equipment = list()

    for obj in json_obj:
        typename = obj['Type']
        item = obj['Name']
        items = item.split(' ')
        tooltips = json.loads(obj['Tooltip'])
        quality = tooltips['Element_001']['value']['qualityValue']
        grade = obj['Grade']
        icon = obj['Icon']
        if '+' in items[0]:
            reforge = items[0]
        else:
            reforge = ''
        while typename in temp.keys():
            typename += '1'
        temp[typename] = dict()
        temp[typename]['item'] = item
        temp[typename]['type'] = typename
        temp[typename]['quality'] = quality
        temp[typename]['grade'] = grade
        temp[typename]['icon'] = icon
        temp[typename]['reforge'] = reforge

    equipment.append(temp['투구'])
    equipment.append(temp['어깨'])
    equipment.append(temp['상의'])
    equipment.append(temp['하의'])
    equipment.append(temp['장갑'])
    equipment.append(temp['무기'])

    equipment.append(temp['목걸이'])
    equipment.append(temp['귀걸이'])
    equipment.append(temp['귀걸이1'])
    equipment.append(temp['반지'])
    equipment.append(temp['반지1'])

    return equipment
