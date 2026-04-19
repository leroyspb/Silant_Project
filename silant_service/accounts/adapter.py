from allauth.account.adapter import DefaultAccountAdapter

class NoSignupAccountAdapter(DefaultAccountAdapter):
    """
    Адаптер для отключения регистрации новых пользователей.
    Регистрация разрешена только администратором через админ-панель.
    """
    def is_open_for_signup(self, request):
        # Возвращаем False, чтобы запретить самостоятельную регистрацию
        return False