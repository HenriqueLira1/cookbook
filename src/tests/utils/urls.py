from django.urls import resolve, reverse


def resolve_by_name(name, **kwargs):
    url = reverse(name, kwargs=kwargs)
    return resolve(url)


def assert_has_actions(allowed, actions):
    assert len(allowed) == len(actions)

    for allows in allowed:
        assert allows in actions


def assert_resolves_actions(resolver, actions_map):
    for key, value in actions_map.items():
        assert key in resolver.func.actions
        assert value in resolver.func.actions[key]
