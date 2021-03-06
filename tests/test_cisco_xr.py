import pytest
from DEVICE_CREDS import *
import netmiko


def setup_module(module):

    module.EXPECTED_RESPONSES = {
        'router_prompt' : 'RP/0/0/CPU0:XRv-1#',
        'router_enable' : 'RP/0/0/CPU0:XRv-1#',
        'interface_ip'  : '169.254.254.181'
    }
    
    show_ver_command = 'show version'
    module.basic_command = 'show ipv4 int brief'
    
    SSHClass = netmiko.ssh_dispatcher(cisco_xr['device_type'])
    net_connect = SSHClass(**cisco_xr)
    module.show_version = net_connect.send_command(show_ver_command)
    module.show_ip = net_connect.send_command(module.basic_command)
    module.router_prompt = net_connect.router_prompt


def test_disable_paging():
    '''
    Verify paging is disabled by looking for string after when paging would
    normally occur
    '''
    assert 'fullk9-x' in show_version


def test_verify_ssh_connect():
    '''
    Verify the connection was established successfully
    '''
    assert 'Cisco IOS XR Software,' in show_version


def test_verify_send_command():
    '''
    Verify a command can be sent down the channel successfully
    '''
    assert EXPECTED_RESPONSES['interface_ip'] in show_ip


def test_find_name():
    '''
    Verify the router prompt is detected correctly
    '''
    assert router_prompt == EXPECTED_RESPONSES['router_prompt']


def test_strip_prompt():
    '''
    Ensure the router prompt is not in the command output
    '''
    assert EXPECTED_RESPONSES['router_prompt'] not in show_ip


def test_strip_command():
    '''
    Ensure that the command that was executed does not show up in the 
    command output
    '''
    assert basic_command not in show_ip


def test_normalize_linefeeds():
    '''
    Ensure no '\r' sequences
    '''
    assert not '\r' in show_version


