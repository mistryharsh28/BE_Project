# -*- coding: utf-8 -*-
import yake
from yake.highlight import TextHighlighter
import nltk
from textblob import TextBlob 
import os

### Sample texts used for testing.
### These will be replaced by transcripts of the video.

text1 = """Irrigation is one of the essential steps for a crop to grow perfectly. But do you know that only one-third area of the total land in India has proper irrigation facility available?
India has the second-largest irrigated land in the world, but still, India faces this problem.
Punjab has the highest percentage area of irrigated land in the country of about 98% irrigated land availability, followed by Haryana. The reason for good irrigation facilities is the availability of water throughout the year from the rivers and dam. This helps the farmers to conduct agricultural operations timely.
But scenario all over the country is not the same. In central India, rivers don’t carry water throughout the year. Due to this, farmers have to depend on the monsoon water for irrigation which is very uncertain. """

text2 = '''
    Supervised machine learning algorithms can apply what has been learned in the past to new data using labeled examples to predict future events. Starting from the analysis of a known training dataset, the learning algorithm produces an inferred function to make predictions about the output values. The system is able to provide targets for any new input after sufficient training. The learning algorithm can also compare its output with the correct, intended output and find errors in order to modify the model accordingly.
    In contrast, unsupervised machine learning algorithms are used when the information used to train is neither classified nor labeled. Unsupervised learning studies how systems can infer a function to describe a hidden structure from unlabeled data. The system doesn’t figure out the right output, but it explores the data and can draw inferences from datasets to describe hidden structures from unlabeled data.
    Semi-supervised machine learning algorithms fall somewhere in between supervised and unsupervised learning, since they use both labeled and unlabeled data for training – typically a small amount of labeled data and a large amount of unlabeled data. The systems that use this method are able to considerably improve learning accuracy. Usually, semi-supervised learning is chosen when the acquired labeled data requires skilled and relevant resources in order to train it / learn from it. Otherwise, acquiring unlabeled data generally doesn’t require additional resources.
    Reinforcement machine learning algorithms is a learning method that interacts with its environment by producing actions and discovers errors or rewards. Trial and error search and delayed reward are the most relevant characteristics of reinforcement learning. This method allows machines and software agents to automatically determine the ideal behavior within a specific context in order to maximize its performance. Simple reward feedback is required for the agent to learn which action is best; this is known as the reinforcement signal.
'''

text3 = "There has been shortage of water"

