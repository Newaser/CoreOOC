class _InGameError(RuntimeError):
    """
    Basic Game Runtime Error
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = self.__doc__
        self.args = msg


class ExcessiveRemovingError(_InGameError):
    """
    The items possessed are less than those are planed to remove
    """


class UnaffordableError(_InGameError):
    """
    Try trading but the trading items or the money is insufficient
    """


class ItemOverflowError(_InGameError):
    """
    Amount of items exceeds amount of inventory slots
    """