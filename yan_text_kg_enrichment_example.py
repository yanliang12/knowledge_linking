import yan_text_kg_enrichment

text = u"""
I graduated from UC Berkeley, and worked for Google for a while. Later I am an engineer at Apple. Now I live in San Jose.
"""

text = u"""
I live in Dubai and study in the Heriot-Watt University Dubai. But I find a job in Abu Dhabi.
"""

yan_text_kg_enrichment.text_knowledge_enrichment(
	text,
	)
