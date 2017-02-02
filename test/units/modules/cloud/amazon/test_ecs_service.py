from __future__ import absolute_import
import unittest
import datetime
from dateutil.tz import tzlocal
from ansible.modules.cloud.amazon.ecs_service import EcsServiceManager


class Ec2Utils(unittest.TestCase):
    def test_is_matching_service(self):

        existing = {u'status': u'ACTIVE',
         u'taskDefinition': u'taskdefinition:1', u'pendingCount': 0,
         u'loadBalancers': [], u'placementConstraints': [],
         u'createdAt': datetime.datetime(2017, 2, 2, 14, 30, 36, 610000, tzinfo=tzlocal()), u'desiredCount': 3,
         u'serviceName': u'zookeeper', u'clusterArn': u'arn:aws:ecs:ap-southeast-2:1234567890:cluster/test-cluster',
         u'serviceArn': u'arn:aws:ecs:ap-southeast-2:1234567890:service/test-service',
         u'deploymentConfiguration': {u'maximumPercent': 200, u'minimumHealthyPercent': 100}, u'runningCount': 3,
         u'placementStrategy': []}

        expected = {'desired_count': existing[u'desiredCount'],
                    'task_definition': existing[u'taskDefinition'],
                    'deployment_configuration': existing[u'deploymentConfiguration'],
                    'load_balancers': existing[u'loadBalancers'] }

        # same shouldn't trigger an update
        self.assertTrue(EcsServiceManager.is_matching_service(expected, existing))

        # different task definition
        expected_1 = expected.copy()
        expected_1['task_definition'] = u'taskdefinition:2'
        self.assertFalse(EcsServiceManager.is_matching_service(expected_1, existing))

        # different load balancer
        expected_2 = expected.copy()
        expected_2['load_balancers'] = ['dummyloadbalancer']
        self.assertFalse(EcsServiceManager.is_matching_service(expected_2, existing))

        # different desired count
        expected_3 = expected.copy()
        expected_3['desired_count'] = existing['desiredCount'] + 1
        self.assertFalse(EcsServiceManager.is_matching_service(expected_3, existing))

        # no deployment configuration provided should not trigger an update
        expected_4 = expected.copy()
        expected_4.pop('deployment_configuration')
        self.assertTrue(EcsServiceManager.is_matching_service(expected_4, existing))

        # empty deployment configuration should not trigger an update
        expected_5 = expected.copy()
        expected_5['deployment_configuration'] = {}
        self.assertTrue(EcsServiceManager.is_matching_service(expected_5, existing))

        # different deployment configuration provided should trigger an update
        expected_6 = expected.copy()
        expected_6['deployment_configuration'] = {'maximumPercent': 150, 'minimumHealthyPercent': 60}
        self.assertFalse(EcsServiceManager.is_matching_service(expected_6, existing))