text4 = '''Three agriculture sector challenges will be important to India’s overall development and the improved welfare of its rural poor:
1. Raising agricultural productivity per unit of land: Raising productivity per unit of land will need to be the main engine of agricultural growth as virtually all cultivable land is farmed. Water resources are also limited and water for irrigation must contend with increasing industrial and urban needs. All measures to increase productivity will need exploiting, amongst them: increasing yields, diversification to higher value crops, and developing value chains to reduce marketing costs.
2. Reducing rural poverty through a socially inclusive strategy that comprises both agriculture as well as non-farm employment: Rural development must also benefit the poor, landless, women, scheduled castes and tribes. Moreover, there are strong regional disparities: the majority of India’s poor are in rain-fed areas or in the Eastern Indo-Gangetic plains. Reaching such groups has not been easy. While progress has been made - the rural population classified as poor fell from nearly 40% in the early 1990s to below 30% by the mid-2000s (about a 1% fall per year) – there is a clear need for a faster reduction. Hence, poverty alleviation is a central pillar of the rural development efforts of the Government and the World Bank.
3. Ensuring that agricultural growth responds to food security needs: The sharp rise in food-grain production during India’s Green Revolution of the 1970s enabled the country to achieve self-sufficiency in food-grains and stave off the threat of famine. Agricultural intensification in the 1970s to 1980s saw an increased demand for rural labor that raised rural wages and, together with declining food prices, reduced rural poverty. However agricultural growth in the 1990s and 2000s slowed down, averaging about 3.5% per annum, and cereal yields have increased by only 1.4% per annum in the 2000s. The slow-down in agricultural growth has become a major cause for concern. India’s rice yields are one-third of China’s and about half of those in Vietnam and Indonesia. The same is true for most other agricultural commodities.
Policy makers will thus need to initiate and/or conclude policy actions and public programs to shift the sector away from the existing policy and institutional regime that appears to be no longer viable and build a solid foundation for a much more productive, internationally competitive, and diversified agricultural sector.
Priority Areas for Support
1. Enhancing agricultural productivity, competitiveness, and rural growth
Promoting new technologies and reforming agricultural research and extension: Major reform and strengthening of India’s agricultural research and extension systems is one of the most important needs for agricultural growth. These services have declined over time due to chronic underfunding of infrastructure and operations, no replacement of aging researchers or broad access to state-of-the-art technologies. Research now has little to provide beyond the time-worn packages of the past. Public extension services are struggling and offer little new knowledge to farmers. There is too little connection between research and extension, or between these services and the private sector.
Improving Water Resources and Irrigation/Drainage Management: Agriculture is India’s largest user of water. However, increasing competition for water between industry, domestic use and agriculture has highlighted the need to plan and manage water on a river basin and multi-sectoral basis. As urban and other demands multiply, less water is likely to be available for irrigation. Ways to radically enhance the productivity of irrigation (“more crop per drop”) need to be found. Piped conveyance, better on-farm management of water, and use of more efficient delivery mechanisms such as drip irrigation are among the actions that could be taken. There is also a need to manage as opposed to exploit the use of groundwater. Incentives to pump less water such as levying electricity charges or community monitoring of use have not yet succeeded beyond sporadic initiatives. Other key priorities include: (i) modernizing Irrigation and Drainage Departments to integrate the participation of farmers and other agencies in managing irrigation water; (ii) improving cost recovery; (iii) rationalizing public expenditures, with priority to completing schemes with the highest returns; and (iv) allocating sufficient resources for operations and maintenance for the sustainability of investments.
Facilitating agricultural diversification to higher-value commodities: Encouraging farmers todiversify to higher value commodities will be a significant factor for higher agricultural growth, particularly in rain-fed areas where poverty is high. Moreover, considerable potential exists for expanding agro-processing and building competitive value chains from producers to urban centers and export markets. While diversification initiatives should be left to farmers and entrepreneurs, the Government can, first and foremost, liberalize constraints to marketing, transport, export and processing. It can also play a small regulatory role, taking due care that this does not become an impediment.
Promoting high growth commodities: Some agricultural sub-sectors have particularly high potential for expansion, notably dairy. The livestock sector, primarily due to dairy, contributes over a quarter of agricultural GDP and is a source of income for 70% of India’s rural families, mostly those who are poor and headed by women. Growth in milk production, at about 4% per annum, has been brisk, but future domestic demand is expected to grow by at least 5% per annum. Milk production is constrained, however, by the poor genetic quality of cows, inadequate nutrients, inaccessible veterinary care, and other factors. A targeted program to tackle these constraints could boost production and have good impact on poverty.
Developing markets, agricultural credit and public expenditures: India’s legacy of extensive government involvement in agricultural marketing has created restrictions in internal and external trade, resulting in cumbersome and high-cost marketing and transport options for agricultural commodities. Even so, private sector investment in marketing, value chains and agro-processing is growing, but much slower than potential. While some restrictions are being lifted, considerably more needs to be done to enable diversification and minimize consumer prices. Improving access to rural finance for farmers is another need as it remains difficult for farmers to get credit. Moreover, subsidies on power, fertilizers and irrigation have progressively come to dominate Government expenditures on the sector, and are now four times larger than investment expenditures, crowding out top priorities such as agricultural research and extension.
2. Poverty alleviation and community actions
While agricultural growth will, in itself, provide the base for increasing incomes, for the 170 million or so rural persons that are below the poverty line, additional measures are required to make this growth inclusive. For instance, a rural livelihoods program that empowers communities to become self-reliant has been found to be particularly effective and well-suited for scaling-up. This program promotes the formation of self-help groups, increases community savings, and promotes local initiatives to increase incomes and employment. By federating to become larger entities, these institutions of the poor gain the strength to negotiate better prices and market access for their products, and also gain the political power over local governments to provide them with better technical and social services. These self-help groups are particularly effective at reaching women and impoverished families.
3. Sustaining the environment and future agricultural productivity
In parts of India, the over-pumping of water for agricultural use is leading to falling groundwater levels. Conversely, water-logging is leading to the build-up of salts in the soils of some irrigated areas. In rain-fed areas on the other hand, where the majority of the rural population live, agricultural practices need adapting to reduce soil erosion and increase the absorption of rainfall. Overexploited and degrading forest land need mitigation measures. There are proven solutions to nearly all of these problems. The most comprehensive is through watershed management programs, where communities engage in land planning and adopt agricultural practices that protect soils, increase water absorption and raise productivity through higher yields and crop diversification. At issue, however, is how to scale up such initiatives to cover larger areas of the country. Climate change must also be considered. More extreme events – droughts, floods, erratic rains – are expected and would have greatest impact in rain-fed areas. The watershed program, allied with initiatives from agricultural research and extension, may be the most suited agricultural program for promoting new varieties of crops and improved farm practices. But other thrusts, such as the livelihoods program and development of off-farm employment may also be key.
'''

### Find keywords without Parameters.

'''
kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

for kw in keywords:
	print(kw)
'''

### Parameters to find Keywords.

language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 10

#text1 = text1.lower()

### Keyword Extractor that returns a pair of keyword and its value.

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(text1)

### Storing the keywords in a list.

keys = []
for kw in keywords:
    keys.append(kw[0])

### TextHighlighter Function within Yake Module.
### It highlights the keywords within the given text.

'''
th = TextHighlighter(max_ngram_size = 3)
th = TextHighlighter(max_ngram_size = 3, highlight_pre = "<span class='my_class' >", highlight_post= "</span>")
print("Text\n",th.highlight(text, keywords))
'''

### Print all the keywords.

print("keys: ",keys)
print()

### Find all the sentences from the transcript that has one or more keywords.

sent = []
a_list = nltk.tokenize.sent_tokenize(text1)
for i in a_list:
	for j in keys:
		if j in i and i not in sent:
			
			sent.append(i)

			### To identify the tokens using TestBlob.

			'''
			blob_object = TextBlob(i)
			print(blob_object.tags)		//debug
			print()
			print()
			'''

### Print all the sentences from the transcript that has one or more keywords.

'''
print(sent)
'''

print()
print()

### To generate questions using the QuestionGenerator.
### It takes command line input/argument in the below form.
### python question.py -s 'text'

for i in sent:
	x = "python question.py -s '" + i +"'"
	print(i)		#debug
	os.system(x)
	print()
	print()
	print()
