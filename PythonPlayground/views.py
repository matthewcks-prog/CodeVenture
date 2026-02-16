from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from CodeVenture.services.judge0_service import Judge0Service

def playground_view(request):
    return render(request, 'playground.html')


@csrf_exempt
def run_code(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            code = body_data.get('code', '')

            service = Judge0Service()
            result = service.run_code(code)

            if 'error_message' in result:
                 return JsonResponse({'result': result['error_message']})
            elif 'stdout' in result:
                 return JsonResponse({'result': result['stdout']})
            elif 'error' in result:
                 return JsonResponse({'result': result['error']})
            else:
                 return JsonResponse({'result': 'Unknown execution result.'})

        except Exception as e:
             return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is supported.'}, status=405)
