from synapse.resources.resources import ResourcesController
from synapse.synapse_exceptions import ResourceException

from synapse.logger import logger


@logger
class ReposController(ResourcesController):

    __resource__ = "repos"

    def read(self, res_id=None, attributes=None):
        """
        Gets a repo definition on host.
        If id is not specified, this method retrieves all repos.

        Incoming request example:

    {
            "action": "read",
            "id": "repo-name",
            "collection": "repos",
    }
        """

        status = {}
        try:
            status = self.module.get_repos(res_id)
            response = self.set_response(status)

        except ResourceException, error:
            response = self.set_response(status, error='%s' % error)

        return response

    def create(self, res_id=None, attributes=None):
        """
        Creates or updates a repo definition on a host.

        Incoming request example:

    {
            "action": "create",
            "id": "repo-name",
            "collection": "yum_repos",
            "attributes": {
                "filename": "filename.repo",
                "name": "My Repo",
                "failovermethod": "priority",
                "baseurl": "http://my.repo.com",
                "mirrorlist": "http://my.mirror.com",
                "enabled": "1",
                "metadata_expire": "7d",
                "gpgcheck": "1",
                "gpgkeyfile": "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-i686"
                }
    }
        """

        if not res_id:
            raise ResourceException("Please provide an ID")

        status = {}
        response = {}
        try:
            self.module.create_repo(res_id, attributes)
            status = self.module.get_repos(res_id)
            response = self.set_response(status)

        except ResourceException, error:
            response = self.set_response({}, error='%s' % error)

        if 'error' in response:
            self.logger.info('Error when creating the repo %s: %s'
                    % (res_id, response['error']))

        return response

    def update(self, res_id=None, attributes=None):
        return self.create(res_id=res_id, attributes=attributes)

    def delete(self, res_id=None, attributes=None):
        """
        Deletes a repo definition on a host.

        Incoming request example:

        {
            "action": "delete",
            "id": "repo-name",
            "collection": "yum_repos",
        }
        """
        if not res_id:
            raise ResourceException("Please provide an ID")

        status = {}

        try:
            self.module.delete_repo(res_id)
            if not self.module.get_repos(res_id):
                status["present"] = False
                response = self.set_response(status)
            else:
                raise ResourceException("Something went wrong when deleting "
                                        "the repo")
        except ResourceException, error:
            response = self.set_response(status, error="%s" % error)

        if 'error' in response:
            self.logger.info('Error when deleting the repo %s: %s'
                    % (res_id, response['error']))

        return response
