from django.http import JsonResponse

class JSONResponseMixin(object):

    def render_to_json_response(self):
        format = self.request.GET.get('format', None)
        formatPost = self.request.POST.get('format', None)
        if format == 'json' or formatPost == 'json':
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = self.get_data()
        return JsonResponse(data, safe=False)
