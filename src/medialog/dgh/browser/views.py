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
        group = self.context.group or None
        usergroup = api.user.get_users(groupname=group)
        userlist = []
        
        import pdb; pdb.set_trace()
        for user in usergroup:
            uuserdata = dict{
              fullname: user.getProperty('fullname'),
        	  fornavn: user.getProperty('fornavn'),
        	  etternavn: user.getProperty('etternavn'),
        	  tittel: user.getProperty('tittel'),
        	  postnr: user.getProperty('postnr'),
        	  postadr: user.getProperty('postadr'),
        	  honnor: user.getProperty('honn_rmedlem'),
        	  tittel: user.getProperty('innmeldingsar'),
        	  telefon: user.getProperty('telefon'),
        	  adresse: user.getProperty('adressse'),
        	  utenbys: user.getProperty('utenbys'),
        	  group:  api.group.get_groups(username=user)
         	 }
         	 userlist.append(userdata)
        return userlist