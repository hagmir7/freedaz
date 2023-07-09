
from django_user_agents.utils import get_user_agent
from django.http import HttpResponseBadRequest



def ignorScrping(request):
    agent = get_user_agent(request)
    # user_agent = request.META.get('HTTP_USER_AGENT', '')
    if agent.browser[0] in ['Python Requests', 'Other']:
        return HttpResponseBadRequest("Bad Request")
    # if not is_browser_recognized(user_agent):
    #     return HttpResponseBadRequest("Unknown browser")
    return True




