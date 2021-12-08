from public.image import Items

_item1 = {
    'id': 'Eq0',
    'name': '彻甲榴爆弹机炮',
    'raw name': 'Penetrator',
    'category': 'equipment',
    'max_obtain': 2,
    'max_hold': 2,
    'group_limit': 1,
    'info': '子弹可穿透路径上多个敌人，并且带有小范围爆炸效果',
    'durability': 1.0,
    'price': 1050,
    'image': Items.equipments[0],
}

_item2 = {
    'id': 'Eq1',
    'name': '热源感应追踪飞弹',
    'raw name': 'Heat-seeking Missile',
    'category': 'equipment',
    'max_obtain': 2,
    'max_hold': 2,
    'group_limit': 1,
    'info': '可发射追踪导弹，导弹必定命中目标，无目标时无法使用，一次性发射四发导弹，发射有两秒冷却时间',
    'durability': 0.75,
    'price': 1300,
    'image': Items.equipments[1],
}

_item3 = {
    'id': 'Ch0',
    'name': '军工部的合金补给',
    'raw name': 'Metal Supply',
    'category': 'chest',
    'max_obtain': -1,
    'max_hold': 50,
    'group_limit': 1,
    'info': '军工部下发的合金箱，来看看今天发了什么吧',
    'durability': -1,
    'price': 100,
    'image': Items.chests[0],
}

# my_items = [_item1, _item2, _item3]

my_items = []
for i in range(5):
    item = {'category': 'equipment', 'image': Items.equipments[i], 'test': i}
    my_items.append(item)

for i in range(6):
    item = {'category': 'material', 'image': Items.metals[i]}
    my_items.append(item)

for i in range(4):
    item = {'category': 'chest', 'image': Items.chests[i]}
    my_items.append(item)

# for item in my_items:
#     print(item)
