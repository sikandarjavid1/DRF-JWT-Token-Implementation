from rest_framework.renderers import JSONRenderer

class EnhancedJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']
        status_code = response.status_code
        success = 200 <= status_code < 300  # Boolean success status based on HTTP status code

        if not success and isinstance(data, dict):
            response_data = {
                "success": success,
                "message": data.get('detail', 'Error processing request'),
                "data": None,
                "errors": data
            }
        else:
            response_data = {
                "success": success,
                "message": "Request processed successfully" if success else "Error processing request",
                "data": data,
                "errors": None
            }

        rendered_data = super().render(response_data, accepted_media_type, renderer_context)
        return rendered_data
