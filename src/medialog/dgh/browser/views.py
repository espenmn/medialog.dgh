## -*- coding: utf-8 -*-

from zope.interface import implements, Interface
from plone.dexterity.utils import iterSchemata
from zope.schema import getFields

from Products.Five import BrowserView
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
        
    @property
    def group_users(self):
        group = self.context.group or None
        usergroup = api.user.get_users(groupname=group)
        userlist = []
        
        for member in usergroup:
            group = api.group.get_groups(user=member)
            grupper = ', '.join(str(e) for e in group[1:])
            if grupper != 'AuthenticatedUsers':
                userlist.append(
                {'etternavn': member.getProperty('etternavn'),
                  'fornavn': member.getProperty('fornavn'),
                  'tittel': member.getProperty('tittel'),
                  'email' : member.getProperty('email'),
                  'postnr': member.getProperty('postnr'),
                  'poststed': member.getProperty('poststed'),
                  'honnor': member.getProperty('honn_rmedlem'),
                  'telefon': member.getProperty('telefon'),
                  'adresse': member.getProperty('adresse'),
                  'utenbys': member.getProperty('utenbys'),
                  'innmeldingsar': member.getProperty('innmeldingsar'),
                  'login_time': member.getProperty('login_time'),
                  'group': grupper,
                  'verified': member.getProperty('login_time').strftime('%Y') != '2000'
                  })
            
        return userlist
        
        
class GroupsEmail(BrowserView):
    """ send email to a group
    """

    def call(self, context):
        group = context.group or None
        usergroup = api.user.get_users(groupname=group)
        self.message = 'some text'
        self.subject = "Email subject"
        for member in usergroup:
            group = api.group.get_groups(user=member)
            grupper = ', '.join(str(e) for e in group[1:])
            receipt = member.getProperty('email')
            self.send_email(self, receipt) 
        
        
    def send_email(self, receipt):
        "Send email to user of this group"
        try:
            mail_host = api.portal.get_tool(name='MailHost')
            # The ``immediate`` parameter causes an email to be sent immediately
            # (if any error is raised) rather than sent at the transaction
            # boundary or queued for later delivery.
            return mail_host.send(mail_text, immediate=True)
        except SMTPRecipientsRefused:
            # Don't disclose email address on failure
            raise SMTPRecipientsRefused('Recipient address rejected by server')
            

        # Use this logger to output debug info from this script if needed
        #import logging
        #logger = logging.getLogger("mailer-logger")

        source = "admin@dgh.com"
        
        mailhost.send(self.message, receipt, source, subject=self.subject, charset="utf-8", )
        

class TestGroupsEmail(BrowserView):
    """ send email to a espen
    """
    
    def __init__(self, context, request):
        super(TestGroupsEmail, self).__init__(context, request)

    def __call__(self, context, request):
        import pdb; pdb.set_trace()
        self.message = 'some text'
        self.subject = "Email subject"
        try:
            mail_host = api.portal.get_tool(name='MailHost')
            # The ``immediate`` parameter causes an email to be sent immediately
            # (if any error is raised) rather than sent at the transaction
            # boundary or queued for later delivery.
            return mail_host.send(mail_text, immediate=True)
            
            source = "admin@dgh.com"
            receipt = "espen@medialog.no"
        
            mailhost.send(self.message, receipt, source, subject=self.subject, charset="utf-8", )
            return "Testmail snt"
        
        except SMTPRecipientsRefused:
            # Don't disclose email address on failure
            raise SMTPRecipientsRefused('Recipient address rejected by server')
            return 'Something wrong happened'
    