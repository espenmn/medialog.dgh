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
    """ get all email for a group
    """

    def call(self, context):
        group = self.context.group or None
        usergroup = api.user.get_users(groupname=group)
        maillist = ''
                
        for member in usergroup:
            group = api.group.get_groups(user=member)
            grupper = ', '.join(str(e) for e in group[1:])
            if grupper != 'AuthenticatedUsers':
                userlist += member.getProperty('email')
            
        return str(maillist)