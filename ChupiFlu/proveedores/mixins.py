from django.http import JsonResponse

class JSONResponseMixin(object):

    def render_to_json_response(self):
        return self.json_to_response()

    def json_to_response(self):
        data = self.get_data()
        return JsonResponse(data, safe=True)
