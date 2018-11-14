# -*- coding: utf-8 -*-
# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields
from odoo.addons.component.core import AbstractComponent, Component


class AmbugestBackend(models.Model):
    _name = 'ambugest.backend'
    _description = 'Ambugest Backend'
    _inherit = 'connector.backend'

    host = fields.Char(string='Host', required=True)
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')

    def import_partner(self, external_id):
        with self.work_on(model_name='ambugest.res.partner') as work:
            importer = work.component(usage='record.importer')
            # returns an instance of PartnerImporter, which has been
            # found with:the collection name (ambugest.backend, the model,
            # and the usage).
            importer.run(partner_id)


# the next 2 components are abstract and are used by inheritance
# by the others
class BaseAmbugestConnectorComponent(AbstractComponent):
    # same inheritance than Odoo models
    _name = 'base.ambugest.connector'
    _inherit = 'base.connector'
    # subscribe to:
    _collection = 'ambugest.backend'
    # the collection will be inherited to the components below,
    # because they inherit from this component


class GenericAdapter(AbstractComponent):
    # same inheritance than Odoo models
    _name = 'ambugest.adapter'
    _inherit = ['base.backend.adapter', 'base.ambugest.connector']
    # usage is used for lookups of components
    _usage = 'backend.adapter'

    _ambugest_model = None

    def _call(self, *args, **kwargs):
        location = self.backend_record.location
        # use client API

    def read(self, fields=None):
        """ Search records according to some criterias
        and returns a list of ids

        :rtype: list
        """
        return self._call('%s.info' % self._ambugest_model, fields)


# these are the components we need for our synchronization
class PartnerAdapter(Component):
    _name = 'ambugest.partner.adapter'
    _inherit = 'ambugest.adapter'
    _apply_on = ['ambugest.res.partner']
    _ambugest_model = 'customer'


class PartnerMapper(Component):
    _name = 'ambugest.partner.import.mapper'
    _inherit = 'ambugest.import.mapper'  # parent component omitted for brevity
    _apply_on = ['ambugest.res.partner']
    _usage = 'import.mapper'


class PartnerBinder(Component):
    _name = 'ambugest.partner.binder'
    _inherit = 'ambugest.binder'  # parent component omitted for brevity
    _apply_on = ['ambugest.res.partner']
    _usage = 'binder'


class PartnerImporter(Component):
    _name = 'ambugest.partner.importer'
    _inherit = 'ambugest.importer'  # parent component omitted for brevity
    _apply_on = ['ambugest.res.partner']
    _usage = 'record.importer'

    def run(self, external_id):
        # get the components we need for the sync

        # this one knows how to speak to ambugest
        backend_adapter = self.component(usage='backend.adapter')
        # this one knows how to convert ambugest data to odoo data
        mapper = self.component(usage='import.mapper')
        # this one knows how to link ambugest/odoo records
        binder = self.component(usage='binder')

        # read external data from ambugest
        external_data = backend_adapter.read(external_id)
        # convert to odoo data
        internal_data = mapper.map_record(external_data).values()
        # find if the ambugest id already exists in odoo
        binding = binder.to_internal(external_id)
        if binding:
            # if yes, we update it
            binding.write(internal_data)
        else:
            # or we create it
            binding = self.model.create(internal_data)
        # finally, we bind both, so the next time we import
        # the record, we'll update the same record instead of
        # creating a new one
        binder.bind(external_id, binding)
