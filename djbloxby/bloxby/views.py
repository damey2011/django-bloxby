import bs4
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from djbloxby.bloxby.models import UserBridge, Template, Page, TemplateAsset


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
        user = UserBridge.objects.get(pk=user_bloxby_id).user
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
        html = template.index_page.render() if template else 'Does not exist'
        return HttpResponse(html)
