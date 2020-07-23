ALL_QUALITY_ATTRIBUTES = """
SELECT ?subject
	WHERE
	{
	 ?subject a :Quality_Attribute.
	 ?subject rdfs:label ?qalabel.
	}
ORDER BY ?subject
"""
