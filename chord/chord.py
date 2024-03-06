class Interface:
    def __init__(self):
        self.chord = Chord()

    def mount_ring(self, num_nodes):
        for i in range(num_nodes):
            node = Node(i, "127.0.0.1", 8000 + i, [], None, None)  
            self.chord.join(node)

    def insert_resource(self, resource):
        self.chord.insert_resource(resource)

    def search_resource(self, resource):
        return self.chord.search_resource(resource)

    def leave_node(self, node_id):
        node = self.chord.ring[node_id]
        self.chord.leave(node)

    def join_node(self, node_id):
        node = self.chord.ring[node_id]
        self.chord.join(node)

class Node:
    def __init__(self, id, ip, port, resources, successor=None, predecessor=None):
        self.id = id
        self.ip = ip
        self.port = port
        self.resources = resources
        self.successor = successor
        self.predecessor = predecessor


class Chord:
    def __init__(self):
        self.ring = []
        self.hash_table = {}

    def join(self, node):
        node.id = hash(node.ip + ":" + str(node.port))
        self.ring.insert(self.get_position(node.id), node)
        self.update_predecessors_and_successors(node)

    def leave(self, node):
        self.ring.remove(node)
        self.update_predecessors_and_successors(node.predecessor, node.successor)

    def insert_resource(self, resource):
        node = self.get_responsible_node(resource)
        node.resources.append(resource)

    def search_resource(self, resource):
        node = self.get_responsible_node(resource)
        for res in node.resources:
            if res == resource:
                return res
        return None

    def get_responsible_node(self, resource):
        resource_id = hash(resource)
        for node in self.ring:
            if node.id >= resource_id:
                return node
        return self.ring[0]

    def get_position(self, node_id):
        for i, node in enumerate(self.ring):
            if node.id > node_id:
                return i
        return len(self.ring)

    def update_predecessors_and_successors(self, node1, node2):
        if node1 is not None:
            node1.successor = node2
        if node2 is not None:
            node2.predecessor = node1

# Criar interface
interface = Interface()

# Menu principal
while True:
    print("----- Menu CHORD -----")
    print("1. Gerenciar Anel")
    print("2. Gerenciar Recursos")
    print("3. Sair")

    option = int(input("Digite a opção desejada: "))

    if option == 1:
        # Submenu Gerenciar Anel
        while True:
            print("----- Submenu Gerenciar Anel -----")
            print("1. Montar Anel")
            print("2. Listar Nós")
            print("3. Ativar Nó")
            print("4. Desativar Nó")
            print("5. Voltar")

            option = int(input("Digite a opção desejada: "))

            if option == 1:
                num_nodes = int(input("Digite o número de nós: "))
                interface.mount_ring(num_nodes)
            elif option == 2:
                print("Nós:")
                for node in interface.chord.ring:
                    print("ID:", node.id, "IP:", node.ip, "Porta:", node.port)
            elif option == 3:
                node_id = int(input("Digite o ID do nó: "))
                interface.join_node(node_id)
            elif option == 4:
                node_id = int(input("Digite o ID do nó: "))
                interface.leave_node(node_id)
            elif option == 5:
                break
            else:
                print("Opção inválida.")

    elif option == 2:
        # Submenu Gerenciar Recursos
        while True:
            print("----- Submenu Gerenciar Recursos -----")
            print("1. Inserir Recurso")
            print("2. Buscar Recurso")
            print("3. Listar Recursos")
            print("4. Voltar")

            option = int(input("Digite a opção desejada: "))

            if option == 1:
                resource = input("Digite o nome do recurso: ")
                interface.insert_resource(resource)
            elif option == 2:
                resource = input("Digite o nome do recurso: ")
                found_resource = interface.search_resource(resource)
                if found_resource is not None:
                    print("O recurso", resource, "foi encontrado.")
                else:
                    print("O recurso", resource, "não foi encontrado.")
            elif option == 3:
                print("Recursos:")
                for node in interface.chord.ring:
                    for res in node.resources:
                        print(res)
            elif option == 4:
                break
            else:
                print("Opção inválida.")

    elif option == 3:
        # Sair
        break
    else:
        print("Opção inválida.")