## food

Exam project: Data Analytics (2016/17) - University of Milan Bicocca

#### Project purposes 

	///

#### Project Report

[1] DATASET

	1.1 Parsing dataset from .tsv into DB (SQLite)

[2] TOPIC MODEL

	2.1 Tokenize reviews: from phrases to relevant tokens
	2.2 Use Joint sentiment/topic algorithm (based on LDA): get principal topics
	    - how many iterations?
	    - how many docs (= reviews tokenized)?
	2.3 Build vector space with docs and topics
	    (each doc is associated to a vector that rapresent his coordinates in space,
	    where dimensions are topics)
	2.4 Use k-means to split docs (in pos/neg ?)
	2.5 Use reviews rating to better split in pos/neg

[3] USER EXPERIENCE

	3.1 Calculate user experience on each topic
	3.2 Calcualte "general" user experienxe

[4] DATA INFO GRAPHIC

	- Model:   Distribution of topics for docs (reviews)
	- Model:   Average variance of topics for docs
	- User:    Distribution of topics
	- User:    Experience for topics
	- User:    Recommendations (?)
	- Product: Distribution of topics
	- Product: Distribution of reviews

#### Based on article:

	**From Amateurs to Connoisseurs: Modeling the Evolution of User Expertise through Online Reviews**

	Julian McAuley, Stanford University
	Jure Leskovec, Stanford University

	**Abstract:** Recommending products to consumers means not only understand- ing their tastes, but also understanding their level of experience. For example, it would be a mistake to recommend the iconic film Seven Samurai simply because a user enjoys other action movies; rather, we might conclude that they will eventually enjoy it—once they are ready. The same is true for beers, wines, gourmet foods— or any products where users have acquired tastes: the ‘best’ prod- ucts may not be the most ‘accessible’. Thus our goal in this pa- per is to recommend products that a user will enjoy now, while acknowledging that their tastes may have changed over time, and may change again in the future. We model how tastes change due to the very act of consuming more products—in other words, as users become more experienced. We develop a latent factor rec- ommendation system that explicitly accounts for each user’s level of experience. We find that such a model not only leads to better recommendations, but also allows us to study the role of user expe- rience and expertise on a novel dataset of fifteen million beer, wine, food, and movie reviews.

