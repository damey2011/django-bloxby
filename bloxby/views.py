from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from bloxby.models import UserBridge, Template, Page, TemplateAsset


class ReceiveFTPItemsView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ReceiveFTPItemsView, self).dispatch(request, *args, **kwargs)

    def on_file_receipt(self, data, template):
        """
        This function is called in the POST, this could be overridden in the class inheriting this class in whatever
        application calling it
        """

    def post(self, request, *args, **kwargs):
        # Handle individual file here, we replace everyone that takes the same target and obj_id
        target = request.POST.get('target')
        obj_id = request.POST.get('obj_id')
        if obj_id == 'null':
            obj_id = None
        files = request.FILES
        user_bloxby_id = request.POST.get('user_bloxby_id')
        user = UserBridge.objects.filter(bloxby_id=user_bloxby_id).first().user
        template, _ = Template.objects.get_or_create(owner=user, obj_id=obj_id, target=target)
        for key, file in files.items():
            if file.name.endswith('.html'):
                page, _ = Page.objects.update_or_create(
                    template=template, name=key, defaults={'html': file, 'is_built': False}
                )
            else:
                asset, _ = TemplateAsset.objects.update_or_create(template=template, initial_path=key,
                                                                  defaults={'file': file})
        self.on_file_receipt(request.POST, template)
        return HttpResponse('success')


class AuthFTPUserView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AuthFTPUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = UserBridge.objects.get(bloxby_id=username).user
            if user.check_password(password):
                return HttpResponse('Success')
        except UserBridge.DoesNotExist:
            return HttpResponse('Error', status=400)
        return HttpResponse('Error', status=400)


class PageRenderView(View):
    def get(self, request, *args, **kwargs):
        template = Template.objects.first()
        if template:
            page = self.request.GET.get('page')
            if not page:
                html = template.index_page.render()
            else:
                try:
                    html = template.page_set.get(name=page).render()
                except Page.DoesNotExist:
                    raise Http404
        else:
            html = 'Does not exist'
        return HttpResponse(html)


class TestIndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super(TestIndexView, self).get_context_data(**kwargs)
        return ctx


class ImportSiteView(View):
    def get(self, request, *args, **kwargs):
        """
        Make sure you pass 'sites_id', 'target' and 'obj_id' in URL parameters
        :sites_id: This is the ID of the site you want to import over
        :target: This can be anything, just for you to be able to identify where you are using the template currently,
        I'm using them as either 'event' or 'home'.
        :obj_id: This is going to be the pk of the instance or event as the case may be
        """
        sites_id = request.GET.get('sites_id')
        target = request.GET.get('target', None)
        obj_id = request.GET.get('obj_id', None)
        if not sites_id:
            raise Http404
        # Sample, we will use it for event number 1
        request.user.userbridge.save_site_from_remote(sites_id, target, obj_id)
        return JsonResponse({'status': 'success'})
