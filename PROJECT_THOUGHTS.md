# Problem identification

I identified a fundamental problem in payment fraud prevention: there is no single fraud pattern that can be reliably targeted. In my view, financial systems often focus on solving specific known vulnerabilities rather than systematically reducing the conditions that allow fraudulent activity to occur in the first place. 

This creates a reactive approach where each new attack becomes another isolated problem to solve. I propose approaching fraud prevention as a broader risk-minimisation problem: instead of simply detecting more known fraud cases, the system should continuously analyse transactions, behaviour, and context to minimise the conditions in which successful fraud can occur. In other words, the objective is not only to detect specific cases, but to make successful fraud cases less likely by design.

## Start
Instead of starting with a predefined list of fraud tactics, I propose analysing the payment process from the ground up. We will model the complete payment lifecycle and examine what the system knows, what it can verify, and where risk can emerge at each stage. This allows us to identify weaknesses and risk conditions before defining specific fraud scenarios, rather than building isolated rules around attacks that are already known.

### Data analysis
I will begin by analysing the dataset to understand the structure and behaviour of the payment data before designing any fraud detection logic. The goal is to identify what information is available, how transactions behave over time, what patterns exist between customers and transactions, and which signals could potentially indicate abnormal behaviour.

I also want to set up the Python environment so I can reuse it for future data analysis and machine learning projects, not just this one. Some of the tools I install might not be needed here, but I want to have a solid setup I can keep using later.

I’m creating a separate data-lab folder for my data analysis work. I want to keep all datasets, notebooks, experiments, and analysis tools in one place so I can reuse the setup across different projects.

