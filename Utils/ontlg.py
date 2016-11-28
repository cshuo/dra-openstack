from FuXi.SPARQL.BackwardChainingStore import TopDownSPARQLEntailingStore
from FuXi.Horn.HornRules import HornFromN3
from rdflib.Graph import Graph
from rdflib import Variable, Namespace
from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.Rete.Util import generateTokenSet
from FuXi.Rete.Magic import MagicSetTransformation, AdornLiteral
from FuXi.SPARQL import RDFTuplesToSPARQL

'''
function for reasoning the related res of the spefified resource
'''
def infer_ontlg(resource_name):
    resNs = Namespace('file:///code/metric.n3#')
    nsMapping = {'mtc' : resNs}
    rules = HornFromN3('metric_rule.n3')
    factGraph = Graph().parse('metric.n3',format='n3')
    factGraph.bind('mtc',resNs)
    dPreds = [resNs.relateTo]

    topDownStore=TopDownSPARQLEntailingStore(factGraph.store,factGraph,idb=rules,derivedPredicates = dPreds,nsBindings=nsMapping)
    targetGraph = Graph(topDownStore)
    targetGraph.bind('ex',resNs)
    #get list of the related resource 
    r_list = list(targetGraph.query('SELECT ?RELATETO { mtc:%s mtc:relateTo ?RELATETO}' % resource_name,initNs=nsMapping))
    
    res_list = []
    for res in r_list:
        res_list.append(str(res).split("#")[1])
    return res_list


def add_ontlg_fact(subName, subType):
    with open('metric.n3', 'a') as apd:
        apd.write(":"+subName + " a " + subType + " .\n")

if __name__ == "__main__":
    add_ontlg_fact("rtlong-timestamp", "RTLong")
    print infer_ontlg("rtlong-timestamp")
