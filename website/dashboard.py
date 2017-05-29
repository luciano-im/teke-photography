"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'bh.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):

    # class Media:
    #     css = {
    #         'all': (
    #             'css/dashboard.css',
    #         ),
    #     }

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # Alta de Usuarios
        self.children.append(modules.ModelList(
            _('Alta de Usuarios'),
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))

        # Tags y Fotos
        self.children.append(modules.ModelList(
            _('Fotos y Tags'),
            column=1,
            collapsible=False,
            models=('website.models.Photo', 'taggit.models.Tag'),
        ))

        # Link list module
        # self.children.append(modules.LinkList(
        #     _('Acciones'),
        #     column=2,
        #     children=[
        #         {
        #             'title': _('ACTUALIZAR EXTRANET'),
        #             'url': reverse('importdata', args=['all']),
        #             'external': False,
        #         },
        #         {
        #             'title': _('Actualizar Cta. Cte. en Pesos'),
        #             'url': reverse('importdata', args=['ctacte']),
        #             'external': False,
        #         },
        #         {
        #             'title': _('Actualizar Cta. Cte. Aplicada'),
        #             'url': reverse('importdata', args=['applied']),
        #             'external': False,
        #         },
        #         {
        #             'title': _('Actualizar Entregas y Ventas'),
        #             'url': reverse('importdata', args=['kilos']),
        #             'external': False,
        #         },
        #         {
        #             'title': _('Actualizar Analisis de Calidad'),
        #             'url': reverse('importdata', args=['analysis']),
        #             'external': False,
        #         },
        #     ]
        # ))

        # Recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=10,
            collapsible=False,
            column=3,
        ))
