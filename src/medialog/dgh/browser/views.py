## -*- coding: utf-8 -*-

from zope.interface import implements, Interface
from plone.dexterity.utils import iterSchemata
from zope.schema import getFields

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IMailSchema
from Products.statusmessages.interfaces import IStatusMessage

import logging

logger = logging.getLogger(__file__)



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
    """ send email to everyone in a group  """

    def __call__(self, context):
        self.send_groupmail()
        
    def send_groupmail(self):
        group = context.group or None
        usergroup = api.user.get_users(groupname=group)
        for member in usergroup:
            group = api.group.get_groups(user=member)
            receipt = member.getProperty('email')
            self.send_email(receipt)
            

    def send_email(self, receipt):
        context = self.context
        title = context.title
        description = context.description

        body_html =  u'<h1 class="documentFirstHeading">' + title + u'</h1><div class="documentDescription description">' + description + u'</div>' + context.text.output   
        
        transforms = getToolByName(self.context, 'portal_transforms')
        stream = transforms.convertTo('text/plain', body_html, mimetype='text/html')
        body_plain = stream.getData().strip()

        #body_plain = u''
   
        # create multipart mail
        try:
            mailhost = api.portal.get_tool(name='MailHost')
            outer = MIMEMultipart('alternative')
            outer['To'] = receipt 
            #Header(u'<%s>' % safe_unicode(receiver['email']))
            outer['From'] = 'admin@dgh.no'
            outer['Subject'] = title
            outer.epilogue = ''

            # Attach text part
            text_part = MIMEText(body_plain, 'plain', _charset='UTF-8')

            # Attach html part with images
            html_part = MIMEMultipart('related')
            html_text = MIMEText(body_html, 'html', _charset='UTF-8')
            html_part.attach(html_text)

            # Add images to the message
            #for image in issue_data['images_to_attach']:
            #    html_part.attach(image)
            outer.attach(text_part)
            outer.attach(html_part)

            mailhost.send(outer.as_string())
            
            return True

        except:
            return 'Something went wrong'       
            
            
    def sendt_testmail(self):
        receipt = 'espen@medialog.no'
        self.send_email(receipt)
        
            
    
