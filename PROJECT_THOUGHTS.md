# Problem identification

I identified a fundamental problem in payment fraud prevention: there is no single fraud pattern that can be reliably targeted. In my view, financial systems often focus on solving specific known vulnerabilities rather than systematically reducing the conditions that allow fraudulent activity to occur in the first place. 

This creates a reactive approach where each new attack becomes another isolated problem to solve. I propose approaching fraud prevention as a broader risk-minimisation problem: instead of simply detecting more known fraud cases, the system should continuously analyse transactions, behaviour, and context to minimise the conditions in which successful fraud can occur. In other words, the objective is not only to detect specific cases, but to make successful fraud cases less likely by design.

## Start
Instead of starting with a predefined list of fraud tactics, I propose analysing the payment process from the ground up. We will model the complete payment lifecycle and examine what the system knows, what it can verify, and where risk can emerge at each stage. This allows us to identify weaknesses and risk conditions before defining specific fraud scenarios, rather than building isolated rules around attacks that are already known.

### Data analysis
I will begin by analysing the dataset to understand the structure and behaviour of the payment data before designing any fraud detection logic. The goal is to identify what information is available, how transactions behave over time, what patterns exist between customers and transactions, and which signals could potentially indicate abnormal behaviour.

I also want to set up the Python environment so I can reuse it for future data analysis and machine learning projects, not just this one. Some of the tools I install might not be needed here, but I want to have a solid setup I can keep using later.

I’m creating a separate data-lab folder for my data analysis work. I want to keep all datasets, notebooks, experiments, and analysis tools in one place so I can reuse the setup across different projects.

### First Analysis
My first analysis shows that no single field clearly separates fraudulent transactions from legitimate ones. Transaction amount, card type, purchase category, and customer age have very similar distributions between the two groups. Merchant and location show more variation, but this is not enough to treat them as reliable indicators on their own. I also found that the transaction description simply duplicates the merchant ID, so it does not provide additional information. This suggests that fraud detection should not rely on isolated fields. The next step is to test whether meaningful signals appear when multiple features are combined and analysed together.

I started by checking the basic structure and quality of the dataset before building any fraud detection logic. The dataset contains 10,000 transactions from 100 customers, covering a period of 2 hours and 46 minutes, with exactly one transaction recorded every second. There are 5,068 fraudulent and 4,932 non-fraudulent transactions. Every customer has changing age, card type, and city values, with an average of 43.3 different cities per customer. Customer fraud rates range from 33% to 60%, with no customer having only fraudulent or only legitimate transactions. I also checked the main transaction fields. The average transaction amount is £4,943.23 for non-fraudulent transactions and £4,973.13 for fraudulent ones, while card type and purchase category have very similar fraud rates across their groups. Location ranges from 43.2% to 60% fraud, while merchants range from 38.8% to 64.2%. I also found that the transaction description duplicates the merchant ID, so it provides no additional information. Overall, these results suggest that individual fields do not clearly separate fraudulent transactions from legitimate ones, so the next step is to investigate whether useful signals appear when multiple features are combined.

The current analysis can be run with:
data-lab\.venv\Scripts\python.exe data-lab\main.py

The main conclusion from this analysis is that this dataset does not contain enough behavioural signal to build a useful fraud detector. Individual features, combinations, and behavioural features all produced results close to random, and the logistic regression model confirmed this with an AUC of around 0.5. Instead of forcing more features onto the same data, I want to step back and ask what information a real payment system would need to capture in order to identify meaningful risk. This moves the project from simply analysing an existing dataset towards designing the data and behaviour model that our fraud engine actually needs.
