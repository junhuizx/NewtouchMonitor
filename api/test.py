from openstack_api import OpenStackAgentClient

def test_openstack_api():
    ops_client = OpenStackAgentClient('172.16.0.10', 10888)
    print ops_client.hypervisor_server_list('')

if __name__ == '__main__':
    test_openstack_api()