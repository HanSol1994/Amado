from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin


class AutoLogout(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_superuser :
            return self.get_response(request)

        if not request.user.is_authenticated :
            #Can't log out if not logged in
            return self.get_response(request)

        try:
            if request.user.has_perm('auth.only_5_6'):
                if not ( datetime.now().hour >= 6 and datetime.now().hour <17):
                    auth.logout(request)
                del request.session['last_touch']
                return self.get_response(request)
            if datetime.now() - request.session['last_touch'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                auth.logout(request)
                del request.session['last_touch']
                return self.get_response(request)
            else:
                request.session['last_touch'] = datetime.now()
                return self.get_response(request)
        except KeyError:  # KeyError thrown if last touch doesn't exist, so set it.
            request.session['last_touch'] = datetime.now()


        return self.get_response(request)


    # def process_request(self, request):
    #
    #     if not request.user.is_authenticated() :
    #         #Can't log out if not logged in
    #         return
    #
    #     try:
    #         if datetime.now() - request.session['last_touch'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
    #             auth.logout(request)
    #             del request.session['last_touch']
    #             return self.get_response(request)
    #         else:
    #             request.session['last_touch'] = datetime.now()
    #             return self.get_response(request)
    #     except KeyError:  # KeyError thrown if last touch doesn't exist, so set it.
    #         request.session['last_touch'] = datetime.now()
    #
