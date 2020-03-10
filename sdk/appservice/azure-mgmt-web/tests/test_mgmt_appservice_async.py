# coding: utf-8

#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import asyncio
import functools

import azure.mgmt.web.aio
from devtools_testutils import AzureMgmtTestCase, ResourceGroupPreparer

AZURE_LOCATION = 'eastus'


def await_prepared_test(test_fn):
    """Synchronous wrapper for async test methods. Used to avoid making changes
    upstream to AbstractPreparer (which doesn't await the functions it wraps)
    """

    @functools.wraps(test_fn)
    def run(test_class_instance, *args, **kwargs):
        loop = asyncio.get_event_loop()
        resource_group = kwargs.get("resource_group")
        result = loop.run_until_complete(test_fn(test_class_instance, resource_group))
        return result

    return run

class MgmtWebSiteTest(AzureMgmtTestCase):

    def setUp(self):
        super(MgmtWebSiteTest, self).setUp()
        self.mgmt_client = self.create_mgmt_client(
            azure.mgmt.web.aio.WebSiteManagementClient
        )

    @ResourceGroupPreparer(location=AZURE_LOCATION)
    @await_prepared_test
    async def test_appservice(self, resource_group):

        SERVERFARM_NAME = "myapimrndxyz"
        BODY = {
          "kind": "app",
          "location": "East US",
          "sku": {
            "name": "P1",
            "tier": "Premium",
            "size": "P1",
            "family": "P",
            "capacity": "1"
          }
        }

        await self.mgmt_client.app_service_plans.create_or_update(resource_group.name, SERVERFARM_NAME, BODY)

        await self.mgmt_client.list_skus()
