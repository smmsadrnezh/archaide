ALL_QUALITY_ATTRIBUTES = """
SELECT ?qalabel
	WHERE
	{
	 ?subject a :Quality_Attribute.
	 ?subject rdfs:label ?qalabel.
	}
ORDER BY ?subject
"""

ALL_QUALITY_ATTRIBUTE_TACTIC = """
SELECT ?tactic_label ?qa_label
	WHERE
	{
	 ?subject a :Tactic.
	?object a :Quality_Attribute.
	 ?subject rdfs:label ?tactic_label.
	?object rdfs:label ?qa_label.
	?subject :achieves ?object

	}
ORDER BY ?qa_label ?tactic_label
"""
