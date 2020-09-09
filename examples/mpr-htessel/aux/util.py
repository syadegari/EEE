

def flatten(l):
    return [item for sublist in l for item in sublist]


def is_list(list_two):
    return type(list_two) == list


def merge_dict(dict1: dict, dict2: dict) -> dict:
    d = {}
    d.update(dict1)
    d.update(dict2)
    return d


def warn_after_first_call(msg):
    def f(func):
        setattr(func, 'counter', 0)

        def g(*args, **kwargs):
            func.counter += 1
            if func.counter > 1:
                print(msg)
            return func(*args, **kwargs)
        return g
    return f
