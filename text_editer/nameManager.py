import re 

class NameManager:
    created_names = {
        "labelText": {
                "count": 0,
                "max": 0,
                "names": {}
            }, 
        "noteBook": {
                "count": 0, 
                "max": 0,
                "names": {}
            }, 
        "freeEdit": {
                "count": 0,
                "max": 0,
                "names": {}
            }
    }

    names_lst = []
    current_name = None 

    @classmethod
    def add_name(cls, mode):
        if mode not in cls.created_names.keys():
            return 
        
        index1 = cls.created_names[mode]['max']
        index2 = cls.created_names[mode]['count']
        if index1 >= index2:
            index = index1 + 1
        else:
            index = index2 + 1

        new_name = f'{mode}_{index}' 
        cls.current_name = new_name     # set newest name as current name
        cls.names_lst.append(new_name)
        cls.created_names[mode]["names"][index] = new_name 
        cls.created_names[mode]["count"] += 1 
        if index > cls.created_names[mode]['max']:
            cls.created_names[mode]['max'] = index 

        return new_name

    
    @classmethod
    def del_name(cls, mode, name):
        # if the name doesn't esist, stop delete operation 
        if name not in cls.created_names[mode]['names'].values():
            return 
        
        key = int(re.findall(r'\D(\d+)', name)[0])
        cls.created_names[mode]['names'].pop(key)
        cls.created_names[mode]['count'] -= 1 
        cls.names_lst.remove(name)
        cls.current_name = cls.names_lst[-1]
        if cls.created_names[mode]['count'] != 0:
            cls.created_names[mode]['max'] = max(list(cls.created_names[mode]['names']))
        else:
            cls.created_names[mode]['max'] = 0 



if __name__ == '__main__':
    NameManager.add_name('labelText')
    NameManager.add_name('labelText')
    NameManager.add_name('labelText')

    print(NameManager.created_names)

    NameManager.del_name('labelText', 'labelText_2')
    print(NameManager.created_names)

    NameManager.add_name('labelText')
    print(NameManager.created_names)

    NameManager.del_name('labelText', 'labelText_3')
    NameManager.del_name('labelText', 'laghhe_4')
    NameManager.del_name('labelText', 'labelText_4')
    NameManager.add_name('labelText')
    print(NameManager.created_names)
