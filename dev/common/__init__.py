class SingletonMeta(type):
    """
        Đối tượng duy nhất [design pattern]
    """
    _instance = {}

    def __call__(cls, *args, **kwargs) -> "SingletonMeta":
        if cls not in cls._instance:
            instance = super().__call__(*args, **kwargs)
            cls._instance[cls] = instance
        return cls._instance[cls]
    
    def __init__(self, *args, **kwargs) -> "SingletonMeta":
        super().__init__(*args, **kwargs)