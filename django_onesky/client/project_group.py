# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import BaseOneSkyClient


class ProjectGroupClient(BaseOneSkyClient):
    """
    Project Group Management
    """

    def get_project_list(self, project_group_id):
        """
        List of projects

        :param project_group_id (OneSky project group id) int
        """
        return self.make_request(
            url="project-groups/%s/projects" % project_group_id)

    def get_project_groups_list(self):
        """
        List of project groups
        """
        return self.make_request(url="project-groups")

    def get_project_group_detail(self, project_group_id):
        """
        Detail of Project Group

        :param project_group_id (OneSky project group id) int
        """
        return self.make_request(url="project-groups/%s/" % project_group_id)

    def create_project_group(self, name, locale="en"):
        """
        Create a new project group

        :param name (Name of the project group) str
        :param locale  (Locale code of the project group base language) str
        """
        params = {
            'name': name,
            'locale': locale
        }
        return self.make_request(url="project-groups", params=params,
                                 method="POST")

    def remove_project_group(self, project_group_id):
        """
        Remove a project group

        :param project_group_id (OneSky project group id) int
        """
        return self.make_request(url="project-groups/%s/" % project_group_id,
                                 method="DELETE")

    def get_project_group_languages(self, project_group_id):
        """
        List enabled languages of a project group

        :param project_group_id (OneSky project group id) int
        """
        return self.make_request(
            url="project-groups/%s/languages" % project_group_id)
