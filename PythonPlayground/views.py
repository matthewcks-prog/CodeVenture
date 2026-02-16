from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from CodeVenture.services.judge0_service import Judge0Service


def playground_view(request):
    return render(request, "playground.html")


@csrf_exempt
def run_code(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            body_data = json.loads(body_unicode)
            code = body_data.get("code", "")

            if not code.strip():
                message = "No code provided."
                return JsonResponse({"result": message, "error": message}, status=400)

            service = Judge0Service()
            result = service.run_code(code)

            if "error_message" in result and result["error_message"]:
                message = result["error_message"]
                return JsonResponse({"result": message, "error": message}, status=400)
            elif "error" in result and result["error"]:
                message = result["error"]
                return JsonResponse({"result": message, "error": message}, status=500)
            elif "stdout" in result:
                return JsonResponse({"result": result["stdout"]})
            else:
                message = "Unknown execution result."
                return JsonResponse({"result": message, "error": message}, status=500)

        except Exception as e:
            message = str(e)
            return JsonResponse(
                {"error": message, "result": f"Error: {message}"}, status=500
            )

    message = "Only POST method is supported."
    return JsonResponse({"error": message, "result": message}, status=405)
