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
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from Products.statusmessages.interfaces import IStatusMessage

from Products.statusmessages.interfaces import IStatusMessage

import logging

logger = logging.getLogger(__file__)



class MedlemmerView(BrowserView):
    """ View to show users
    """

    template   = ViewPageTemplateFile('medlemmer_view.pt')
    m_template = ViewPageTemplateFile('medlemmer_full_view.pt')

    def __call__(self, *args, **kw):
        #current = api.user.get_current()
        if api.user.get_permissions()['Manage portal']:
            return self.m_template(self.context)
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
            grupper = ' '.join(str(e) for e in group[0:]).split()
            grupper.remove('AuthenticatedUsers')
            norm_grupper = ', '.join(str(e) for e in grupper)
            userlist.append(
                { 'id': member.getProperty('id'),
                  'etternavn': member.getProperty('etternavn'),
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
                  'group': norm_grupper,
                  'verified': (member.getProperty('login_time').strftime('%Y') == '2000'),
                  'login_time': member.getProperty('login_time').strftime('%Y/%m/%d'),
                  })

        return userlist


class GroupsEmail(BrowserView):
    """ send email to everyone in a group  """

    def __call__(self, context):
        pass

    def send_groupmail(self):
        context = self.context
        request = self.request
        if hasattr(context, 'group'):
            group = context.group
            usergroup = api.user.get_users(groupname=group)
        else:
            usergroup = api.user.get_users()

        for member in usergroup:
            group = api.group.get_groups(user=member)
            receipt = member.getProperty('email')
            self.send_email(context, request, receipt)

        self.request.response.redirect(self.context.absolute_url())


    def send_email(self, context, request, receipt):
        title = context.Title()
        description = context.Description()
        body_html =  u'<html><div class="mailcontent"><h1 class="documentFirstHeading">' + title.decode('utf-8') + u'</h1><div class="documentDescription description">' + description.decode('utf-8') + u'</div>' + context.text.output + u'</div></html>'

        #for 'non HTML mail clients'
        transforms = api.portal.get_tool(name='portal_transforms')
        stream = transforms.convertTo('text/plain', body_html, mimetype='text/html')
        body_plain = stream.getData().strip()

        messages = IStatusMessage(self.request)

        # ready to create multipart mail
        try:
            mailhost = api.portal.get_tool(name='MailHost')
            # discovered that plone api might do this better
            # plone.api.portal.send_email , maybe
            outer = MIMEMultipart('alternative')
            outer['To'] = receipt
            outer['From'] = api.portal.get_registry_record('plone.email_from_address')
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

            messages.add(_("sent_mail_message",  default=u"Sendt til $email",
                                                 mapping={'email': receipt },
                                                 ),
                                                 type="info")

        except:
            messages.add(_("cant_send_mail_message",
                                                 default=u"Kunne ikke sende til $email",
                                                 mapping={'email': receipt },
                                                 ),
                                                 type="warning")


    def sendt_testmail(self):
        context = self.context
        request = self.request
        member = api.user.get_current()
        receipt = member.getProperty('email')
        self.send_email(context, request, receipt)
        self.request.response.redirect(self.context.absolute_url())
