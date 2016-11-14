import os
from py2neo import Graph, Node, NodeSelector, Relationship


class CollatzConjecture():
    number = 1
    complex = False
    result = []
    result_list = []

    def __init__(self, number, complex):
        self.number = number
        self.complex = complex

    def calculate(self):
        if self.complex:
            for n in range(self.number, 1, -1):
                self.result = list(self.control_path(n))
                self.result_list.append(list(self.result))
        else:
            self.result = list(self.control_path(self.number))
            self.result_list.append(list(self.result))

    def control_path(self, number):
        while number != 1:
            yield int(number)
            number = self.number_path(number)
        yield int(number)

    def number_path(self, number):
        result = 1
        if number % 2 == 0:
            result = number/2
        else:
            result = (number*3)+1

        return result

    def get_result(self):
        if self.complex:
            return self.result_list
        return self.result

    def save_graph(self):
        if self.complex:
            self.save_complex_graph()
        else:
            self.save_simple_graph(self.result)

    def save_complex_graph(self):
        for item in self.result_list:
            self.save_simple_graph(item)

    def save_simple_graph(self, number_list):
        client = Graph(password=os.getenv('NEO4J_PASSWORD', 'Neo4j'))
        graph = client.begin()
        prev_number = 0
        for item in number_list:
            number_node = self.node_exist(int(item))
            if prev_number != 0 and number_node:
                prev_number_node = Node("number", number=int(prev_number))
                prev_number = int(item)
                num_relationship = Relationship(
                    prev_number_node, "NEXT", number_node)
                graph.merge(num_relationship)
                break
            number = Node("number", number=int(item))
            graph.merge(number)
            if prev_number == 0:
                prev_number = int(item)
                continue
            prev_number_node = Node("number", number=int(prev_number))
            prev_number = int(item)
            num_relationship = Relationship(prev_number_node, "NEXT", number)
            graph.merge(prev_number_node)
            graph.merge(num_relationship)
        graph.commit()

    def node_exist(self, number):
        client = Graph(password=os.getenv('NEO4J_PASSWORD', 'Neo4j'))
        selector = NodeSelector(client)
        selected = selector.select("number", **{"number": number}).first()
        if selected:
            return selected
        return False
