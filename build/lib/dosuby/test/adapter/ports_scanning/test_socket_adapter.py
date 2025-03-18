from dosuby.src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter




# def test_socket_ports():
    
#     socket_adapter = SocketPortScanningAdapter()
#     assert socket_adapter.ports == [80]

# def test_socket_scanning_of_a_domain_list():
#     targets = ['cab.algerac.dz', 'mail.algerac.dz']
#     ports = []
    
#     port_scanning = SocketPortScanningAdapter()
#     for target in targets:
#         port_scanning.target_uri = target
#         open_ports = port_scanning.run()
#         ports.append(open_ports)
    
#     print(ports)