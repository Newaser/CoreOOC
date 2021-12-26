from db.item import get_id_list, get_category_list, ItemQuery

if __name__ == '__main__':
    print(get_id_list())
    print(get_category_list())
    print(ItemQuery('Eq4'))
