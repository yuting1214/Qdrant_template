
VOCABULARY_EXTRACTOR_PROMPT = """
Extract advanced vocabulary from the given corpus. Advanced vocabulary refers to words requiring higher
reading comprehension due to their complexity, specificity, or rarity. These words often consist of intricate meanings,
multiple definitions, or subtle nuances. They may be highly specialized or domain-specific, contributing to the
sophistication and depth of written language. Examples of advanced vocabulary include words like 'efficacious,'
'abstruse,' 'luminous,' 'pervasive,' and 'ephemeral.' Please identify and list such advanced vocabulary found within
the corpus, ensuring that the extracted words match the form used in the input corpus.

Return the list of advanced vocabulary in a JSON-parsable format as follows:
{
  'vocabulary': ['advanced_word1', 'advanced_word2', ...]
}
If no advanced vocabulary is found, return an empty JSON as follows:
{}
"""

# Preferred
VOCABULARY_EXTRACTOR_PROMPT_v2 = """
Extract advanced vocabulary from the given corpus. Advanced vocabulary refers to words or phrases requiring higher reading comprehension due to their complexity, specificity, or rarity. These words or phrases often consist of intricate meanings, multiple definitions, or subtle nuances. They may be highly specialized or domain-specific, contributing to the sophistication and depth of written language. Examples of advanced vocabulary include words like 'efficacious,' 'abstruse,' 'luminous, and 'ephemeral.' Please identify and list such advanced vocabulary found within the corpus, ensuring that the extracted words or phrases match the form used in the input corpus.

Additionally, consider compound words or phrases as potential advanced vocabulary. These may include hyphenated compounds like 'top-notch' or 'well-being,' as well as multi-word expressions like 'dwell on' or 'come up with.' Ensure that compound words or phrases are correctly identified and included in the list of advanced vocabulary.

Consider the difficulty level of each word or phrase, prioritizing the extraction of the most difficult ones first.

It's encouraged to be pasrsimonious for identification and absolutely avoid redundancy in the list of advanced vocabulary.

Use linguistic complexity measures, frequency analysis, or other relevant techniques to determine the difficulty level of each term.

Provide your output in json format with the
key: vocabulary; value: list of advanced words or phrases. 
It is okay to return an empty list if no advanced vocabulary is found.

"""

# Preferred
VOCABULARY_EXTRACTOR_PROMPT_v3 = """
Extract advanced vocabulary from the given corpus. Advanced vocabulary refers to words or phrases requiring higher \
reading comprehension due to their complexity, specificity, or rarity. These words or phrases often consist of intricate \
meanings, multiple definitions, or subtle nuances. They may be highly specialized or domain-specific, contributing to the \
sophistication and depth of written language. Examples of advanced vocabulary include words like 'efficacious,' 'abstruse,' \
'luminous, and 'ephemeral.' Also, consider compound words or phrases as potential advanced vocabulary. These may include hyphenated \
compounds like 'top-notch', as well as multi-word expressions like 'dwell on'. 
 
Please identify and list such advanced vocabulary found within the corpus, ensuring that the extracted words or phrases match the form used in the input corpus.

It's encouraged to be pasrsimonious for identification and absolutely avoid redundancy in the list of advanced vocabulary.

Provide your output in json format with the
key: vocabulary; value: list of advanced words or phrases. 
It is okay to return an empty list if no advanced vocabulary is found.

"""