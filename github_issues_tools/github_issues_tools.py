# Copyright 2018 Lionheart Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import logging
import requests
import json

logger = logging.getLogger(__name__)
GITHUB_API_ENDPOINT = "https://api.github.com"
github_url = lambda *components: "{}/{}".format(GITHUB_API_ENDPOINT, "/".join(components))

class GitHubIssuesTools(object):
    def __init__(self, api_key):
        self.api_key = api_key

    @property
    def HEADERS(self):
        return {
            'Authorization': "token {}".format(self.api_key),
            'Content-Type': "application/json",
            'Accept': "application/vnd.github.symmetra-preview+json"
        }

    def get_labels(self, organization, repository):
        label_url = github_url("repos", organization, repository, "labels")
        return labels

    def export_labels(self, organization, repository):
        list_label_url = github_url("repos", organization, repository, "labels")
        label_response = requests.get(list_label_url, headers=self.HEADERS)
        print(json.dumps(label_response.json()))

    def copy_labels(self, source_organization, source_repository, target_organization, target_repository):
        list_label_url = github_url("repos", source_organization, source_repository, "labels")
        create_label_url = github_url("repos", target_organization, target_repository, "labels")
        label_response = requests.get(list_label_url, headers=self.HEADERS)
        for label_json in label_response.json():
            del label_json['id']
            del label_json['url']
            del label_json['default']
            name = label_json['name']
            print(label_json)

            response = requests.patch(create_label_url + "/" + name, json=label_json, headers=self.HEADERS)
            if response.status_code != 200:
                requests.post(create_label_url, json=label_json, headers=self.HEADERS)

            print("Copied {name} from {source_organization}/{source_repository} to {target_organization}/{target_repository}".format(
                name=name,
                source_organization=source_organization,
                source_repository=source_repository,
                target_organization=target_organization,
                target_repository=target_repository
            ))

