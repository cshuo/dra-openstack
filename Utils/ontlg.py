from FuXi.SPARQL.BackwardChainingStore import TopDownSPARQLEntailingStore
from FuXi.Horn.HornRules import HornFromN3
from rdflib.Graph import Graph
from rdflib import Variable, Namespace
from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.Rete.Util import generateTokenSet
from FuXi.Rete.Magic import MagicSetTransformation, AdornLiteral
from FuXi.SPARQL import RDFTuplesToSPARQL

from dra.Openstack.Service.Nova import Nova

_nova = Nova()

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

'''
the vms/res an app/vm related.
'''
def get_related(types, **kwargs):
    famNs = Namespace('http://cetc/onto.n3#')
    nsMapping = {'': famNs}
    rule_store, rule_graph, network = SetupRuleStore(makeNetwork=True)
    closureDeltaGraph=Graph()
    closureDeltaGraph.bind('', famNs)
    network.inferredFacts = closureDeltaGraph

    for rule in HornFromN3('rule.n3'):
        network.buildNetworkFromClause(rule)

    factGraph = Graph().parse('resource.n3', format='n3')
    factGraph.bind('', famNs)
    network.feedFactsToAdd(generateTokenSet(factGraph))

    # print closureDeltaGraph.serialize(format='n3')
    rs = []
    if types == 'res':
        r_list = list(closureDeltaGraph.query('SELECT ?RESULT {:%s :key_res ?RESULT}' % kwargs['app'], initNs=nsMapping))
        for r in r_list:
            rs.append(str(r.split('#')[1]))
    elif types == 'app':
        r_list = list(closureDeltaGraph.query('SELECT ?RESULT {:%s :related_to ?RESULT}' % kwargs[types], initNs=nsMapping))
        id_maps = _nova.get_id_name_maps(r_list)
        for r in r_list:
            rs.append({'name': r, 'id': id_maps[r]})
    elif typs == 'vm':
        for r in r_list:
            pass

    return rs


if __name__ == "__main__":
    add_ontlg_fact("rtlong-timestamp", "RTLong")
    print infer_ontlg("rtlong-timestamp")
