tasks = [
    {
        'id': 1,
        'name': 'Implementar To Do APP',
        'completed': False
    },
    {
        'id': 2,
        'name': 'Incidente Menu Favorito',
        'completed': False
    }
]

def new_id():
    max_id = 0

    for task in tasks:
        if task.get('id') > max_id:
            max_id = task.get('id')

    return max_id + 1
