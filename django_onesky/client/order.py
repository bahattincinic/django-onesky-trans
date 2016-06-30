# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import BaseOneSkyClient


class OrderClient(BaseOneSkyClient):
    """
    Order Management
    """

    def get_order_list(self, project_id, page=1, per_page=50,
                       file_name=None):
        """
        List of Orders

        :param project_id (OneSky project id) int
        :param page (set page number to retrieve) int
        :param per_page (set how many groups to retrieve for each time) int
        :param file_name (Filter orders by file name) str
        """
        params = {
            'page': page,
            'per_page': per_page,
        }
        if file_name:
            params.update({'file_name': file_name})

        return self.make_request(url="projects/%s/orders" % project_id,
                                 params=params)

    def get_order_detail(self, project_id, order_id):
        """
        Retrieve details of an order

        :param project_id (OneSky project id) int
        :param order_id (OneSky order id) int
        """

        return self.make_request(
            url="projects/%s/orders/%s" % (project_id, order_id))

    def create_order(self, project_id, files, to_locale, options):
        """
        Create a new order

        :param files (Files to be translated in the order) list
        :param to_locale (Target language to tranlate) str
        """
        params = {
            'files': files,
            'to_locale': to_locale
        }
        if options:
            params.update(options)

        return self.make_request(url="projects/%s/orders/" % project_id,
                                 method="POST", params=params)
