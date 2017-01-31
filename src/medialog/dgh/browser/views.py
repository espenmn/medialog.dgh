from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

class MedlemmerView(BrowserView):
    """ View to show users
    """

    template = ViewPageTemplateFile('medlemmer_view.pt')

    def __call__(self, *args, **kw):
        return self.template(self.context)
        
    def all_users(self):
        return api.user.get_users()
        
    def group_users(self):
        group = self.context.group
        return api.user.get_users(groupname=group)
        


