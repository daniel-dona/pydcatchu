import rdflib
from rdflib.namespace import FOAF
import uuid

DCAT = rdflib.Namespace("http://www.w3.org/ns/dcat#")
SPDX = rdflib.Namespace("http://spdx.org/rdf/terms#")
DCT = rdflib.Namespace("http://purl.org/dc/terms/")

class Functions:
	
	'''@staticmethod
	def parse_DCAT(graph):
		
	DCAT = rdflib.Namespace("http://www.w3.org/ns/dcat#")

    catalogs = list(graph.triples((None, rdflib.RDF.type, DCAT.Catalog)))
    
    print("Found",len(catalogs), "catalogs!")
    
    for catalog in catalogs:
		
		datasets = list('''
		
	pass
		
	

class BaseNamespace:
	
	def __init__(self, base_uri):
		self.base_uri = base_uri
		self.entities = []
		
	def bind(self, graph):
		graph.bind("dcat", DCAT)
		graph.bind("foaf", FOAF)
		graph.bind("dct", DCT)
		
	def generate_uri(self, dcat_object):
		
		if isinstance(dcat_object, Agent):
		
			return self.base_uri + "uuid/agent/" + str(uuid.uuid4()) + "/"
			
		if isinstance(dcat_object, Catalogue):
		
			return self.base_uri + "uuid/catalogue/" + str(uuid.uuid4()) + "/"
			
		if isinstance(dcat_object, Dataset):
		
			return self.base_uri + "uuid/dataset/" + str(uuid.uuid4()) + "/"
			
		if isinstance(dcat_object, Distribution):
		
			return self.base_uri + "uuid/distribution/" + str(uuid.uuid4()) + "/"
			
		return None
		

class Agent:
	
	def __init__(self, name):
		self.name = name
		self.namespace = None
	
	def set_namespace(self, namespace):
		self.namespace = namespace
		self.uri = namespace.generate_uri(self)
	
	def get_id(self):
		return self.uri
	
	def graph(self):
		
		if self.namespace is None:
			raise RuntimeError("Namespace not configured, set it to generate graph")
		
		g = rdflib.Graph()
		self.namespace.bind(g)
		
		g.add((rdflib.URIRef(self.uri), rdflib.RDF.type, FOAF.Agent))
		g.add((rdflib.URIRef(self.uri), FOAF.name, rdflib.Literal(self.name)))
		
		return g

class Catalogue:
	
	def __init__(self, title, description, publisher):
		self.title = title
		self.description = description
		self.datasets = []
		
		if not isinstance(publisher, Agent):
			raise TypeError("Publisher must be an object of class Agent")
		
		self.publisher = publisher
		self.namespace = None
		
	def set_namespace(self, namespace):
		self.namespace = namespace
		self.uri = namespace.generate_uri(self)
	
	def get_id(self):
		return self.uri
		
	def add_dataset(self, dataset):
		
		if not isinstance(dataset, Dataset):
			raise TypeError("Dataset must be an object of class Dataset")
		
		self.datasets.append(dataset)
		
	def graph(self):
		
		if self.namespace is None:
			raise RuntimeError("Namespace not configured, set it to generate graph")
			
		if len(self.datasets) == 0:
			raise RuntimeError("Dataset(s) not configured, use add_dataset()")
		
		g = rdflib.Graph()
		self.namespace.bind(g)
		
		g.add((rdflib.URIRef(self.uri), rdflib.RDF.type, DCAT.Catalog))
		g.add((rdflib.URIRef(self.uri), DCT.title, rdflib.Literal(self.title)))
		g.add((rdflib.URIRef(self.uri), DCT.description, rdflib.Literal(self.title)))
		g.add((rdflib.URIRef(self.uri), DCT.publisher, rdflib.URIRef(self.publisher.get_id())))
		
		g += self.publisher.graph()
		
		for dataset in self.datasets:
			g.add((rdflib.URIRef(self.uri), DCAT.dataset, rdflib.URIRef(dataset.get_id())))
			g += dataset.graph()
		
		return g
	

class Dataset:
	
	def __init__(self, title, description):
		self.title = title
		self.description = description
		self.distributions = []
		self.namespace = None
	
	def set_namespace(self, namespace):
		self.namespace = namespace
		self.uri = namespace.generate_uri(self)
	
	def get_id(self):
		return self.uri
		
	def add_distribution(self, distribution):
		
		if not isinstance(distribution, Distribution):
			raise TypeError("Distribution must be an object of class Distribution")
		
		self.distributions.append(distribution)
		
	def graph(self):
		
		if self.namespace is None:
			raise RuntimeError("Namespace not configured, set it to generate graph")
			
		if len(self.distributions) == 0:
			raise RuntimeError("Distributions(s) not configured, use add_distribution()")
		
		g = rdflib.Graph()
		self.namespace.bind(g)
		
		g.add((rdflib.URIRef(self.uri), rdflib.RDF.type, DCAT.Dataset))
		g.add((rdflib.URIRef(self.uri), DCT.title, rdflib.Literal(self.title)))
		g.add((rdflib.URIRef(self.uri), DCT.description, rdflib.Literal(self.description)))
		
		for distribution in self.distributions:
			g.add((rdflib.URIRef(self.uri), DCAT.distribution, rdflib.URIRef(distribution.get_id())))
			g += distribution.graph()
		
		
		return g

class Distribution:
	
	def __init__(self, access_url):
		self.access_url = access_url
		self.namespace = None
		self.title = None
	
	def set_namespace(self, namespace):
		self.namespace = namespace
		self.uri = namespace.generate_uri(self)
		
	def set_title(self, title):
		self.title = title
	
	def get_id(self):
		return self.uri
		
	def graph(self):
		
		if self.namespace is None:
			raise RuntimeError("Namespace not configured, set it to generate graph")
		
		g = rdflib.Graph()
		self.namespace.bind(g)
		
		g.add((rdflib.URIRef(self.uri), rdflib.RDF.type, DCAT.Distribution))
		g.add((rdflib.URIRef(self.uri), DCAT.accessURL, rdflib.URIRef(self.access_url)))
		
		if self.title != None:
			
			g.add((rdflib.URIRef(self.uri), DCT.title, rdflib.Literal(self.title)))	
			
		
		return g

