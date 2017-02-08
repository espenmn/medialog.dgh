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

    def __call__(self, context):
        import pdb; pdb.set_trace()
        group = context.group or None
        usergroup = api.user.get_users(groupname=group)
        self.message = self.context.text.output
        self.subject = "Email subject"
        for member in usergroup:
            group = api.group.get_groups(user=member)
            grupper = ', '.join(str(e) for e in group[1:])
            receipt = member.getProperty('email')
            self.send_email(self, receipt) 
        
        
    def send_email(self, receipt):
        "Send email to user of this group"
        try:
            mailhost = api.portal.get_tool(name='MailHost')
            # Use this logger to output debug info from this script if needed
            #import logging
            #logger = logging.getLogger("mailer-logger")
            source = "admin@dgh.no"
        
            mailhost.send(self.message, receipt, source, subject=self.subject, charset="utf-8", )
        
        except:
            return 'Something wrong happened'
            
        

class XTestGroupsEmail(BrowserView):
    """ send email to a espen
    """
    
    #def __init__(self, context, request):
    #    super(TestGroupsEmail, self).__init__(context, request)

    def __call__(self):
        message = "<html>" + self.context.text.output + '</html>'
        subject = "Email subject"
        try:
            mailhost = api.portal.get_tool(name='MailHost')
            source = "admin@dgh.no"
            receipt = "espen@medialog.no"
        
            #mailhost.send(message, subtype='html', receipt, source, subject=subject, charset="utf-8", )
            return "Testmail sent"
        
        except:
            return 'Something wrong happened'
            
            
            
            
class TestGroupsEmail(BrowserView):
    """ send email to a espen
    """
    
    def __call__(self, context):
        e_subject = context.Title
        e_from = u'admin@dgh'
        e_to = u'espen@medialog.no'
        body_html = u'<html>' + context.text.output + u'</html>'
        body_plain = context.text.raw

        mime_msg = MIMEMultipart('related')
        mime_msg['Subject'] = e_subject
        mime_msg['From'] = e_from
        mime_msg['To'] = e_to
        mime_msg.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body 
        # in an 'alternative' part, so message agents can decide 
        # which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        mime_msg.attach(msgAlternative)

        # plain part
        msg_txt = MIMEText(body,  _charset='utf-8')
        msgAlternative.attach(msg_txt)

        # html part
        msg_txt = MIMEText(rendered_html, _subtype='html', 
                           _charset='utf-8')
        msgAlternative.attach(msg_txt)

        try:
            mailhost.send(mime_msg.as_string())
            return "Testmail sent"
        
        except:
            return 'Something wrong happened'       
    