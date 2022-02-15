from .parent import BaseTranslator

# BaseTranslator.register(YandexTranslator)
# BaseTranslator.register(QCRI)
# BaseTranslator.register(DeepL)
# BaseTranslator.register(MicrosoftTranslator)
# BaseTranslator.register(PapagoTranslator)


def generate_engines_dict(_all: list, _locals: dict) -> dict:
    base_translator_type = BaseTranslator

    def is_translator(__object: object) -> bool:
        try:
            return issubclass(__object, base_translator_type)
        except TypeError:
            return False

    translation_engines = {}
    for _object in _all:
        __object = _locals.get(_object, 'failed')
        key_name = _object.replace('Translator', '').lower()
        if is_translator(__object):
            translation_engines.update({key_name: __object})
    return translation_engines


def engine(engine_name: str, *args, **kwargs) -> BaseTranslator:
    """Return translation engine.

    Free and keyless engines are 'google', 'pons', 'linguee', 'mymemory',
    'libre'.

    Args:
        engine_name: the name of the engine
        *args: positional argument to pass to the engine
        **kwargs: named argument to pass to the engine
    Return:
        A translation engine
    """
    engine.translation_engines = {}
    try:
        return engine.translation_engines[engine_name.lower()](*args, **kwargs)
    except KeyError:
        keys = '\', \''.join(engine.translation_engines.keys())
        raise(KeyError(f'Please provide a valid engine name (\'{keys}\')'))
