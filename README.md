## uni-da

Exam project: Data Analytics (2016/17) - University of Milan Bicocca

#### Project purposes 

Sentiment analysis on amazon reviews

#### Project Report

[1] DATASET

	1.1 Parse dataset from .tsv (or .json) into DB (SQLite)

[2] TOPIC MODEL

	2.1 Tokenize reviews: from phrases obtain relevant tokens
	2.2 Use Joint sentiment/topic algorithm (based on LDA) to get principal topics
	    - how many iterations?
	    - how many docs (= reviews tokenized)?

[3] USER EXPERIENCE

	3.1 Calculate user experience on each topic
	3.2 Calculate "general" user experienxe

[4] DATA INFO GRAPHIC

	4.1 Use Django to build local webapp and navigate into data
	4.2 Build page for users, products, reviews and topics
	4.3 Build charts on 
		- user rates (pie chart)
		- user topics (2 line chart, one for pos, one for neg; line = topic, x = review timestamp, y = affinity topic-review)
		- product rates (pie chart)
		- product topics (pie chart)
	4.4 #todo: reccomendation based on user preferences and topics
	

#### Based on article:

**From Amateurs to Connoisseurs: Modeling the Evolution of User Expertise through Online Reviews**

Julian McAuley, Stanford University
Jure Leskovec, Stanford University

**Abstract:** Recommending products to consumers means not only understand- ing their tastes, but also understanding their level of experience. For example, it would be a mistake to recommend the iconic film Seven Samurai simply because a user enjoys other action movies; rather, we might conclude that they will eventually enjoy it—once they are ready. The same is true for beers, wines, gourmet foods— or any products where users have acquired tastes: the ‘best’ prod- ucts may not be the most ‘accessible’. Thus our goal in this pa- per is to recommend products that a user will enjoy now, while acknowledging that their tastes may have changed over time, and may change again in the future. We model how tastes change due to the very act of consuming more products—in other words, as users become more experienced. We develop a latent factor rec- ommendation system that explicitly accounts for each user’s level of experience. We find that such a model not only leads to better recommendations, but also allows us to study the role of user expe- rience and expertise on a novel dataset of fifteen million beer, wine, food, and movie reviews.

