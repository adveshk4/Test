from strawberry.django.views import GraphQLView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse

class JWTAuthGraphQLView(GraphQLView):
    authentication = JWTAuthentication()
    def get_context(self, request, response, *args, **kwargs):
        auth = self.authentication
        header = auth.get_header(request)
        raw_token = auth.get_raw_token(header) if header else None
        validated_token = auth.get_validated_token(raw_token) if raw_token else None
        print(validated_token)
        user = auth.get_user(validated_token) if validated_token else None
        print(user)
        if user is None or not user.is_authenticated:
            raise Exception("Authentication required.")
        request.user = user
        return super().get_context(request, response, *args, **kwargs)